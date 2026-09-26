// Renderiza uma peça do QR com o Chromium do Playwright. Chamado por gerar.py.
//   node render.cjs <peca.html> <saida.pdf> [saida.png] [ppp]
// Escreve o PDF (tamanho da página = @page do CSS), opcionalmente um PNG da .face ao ppp pedido,
// e imprime em JSON as medidas em mm de cada texto (tamanho, contraste, fonte) e de cada QR [data-qr].
// NODE_PATH=/opt/node22/lib/node_modules
const { chromium } = require('playwright');
const path = require('path');

function medir() {
  const MM = 25.4 / 96;
  const lin = c => { c /= 255; return c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4; };
  const lum = ([r, g, b]) => 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b);
  const rgb = s => (s.match(/[\d.]+/g) || []).map(Number);
  const fundo = el => {
    for (let e = el; e; e = e.parentElement) {
      const c = rgb(getComputedStyle(e).backgroundColor);
      if (c.length >= 3 && (c.length < 4 || c[3] > 0.5)) return c.slice(0, 3);
    }
    return [255, 255, 255];
  };
  const emMM = b => [b.left * MM, b.top * MM, b.right * MM, b.bottom * MM];
  const textos = [], vistos = new Set();
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while (w.nextNode()) {
    const t = w.currentNode.textContent.trim(), el = w.currentNode.parentElement;
    if (!t || vistos.has(el) || el.closest('.so-leitor,title,style,svg')) continue;
    vistos.add(el);
    const cs = getComputedStyle(el);
    const [a, b] = [lum(rgb(cs.color).slice(0, 3)), lum(fundo(el))].sort((x, y) => y - x);
    textos.push({ t, tt: cs.textTransform, familia: cs.fontFamily.split(',')[0].replace(/["']/g, '').trim(),
      peso: +cs.fontWeight, pt: +(parseFloat(cs.fontSize) * 0.75).toFixed(2),
      contraste: +((a + 0.05) / (b + 0.05)).toFixed(2), mm: emMM(el.getBoundingClientRect()) });
  }
  const qrs = [...document.querySelectorAll('[data-qr]')].map(e => ({ mm: emMM(e.getBoundingClientRect()),
    modulos: +e.dataset.qr, nome: e.dataset.nome || '' }));
  const regua = document.querySelector('[data-regua]');
  return { textos, qrs, regua: regua ? emMM(regua.getBoundingClientRect()) : null };
}

(async () => {
  const [html, pdf, png, ppp] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1000, height: 1400 }, deviceScaleFactor: (+ppp || 96) / 96 });
  await page.goto('file://' + path.resolve(html));
  await page.evaluate(() => document.fonts.ready);
  const falhas = await page.evaluate(() => [...document.fonts].filter(f => f.status === 'error').map(f => f.family));
  if (falhas.length) { console.error('fontes que não carregaram: ' + falhas.join(', ')); process.exit(1); }
  await page.pdf({ path: pdf, preferCSSPageSize: true, printBackground: true });
  if (png) await (await page.$('.face')).screenshot({ path: png });
  console.log(JSON.stringify(await page.evaluate(medir)));
  await browser.close();
})();
