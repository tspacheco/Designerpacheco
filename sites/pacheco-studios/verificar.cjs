// Testes do site com o Chromium do Playwright (chamado por gerar.py).
// Telemóvel 360 px e 390 px e computador 1280 px: sem scroll horizontal, alvos de toque ≥ 44 px, letra ≥ 12 px,
// contraste de cada texto, títulos por ordem, formulário do endereço (vazio → erro; texto → navega para /endereço).
// Uso: NODE_PATH=/opt/node22/lib/node_modules node verificar.cjs <pasta-do-site> [pasta-capturas]
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const pasta = path.resolve(process.argv[2] || '.');
  const capturas = process.argv[3];
  const http = require('http'), fs = require('fs');
  const tipos = { '.html': 'text/html; charset=utf-8', '.webp': 'image/webp', '.png': 'image/png' };
  const servidor = http.createServer((req, res) => {
    let f = path.join(pasta, decodeURIComponent(req.url.split('?')[0]));
    if (f.endsWith('/')) f += 'index.html';
    const existe = f.startsWith(pasta) && fs.existsSync(f) && fs.statSync(f).isFile();
    res.writeHead(existe ? 200 : 404, { 'Content-Type': tipos[path.extname(existe ? f : '404.html')] || 'application/octet-stream' });
    res.end(fs.readFileSync(existe ? f : path.join(pasta, '404.html')));
  });
  await new Promise(r => servidor.listen(0, '127.0.0.1', r));
  const base = `http://127.0.0.1:${servidor.address().port}`;
  const url = base + '/';
  const browser = await chromium.launch();
  let falhas = 0;
  const mal = m => { falhas++; console.log('  ✗ ' + m); };

  for (const [nome, vp] of [['360', { width: 360, height: 780 }], ['390', { width: 390, height: 844 }], ['1280', { width: 1280, height: 800 }]]) {
    const ctx = await browser.newContext({ viewport: vp, deviceScaleFactor: 2, reducedMotion: 'reduce', locale: 'pt-PT' });
    const p = await ctx.newPage();
    const erros = [];
    p.on('pageerror', e => erros.push(e.message));
    await p.goto(url);
    await p.evaluate(() => document.fonts.ready);
    const r = await p.evaluate(() => {
      const lin = c => { c /= 255; return c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4; };
      const lum = ([r, g, b]) => 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b);
      const rgb = s => (s.match(/[\d.]+/g) || []).map(Number);
      const fundo = el => {
        for (let e = el; e; e = e.parentElement) {
          const c = rgb(getComputedStyle(e).backgroundColor);
          if (c.length >= 3 && (c.length < 4 || c[3] > 0.5)) return c.slice(0, 3);
        }
        return rgb(getComputedStyle(document.documentElement).backgroundColor).slice(0, 3);
      };
      const visivel = el => { const b = el.getBoundingClientRect(); const cs = getComputedStyle(el);
        return b.width > 1 && b.height > 1 && cs.visibility !== 'hidden' && !el.closest('[inert],.so-leitor,.saltar'); };
      const textos = [], vistos = new Set();
      const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      while (w.nextNode()) {
        const el = w.currentNode.parentElement, t = w.currentNode.textContent.trim();
        if (!t || vistos.has(el) || !visivel(el) || el.closest('script,style')) continue;
        vistos.add(el);
        const cs = getComputedStyle(el);
        const [a, b] = [lum(rgb(cs.color).slice(0, 3)), lum(fundo(el))].sort((x, y) => y - x);
        textos.push({ t: t.slice(0, 40), px: parseFloat(cs.fontSize), peso: +cs.fontWeight, c: +((a + 0.05) / (b + 0.05)).toFixed(2) });
      }
      const alvos = [...document.querySelectorAll('a,button,input')].filter(visivel).map(e => {
        const b = e.getBoundingClientRect(); return { t: (e.textContent || e.id || e.name).trim().slice(0, 30), h: Math.round(b.height), w: Math.round(b.width) };
      });
      const titulos = [...document.querySelectorAll('h1,h2,h3')].map(h => +h.tagName[1]);
      return { textos, alvos, titulos, largura: document.documentElement.scrollWidth, janela: innerWidth };
    });
    console.log(`\n${nome} px`);
    if (r.largura > r.janela) mal(`scroll horizontal: ${r.largura} > ${r.janela}`);
    for (const t of r.textos) {
      const grande = t.px >= 24 || (t.px >= 18.66 && t.peso >= 700);
      if (t.px < 12) mal(`letra ${t.px}px: «${t.t}»`);
      if (t.c < (grande ? 3 : 4.5)) mal(`contraste ${t.c}:1 (${t.px}px): «${t.t}»`);
    }
    for (const a of r.alvos) if (a.h < 44) mal(`alvo de toque com ${a.h}px de altura: «${a.t}»`);
    let ant = 0; for (const h of r.titulos) { if (h > ant + 1) mal(`título salta de h${ant} para h${h}`); ant = h; }
    const minC = Math.min(...r.textos.map(t => t.c)), minPx = Math.min(...r.textos.map(t => t.px));
    console.log(`  textos: ${r.textos.length} · contraste mínimo ${minC}:1 · letra mínima ${minPx}px · alvos: ${r.alvos.length} · títulos: ${r.titulos.join(' ')}`);
    if (erros.length) mal('erros de JavaScript: ' + erros.join(' | '));
    if (capturas) {
      await p.evaluate(() => Promise.all([...document.images].map(i => i.decode().catch(() => {}))));
      await p.screenshot({ path: path.join(capturas, `site-${nome}.png`), fullPage: true });
    }

    if (nome === '390') {
      // formulário: vazio → mensagem de erro; "Mercado da Vila" → navega para /mercado-da-vila
      await p.click('#form-endereco button');
      const msg = await p.textContent('#endereco-erro');
      if (!msg || !msg.trim()) mal('formulário vazio não mostrou erro'); else console.log('  ✓ vazio → «' + msg.trim().slice(0, 60) + '…»');
      await p.fill('#endereco', '  Mercado da Vila ');
      await Promise.all([p.waitForURL(/mercado-da-vila/, { timeout: 5000 }).catch(() => {}), p.click('#form-endereco button')]);
      if (!/\/mercado-da-vila$/.test(p.url())) mal('formulário não navegou: ' + p.url());
      else {
        const h1 = (await p.textContent('h1')).trim();
        console.log('  ✓ «Mercado da Vila» → /mercado-da-vila → página 404: «' + h1 + '»');
        if (capturas) await p.screenshot({ path: path.join(capturas, 'site-404.png'), fullPage: true });
      }
    }
    await ctx.close();
  }

  // barra fixa: aparece depois do herói no telemóvel (com movimento normal)
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 });
  const p = await ctx.newPage();
  await p.goto(url);
  await p.waitForTimeout(400);
  const antes = await p.$eval('#barra', b => b.classList.contains('visivel'));
  await p.evaluate(() => window.scrollTo(0, document.querySelector('#trabalhos').offsetTop + 300));
  await p.waitForTimeout(500);
  const depois = await p.$eval('#barra', b => b.classList.contains('visivel') && !b.hasAttribute('inert'));
  await p.evaluate(() => document.getElementById('contacto').scrollIntoView());
  await p.waitForTimeout(500);
  const fim = await p.$eval('#barra', b => b.classList.contains('visivel'));
  if (antes || !depois || fim) mal(`barra fixa: no herói=${antes}, a meio=${depois}, no contacto=${fim}`);
  else console.log('\n  ✓ barra fixa: escondida no herói, visível a meio, escondida no contacto');
  if (capturas) {
    await p.evaluate(() => window.scrollTo(0, 0));
    await p.reload(); await p.waitForTimeout(1600);
    await p.screenshot({ path: path.join(capturas, 'site-390-heroi.png') });
  }
  await browser.close();
  servidor.close();
  console.log(falhas ? `\n${falhas} problema(s).` : '\n✓ Sem problemas.');
  process.exit(falhas ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
