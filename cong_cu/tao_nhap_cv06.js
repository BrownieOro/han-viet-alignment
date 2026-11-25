/* Prepare reviewable segmentation; do not overwrite an existing edited project. */
const fs = require('node:fs');
const path = require('node:path');
const {split} = require('../cv06_split.js');
const dir = process.argv[2];
if (!dir) throw new Error('Cần đường dẫn đợt đã OCR.');
const manifest = JSON.parse(fs.readFileSync(path.join(dir,'dot_xu_ly.json'),'utf8'));
if (fs.existsSync(path.join(dir,'du_an.json')) || fs.existsSync(path.join(dir,'03_text_sach'))) {
 throw new Error('Đã có dự án hoặc text sạch: dừng để không ghi đè chỉnh sửa.');
}
const versions=['han','viet','dich_am','dich_nghia','dich_tho','unclassified','excluded'];
const pages={};
for (let page=manifest.from; page<=manifest.to; page++) {
 if ((manifest.skipped||[]).includes(page)) continue;
 const name=String(page).padStart(4,'0');
 const rawPath=path.join(dir,'02_ocr_tho',name+'.txt');
 const imagePath=path.join(dir,'01_nguon',name+'.png');
 if (!fs.existsSync(rawPath)||!fs.existsSync(imagePath)) throw new Error('Thiếu trang '+page+'; chưa tạo bản nháp.');
 const raw=fs.readFileSync(rawPath,'utf8');
 const sidecar=path.join(dir,'02_ocr_tho',name+'.meta.json');
 const source=fs.existsSync(sidecar)?JSON.parse(fs.readFileSync(sidecar,'utf8')):null;
 pages[String(page)]={page,image:'data:image/png;base64,'+fs.readFileSync(imagePath).toString('base64'),raw,parts:split(raw),engine:source?.engine||manifest.model,checked:false,notes:source?.note||'Tách tự động; chưa đối chiếu; kiểm đầu/chân trang, chú thích và nối bản qua trang.'};
}
const output={format:'cv06-project-v2',meta:{work:manifest.work,owner:'Trân',title:manifest.section,url:'',source:manifest.source_name},pages};
for (const v of versions) {
 const text=Object.values(pages).map(p=>p.parts[v].trim()).filter(Boolean).join('\n\n');
 if (!text) continue;
 const dest=path.join(dir,v==='unclassified'?'can_phan_loai':v==='excluded'?'ghi_chu_phan_loai':'03_text_sach');
 fs.mkdirSync(dest,{recursive:true});fs.writeFileSync(path.join(dest,v+'.txt'),text+'\n',{flag:'wx'});
}
fs.writeFileSync(path.join(dir,'du_an.json'),JSON.stringify(output),{flag:'wx'});
const exceptions=Object.values(pages).filter(p=>p.engine!==manifest.model).map(p=>`- PDF ${p.page}: ${p.engine}. ${p.notes}`).join('\n');
fs.writeFileSync(path.join(dir,'README.md'),`# ${manifest.work}: ${manifest.section}\n\nNguồn: ${manifest.source_name}; PDF ${manifest.from}–${manifest.to}; người phụ trách: Trân. Trang bỏ qua sau khi xem nguồn: ${(manifest.skipped||[]).join(', ')||'không'}.\n\n01: ảnh từng trang. 02: OCR thô ${manifest.model}, trừ các ngoại lệ bên dưới; không tự xem là đúng. 03: bản tách tự động theo nhãn, CHƯA ĐỐI CHIẾU. Nội dung không xác định nằm tại can_phan_loai; chú thích nhận diện được nằm tại ghi_chu_phan_loai. Quy tắc có thể nhầm chú thích, tiêu đề, giới thiệu, ranh giới trang và bỏ sót các bản thiếu nhãn; phải kiểm tất cả với ảnh trước khi gộp, dóng hàng hoặc tính chỉ tiêu. Mở du_an.json bằng tool để sửa. Chưa có 04.\n\nNgoại lệ nguồn text:\n${exceptions||'- Không.'}\n`,{flag:'wx'});
console.log('Đã tạo nháp cho',Object.keys(pages).length,'trang; chưa đối chiếu.');
