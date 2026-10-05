// Vídeo B: captura video.html a 30 fps (PT, RO e EN), junta o som de som.py e grava 9:16 (Reels/Stories) e 4:5 (feed).
// O 4:5 é o recorte y 285–1635 do 9:16 (a composição foi desenhada para isso).
// Uso: node render.cjs [pasta-temporária] [pt|ro|en]
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const { execFileSync } = require('child_process');
const fs = require('fs'), path = require('path');
const TMP = process.argv[2] || '/tmp/video-b', LANGS = process.argv[3] ? [process.argv[3]] : ['pt', 'ro', 'en'], FPS = 30;
(async () => {
  fs.mkdirSync(TMP, { recursive: true });
  const som = path.join(TMP, 'som.wav');
  execFileSync('python3', [path.join(__dirname, 'som.py'), som]);
  const b = await chromium.launch();
  for (const l of LANGS) {
    const dir = path.join(TMP, l); fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir);
    const p = await (await b.newContext({ viewport: { width: 1080, height: 1920 } })).newPage();
    await p.goto('file://' + path.join(__dirname, 'video.html') + '?l=' + l);
    await p.evaluate(() => document.fonts.ready);
    const dur = await p.evaluate(() => window.DUR), n = Math.round(dur * FPS);
    for (let i = 0; i < n; i++) {
      await p.evaluate(t => render(t), i / FPS);
      await p.screenshot({ path: path.join(dir, `f${String(i).padStart(4, '0')}.jpg`), type: 'jpeg', quality: 95 });
    }
    await p.close();
    const enc = (vf, out) => execFileSync('ffmpeg', ['-v', 'error', '-y', '-framerate', String(FPS), '-i', path.join(dir, 'f%04d.jpg'), '-i', som,
      '-vf', vf, '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-shortest',
      '-movflags', '+faststart', path.join(__dirname, out)], { stdio: 'inherit' });
    enc('format=yuv420p', `video-b-${l}-9x16.mp4`);
    enc('crop=1080:1350:0:285,format=yuv420p', `video-b-${l}-4x5.mp4`);
  }
  await b.close();
})();
