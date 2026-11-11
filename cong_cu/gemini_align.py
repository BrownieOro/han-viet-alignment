"""Small-block Gemini alignment; caller must provide one block only."""
import json,re
from pathlib import Path
from urllib import request,error
MODELS={'gemini-3.5-flash-lite','gemini-3.5-flash'}; KEY_FILE=Path(__file__).resolve().parents[1]/'.gemini_api_key'
def local_key():
 try:return KEY_FILE.read_text(encoding='utf-8-sig').strip()
 except FileNotFoundError:return ''
def align(data):
 key=str(data.get('apiKey','')).strip() or local_key(); model=data.get('model','gemini-3.5-flash-lite'); versions=data.get('versions',[]); texts=data.get('texts',{})
 if not key:return 400,{'error':'Chưa có Gemini key.'}
 if model not in MODELS or len(versions) not in {2,4}:return 400,{'error':'Model hoặc số bản không hợp lệ.'}
 if any(len(texts.get(v,[]))>60 for v in versions):return 413,{'error':'Mỗi block tối đa 60 dòng/bản.'}
 prompt=('Gợi ý dóng hàng Hán–Việt. Không dịch, không sửa text. Các bản theo thứ tự '+', '.join(versions)+'. Trả JSON duy nhất {"groups":[{"lines":{"version":[1]},"status":"pending","note":""}]}. Chỉ số dòng bắt đầu từ 1; cho phép [] và nhóm nhiều dòng; không bỏ đoạn; chỗ không chắc ghi note. Dữ liệu:\n'+json.dumps(texts,ensure_ascii=False))
 body=json.dumps({'contents':[{'parts':[{'text':prompt}]}],'generationConfig':{'maxOutputTokens':4096,'thinkingConfig':{'thinkingLevel':'minimal'}}}).encode(); req=request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent',data=body,headers={'Content-Type':'application/json','x-goog-api-key':key},method='POST')
 try:
  with request.urlopen(req,timeout=45) as res: out=json.load(res)
 except error.HTTPError as e:return e.code,{'error':'Gemini alignment lỗi HTTP '+str(e.code)}
 except Exception as e:return 504,{'error':str(e)}
 raw=''.join(p.get('text','') for p in (out.get('candidates',[{}])[0].get('content',{}).get('parts',[]) or [])); raw=re.sub(r'^```json\s*|\s*```$','',raw.strip())
 try: result=json.loads(raw)
 except Exception:return 422,{'error':'Gemini không trả JSON hợp lệ.','raw':raw[:1000]}
 return (200,{'groups':result['groups'],'usage':out.get('usageMetadata',{})}) if isinstance(result.get('groups'),list) else (422,{'error':'Thiếu groups.'})
