
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [,, html, outdir, fps] = process.argv;
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.resolve(html));
  await p.evaluate(() => document.fonts.ready);
  // pré-carregar as sequências de vídeo e as fotos
  await p.evaluate(async () => {
    const urls = [...document.querySelectorAll('img')].map(i => i.getAttribute('src')).filter(Boolean);
    for (let k = 1; k <= 76; k++) urls.push('img/v1/' + String(k).padStart(3, '0') + '.jpg');
    for (let k = 1; k <= 40; k++) urls.push('img/v2/' + String(k).padStart(3, '0') + '.jpg');
    await Promise.all(urls.map(u => new Promise(r => { const i = new Image(); i.onload = i.onerror = r; i.src = u; })));
  });
  const dur = await p.evaluate(() => window.DUR);
  const n = Math.round(dur * fps);
  for (let f = 0; f < n; f++) {
    await p.evaluate(t => window.render(t), f / fps);
    await p.screenshot({ path: path.join(outdir, String(f).padStart(4, '0') + '.jpg'), type: 'jpeg', quality: 93 });
    if (f % 60 === 0) console.log('frame', f, '/', n);
  }
  await b.close();
})();
