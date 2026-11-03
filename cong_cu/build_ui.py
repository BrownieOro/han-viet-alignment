"""Keep index.html standalone; replace bundled modules from editable sources."""
from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]
p=root/'index.html';text=p.read_text(encoding='utf-8')
matches=list(re.finditer(r'<script>(.*?)</script>',text,re.S))
core=matches[0].group(1)
core=core.replace('b=enc.encode(content),c=crc(b)','b=content instanceof Uint8Array?content:enc.encode(content),c=crc(b)')
names=['demo_data.js','box_editor.js','review_import.js','local_sync.js','quick_input.js','input_ocr.js']
scripts=[core]+[(root/'cong_cu/ui'/n).read_text(encoding='utf-8') for n in names]
text=text[:matches[0].start()]+''.join('<script>\n'+s.replace('</script','<\\/script')+'\n</script>' for s in scripts)+'</html>\n'
p.write_text(text,encoding='utf-8');print('Built single-file index.html')
