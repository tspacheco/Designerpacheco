const {chromium}=require('playwright');
(async()=>{const dir=process.argv[2],T=+process.argv[3],fps=30;
const b=await chromium.launch({args:['--allow-file-access-from-files']});const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+dir+'/overlay.html');await p.evaluate(()=>document.fonts.ready);
for(let i=0;i<=T*fps;i++){await p.evaluate(t=>render(t),i/fps);await p.screenshot({path:`${dir}/fr/${String(i).padStart(4,'0')}.png`,omitBackground:true});}
await b.close();})();
