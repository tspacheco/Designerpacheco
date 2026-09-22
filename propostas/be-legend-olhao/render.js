// NODE_PATH=$(npm root -g) node render.js  → PDF + PNGs de pré-visualização
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.resolve(__dirname, 'proposta.html'), { waitUntil: 'load' });
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: path.resolve(__dirname, 'Be-Legend-Olhao-Follow-up-e-Recuperacao.pdf'), format: 'A4', printBackground: true, preferCSSPageSize: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
  const out = process.argv[2];
  if (out) {
    const n = await p.$$eval('.page', els => els.length);
    for (let i = 0; i < n; i++) {
      const el = (await p.$$('.page'))[i];
      await el.screenshot({ path: `${out}/p${i + 1}.png` });
    }
  }
  await b.close();
  console.log('ok');
})();
