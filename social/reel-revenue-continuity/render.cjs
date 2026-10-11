// Reel «Revenue leaks after the yes»: captura overlay.html a 30 fps em PNG com alfa, sobrepõe ao clip limpo (clean.mp4,
// 1080×1920, 35 s), junta o som de som.py e grava 9:16 H.264/AAC com moov no início.
// Uso: node render.cjs <pasta-temp> <clean.mp4> [so-overlay]   (pré-visualizar: node render.cjs <pasta> <clean.mp4> frames 0.4,5.6,...)
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const { execFileSync } = require('child_process');
const fs = require('fs'), path = require('path');
const TMP = process.argv[2], BASE = process.argv[3], FPS = 30, NOME = 'reel-en-revenue-leaks-9x16', CAPA = 1.2;
(async () => {
  const dir = path.join(TMP, 'ov'); fs.mkdirSync(dir, { recursive: true });
  const b = await chromium.launch();
  const p = await (await b.newContext({ viewport: { width: 1080, height: 1920 } })).newPage();
  p.on('pageerror', e => { throw e; });
  await p.goto('file://' + path.join(__dirname, 'overlay.html'));
  await p.evaluate(() => document.fonts.ready);
  const sfx = await p.evaluate(() => window.SFX), dur = await p.evaluate(() => window.DUR);
  if (process.argv[4] === 'frames') {   // só alguns fotogramas, compostos sobre o vídeo, para rever
    for (const t of process.argv[5].split(',')) {
      await p.evaluate(t => render(t), +t);
      const png = path.join(dir, `prev_${t}.png`);
      await p.screenshot({ path: png, omitBackground: true });
      execFileSync('ffmpeg', ['-v', 'error', '-y', '-ss', t, '-i', BASE, '-i', png, '-filter_complex', '[0:v][1:v]overlay=0:0', '-frames:v', '1', path.join(dir, `comp_${t}.jpg`)]);
    }
    await b.close(); return;
  }
  fs.writeFileSync(path.join(dir, 'tempos.json'), JSON.stringify(sfx));
  const n = process.argv[4] === 'compor' ? 0 : Math.round(dur * FPS);   // «compor»: os PNG já existem, só monta
  for (let i = 0; i < n; i++) {
    await p.evaluate(t => render(t), i / FPS);
    await p.screenshot({ path: path.join(dir, `f${String(i).padStart(4, '0')}.png`), omitBackground: true });
  }
  await p.close(); await b.close();
  if (process.argv[4] === 'so-overlay') return;
  const som = path.join(TMP, 'som.wav');
  execFileSync('python3', [path.join(__dirname, 'som.py'), path.join(dir, 'tempos.json'), som], { stdio: 'inherit' });
  const out = path.join(__dirname, `${NOME}.mp4`);
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', BASE, '-framerate', String(FPS), '-i', path.join(dir, 'f%04d.png'), '-i', som,
    '-filter_complex', `[0:v]trim=duration=${dur},setpts=PTS-STARTPTS,fps=${FPS}[v0];[v0][1:v]overlay=0:0:format=auto,format=yuv420p[v]`,
    '-map', '[v]', '-map', '2:a', '-c:v', 'libx264', '-preset', 'slow', '-crf', '19', '-c:a', 'aac', '-b:a', '160k', '-t', String(dur),
    '-movflags', '+faststart', out], { stdio: 'inherit' });
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-ss', String(CAPA), '-i', out, '-frames:v', '1', '-q:v', '2', path.join(__dirname, `${NOME}-capa.jpg`)], { stdio: 'inherit' });
  console.log('ok', out);
})();
