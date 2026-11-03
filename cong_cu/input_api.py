"""Known local sources and single-image OCR jobs; nothing leaves this machine."""
from pathlib import Path
import base64
import io
import os
import threading
import uuid
import time

ROOT=Path(__file__).resolve().parents[1]
SPECS=[('CPO01_HAN','Tang thương ngẫu lục — Hán',138),('CPO01_VI','Tang thương ngẫu lục — Việt',237),('CPO02','Hoàng Việt văn tuyển',166),('CPO03','Ngô Thì Nhậm toàn tập 1',882),('CPO04','Thơ văn Phan Huy Ích 2',160),('CPO05','Tổng tập văn học Việt Nam 1',461)]
JOBS={};LOCK=threading.Lock();ENGINES={}
def sources():return [dict(id=i+1,code=c,name=n,pages=p,available=(ROOT/f'inputs/source_{i+1}.pdf').is_file()) for i,(c,n,p) in enumerate(SPECS)]
def source_path(value):
    i=int(value)
    if not 1<=i<=6:raise ValueError('Nguồn không hợp lệ')
    p=ROOT/f'inputs/source_{i}.pdf'
    if not p.is_file():raise ValueError('Thiếu file nguồn')
    return p
def page_png(source,page):
    import pymupdf
    with pymupdf.open(source_path(source)) as d:
        page=int(page)
        if not 1<=page<=len(d):raise ValueError('Trang ngoài phạm vi')
        p=d[page-1];scale=min(2,1600/max(p.rect.width,p.rect.height))
        return p.get_pixmap(matrix=pymupdf.Matrix(scale,scale),alpha=False).tobytes('png')
def start_ocr(data):
    if len([j for j in JOBS.values() if j['status'] in {'queued','running'}])>=3:raise ValueError('Đang có nhiều ảnh chờ. Đợi xong rồi gửi tiếp.')
    lang=data.get('lang','ch')
    if lang not in {'ch','vi'}:raise ValueError('Chọn Hán hoặc Việt')
    raw=base64.b64decode(data['image'],validate=True)
    if len(raw)>15*1024*1024:raise ValueError('Ảnh tối đa 15 MB')
    from PIL import Image
    with Image.open(io.BytesIO(raw)) as im:
        if im.width*im.height>20_000_000:raise ValueError('Ảnh tối đa 20 triệu pixel')
        im.verify()
    key=str(uuid.uuid4());JOBS[key]={'status':'queued','created':time.time()}
    def run():
        with LOCK:
            JOBS[key]={'status':'running','message':'Đang OCR trên CPU; lần đầu cần nạp mô hình.'}
            try:
                os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION']='python'
                from paddleocr import PaddleOCR
                import numpy as np
                if lang not in ENGINES:ENGINES[lang]=PaddleOCR(lang=lang,use_gpu=False,show_log=False,cpu_threads=2,enable_mkldnn=False,det_limit_side_len=1400)
                with Image.open(io.BytesIO(raw)) as im:
                    im=im.convert('RGB');w,h=im.size;a=np.asarray(im)[:,:,::-1].copy()
                result=ENGINES[lang].ocr(a,cls=False)
                rows=[{'bbox':b,'text':t,'confidence':float(s)} for p in result if p for b,(t,s) in p]
                JOBS[key]={'status':'done','image_width':w,'image_height':h,'rows':rows,'lang':lang}
            except Exception as e:JOBS[key]={'status':'error','message':str(e)}
    threading.Thread(target=run,daemon=True).start();return key
