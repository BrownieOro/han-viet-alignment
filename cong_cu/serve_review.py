"""Loopback-only viewer; reads submitted files, never writes student output."""
from pathlib import Path
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import argparse
import json
import hashlib
import mimetypes
from input_api import sources,source_path,page_png,start_ocr,JOBS
from gemini_ocr import recognize, MAX_REQUEST_BYTES, local_key

# Serve ES modules consistently, including Windows registry MIME overrides.
mimetypes.init()
mimetypes.add_type('text/javascript', '.mjs')

PORT=7070
ROOT=Path(__file__).resolve().parents[1]
SUBMISSIONS=ROOT/'bai_lam'
STATIC={'alignment.html','alignment.js','alignment_export.js','alignment_link.js','hanviet.js','assets/hanviet/readings.json','assets/hanviet/SOURCE.md','assets/hanviet/LICENSE.txt','index.html','advanced.html','OUTPUT_CONTRACT.md','quick_tools.js','gemini_ocr.js','mau/ocr_da_thu.txt','assets/pdfjs/pdf.mjs','assets/pdfjs/pdf.worker.mjs','assets/tesseract/tesseract.min.js','assets/tesseract/worker.min.js'}|{f'inputs/source_{i}.pdf' for i in range(1,7)}

class Handler(BaseHTTPRequestHandler):
    def send(self,status,body,mime='application/json; charset=utf-8'):
        if isinstance(body,str):body=body.encode('utf-8')
        self.send_response(status);self.send_header('Content-Type',mime)
        self.send_header('Content-Length',str(len(body)));self.send_header('Cache-Control','no-store')
        self.send_header('X-Content-Type-Options','nosniff');self.send_header('Cross-Origin-Resource-Policy','same-origin')
        self.end_headers();self.wfile.write(body)
    def do_GET(self):
        if self.headers.get('Host') not in {f'127.0.0.1:{PORT}',f'localhost:{PORT}'}:
            self.send(403,'Host rejected');return
        origin=self.headers.get('Origin')
        if origin and origin not in {f'http://127.0.0.1:{PORT}',f'http://localhost:{PORT}'}:
            self.send(403,'Origin rejected');return
        u=urlparse(self.path)
        if u.path=='/api/gemini-config':
            try:self.send(200, json.dumps({'localKeyConfigured': bool(local_key())}))
            except OSError:self.send(500, json.dumps({'error': 'Không đọc được file key local.'}))
            return
        if u.path=='/api/sources':self.send(200,json.dumps(sources(),ensure_ascii=False));return
        if u.path=='/api/source':
            try:p=source_path(parse_qs(u.query).get('id',[''])[0]);self.send(200,p.read_bytes(),'application/pdf')
            except Exception as e:self.send(400,json.dumps({'error':str(e)}))
            return
        if u.path=='/api/page':
            try:q=parse_qs(u.query);self.send(200,page_png(q['id'][0],q['page'][0]),'image/png')
            except Exception as e:self.send(400,json.dumps({'error':str(e)}))
            return
        if u.path=='/api/ocr':
            key=parse_qs(u.query).get('id',[''])[0]
            self.send(200,json.dumps(JOBS.get(key,{'status':'error','message':'Không thấy tác vụ OCR'}),ensure_ascii=False));return
        if u.path=='/api/files':
            files=[]
            for p in sorted(SUBMISSIONS.rglob('*')):
                if not p.is_file() or not p.resolve().is_relative_to(SUBMISSIONS.resolve()):continue
                if p.suffix.lower() not in {'.tsv','.xlsx','.txt','.pdf','.png','.jpg','.jpeg','.webp'}:continue
                stat=p.stat();files.append({'path':p.relative_to(ROOT).as_posix(),'size':stat.st_size,'modified':stat.st_mtime_ns})
            version=hashlib.sha256(json.dumps(files,sort_keys=True).encode()).hexdigest()
            self.send(200,json.dumps({'version':version,'files':files},ensure_ascii=False));return
        if u.path=='/api/file':
            value=parse_qs(u.query).get('path',[''])[0];p=(ROOT/value).resolve()
            if not p.is_relative_to(SUBMISSIONS.resolve()) or not p.is_file():self.send(404,'Not found');return
            if p.stat().st_size>40*1024*1024:self.send(413,'File larger than 40 MB');return
            self.send(200,p.read_bytes(),mimetypes.guess_type(p.name)[0] or 'application/octet-stream');return
        name=u.path.lstrip('/') or 'index.html'
        if name not in STATIC:self.send(404,'Not found');return
        p=ROOT/name
        if not p.exists():self.send(404,'Not found');return
        self.send(200,p.read_bytes(),mimetypes.guess_type(name)[0] or 'text/plain')
    def log_message(self,*args):pass
    def do_POST(self):
        if self.headers.get('Host') not in {f'127.0.0.1:{PORT}',f'localhost:{PORT}'} or self.headers.get('Origin') not in {f'http://127.0.0.1:{PORT}',f'http://localhost:{PORT}'}:
            self.send(403,'Origin rejected');return
        try:
            if self.path not in {'/api/ocr', '/api/gemini-ocr'}:self.send(404,'Not found');return
            n=int(self.headers.get('Content-Length','0'))
            limit = MAX_REQUEST_BYTES if self.path == '/api/gemini-ocr' else 22*1024*1024
            if not 0<n<limit:
                self.send(413, json.dumps({'error': 'Request vượt giới hạn ' + str(limit / 1_000_000) + ' MB của tool.'}));return
            if self.path == '/api/gemini-ocr':
                data = json.loads(self.rfile.read(n))
                if not isinstance(data, dict):
                    self.send(400, json.dumps({'error': 'Request phải là một đối tượng JSON.'}));return
                status, result = recognize(data)
                self.send(status, json.dumps(result, ensure_ascii=False));return
            key=start_ocr(json.loads(self.rfile.read(n)))
            self.send(202,json.dumps({'id':key}))
        except Exception as e:self.send(400,json.dumps({'error':str(e)},ensure_ascii=False))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=7070);PORT=parser.parse_args().port
    print(f'Open http://127.0.0.1:{PORT} — reads bai_lam/, no writes to submitted files.',flush=True)
    ThreadingHTTPServer(('127.0.0.1',PORT),Handler).serve_forever()
