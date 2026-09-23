// Herói em vídeo a partir de uma fotografia: zoom lento (loop perfeito) + nuvens de especiarias + grãos, tudo determinístico.
// Uso: NODE_PATH=$(npm root -g) node video-foto.js <foto.jpg> <saida.mp4> <largura> <altura> [segundos=10] [fps=24]   (gera também o .webm ao lado)
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), { execFileSync } = require('child_process');
(async () => {
  const [foto, mp4, W, H] = [path.resolve(process.argv[2]), path.resolve(process.argv[3]), +process.argv[4], +process.argv[5]];
  const T = +process.argv[6] || 10, FPS = +process.argv[7] || 24, X = 2; // X = segundos de fusão para o loop das partículas
  const out = mp4 + '.frames'; fs.rmSync(out, { recursive: true, force: true }); fs.mkdirSync(out, { recursive: true });
  const b64 = 'data:image/jpeg;base64,' + fs.readFileSync(foto).toString('base64');
  const html = `<!doctype html><html><head><style>html,body{margin:0;background:#000;overflow:hidden}canvas{display:block}</style></head><body><canvas id="c" width="${W}" height="${H}"></canvas>
<script>
var cv=document.getElementById('c'),ctx=cv.getContext('2d'),W=${W},H=${H},T=${T},img=new Image();img.src=${JSON.stringify(b64)};
function seed(i){var x=Math.sin(i*127.1+311.7)*43758.5453;return x-Math.floor(x);}
function sprite(cor){var s=document.createElement('canvas');s.width=s.height=128;var c=s.getContext('2d');var g=c.createRadialGradient(64,64,0,64,64,64);g.addColorStop(0,'rgba('+cor+',1)');g.addColorStop(.35,'rgba('+cor+',.55)');g.addColorStop(1,'rgba('+cor+',0)');c.fillStyle=g;c.fillRect(0,0,128,128);return s;}
var CORES=[{c:'232,168,37',x:.22},{c:'196,32,43',x:.56},{c:'94,138,74',x:.82}],SP=CORES.map(function(k){return sprite(k.c)});
var PLUMAS=3,POR=70,VIDA=9,GRAOS=55;
window.render=function(t){
  ctx.globalCompositeOperation='source-over';ctx.globalAlpha=1;ctx.filter='none';
  /* fotografia: respiração lenta (período T) + deriva */
  var u=t/T*Math.PI*2, s=1.06+0.05*(0.5-0.5*Math.cos(u)), dx=Math.sin(u)*W*0.012, dy=Math.cos(u)*H*0.008;
  var iw=W*s, ih=H*s; ctx.drawImage(img,(W-iw)/2+dx,(H-ih)/2+dy,iw,ih);
  /* calor: velatura quente + vinheta */
  var q=ctx.createLinearGradient(0,0,0,H);q.addColorStop(0,'rgba(60,30,10,.12)');q.addColorStop(.6,'rgba(30,15,8,.06)');q.addColorStop(1,'rgba(18,11,8,.5)');ctx.fillStyle=q;ctx.fillRect(0,0,W,H);
  /* feixes de luz */
  ctx.save();ctx.globalAlpha=.10;ctx.globalCompositeOperation='lighter';
  for(var f=0;f<2;f++){var fx=W*(0.3+f*0.4)+Math.sin(t*.08+f)*W*.06;var lg=ctx.createLinearGradient(fx-W*.12,0,fx+W*.12,0);lg.addColorStop(0,'rgba(243,198,74,0)');lg.addColorStop(.5,'rgba(243,198,74,.9)');lg.addColorStop(1,'rgba(243,198,74,0)');ctx.fillStyle=lg;ctx.beginPath();ctx.moveTo(fx-W*.25,0);ctx.lineTo(fx+W*.25,0);ctx.lineTo(fx+W*.05,H);ctx.lineTo(fx-W*.05,H);ctx.closePath();ctx.fill();}
  ctx.restore();
  /* plumas de especiarias */
  ctx.globalCompositeOperation='lighter';var base=Math.min(W,H);
  for(var p=0;p<PLUMAS;p++){var k=CORES[p],sp=SP[p],ox=W*k.x,oy=H*1.02;
    for(var i=0;i<POR;i++){var id=p*1000+i,ph=seed(id)*VIDA,idade=(t+ph)%VIDA,uu=idade/VIDA;
      var sway=Math.sin(idade*.9+seed(id+7)*6.28)*base*.10+Math.sin(idade*.31+seed(id+3)*6.28)*base*.16;
      var x=ox+(seed(id+1)-.5)*base*.28+sway*(uu+.2),y=oy-uu*H*(0.85+seed(id+2)*.3);
      var r=base*(0.05+seed(id+4)*0.11)*(0.5+uu*1.4),a=Math.sin(uu*Math.PI)*(0.07+seed(id+5)*0.07)*(1-uu*.4);
      ctx.globalAlpha=a;ctx.drawImage(sp,x-r,y-r,r*2,r*2);}}
  /* grãos */
  ctx.globalCompositeOperation='source-over';
  for(var g=0;g<GRAOS;g++){var gid=9000+g,gph=seed(gid)*7,gt=(t*(0.5+seed(gid+1)*.6)+gph)%7,gu=gt/7;
    var gx=W*seed(gid+2)+Math.sin(gt*1.3+seed(gid+3)*6.28)*base*.03,gy=-H*.05+gu*H*1.1,prof=seed(gid+4),len=base*(0.006+prof*0.012),esp=len*.36;
    ctx.save();ctx.translate(gx,gy);ctx.rotate(gt*(0.6+prof)+seed(gid+5)*6.28);ctx.globalAlpha=0.45+prof*.4;ctx.fillStyle=prof>.6?'#FFF6E6':'#E9D9C2';if(prof<.35)ctx.filter='blur(1.5px)';
    ctx.beginPath();ctx.ellipse(0,0,esp,len,0,0,Math.PI*2);ctx.fill();ctx.restore();}
  ctx.globalAlpha=1;var v=ctx.createRadialGradient(W*.5,H*.45,base*.35,W*.5,H*.5,base*1.1);v.addColorStop(0,'rgba(18,11,8,0)');v.addColorStop(1,'rgba(18,11,8,.6)');ctx.fillStyle=v;ctx.fillRect(0,0,W,H);
};
</script></body></html>`;
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const pg = await (await browser.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: 1 })).newPage();
  await pg.setContent(html); await pg.waitForFunction(() => document.querySelector('canvas') && window.render);
  await pg.evaluate(() => new Promise(r => { const i = new Image(); i.onload = r; i.src = document.querySelector('script') && ''; setTimeout(r, 300); }));
  const N = T * FPS, NX = X * FPS;
  for (let i = 0; i < N + NX; i++) {
    await pg.evaluate((t) => window.render(t), 3 + i / FPS);
    await pg.screenshot({ path: path.join(out, `f${String(i).padStart(4, '0')}.png`), clip: { x: 0, y: 0, width: W, height: H } });
  }
  await browser.close();
  // fusão do fim com o início (loop sem salto) + codificação
  execFileSync('python3', ['-c', `
import sys, os
from PIL import Image
out, N, NX = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
for i in range(NX):
    w = 1 - i / NX
    a = Image.open(os.path.join(out, 'f%04d.png' % i)).convert('RGB'); b = Image.open(os.path.join(out, 'f%04d.png' % (N + i))).convert('RGB')
    Image.blend(a, b, w).save(os.path.join(out, 'f%04d.png' % i))
for i in range(N, N + NX): os.remove(os.path.join(out, 'f%04d.png' % i))
`, out, String(N), String(NX)]);
  const ff = execFileSync('python3', ['-c', 'import imageio_ffmpeg as f; print(f.get_ffmpeg_exe())']).toString().trim();
  execFileSync(ff, ['-y', '-hide_banner', '-loglevel', 'error', '-framerate', String(FPS), '-i', path.join(out, 'f%04d.png'), '-c:v', 'libx264', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-crf', '23', '-movflags', '+faststart', '-an', mp4]);
  const webm = mp4.replace(/\.mp4$/, '.webm');
  execFileSync(ff, ['-y', '-hide_banner', '-loglevel', 'error', '-framerate', String(FPS), '-i', path.join(out, 'f%04d.png'), '-c:v', 'libvpx-vp9', '-b:v', '0', '-crf', '34', '-row-mt', '1', '-pix_fmt', 'yuv420p', '-an', webm]);
  fs.rmSync(out, { recursive: true, force: true });
  console.log('mp4:', mp4, (fs.statSync(mp4).size / 1048576).toFixed(2), 'MB · webm:', (fs.statSync(webm).size / 1048576).toFixed(2), 'MB');
})();
