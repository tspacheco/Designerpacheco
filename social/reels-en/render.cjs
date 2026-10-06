// Reels EN: captura reel.html a 30 fps (?r=1 e ?r=2), gera o som com som.py a partir dos tempos da página e grava 9:16 e uma capa.
// Uso: node render.cjs [pasta-temporária] [1|2]
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const { execFileSync } = require('child_process');
const fs = require('fs'), path = require('path');
const TMP = process.argv[2] || '/tmp/reels-en', RS = process.argv[3] ? [process.argv[3]] : ['1', '2'], FPS = 30;
const NOME = { 1: 'reel-en-1-lost-customers', 2: 'reel-en-2-evenings-back' };
(async () => {
  const b = await chromium.launch();
  for (const r of RS) {
    const dir = path.join(TMP, 'r' + r); fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
    const p = await (await b.newContext({ viewport: { width: 1080, height: 1920 } })).newPage();
    p.on('pageerror', e => { throw e; });
    await p.goto('file://' + path.join(__dirname, 'reel.html') + '?r=' + r);
    await p.evaluate(() => document.fonts.ready);
    const sfx = await p.evaluate(() => window.SFX), dur = await p.evaluate(() => window.DUR), n = Math.round(dur * FPS);
    fs.writeFileSync(path.join(dir, 'tempos.json'), JSON.stringify(sfx));
    const som = path.join(dir, 'som.wav');
    execFileSync('python3', [path.join(__dirname, 'som.py'), path.join(dir, 'tempos.json'), som]);
    for (let i = 0; i < n; i++) {
      await p.evaluate(t => render(t), i / FPS);
      await p.screenshot({ path: path.join(dir, `f${String(i).padStart(4, '0')}.jpg`), type: 'jpeg', quality: 95 });
    }
    await p.evaluate(() => render(1.6));
    await p.screenshot({ path: path.join(__dirname, `${NOME[r]}-capa.jpg`), type: 'jpeg', quality: 92 });
    await p.close();
    execFileSync('ffmpeg', ['-v', 'error', '-y', '-framerate', String(FPS), '-i', path.join(dir, 'f%04d.jpg'), '-i', som,
      '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-shortest',
      '-movflags', '+faststart', path.join(__dirname, `${NOME[r]}-9x16.mp4`)], { stdio: 'inherit' });
  }
  await b.close();
})();
