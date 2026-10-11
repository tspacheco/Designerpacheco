// Fotografa cada .slide de um HTML em JPG 1080x1350.
// Uso: NODE_PATH=$(npm root -g) node fotografar.js pagina.html pasta-saida prefixo
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [html, saida, prefixo] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.resolve(html));
  await p.evaluate(() => document.fonts.ready);
  const slides = await p.$$('.slide');
  for (let i = 0; i < slides.length; i++) {
    const n = String(i + 1).padStart(2, '0');
    await slides[i].screenshot({ path: path.join(saida, `${prefixo}-${n}.jpg`), type: 'jpeg', quality: 92 });
  }
  console.log(slides.length, 'slides');
  await b.close();
})();
