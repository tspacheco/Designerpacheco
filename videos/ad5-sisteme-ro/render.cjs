// Captura os fotogramas de reel.html (30 fps) e monta o MP4 9:16 com o clip limpo da intro por baixo.
// Uso: node render.cjs [pasta-temporária]   ·   pré-visualização: node render.cjs <pasta> 2.5,7,12
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const { execFileSync } = require('child_process');
const fs = require('fs'), path = require('path');
const OUT = process.argv[2] || '/tmp/ad5-ro', ONLY = process.argv[3];
const FPS = 30, DUR = 40;
(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const b = await chromium.launch();
  const p = await (await b.newContext({ viewport: { width: 1080, height: 1920 } })).newPage();
  await p.goto('file://' + path.join(__dirname, 'reel.html'));
  await p.evaluate(() => document.fonts.ready);
  const times = ONLY ? ONLY.split(',').map(Number) : [...Array(FPS * DUR).keys()].map(i => i / FPS);
  for (const [i, t] of times.entries()) {
    await p.evaluate(t => render(t), t);
    if (t > 5 && t < 5.1) await p.waitForTimeout(150); // imagens dos esquemas
    await p.screenshot({ path: path.join(OUT, `f${String(i).padStart(4, '0')}.png`), omitBackground: true });
  }
  await b.close();
  if (ONLY) return;
  const clip = path.join(__dirname, '../fontes/ad5-intro-limpo.mp4');
  execFileSync('ffmpeg', ['-v', 'error', '-y',
    '-i', clip, '-framerate', String(FPS), '-i', path.join(OUT, 'f%04d.png'),
    '-f', 'lavfi', '-t', String(DUR), '-i', 'anullsrc=r=48000:cl=stereo',
    '-filter_complex', `color=c=black:s=1080x1920:r=${FPS}:d=${DUR}[base];[0:v]fps=${FPS},scale=1080:1920,setpts=PTS-STARTPTS[clip];[base][clip]overlay=0:0:eof_action=pass[bg];[bg][1:v]overlay=0:0,format=yuv420p[v]`,
    '-map', '[v]', '-map', '2:a', '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-c:a', 'aac', '-t', String(DUR), '-movflags', '+faststart', path.join(__dirname, 'ad5-sisteme-ro.mp4')], { stdio: 'inherit' });
})();
