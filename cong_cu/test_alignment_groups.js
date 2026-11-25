'use strict';
const assert=require('node:assert/strict');
const {materialize}=require('../alignment_groups');
for(const versions of [['han','viet'],['han','dich_am','dich_nghia','dich_tho']]){
 const texts=Object.fromEntries(versions.map(v=>[v,[v+' 1',v+' 2']]));
 const group=n=>({lines:Object.fromEntries(versions.map(v=>[v,[n]]))});
 assert.deepEqual(materialize([group(1),group(2)],versions,texts),[versions.map(v=>v+' 1'),versions.map(v=>v+' 2')]);
 assert.throws(()=>materialize([group(1)],versions,texts));
 assert.throws(()=>materialize([group(1),group(1),group(2)],versions,texts));
 assert.throws(()=>materialize([group(2),group(1)],versions,texts));
}
console.log('Alignment validation: 2/4 columns, missing, duplicate and out-of-order cases passed');
