// node shot.js page.html out.png [width] [height]  — ou  node shot.js page.html outdir --slides
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [,, html, out, a, b] = process.argv;
  const browser = await chromium.launch();
  if (a === '--slides') {
    const p = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
    await p.goto('file://' + path.resolve(html));
    await p.evaluate(() => document.fonts.ready);
    const ids = await p.$$eval('.slide', els => els.map(e => e.id));
    for (const id of ids) {
      const el = await p.$('[id="' + id + '"]');
      await el.screenshot({ path: path.join(out, id + '.png') });
      console.log(id);
    }
  } else {
    const p = await browser.newPage({ viewport: { width: +(a || 1200), height: +(b || 800) }, deviceScaleFactor: 1 });
    await p.goto('file://' + path.resolve(html));
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: out, fullPage: true });
  }
  await browser.close();
})();
