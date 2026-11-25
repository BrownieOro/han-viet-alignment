(function(root){'use strict';
 function materialize(groups,versions,texts){
  if(!Array.isArray(groups)||!groups.length)throw Error('Gợi ý không có hàng.');
  const seen=Object.fromEntries(versions.map(v=>[v,[]]));
  const rows=groups.map(g=>{if(!g||!g.lines||typeof g.lines!=='object')throw Error('Thiếu chỉ số dòng.');return versions.map(v=>{const ids=g.lines[v];if(!Array.isArray(ids))throw Error('Thiếu bản '+v);for(const id of ids){if(!Number.isInteger(id)||id<1||id>texts[v].length)throw Error('Chỉ số dòng không hợp lệ ở '+v);seen[v].push(id)}return ids.map(id=>texts[v][id-1]).join(' ')})});
  for(const v of versions){const expected=texts[v].map((_,i)=>i+1);if(JSON.stringify(seen[v])!==JSON.stringify(expected))throw Error('Dòng '+v+' bị thiếu, trùng hoặc sai thứ tự; chưa nạp gợi ý.')}
  if(rows.some(r=>r.every(x=>!x)))throw Error('Có hàng rỗng.');return rows;
 }
 if(typeof module!=='undefined'&&module.exports)module.exports={materialize};root.AlignmentGroups={materialize};
})(typeof window==='undefined'?globalThis:window);
