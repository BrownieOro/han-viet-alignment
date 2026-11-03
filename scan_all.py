"""Local OCR audit, not sentence alignment or a ground-truth generator."""
import os
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
from pathlib import Path
import argparse
import concurrent.futures as futures
import csv
import json
import re
import time
import unicodedata

ENGINES = {}
HAN = re.compile(r'[\u3400-\u9fff\U00020000-\U0002fa1f]')
SOURCES = [
 ('CPO01_HAN','source_1.pdf',['ch']),
 ('CPO01_VI','source_2.pdf',['vi']),
 ('CPO02','source_3.pdf',['ch','vi']),
 ('CPO03','source_4.pdf',['ch','vi']),
 ('CPO04','source_5.pdf',['ch','vi']),
 ('CPO05','source_6.pdf',['ch','vi']),
]

def initialize():
    from paddleocr import PaddleOCR
    for lang in ['ch','vi']:
        ENGINES[lang] = PaddleOCR(lang=lang,use_gpu=False,show_log=False,
                                  cpu_threads=1,enable_mkldnn=False,
                                  det_limit_side_len=1400)

def process(task):
    import pymupdf
    name,path,page,langs,dest = task
    target=Path(dest)/name/f'{page:04d}.json'
    if target.exists():
        cached=json.loads(target.read_text(encoding='utf-8'))
        if cached.get('status')=='ok':
            return cached['summary']
    started=time.time()
    try:
        with pymupdf.open(path) as pdf:
            p=pdf[page-1]
            scale=min(2.0,1400/max(p.rect.width,p.rect.height))
            pix=p.get_pixmap(matrix=pymupdf.Matrix(scale,scale),alpha=False)
        import numpy as np
        img=np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.width,3)[:,:,::-1].copy()
        results={}
        for lang in langs:
            raw=ENGINES[lang].ocr(img,cls=False)
            results[lang]=[{'bbox':b,'text':t,'confidence':float(s)}
                           for sheet in raw if sheet for b,(t,s) in sheet]
        # Choose CJK lines from Chinese model, Latin lines from Vietnamese model.
        # This is an audit view, not a guarantee of correct layout or text.
        zh=[r for r in results.get('ch',[]) if len(HAN.findall(r['text']))>=max(1,len(r['text'].replace(' ',''))*.35)]
        def overlap(a,b):
            ax=[p[0] for p in a['bbox']]; ay=[p[1] for p in a['bbox']]
            bx=[p[0] for p in b['bbox']]; by=[p[1] for p in b['bbox']]
            inter=max(0,min(max(ax),max(bx))-max(min(ax),min(bx)))*max(0,min(max(ay),max(by))-max(min(ay),min(by)))
            area=max(1,(max(ax)-min(ax))*(max(ay)-min(ay)))
            return inter/area
        vi=[r for r in results.get('vi',[]) if not any(overlap(r,z)>.5 for z in zh)]
        chosen=(zh+vi) if len(langs)>1 else results[langs[0]]
        chosen.sort(key=lambda r:(min(p[1] for p in r['bbox']),min(p[0] for p in r['bbox'])))
        text='\n'.join(r['text'] for r in chosen)
        chars=len(re.sub(r'\s','',text))
        weak=sum(r['confidence']<.8 for r in chosen)
        ratio=weak/max(1,len(chosen))
        flags=[]
        if chars<30: flags.append('RAT_IT_TEXT')
        if ratio>.25: flags.append('NHIEU_BOX_CONF_THAP')
        if chosen and sum(r['confidence'] for r in chosen)/len(chosen)<.8: flags.append('CONF_TRUNG_BINH_THAP')
        if name=='CPO01_HAN': flags.append('CAN_XEP_THU_TU_COT_DOC')
        latin=' '.join(r['text'] for r in vi if len(re.findall(r'[A-Za-zÀ-ỹ]',r['text']))>5)
        words=re.findall(r'[A-Za-zÀ-ỹ]+',latin)
        accents=sum(any(unicodedata.normalize('NFD',c)!=c or c in 'đĐ' for c in w) for w in words)
        if len(words)>40 and accents/len(words)<.12: flags.append('NGHI_MAT_DAU_VIET')
        summary={'source':name,'pdf_page':page,'chars':chars,'boxes':len(chosen),
                 'weak_box_ratio':round(ratio,3),'han_chars':len(HAN.findall(text)),
                 'flags':';'.join(flags),'seconds':round(time.time()-started,2),'status':'ok'}
        result={'status':'ok','summary':summary,'raw_by_model':results,'audit_view':chosen,
                'image_width':pix.width,'image_height':pix.height,
                'note':'Heuristic audit. Not verified text; reading order may be wrong.'}
        target.parent.mkdir(parents=True,exist_ok=True)
        temp=target.with_suffix('.tmp')
        temp.write_text(json.dumps(result,ensure_ascii=False),encoding='utf-8')
        temp.replace(target)
        target.with_suffix('.txt').write_text(text,encoding='utf-8')
        return summary
    except Exception as exc:
        summary={'source':name,'pdf_page':page,'chars':0,'boxes':0,'weak_box_ratio':0,
                'han_chars':0,'flags':'OCR_FAILED','seconds':round(time.time()-started,2),
                'status':str(exc)}
        target.parent.mkdir(parents=True,exist_ok=True)
        target.with_suffix('.error.json').write_text(json.dumps(summary,ensure_ascii=False),encoding='utf-8')
        return summary

