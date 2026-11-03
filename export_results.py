"""Freeze completed checkpoints into a reviewable ZIP (no source PDFs)."""
from pathlib import Path
from datetime import datetime
import json
import shutil
import sys
import zipfile
from collections import Counter
from scan_all import report

root=Path(__file__).resolve().parent
workspace=root.parent
stamp=datetime.now().strftime('%Y%m%d_%H%M%S')
out=workspace/'outputs'/f'ket_qua_OCR_{stamp}'
out.mkdir(parents=True)
rows=[]
texts={}
for path in sorted((root/'data/audit/pages').glob('*/*.json')):
    if path.name.endswith('.error.json'):continue
    item=json.loads(path.read_text(encoding='utf-8'))
    if item.get('status')!='ok':continue
    row=item['summary'];rows.append(row)
    dest=out/'pages'/path.parent.name/path.name
    dest.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(path,dest)
    text='\n'.join(r['text'] for r in item['audit_view'])
    dest.with_suffix('.txt').write_text(text,encoding='utf-8')
    texts.setdefault(row['source'],[]).append(f"===== TRANG PDF {row['pdf_page']} | {row['flags'] or 'CHUA_CO_CO'} =====\n{text}")
report(rows,out,2044)
for source,parts in texts.items():
    (out/f'{source}_OCR_CHUA_SUA.txt').write_text('\n\n'.join(parts)+'\n',encoding='utf-8')
shutil.copytree(root/'data/sample',out/'MAU_33_TRANG')
sample=out/'MAU_DONG_8_HANG';sample.mkdir()
for name in ['CPO03_poem01_verse_parallel.tsv','CPO03_poem01_verse_parallel.xlsx']:
    shutil.copy2(workspace/'pipeline/trial/output'/name,sample/name)
shutil.copy2(root/'KET_QUA_THU.md',out/'KET_QUA_THU_33_TRANG.md')
counts=Counter(r['source'] for r in rows)
lines=['# Kết quả OCR đã xuất','',f'Bản chụp kết quả: {len(rows)}/2.044 trang đã OCR thành công. Đây chưa phải kết quả quét xong toàn bộ.','',
       '## Mở tệp nào?','',
       '- review.html: lọc trang có cờ, xem text OCR và mở PDF đúng trang trên máy hiện tại.',
       '- all_pages.csv: mở bằng Excel, mỗi hàng là một trang đã xử lý.',
       '- review_pages.csv: chỉ các trang có cờ; cờ không phải lỗi đã được xác minh.',
       '- *_OCR_CHUA_SUA.txt: text OCR nối theo nguồn, có dấu phân trang PDF.',
       '- pages/: TXT từng trang và JSON chứa OCR thô của từng mô hình, bbox, confidence.',
       '- MAU_33_TRANG/: đợt thử riêng đã đủ 33 trang phân bố trên cả sáu PDF.',
       '- MAU_DONG_8_HANG/: tám hàng thơ đã sửa/dóng thủ công trước đó, đủ bốn cột; không phải kết quả tự dóng hàng loạt.','',
       '## Phạm vi đợt quét toàn bộ tại lúc xuất','', '| Nguồn | Trang đã OCR |','|---|---:|']
for s in ['CPO01_HAN','CPO01_VI','CPO02','CPO03','CPO04','CPO05']:
    lines.append(f'| {s} | {counts[s]} |')
lines+=['','Text OCR chưa sửa, chưa tách hoàn chỉnh từng bản và chưa dóng toàn bộ. Thứ tự bản xem nhanh có thể sai, đặc biệt cột dọc. Không dùng trực tiếp làm dữ liệu nộp.','',
        'Tên cờ: RAT_IT_TEXT = ít chữ; NHIEU_BOX_CONF_THAP / CONF_TRUNG_BINH_THAP = nhận dạng yếu; NGHI_MAT_DAU_VIET = nghi mất dấu; CAN_XEP_THU_TU_COT_DOC = cần kiểm thứ tự cột.']
(out/'DOC_TRUOC.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
import subprocess
subprocess.run([sys.executable,'-X','utf8',str(root/'make_report.py'),'--audit',str(out)],check=True)
archive=out.with_suffix('.zip')
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for p in out.rglob('*'):
        if p.is_file():z.write(p,p.relative_to(out))
print(json.dumps({'folder':str(out),'zip':str(archive),'pages':len(rows),'by_source':dict(counts)},ensure_ascii=False))
