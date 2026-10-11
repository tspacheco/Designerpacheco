// HTML → PDF A4 com o Chromium do Playwright. Uso: node imprimir.js in.html out.pdf [in2.html out2.pdf ...]
const { chromium } = require('playwright');
(async () => {
  const args = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage();
  for (let i = 0; i < args.length; i += 2) {
    await p.goto('file://' + require('path').resolve(args[i]), { waitUntil: 'load' });
    await p.evaluate(() => document.fonts.ready);
    await p.pdf({ path: args[i + 1], format: 'A4', printBackground: true, preferCSSPageSize: true });
  }
  await b.close();
})();
