// Herói em vídeo: montagem de fotografias da loja (entrada → corredores → parede dos telemóveis), zoom/pan lento em cada
// plano, fusões curtas entre planos e loop perfeito (o último plano funde com o primeiro). Sem partículas.
// Uso: NODE_PATH=$(npm root -g) node video-montagem.js <saida.mp4> <largura> <altura> <plano.jpg:seg:x0,y0,s0:x1,y1,s1> ...
//   x,y = ponto de interesse (0–1) que fica ao centro; s = zoom (1 = cobre o ecrã). Gera também o .webm ao lado.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), { execFileSync } = require('child_process');
(async () => {
  const [mp4, W, H] = [path.resolve(process.argv[2]), +process.argv[3], +process.argv[4]];
  const FPS = 24, FUSAO = 0.7;
  const planos = process.argv.slice(5).map((a) => { const [f, seg, de, ate] = a.split(':'); const n = (s) => s.split(',').map(Number);
    return { src: 'data:image/jpeg;base64,' + fs.readFileSync(path.resolve(f)).toString('base64'), seg: +seg, de: n(de), ate: n(ate) }; });
  const total = planos.reduce((s, p) => s + p.seg, 0);
  const out = mp4 + '.frames'; fs.rmSync(out, { recursive: true, force: true }); fs.mkdirSync(out, { recursive: true });
  const html = `<!doctype html><html><head><style>html,body{margin:0;background:#000;overflow:hidden}canvas{display:block}</style></head><body><canvas id="c" width="${W}" height="${H}"></canvas>
<script>
var cv=document.getElementById('c'),ctx=cv.getContext('2d'),W=${W},H=${H},FUSAO=${FUSAO},PL=${JSON.stringify(planos.map(p => ({ seg: p.seg, de: p.de, ate: p.ate })))},IM=[];
var srcs=${JSON.stringify(planos.map(p => p.src))};
window.pronto=Promise.all(srcs.map(function(s){return new Promise(function(r){var i=new Image();i.onload=function(){r(i)};i.src=s;})})).then(function(a){IM=a;});
var ini=[];PL.reduce(function(s,p,i){ini[i]=s;return s+p.seg;},0);var TOTAL=PL.reduce(function(s,p){return s+p.seg;},0);
function ease(u){return u<.5?2*u*u:1-Math.pow(-2*u+2,2)/2;}
function desenha(i,u,alpha){var p=PL[i],im=IM[i],e=ease(u);
  var x=p.de[0]+(p.ate[0]-p.de[0])*e,y=p.de[1]+(p.ate[1]-p.de[1])*e,s=p.de[2]+(p.ate[2]-p.de[2])*e;
  var esc=Math.max(W/im.width,H/im.height)*s,iw=im.width*esc,ih=im.height*esc;
  var dx=W/2-x*iw,dy=H/2-y*ih;dx=Math.min(0,Math.max(W-iw,dx));dy=Math.min(0,Math.max(H-ih,dy));
  ctx.globalAlpha=alpha;ctx.drawImage(im,dx,dy,iw,ih);}
window.render=function(t){t=((t%TOTAL)+TOTAL)%TOTAL;var i=0;while(i<PL.length-1&&t>=ini[i+1])i++;var loc=t-ini[i],p=PL[i];
  ctx.globalAlpha=1;ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
  desenha(i,loc/p.seg,1);
  if(loc<FUSAO){var j=(i+PL.length-1)%PL.length;var a=1-loc/FUSAO;desenha(j,1,a*a);}
  /* graduação quente + vinheta, subtil */
  ctx.globalAlpha=1;var q=ctx.createLinearGradient(0,0,0,H);q.addColorStop(0,'rgba(40,22,10,.10)');q.addColorStop(1,'rgba(18,11,8,.42)');ctx.fillStyle=q;ctx.fillRect(0,0,W,H);
  var v=ctx.createRadialGradient(W*.5,H*.5,Math.min(W,H)*.4,W*.5,H*.5,Math.max(W,H)*.8);v.addColorStop(0,'rgba(0,0,0,0)');v.addColorStop(1,'rgba(0,0,0,.4)');ctx.fillStyle=v;ctx.fillRect(0,0,W,H);
};
</script></body></html>`;
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const pg = await (await browser.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: 1 })).newPage();
  await pg.setContent(html); await pg.evaluate(() => window.pronto);
  const N = Math.round(total * FPS);
  for (let i = 0; i < N; i++) {
    await pg.evaluate((t) => window.render(t), i / FPS);
    await pg.screenshot({ path: path.join(out, `f${String(i).padStart(4, '0')}.png`), clip: { x: 0, y: 0, width: W, height: H } });
  }
  await browser.close();
  const ff = execFileSync('python3', ['-c', 'import imageio_ffmpeg as f; print(f.get_ffmpeg_exe())']).toString().trim();
  const comum = ['-y', '-hide_banner', '-loglevel', 'error', '-framerate', String(FPS), '-i', path.join(out, 'f%04d.png'), '-pix_fmt', 'yuv420p', '-an'];
  execFileSync(ff, [...comum, '-c:v', 'libx264', '-preset', 'slow', '-crf', '23', '-movflags', '+faststart', mp4]);
  const webm = mp4.replace(/\.mp4$/, '.webm');
  execFileSync(ff, [...comum, '-c:v', 'libvpx-vp9', '-b:v', '0', '-crf', '34', '-row-mt', '1', webm]);
  fs.rmSync(out, { recursive: true, force: true });
  console.log('mp4:', mp4, (fs.statSync(mp4).size / 1048576).toFixed(2), 'MB · webm:', (fs.statSync(webm).size / 1048576).toFixed(2), 'MB');
})();
