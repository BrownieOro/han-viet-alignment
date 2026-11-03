"""Make a local searchable review page from completed OCR checkpoints."""
from pathlib import Path
import json
import html
import argparse

CONTENT = {'CPO01_HAN':[(14,138)],'CPO01_VI':[(17,232)],'CPO02':[(19,109),(113,161)],
           'CPO03':[(44,203),(209,320),(326,867)],'CPO04':[(4,45),(47,156)],'CPO05':[(213,456)]}
FILES = {'CPO01_HAN':'source_1.pdf','CPO01_VI':'source_2.pdf','CPO02':'source_3.pdf',
         'CPO03':'source_4.pdf','CPO04':'source_5.pdf','CPO05':'source_6.pdf'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--audit',type=Path,default=Path(__file__).resolve().parent/'data/audit')
    p.add_argument('--sources',type=Path,default=Path(__file__).resolve().parents[1]/'source-inventory')
    args=p.parse_args();records=[]
    for path in sorted((args.audit/'pages').glob('*/*.json')):
        if path.name.endswith('.error.json'): continue
        item=json.loads(path.read_text(encoding='utf-8'));s=item['summary']
        s['content']=any(a<=s['pdf_page']<=b for a,b in CONTENT[s['source']])
        s['pdf']=(args.sources/FILES[s['source']]).resolve().as_uri()+f"#page={s['pdf_page']}"
        s['text']='\n'.join(r['text'] for r in item['audit_view'])
        records.append(s)
    data=json.dumps(records,ensure_ascii=False).replace('</','<\\/')
    page='''<!doctype html><html lang="vi"><meta charset="utf-8"><title>Trang OCR cần xem</title>
<style>body{font:16px system-ui;max-width:1100px;margin:32px auto;padding:0 20px;color:#203047}h1{margin-bottom:8px}button,select,input{font:inherit;padding:8px;margin:4px}article{border:1px solid #ccd5df;border-radius:8px;margin:12px 0;padding:16px}pre{white-space:pre-wrap;font:16px/1.6 system-ui;max-height:350px;overflow:auto}.flag{color:#a23d1c}small{color:#53657b}</style>
<h1>OCR: mở trang nào để sửa?</h1><p id="count"></p>
<p>Đây là kết quả máy chưa sửa. Cờ chỉ để ưu tiên xem, không xác nhận trang còn lại đúng. Chỉ khi đối chiếu ảnh mới biết lỗi thật.</p>
<p><b>Làm ngay:</b> chọn nguồn của mình → mở PDF đúng trang → tìm text sẵn hoặc sửa text OCR → tách các bản theo bài → dóng → đổi người kiểm.</p>
<select id="source"><option value="">Mọi nguồn</option></select>
<select id="scope"><option value="content">Trong phạm vi nội dung đã chia</option><option value="all">Mọi trang, kể cả bìa/mục lục</option></select>
<select id="flag"><option value="any">Có cờ cần xem</option><option value="all">Cả trang chưa có cờ</option><option value="quality">Cờ chất lượng (bỏ cờ cột dọc)</option></select>
<input id="query" placeholder="Tìm trong text OCR"><button id="prev">Trước</button><button id="next">Sau</button><span id="paging"></span><main id="list"></main>
<script>const rows=DATA;let offset=0;const $=id=>document.getElementById(id);const escape=s=>String(s).replace(/[&<>\"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
[...new Set(rows.map(r=>r.source))].forEach(s=>{let o=document.createElement('option');o.value=s;o.textContent=s;$('source').append(o)});
$('count').textContent=`Đã có ${rows.length}/2044 trang trong báo cáo này. Chạy lại make_report.py để cập nhật khi quét xong.`;
function render(){let r=rows.filter(r=>(!$('source').value||r.source===$('source').value)&&($('scope').value==='all'||r.content)&&($('flag').value==='all'||($('flag').value==='quality'?r.flags.split(';').some(f=>f&&f!=='CAN_XEP_THU_TU_COT_DOC'):r.flags))&&r.text.toLowerCase().includes($('query').value.toLowerCase()));r.sort((a,b)=>b.weak_box_ratio-a.weak_box_ratio||a.source.localeCompare(b.source)||a.pdf_page-b.pdf_page);offset=Math.min(offset,Math.max(0,Math.floor((r.length-1)/20)*20));$('paging').textContent=`${offset+1}–${Math.min(offset+20,r.length)} / ${r.length}`;$('list').innerHTML=r.slice(offset,offset+20).map(r=>`<article><b>${escape(r.source)} · PDF trang ${r.pdf_page}</b> <a href="${escape(r.pdf)}" target="_blank">Mở PDF</a><p class="flag">${escape(r.flags||'Chưa có cờ — vẫn cần QA')}</p><small>${r.chars} ký tự · ${r.boxes} box · ${(100*r.weak_box_ratio).toFixed(0)}% box confidence dưới 0,8</small><details><summary>Xem text OCR chưa sửa</summary><pre>${escape(r.text)}</pre></details></article>`).join('')}
['source','scope','flag','query'].forEach(id=>$(id).addEventListener('input',()=>{offset=0;render()}));$('prev').onclick=()=>{offset=Math.max(0,offset-20);render()};$('next').onclick=()=>{offset+=20;render()};render();</script></html>'''.replace('DATA',data)
    target=args.audit/'review.html';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(page,encoding='utf-8')
    print(f'Report: {len(records)} successful pages -> {target}')

if __name__=='__main__':main()
