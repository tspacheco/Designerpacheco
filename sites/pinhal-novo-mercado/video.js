// Exporta o herói "Nuvens de especiarias" em vídeo: fotogramas determinísticos do canvas da própria página + ffmpeg.
// Uso: NODE_PATH=$(npm root -g) node video.js <url do index.html> <pasta de saída> <largura> <altura> [segundos=8] [fps=30]
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), { execFileSync } = require('child_process');
(async () => {
  const [url, out, W, H] = [process.argv[2], process.argv[3], +process.argv[4], +process.argv[5]];
  const S = +process.argv[6] || 8, FPS = +process.argv[7] || 30;
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const pg = await (await browser.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: 1 })).newPage();
  await pg.goto(url); await pg.waitForTimeout(500);
  await pg.evaluate(() => {
    window.__especiarias.parar();
    var h = document.getElementById('heroi');
    h.style.cssText = 'position:fixed;inset:0;min-height:0;z-index:9999';
    h.querySelector('.veu').style.display = 'none'; h.querySelector('.dentro').style.display = 'none';
    document.body.style.overflow = 'hidden';
    window.__especiarias.tamanho();
  });
  const n = S * FPS;
  for (let i = 0; i < n; i++) {
    await pg.evaluate((t) => window.__especiarias.render(t), 2 + i / FPS);
    await pg.screenshot({ path: path.join(out, `f${String(i).padStart(4, '0')}.png`), clip: { x: 0, y: 0, width: W, height: H } });
  }
  await browser.close();
  const ff = execFileSync('python3', ['-c', 'import imageio_ffmpeg as f; print(f.get_ffmpeg_exe())']).toString().trim();
  const mp4 = path.join(out, '..', `heroi-mercado-${W}x${H}.mp4`);
  execFileSync(ff, ['-y', '-hide_banner', '-loglevel', 'error', '-framerate', String(FPS), '-i', path.join(out, 'f%04d.png'), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-movflags', '+faststart', mp4]);
  console.log('mp4:', mp4, (fs.statSync(mp4).size / 1048576).toFixed(2), 'MB');
})();
