"""Build reviewable alignment cases from collected Markdown files."""
from pathlib import Path
import json,re,unicodedata
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'cases'; OUT.mkdir(exist_ok=True)
HEAD={'Hán':'han','Dịch âm':'dich_am','Dịch nghĩa / Việt văn xuôi':'dich_nghia','Dịch thơ':'dich_tho'}
def slug(s): return re.sub(r'[^a-z0-9]+','_',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()).strip('_')
def parse(p):
 s=p.read_text(encoding='utf-8').replace('\r',''); title=re.search(r'^# Tên bài:\s*(.*)$',s,re.M); work=re.search(r'^- Tác phẩm:\s*(.*)$',s,re.M); page=re.search(r'^- Trang PDF:\s*\[?([^\]\n]+)',s,re.M); source=re.search(r'^- Nguồn sách:\s*(.*)$',s,re.M); link=re.search(r'^- Link lấy text:\s*(.*)$',s,re.M); match=re.search(r'^- Đối chiếu sách:\s*(.*)$',s,re.M); sections={}; ms=list(re.finditer(r'^## (.+?)\s*$',s,re.M))
 for i,m in enumerate(ms):
  k=HEAD.get(m.group(1).strip()); end=ms[i+1].start() if i+1<len(ms) else len(s)
  if k: sections[k]=s[m.end():end].strip()
 versions=[k for k in ['han','dich_am','dich_nghia','dich_tho'] if sections.get(k) and not sections[k].startswith('[Dán') and 'Chưa tìm thấy' not in sections[k]]
 if 'han' not in versions or not any(k in versions for k in ['dich_am','dich_nghia']): return None
 return {'work_id':f'{p.parts[-3]}_{slug(title.group(1) if title else p.stem)}','title':title.group(1).strip() if title else p.stem,'work':work.group(1).strip() if work else '','pdf_page':page.group(1).strip() if page else '','source_file':source.group(1).strip() if source else '','match_status':match.group(1).strip() if match else '','source_link':link.group(1).strip() if link and link.group(1).strip() not in {'Không','[]'} else '','kind':'poetry' if 'dich_tho' in versions else 'prose','versions':versions,'text':{k:[x.strip() for x in sections[k].splitlines() if x.strip()] for k in versions},'file':p.relative_to(ROOT).as_posix()}
cases=[]
for p in sorted((ROOT/'bai_lam').rglob('*.md')):
 c=parse(p)
 if c: cases.append(c)
(OUT/'index.json').write_text(json.dumps({'schema':'hanviet-cases-v1','cases':cases},ensure_ascii=False,indent=2),encoding='utf-8'); print('built',len(cases),'cases')
