// Imprime os .html desta pasta em PDF (e PNG de pré-visualização com --png).
// Uso: node pdf.js [--png]
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

const AQUI = __dirname;
const FICHEIROS = [
  ['afis-recenzii-a4', false],
  ['afis-recenzii-a5x2', true],
  ['oferta-ro', false],
  ['oferta-pt', false],
  ['audit-ro', false],
  ['auditoria-pt', false],
];

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1200, height: 1700 }, deviceScaleFactor: 2 });
  for (const [nome, deitado] of FICHEIROS) {
    await page.goto('file://' + path.join(AQUI, nome + '.html'));
    await page.emulateMedia({ media: 'print' });
    await page.evaluate(() => document.fonts.ready);
    await page.pdf({ path: path.join(AQUI, nome + '.pdf'), format: 'A4', landscape: deitado, printBackground: true, preferCSSPageSize: true });
    if (process.argv.includes('--png')) {
      await page.screenshot({ path: path.join(AQUI, '_previa', nome + '.png'), fullPage: true });
    }
    console.log('ok', nome + '.pdf');
  }
  await browser.close();
})();
