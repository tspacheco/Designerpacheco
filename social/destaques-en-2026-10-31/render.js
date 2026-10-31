const { chromium } = require('playwright'); const fs=require('fs'); const path=require('path');
(async()=>{ const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1080,height:1920}});
for (const f of fs.readdirSync(__dirname).filter(f=>f.endsWith('.html')).sort()){
 await p.goto('file://'+path.join(__dirname,f)); await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(300);
 const over=await p.evaluate(()=>{const fr=document.querySelector('.foot').getBoundingClientRect();return fr.bottom>1920-105});
 await p.screenshot({path:path.join(__dirname,f.replace('.html','.png'))}); console.log(f, over?'OVERFLOW':'ok');}
await b.close();})();
