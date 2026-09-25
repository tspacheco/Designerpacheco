// Renderiza o cartão com o Chromium do Playwright: PDF de impressão, PNG por face e pré-visualização,
// e mede tamanhos de letra e contraste de cada texto. Chamado por gerar.py.
// Uso: NODE_PATH=/opt/node22/lib/node_modules node render.cjs cartao.html <pasta-saida> <prova:0|1>
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const [, , html, outDir, prova] = process.argv;
  const url = 'file://' + path.resolve(html);
  const browser = await chromium.launch();

  // 1) PDF de impressão (91×61 mm por face, com sangria)
  const pPdf = await browser.newPage();
  await pPdf.goto(url);
  await pPdf.evaluate(() => document.fonts.ready);
  if (prova === '1') await pPdf.evaluate(() => document.body.classList.add('prova'));
  await pPdf.pdf({ path: path.join(outDir, prova === '1' ? 'cartao-impressao-PROVA.pdf' : 'cartao-impressao.pdf'),
    width: '91mm', height: '61mm', printBackground: true, preferCSSPageSize: true });

  // 2) PNG de cada face a 600 ppp (com sangria) — usado também para testar o QR
  const dpi = 600, dsf = dpi / 96;
  const pFace = await browser.newPage({ deviceScaleFactor: dsf, viewport: { width: 400, height: 520 } });
  await pFace.goto(url);
  await pFace.evaluate(() => document.fonts.ready);
  const faces = await pFace.$$('.face');
  const nomes = ['frente', 'verso'];
  for (let i = 0; i < faces.length; i++) {
    await faces[i].screenshot({ path: path.join(outDir, `face-${nomes[i]}-600ppp.png`) });
  }

  // 3) Medições de acessibilidade: tamanho e contraste de cada elemento com texto
  const relatorio = await pFace.evaluate(() => {
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
    const out = [];
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    const vistos = new Set();
    while (walker.nextNode()) {
      const t = walker.currentNode.textContent.trim();
      const el = walker.currentNode.parentElement;
      if (!t || vistos.has(el) || !el.closest('.face')) continue;
      vistos.add(el);
      const cs = getComputedStyle(el);
      const fg = rgb(cs.color).slice(0, 3), bg = fundo(el);
      const [a, b] = [lum(fg), lum(bg)].sort((x, y) => y - x);
      out.push({ face: el.closest('.face').classList.contains('frente') ? 'frente' : 'verso',
        texto: t.slice(0, 34), pt: +(parseFloat(cs.fontSize) * 0.75).toFixed(2),
        peso: cs.fontWeight, contraste: +((a + 0.05) / (b + 0.05)).toFixed(2) });
    }
    return out;
  });
  fs.writeFileSync(path.join(outDir, 'acessibilidade.json'), JSON.stringify(relatorio, null, 1));

  // 4) Pré-visualização lado a lado (sem sangria)
  const pPrev = await browser.newPage({ deviceScaleFactor: 3, viewport: { width: 760, height: 330 } });
  await pPrev.goto(url);
  await pPrev.evaluate(() => { document.body.classList.add('preview'); return document.fonts.ready; });
  const corpo = await pPrev.$('body');
  await corpo.screenshot({ path: path.join(outDir, 'cartao-preview.png') });

  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
