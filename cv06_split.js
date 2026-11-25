/* Conservative page segmentation: unclassified and excluded text remain reviewable. */
(function (root) {
  'use strict';
  const labels = {
    'PHIÊN ÂM':'dich_am','PHIEN AM':'dich_am','DỊCH ÂM':'dich_am','DICH AM':'dich_am',
    'DỊCH NGHĨA':'dich_nghia','DICH NGHIA':'dich_nghia','DỊCH THƠ':'dich_tho','DICH THO':'dich_tho',
    'NGUYÊN VĂN':'han','NGUYEN VAN':'han','CHỮ HÁN':'han','CHU HAN':'han',
    'CHÚ THÍCH':'excluded','CHU THICH':'excluded','KHẢO DỊ':'excluded','KHAO DI':'excluded'
  };
  function split(raw) {
    const result = {han:'',viet:'',dich_am:'',dich_nghia:'',dich_tho:'',unclassified:'',excluded:''};
    let section = 'unclassified';
    for (const line of String(raw || '').replace(/\r\n?/g,'\n').replace(/\[(?:không đọc rõ|字未詳)\]/giu,'[MASK]').split('\n')) {
      const key = line.trim().replace(/[:：]\s*$/, '').toLocaleUpperCase('vi');
      if (Object.prototype.hasOwnProperty.call(labels,key)) { section=labels[key]; continue; }
      // A CJK-only line can be assigned safely; mixed or unlabeled text stays visible for review.
      const trimmed=line.trim();
      const target = section === 'unclassified' && trimmed && /[\u3400-\u9fff]/u.test(trimmed) && !/[A-Za-zÀ-ỹ]/u.test(trimmed) ? 'han' : section;
      result[target] += (result[target] ? '\n' : '') + line;
    }
    for (const key of Object.keys(result)) result[key]=result[key].trim();
    return result;
  }
  if (typeof module !== 'undefined' && module.exports) module.exports={split};
  root.CV06Split={split};
})(typeof window === 'undefined' ? globalThis : window);
