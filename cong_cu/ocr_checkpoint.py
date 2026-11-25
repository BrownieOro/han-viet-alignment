#!/usr/bin/env python3
"""OCR a bounded PDF range with durable per-page output; never overwrite work."""
import argparse
import base64
import fcntl
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from gemini_ocr import recognize

ROOT = Path(__file__).resolve().parents[1]
MODEL = 'gemini-3.5-flash-lite'


def atomic(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.tmp')
    with temp.open('wb') as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temp, path)


def keys_from(path):
    # Lines may contain an account label followed by the key. Never log either.
    result = []
    for line in path.read_text(encoding='utf-8-sig').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        key = line.split()[-1]
        if key not in result and len(key) >= 20 and all(33 <= ord(c) <= 126 for c in key):
            result.append(key)
    if not result:
        raise ValueError('Danh sách key rỗng hoặc không hợp lệ.')
    return result


def event(out, **fields):
    fields['time_utc'] = datetime.now(timezone.utc).isoformat()
    with (out / 'nhat_ky.jsonl').open('a', encoding='utf-8') as handle:
        handle.write(json.dumps(fields, ensure_ascii=False) + '\n')
        handle.flush()
        os.fsync(handle.fileno())


def run(args):
    source = Path(args.pdf).resolve()
    out = Path(args.output).resolve()
    with source.open('rb') as handle:
        source_hash = hashlib.file_digest(handle, 'sha256').hexdigest()
    out.mkdir(parents=True, exist_ok=True)
    with (out / '.lock').open('w') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise RuntimeError('Đợt này đang được xử lý bởi tiến trình khác.') from None
        config = {'source_name': source.name, 'sha256': source_hash, 'from': args.start,
                  'to': args.end, 'work': args.work, 'section': args.section, 'model': MODEL}
        skipped = sorted(set(getattr(args, 'skip', []) or []))
        if any(n < args.start or n > args.end for n in skipped):
            raise ValueError('Trang bỏ qua nằm ngoài phạm vi.')
        if skipped:
            config['skipped'] = skipped
        review = sorted(set(getattr(args, 'review', []) or []))
        if any(n < args.start or n > args.end or n in skipped for n in review):
            raise ValueError('Trang cần kiểm nằm ngoài phạm vi hoặc bị bỏ qua.')
        if review:
            config['review_pages'] = review
        manifest = out / 'dot_xu_ly.json'
        if manifest.exists():
            if json.loads(manifest.read_text(encoding='utf-8')) != config:
                raise RuntimeError('Nguồn hoặc phạm vi không khớp đợt đã lưu; chọn thư mục khác.')
        else:
            atomic(manifest, (json.dumps(config, ensure_ascii=False, indent=2)+'\n').encode())
        keys = keys_from(Path(args.keys))
        key_index = 0
        info = subprocess.run(['pdfinfo', str(source)], check=True, capture_output=True, text=True).stdout
        match = re.search(r'^Pages:\s+(\d+)', info, re.MULTILINE)
        if not match:
            raise ValueError('Không đọc được số trang PDF.')
        if not 1 <= args.start <= args.end <= int(match.group(1)):
                raise ValueError('Khoảng trang nằm ngoài PDF.')
        for number in range(args.start, args.end + 1):
                if number in skipped:
                    continue
                png = out / '01_nguon' / f'{number:04}.png'
                raw = out / '02_ocr_tho' / f'{number:04}.txt'
                if raw.exists():
                    if not raw.stat().st_size or not png.exists() or not png.stat().st_size:
                        raise RuntimeError(f'Trang {number}: tệp đã có không đầy đủ; dừng để tránh ghi đè.')
                    print(f'{number}: đã có, bỏ qua', flush=True)
                    continue
                command = ['pdftoppm', '-f', str(number), '-l', str(number), '-singlefile', '-scale-to', '1600']
                if not png.exists():
                    png_bytes = subprocess.run(command + ['-png', str(source)], check=True, capture_output=True).stdout
                    atomic(png, png_bytes)
                jpg_bytes = subprocess.run(command + ['-jpeg', '-jpegopt', 'quality=90', str(source)], check=True, capture_output=True).stdout
                image = base64.b64encode(jpg_bytes).decode()
                attempts = 0
                while True:
                    attempts += 1
                    status, result = recognize({'apiKey': keys[key_index], 'model': MODEL,
                                                'language': 'mixed', 'layout': '3', 'image': image})
                    event(out, page=number, status=status, key_number=key_index + 1,
                          attempt=attempts, error=result.get('error', ''))
                    if status == 200:
                        atomic(raw, (result['text'].rstrip() + '\n').encode('utf-8'))
                        print(f'{number}: OCR xong; key số {key_index+1}; {len(result["text"])} ký tự', flush=True)
                        break
                    if status == 429 and result.get('retryable') and attempts <= 2:
                        time.sleep(min(60, result.get('retryAfter', 10)))
                        continue
                    if status in {401, 403, 429} and key_index + 1 < len(keys):
                        key_index += 1
                        attempts = 0
                        print(f'{number}: key trước bị giới hạn hoặc không có quyền; thử key số {key_index+1}', flush=True)
                        continue
                    if status in {502, 503, 504} and attempts < 3:
                        time.sleep(10 * attempts)
                        continue
                    print(f'{number}: dừng an toàn; HTTP {status}: {result.get("error", "lỗi")}', flush=True)
                    return 1
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pdf', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--start', type=int, required=True)
    parser.add_argument('--end', type=int, required=True)
    parser.add_argument('--work', required=True)
    parser.add_argument('--section', required=True)
    parser.add_argument('--skip', nargs='*', type=int, default=[], help='Các trang bỏ qua sau khi xem nguồn')
    parser.add_argument('--review', nargs='*', type=int, default=[], help='Trang có ranh giới cần phân loại thủ công')
    parser.add_argument('--keys', default=str(ROOT / 'gemini_keys.txt'))
    args = parser.parse_args()
    try:
        return run(args)
    except (OSError, ValueError, RuntimeError) as exc:
        print('Dừng an toàn:', exc, file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
