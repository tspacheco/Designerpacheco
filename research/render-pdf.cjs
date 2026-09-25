// Converte um HTML (A4, com @page) em PDF com o Chromium do Playwright, e opcionalmente guarda um PNG por página
// para revisão. Uso: NODE_PATH=/opt/node22/lib/node_modules node render-pdf.cjs <ficheiro.html> [pasta-png]
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const html = path.resolve(process.argv[2]);
  const png = process.argv[3];
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + html);
  await page.evaluate(() => document.fonts.ready);
  await page.emulateMedia({ media: 'print' });
  const pdf = html.replace(/\.html$/, '.pdf');
  await page.pdf({ path: pdf, format: 'A4', printBackground: true, preferCSSPageSize: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
  console.log('PDF:', path.basename(pdf));
  if (png) {
    // pré-visualização: cada .pagina (210×297 mm) como imagem
    await page.emulateMedia({ media: 'screen' });
    const paginas = await page.$$('.pagina');
    for (const [i, p] of paginas.entries()) {
      await p.screenshot({ path: path.join(png, `${path.basename(html, '.html')}-p${i + 1}.png`) });
    }
    console.log(`${paginas.length} páginas em PNG`);
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