def report(rows,out,total):
    rows.sort(key=lambda r:(r['source'],r['pdf_page']))
    fields=['source','pdf_page','chars','boxes','weak_box_ratio','han_chars','flags','seconds','status']
    for filename,items in [('all_pages.csv',rows),('review_pages.csv',[r for r in rows if r['flags']])]:
        with (out/filename).open('w',encoding='utf-8-sig',newline='') as f:
            w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(items)
    summary={'expected_pages':total,'processed_pages':len(rows),
             'ok_pages':sum(r['status']=='ok' for r in rows),
             'flagged_pages':sum(bool(r['flags']) for r in rows),
             'by_source':{s:{'processed':sum(r['source']==s for r in rows),
                              'flagged':sum(r['source']==s and bool(r['flags']) for r in rows)} for s,_,_ in SOURCES},
             'warning':'Flags are heuristics, not measured OCR error. Unflagged pages still require QA.'}
    (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')

def main():
    import pymupdf
    p=argparse.ArgumentParser()
    p.add_argument('--sources',type=Path,default=Path(__file__).resolve().parents[1]/'source-inventory')
    p.add_argument('--out',type=Path,default=Path(__file__).resolve().parent/'data/audit')
    p.add_argument('--workers',type=int,default=8)
    p.add_argument('--limit',type=int,default=0,help='Per source; 0 scans every page')
    p.add_argument('--sample',action='store_true',help='Distributed content sample across all six PDFs')
    args=p.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    tasks=[]
    for name,file,langs in SOURCES:
        path=args.sources/file
        with pymupdf.open(path) as d: n=len(d)
        pages=range(1,(min(n,args.limit) if args.limit else n)+1)
        if args.sample:
            samples={'CPO01_HAN':[14,45,80,110,136], 'CPO01_VI':[17,60,120,180,228],
                     'CPO02':[19,55,100,113,140,160], 'CPO03':[44,209,326,520,586,740,850],
                     'CPO04':[4,25,47,90,150], 'CPO05':[213,270,330,390,450]}
            pages=samples[name]
        for page in pages:
            tasks.append((name,str(path),page,langs,str(args.out/'pages')))
    rows=[];start=time.time()
    with futures.ProcessPoolExecutor(max_workers=args.workers,initializer=initialize) as pool:
        jobs=[pool.submit(process,t) for t in tasks]
        for job in futures.as_completed(jobs):
            rows.append(job.result())
            if len(rows)%25==0 or len(rows)==len(tasks):
                report(rows,args.out,len(tasks))
                print(f'{len(rows)}/{len(tasks)} pages; elapsed {time.time()-start:.0f}s',flush=True)
    report(rows,args.out,len(tasks))

if __name__=='__main__': main()
