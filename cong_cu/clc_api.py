"""Client for Kim Hán Nôm's documented web API."""
import json
import base64
import uuid
from pathlib import Path
from urllib import request, error

BASE = 'https://kimhannom.fit.hcmus.edu.vn'
CONFIG = Path(__file__).resolve().parents[1] / '.cv06_secrets.json'


def load_token():
    try:
        data = json.loads(CONFIG.read_text(encoding='utf-8'))
    except FileNotFoundError:
        return ''
    return str(data.get('kimhannom_token', '')).strip()


def sentence_alignment(han, vietnamese, token=None):
    """Request sentence suggestions. Return the API result without rewriting sources."""
    token = load_token() if token is None else token.strip()
    if not token or any(ord(c) < 33 or ord(c) > 126 for c in token):
        raise ValueError('Cần token Kim Hán Nôm hợp lệ trong cấu hình local.')
    if not han.strip() or not vietnamese.strip():
        raise ValueError('Cần nội dung Hán và Việt để dóng hàng.')
    body = json.dumps({'han': han, 'vi': vietnamese}, ensure_ascii=False).encode('utf-8')
    req = request.Request(BASE + '/api/web/clc-sinonom/sentence-alignment', data=body,
                          headers={'User-Agent': 'CV06-local/1.0', 'Authorization': 'Bearer ' + token,
                                   'Content-Type': 'application/json'}, method='POST')
    try:
        with request.urlopen(req, timeout=30) as response:
            result = json.load(response)
    except error.HTTPError as exc:
        raise RuntimeError(f'Kim Hán Nôm trả HTTP {exc.code}.') from exc
    except (error.URLError, TimeoutError) as exc:
        raise RuntimeError('Không kết nối được Kim Hán Nôm hoặc request quá thời gian.') from exc
    if not result.get('is_success') or result.get('code') != '000000':
        raise RuntimeError('Kim Hán Nôm không trả kết quả thành công; kiểm tra hạn mức và token.')
    return result.get('data', {}).get('result', [])


def image_ocr(image, language, layout):
    """Upload a JPEG and return the documented OCR text and bounding boxes."""
    token = load_token()
    if not token or any(ord(c) < 33 or ord(c) > 126 for c in token):
        raise ValueError('Cần token Kim Hán Nôm hợp lệ trong cấu hình local.')
    try:
        raw = base64.b64decode(image, validate=True)
    except (ValueError, TypeError):
        raise ValueError('Ảnh OCR không hợp lệ.') from None
    if not raw.startswith(b'\xff\xd8\xff') or len(raw) > 10_000_000:
        raise ValueError('Cần ảnh JPEG tối đa 10 MB.')
    boundary = 'cv06' + uuid.uuid4().hex
    body = (f'--{boundary}\r\nContent-Disposition: form-data; name="image_file"; filename="page.jpg"\r\n'
            'Content-Type: image/jpeg\r\n\r\n').encode() + raw + f'\r\n--{boundary}--\r\n'.encode()
    headers = {'User-Agent': 'CV06-local/1.0', 'Authorization': 'Bearer ' + token}
    def call(path, data, mime):
        req = request.Request(BASE + path, data=data, headers={**headers, 'Content-Type': mime}, method='POST')
        try:
            with request.urlopen(req, timeout=60) as response:
                result = json.load(response)
        except error.HTTPError as exc:
            raise RuntimeError(f'Kim Hán Nôm trả HTTP {exc.code}.') from exc
        except (error.URLError, TimeoutError) as exc:
            raise RuntimeError('Không kết nối được Kim Hán Nôm hoặc request quá thời gian.') from exc
        if not result.get('is_success') or result.get('code') != '000000':
            raise RuntimeError('Kim Hán Nôm không trả kết quả thành công; kiểm tra token và hạn mức.')
        return result.get('data') or {}
    uploaded = call('/api/web/clc-sinonom/image-upload', body, f'multipart/form-data; boundary={boundary}')
    filename = uploaded.get('file_name')
    if not filename:
        raise RuntimeError('Kim Hán Nôm không trả tên ảnh đã tải lên.')
    if language == 'vie':
        payload = {'file_name': filename, 'image': 'data:image/jpeg;base64,' + image}
        result = call('/api/web/clc-sinonom/viet-ocr', json.dumps(payload).encode(), 'application/json')
    elif language == 'chi_tra':
        payload = {'file_name': filename, 'ocr_id': 1 if layout == '5' else 4,
                   'lang_type': 1, 'epitaph': 0, 'tag': None,
                   'reading_direction': 1 if layout == '5' else 2}
        result = call('/api/web/clc-sinonom/image-ocr', json.dumps(payload).encode(), 'application/json')
    else:
        raise ValueError('Ngôn ngữ OCR không hợp lệ.')
    text = result.get('result_ocr_text', result.get('text', ''))
    if isinstance(text, list):
        text = '\n'.join(str(item) for item in text)
    if not isinstance(text, str) or not text.strip():
        raise RuntimeError('Kim Hán Nôm trả text rỗng hoặc định dạng chưa được hỗ trợ.')
    return {'text': text, 'bbox': result.get('result_bbox', [])}
