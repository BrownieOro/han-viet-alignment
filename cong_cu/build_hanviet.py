"""Build offline reading hints from a pinned Unicode Unihan release."""
from pathlib import Path
import io,json,re,urllib.request,zipfile,hashlib,csv,ast
root=Path(__file__).resolve().parents[1]
url='https://www.unicode.org/Public/17.0.0/ucd/Unihan.zip'
raw=urllib.request.urlopen(url,timeout=60).read()
with zipfile.ZipFile(io.BytesIO(raw)) as z:
 readings={};variants={}
 for line in z.read('Unihan_Readings.txt').decode('utf-8').splitlines():
  if line.startswith('#') or not line.strip():continue
  cp,field,value=line.split('\t',2)
  if field=='kVietnamese':readings[chr(int(cp[2:],16))]=list(dict.fromkeys(v.lower() for v in value.split()))
 for line in z.read('Unihan_Variants.txt').decode('utf-8').splitlines():
  if line.startswith('#') or not line.strip():continue
  cp,field,value=line.split('\t',2)
  if field in {'kTraditionalVariant','kSimplifiedVariant','kZVariant'}:
   c=chr(int(cp[2:],16))
   for h in re.findall(r'U\+([0-9A-F]+)',value):
    other=chr(int(h,16));variants.setdefault(c,set()).add(other);variants.setdefault(other,set()).add(c)
 result={c:list(v) for c,v in readings.items()}
 for c,others in variants.items():
  for other in sorted(others):
   for v in readings.get(other,[]):
    if v not in result.setdefault(c,[]):result[c].append(v)
 result={c:v for c,v in result.items() if v}
out=root/'assets/hanviet';out.mkdir(parents=True,exist_ok=True)
primary={}
base='https://raw.githubusercontent.com/ph0ngp/hanviet-pinyin-wordlist/b9923df92c8b55f013001390e37cddd35e986dc1/'
csvraw=urllib.request.urlopen(base+'hanviet.csv',timeout=60).read()
for item in csv.DictReader(io.StringIO(csvraw.decode('utf-8-sig'))):
 c=item['char'];values=ast.literal_eval(item['hanviet'])
 if len(c)!=1 or not isinstance(values,list):continue
 for v in values:
  if isinstance(v,str) and v not in primary.setdefault(c,[]):primary[c].append(v)
for c,values in primary.items():
 if values:result[c]=list(dict.fromkeys(values+result.get(c,[])))
(out/'PHONG_PHAN_LICENSE.txt').write_bytes(urllib.request.urlopen(base+'LICENSE',timeout=60).read())
(out/'readings.json').write_text(json.dumps(result,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
(out/'SOURCE.md').write_text('Âm gợi ý ưu tiên Phong Phan hanviet-pinyin-wordlist (MIT), commit b9923df92c8b55f013001390e37cddd35e986dc1; gộp âm của các pinyin vì chưa chọn theo ngữ cảnh. Bổ sung Unicode Unihan 17.0.0 kVietnamese và một bước biến thể kTraditionalVariant/kSimplifiedVariant/kZVariant (hai chiều). kVietnamese có thể chứa âm Nôm; tất cả chỉ là gợi ý, không tự xác nhận âm đúng. Không đổi chữ nguồn.\n\nNguồn CSV: '+base+'hanviet.csv\nSHA-256 CSV: '+hashlib.sha256(csvraw).hexdigest()+'\nNguồn Unihan: '+url+'\nSHA-256 ZIP: '+hashlib.sha256(raw).hexdigest()+'\n\nTạo lại: python cong_cu/build_hanviet.py (chỉ thư viện chuẩn, cần mạng lúc build).\nGiấy phép: PHONG_PHAN_LICENSE.txt (MIT) và LICENSE.txt (Unicode).\n',encoding='utf-8')
print(len(result),'characters;', {c:result.get(c) for c in '為爲絡'})
