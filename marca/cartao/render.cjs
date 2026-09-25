// Renderiza o cartão com o Chromium do Playwright e mede-o. Chamado por gerar.py.
//   node render.cjs cartao.html <pasta> <prova:0|1>        → PDF, PNG 600 ppp por face, pré-visualização, acessibilidade.json
//   node render.cjs --verso <saida-pasta> a.html b.html …  → verso de cada ficheiro, cortado (para comparar frases)
// NODE_PATH=/opt/node22/lib/node_modules
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

async function versos(browser, pasta, ficheiros) {
  const p = await browser.newPage({ deviceScaleFactor: 4, viewport: { width: 760, height: 330 } });
  for (const [i, f] of ficheiros.entries()) {
    await p.goto('file://' + path.resolve(f));
    await p.evaluate(() => { document.body.classList.add('preview'); return document.fonts.ready; });
    const cortes = await p.$$('.corte');
    await cortes[1].screenshot({ path: path.join(pasta, `verso-${i + 1}.png`) });
  }
}

// Mede cada texto (tamanho, contraste, fonte, caixa em mm) e procura textos sobrepostos.
// A margem segura e a zona de silêncio do QR são verificadas nos píxeis, em gerar.py (a tinta real, não caixas).
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
  const emMM = (b, face) => { const f = face.getBoundingClientRect();
    return [(b.left - f.left) * MM, (b.top - f.top) * MM, (b.right - f.left) * MM, (b.bottom - f.top) * MM]; };
  const bloco = el => { let e = el; while (e.parentElement && getComputedStyle(e).display === 'inline') e = e.parentElement; return e; };
  const textos = [], erros = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const vistos = new Set();
  while (walker.nextNode()) {
    const t = walker.currentNode.textContent.trim();
    const el = walker.currentNode.parentElement;
    const face = el.closest('.face');
    if (!t || vistos.has(el) || !face || el.closest('.so-leitor')) continue;
    vistos.add(el);
    const cs = getComputedStyle(el);
    const [a, b] = [lum(rgb(cs.color).slice(0, 3)), lum(fundo(el))].sort((x, y) => y - x);
    textos.push({ el, face: face.classList.contains('frente') ? 'frente' : 'verso', t, tt: cs.textTransform,
      familia: cs.fontFamily.split(',')[0].replace(/["']/g, '').trim(), peso: +cs.fontWeight,
      pt: +(parseFloat(cs.fontSize) * 0.75).toFixed(2), contraste: +((a + 0.05) / (b + 0.05)).toFixed(2),
      // caixa do bloco: um span em linha (ex.: a palavra a laranja) mede-se pela linha onde está
      mm: emMM(bloco(el).getBoundingClientRect(), face) });
  }
  const cruza = (p, q, t = .15) => p[0] + t < q[2] && q[0] + t < p[2] && p[1] + t < q[3] && q[1] + t < p[3];
  for (let i = 0; i < textos.length; i++) for (let j = i + 1; j < textos.length; j++) {
    const a = textos[i], b = textos[j];
    if (a.face !== b.face || a.el.contains(b.el) || b.el.contains(a.el)) continue;
    if (cruza(a.mm, b.mm)) erros.push(`sobrepostos: «${a.t.slice(0, 20)}» e «${b.t.slice(0, 20)}»`);
  }
  const qrEl = document.querySelector('.verso .qr svg');
  const qr = qrEl ? { mm: emMM(qrEl.getBoundingClientRect(), qrEl.closest('.face')),
                      modulos: +qrEl.getAttribute('viewBox').split(' ')[2] } : null;
  return { textos: textos.map(({ el, ...r }) => ({ ...r, mm: r.mm.map(v => +v.toFixed(2)) })), erros, qr };
}

(async () => {
  const browser = await chromium.launch();
  if (process.argv[2] === '--verso') {
    await versos(browser, process.argv[3], process.argv.slice(4));
    await browser.close();
    return;
  }
  const [, , html, outDir, prova] = process.argv;
  const url = 'file://' + path.resolve(html);

  // 1) PDF de impressão (91×61 mm por face, com sangria)
  const pPdf = await browser.newPage();
  await pPdf.goto(url);
  await pPdf.evaluate(() => document.fonts.ready);
  if (prova === '1') await pPdf.evaluate(() => document.body.classList.add('prova'));
  await pPdf.pdf({ path: path.join(outDir, prova === '1' ? 'cartao-impressao-PROVA.pdf' : 'cartao-impressao.pdf'),
    width: '91mm', height: '61mm', printBackground: true, preferCSSPageSize: true });

  // 2) PNG de cada face a 600 ppp (com sangria) — usado também para testar o QR
  const pFace = await browser.newPage({ deviceScaleFactor: 600 / 96, viewport: { width: 400, height: 520 } });
  await pFace.goto(url);
  await pFace.evaluate(() => document.fonts.ready);
  const faces = await pFace.$$('.face');
  for (const [i, nome] of ['frente', 'verso'].entries()) {
    await faces[i].screenshot({ path: path.join(outDir, `face-${nome}-600ppp.png`) });
  }

  // 3) Medições
  fs.writeFileSync(path.join(outDir, 'acessibilidade.json'), JSON.stringify(await pFace.evaluate(medir), null, 1));

  // 4) Pré-visualização lado a lado (sem sangria)
  const pPrev = await browser.newPage({ deviceScaleFactor: 3, viewport: { width: 760, height: 330 } });
  await pPrev.goto(url);
  await pPrev.evaluate(() => { document.body.classList.add('preview'); return document.fonts.ready; });
  await (await pPrev.$('body')).screenshot({ path: path.join(outDir, 'cartao-preview.png') });

  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
