"""One short consecutive excerpt per source, preserving original scan pages."""
from pathlib import Path
import io
import json
import pymupdf
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors

root=Path(__file__).resolve().parents[1]
workspace=root.parent
out=workspace/'output/pdf'
out.mkdir(parents=True,exist_ok=True)
specs=[
 (1,'Tang thương - Vua Thần Tôn: Hán',[14],'Đối chiếu bản Việt ngay sau'),
 (2,'Tang thương - Vua Thần Tôn: Việt',[17,18,19],'Dừng trước đề mục Vua Hiến Tôn ở trang cuối'),
 (3,'Hoàng Việt - Ngọc tỉnh liên phú: Hán',[154,153,152,151],'Đảo thứ tự trang PDF để theo thứ tự tờ Hán 1a-2b'),
 (3,'Hoàng Việt - Ngọc tỉnh liên phú: Việt',list(range(19,26)),'Phiên âm, bản dịch và chú thích trong sách'),
 (4,'Ngô Thì Nhậm - Tân niên cung hạ nghiêm thân',[44,45,46],'Đủ Hán/âm/nghĩa/thơ; dừng trước bài số 2'),
 (5,'Phan Huy Ích - Lên chòi Hoàng Hạc (bài 160)',[25,26],'Hán, phiên âm, dịch nghĩa, dịch thơ'),
 (6,'Tổng tập văn học VN 1 - Quốc tộ',[217],'Hán, phiên âm, dịch nghĩa, dịch thơ trong một trang'),
]
pdfmetrics.registerFont(TTFont('Arial','C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('ArialBold','C:/Windows/Fonts/arialbd.ttf'))
buffer=io.BytesIO()
c=canvas.Canvas(buffer,pagesize=A4)
w,h=A4
c.setFont('ArialBold',20);c.drawString(42,h-60,'MẪU OCR VÀ DÓNG HÀNG - ĐỦ BẢN')
c.setFont('Arial',11)
for i,line in enumerate(['21 trang scan + 1 trang hướng dẫn; đủ 6 file nguồn của 5 tác phẩm.',
                         'Lấy cùng bài ở các bản tương ứng, giữ nguyên ảnh scan.',
                         'Trang nguồn là số trang PDF, tính từ 1; phần Hán Hoàng Việt được sắp lại.']):
    c.drawString(42,h-88-i*18,line)
style=ParagraphStyle('body',fontName='Arial',fontSize=10,leading=14)
header=ParagraphStyle('header',parent=style,fontName='ArialBold',textColor=colors.white)
data=[[Paragraph(s,header) for s in ['Nguồn / đặc điểm','PDF gốc','PDF mẫu']]]
index=2;manifest=[]
for f,name,pages,desc in specs:
    count=len(pages)
    page_label='154 → 151' if pages==[154,153,152,151] else (str(pages[0]) if count==1 else f'{pages[0]}-{pages[-1]}')
    data.append([Paragraph(name+'<br/>'+desc,style),Paragraph(page_label,style),Paragraph(f'{index}-{index+count-1}',style)])
    manifest.append({'source_file':f'source_{f}.pdf','title':name,'source_pages':pages,'sample_pages':[index,index+count-1]})
    index+=count
t=Table(data,colWidths=[340,80,90])
t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#234968')),
                      ('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),9),
                      ('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),10),
                      ('BOTTOMPADDING',(0,0),(-1,-1),10),
                      ('LINEBELOW',(0,1),(-1,-1),.4,colors.HexColor('#d5dce3'))]))
tw,th=t.wrap(510,h)
t.drawOn(c,42,h-165-th)
c.setFont('ArialBold',11);c.drawString(42,h-195-th,'Cách dùng')
c.setFont('Arial',10)
for i,line in enumerate(['Chỉ OCR trang 2-22; bỏ trang hướng dẫn này. Chú thích không đem dóng.',
                         'Trang cuối mỗi khúc có thể chứa đầu bài sau: chỉ xử lý bài ghi trong bảng.',
                         'Mẫu có bản đối chiếu để thử pipeline, chưa phải kết quả đã dóng.']):
    c.drawString(42,h-215-th-i*17,line)
c.save();buffer.seek(0)
result=pymupdf.open(stream=buffer.getvalue(),filetype='pdf')
toc=[]
for f,name,pages,_ in specs:
    toc.append([1,name,len(result)+1])
    with pymupdf.open(workspace/f'source-inventory/source_{f}.pdf') as src:
        for page in pages:
            result.insert_pdf(src,from_page=page-1,to_page=page-1)
result.set_toc(toc)
result.set_metadata({'title':'Mẫu OCR và dóng hàng - đủ bản đối chiếu','subject':'21 trang scan từ 6 PDF; các bài có bản tương ứng'})
target=out/'sample_OCR_6_nguon.pdf'
result.save(target,garbage=4,deflate=True)
assert len(result)==22
qa=workspace/'source-inventory/sample_pdf_qa'
qa.mkdir(exist_ok=True)
from PIL import Image,ImageDraw
sheet=Image.new('RGB',(1000,((len(result)+4)//5)*330),'#ddd')
draw=ImageDraw.Draw(sheet)
for i,p in enumerate(result):
    pix=p.get_pixmap(matrix=pymupdf.Matrix(min(190/p.rect.width,295/p.rect.height),min(190/p.rect.width,295/p.rect.height)))
    im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
    x=(i%5)*200;y=(i//5)*330
    sheet.paste(im,(x,y+20));draw.text((x+5,y+3),f'Page {i+1}',fill='black')
sheet.save(qa/'contact.png')
result[0].get_pixmap(matrix=pymupdf.Matrix(1.3,1.3)).save(qa/'cover.png')
print(json.dumps({'pdf':str(target),'pages':len(result),'bytes':target.stat().st_size,'sections':manifest},ensure_ascii=False))
