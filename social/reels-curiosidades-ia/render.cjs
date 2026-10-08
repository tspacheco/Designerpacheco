// Reel «5 things under one AI question»: captura overlay.html a 30 fps em PNG com alfa, sobrepõe ao clip 3D do Higgsfield
// (base.mp4, já 1080×1920 e 15 s), junta o som de som.py (mistura com o áudio do clip, se existir) e grava 9:16 H.264/AAC com
// moov no início (a Meta não carrega MP4 fragmentado). Uso: node render.cjs <pasta-temp> <base.mp4> [so-overlay]
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const { execFileSync } = require('child_process');
const fs = require('fs'), path = require('path');
const TMP = process.argv[2] || '/tmp/reel-abyss', BASE = process.argv[3], FPS = 30, NOME = 'reel-en-5-under-one-question', CAPA = 0.9;
(async () => {
  const dir = path.join(TMP, 'ov'); fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
  const b = await chromium.launch();
  const p = await (await b.newContext({ viewport: { width: 1080, height: 1920 } })).newPage();
  p.on('pageerror', e => { throw e; });
  await p.goto('file://' + path.join(__dirname, 'overlay.html'));
  await p.evaluate(() => document.fonts.ready);
  const sfx = await p.evaluate(() => window.SFX), dur = await p.evaluate(() => window.DUR), n = Math.round(dur * FPS);
  fs.writeFileSync(path.join(dir, 'tempos.json'), JSON.stringify(sfx));
  for (let i = 0; i < n; i++) {
    await p.evaluate(t => render(t), i / FPS);
    await p.screenshot({ path: path.join(dir, `f${String(i).padStart(4, '0')}.png`), omitBackground: true });
  }
  await p.close(); await b.close();
  if (process.argv[4] === 'so-overlay') return;
  const som = path.join(TMP, 'som.wav');
  execFileSync('python3', [path.join(__dirname, 'som.py'), path.join(dir, 'tempos.json'), BASE, som], { stdio: 'inherit' });
  const out = path.join(__dirname, `${NOME}-9x16.mp4`);
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', BASE, '-framerate', String(FPS), '-i', path.join(dir, 'f%04d.png'), '-i', som,
    '-filter_complex', `[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,trim=duration=${dur},setpts=PTS-STARTPTS,fps=${FPS}[v0];[v0][1:v]overlay=0:0:format=auto,format=yuv420p[v]`,
    '-map', '[v]', '-map', '2:a', '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-c:a', 'aac', '-b:a', '192k', '-t', String(dur),
    '-movflags', '+faststart', out], { stdio: 'inherit' });
  // capa: fotograma do vídeo final no instante CAPA
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-ss', String(CAPA), '-i', out, '-frames:v', '1', '-q:v', '2', path.join(__dirname, `${NOME}-capa.jpg`)], { stdio: 'inherit' });
  console.log('ok', out);
})();
