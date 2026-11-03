"""Loopback-only viewer; reads submitted files, never writes student output."""
from pathlib import Path
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import hashlib
import mimetypes

ROOT=Path(__file__).resolve().parents[1]
SUBMISSIONS=ROOT/'bai_lam'
STATIC={'index.html','box_editor.js','review_import.js','demo_data.js','local_sync.js'}

class Handler(BaseHTTPRequestHandler):
    def send(self,status,body,mime='application/json; charset=utf-8'):
        if isinstance(body,str):body=body.encode('utf-8')
        self.send_response(status);self.send_header('Content-Type',mime)
        self.send_header('Content-Length',str(len(body)));self.send_header('Cache-Control','no-store')
        self.send_header('X-Content-Type-Options','nosniff');self.send_header('Cross-Origin-Resource-Policy','same-origin')
        self.end_headers();self.wfile.write(body)
    def do_GET(self):
        if self.headers.get('Host') not in {'127.0.0.1:7070','localhost:7070'}:
            self.send(403,'Host rejected');return
        origin=self.headers.get('Origin')
        if origin and origin not in {'http://127.0.0.1:7070','http://localhost:7070'}:
            self.send(403,'Origin rejected');return
        u=urlparse(self.path)
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

if __name__=='__main__':
    print('Open http://127.0.0.1:7070 — reads bai_lam/, no writes to submitted files.',flush=True)
    ThreadingHTTPServer(('127.0.0.1',7070),Handler).serve_forever()
