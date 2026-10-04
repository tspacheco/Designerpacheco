// Gera os 5 cartões 4:5 do carrossel (PT e RO) a partir de carrossel.html.
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs'), path = require('path');
(async () => {
  fs.mkdirSync(path.join(__dirname, 'cartoes'), { recursive: true });
  const b = await chromium.launch();
  const p = await (await b.newContext({ viewport: { width: 1080, height: 1350 } })).newPage();
  await p.goto('file://' + path.join(__dirname, 'carrossel.html'));
  for (const l of ['pt', 'ro']) for (let n = 0; n < 5; n++) {
    await p.evaluate(([l, n]) => card(l, n), [l, n]);
    await p.evaluate(() => Promise.all([document.fonts.ready, ...[...document.images].map(i => i.decode().catch(() => {}))]));
    await p.screenshot({ path: path.join(__dirname, 'cartoes', `${l}-${n + 1}.png`) });
  }
  await b.close();
})();
