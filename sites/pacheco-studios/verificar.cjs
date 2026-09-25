// Testes da página com o Chromium do Playwright, sobre a pasta dist/ servida por HTTP como no Netlify.
// Uso: NODE_PATH=/opt/node22/lib/node_modules node verificar.cjs <dist> [pasta-capturas]
// Em 360, 390 e 1280 px: sem scroll horizontal, letra ≥ 12 px, contraste, alvos ≥ 44 px, títulos por ordem.
// Depois: separadores (com e sem JavaScript), automatizações a abrir, ligações dos quadrados a existir,
// botão «Înapoi» nas cópias dos sites, 404 e barra fixa.
const { chromium } = require('playwright');
const path = require('path');
const http = require('http');
const fs = require('fs');

(async () => {
  const dist = path.resolve(process.argv[2] || 'dist');
  const capturas = process.argv[3];
  const tipos = { '.html': 'text/html; charset=utf-8', '.webp': 'image/webp', '.png': 'image/png', '.jpg': 'image/jpeg', '.mp4': 'video/mp4', '.webm': 'video/webm', '.json': 'application/json' };
  const servidor = http.createServer((req, res) => {
    let f = path.join(dist, decodeURIComponent(req.url.split('?')[0].split('#')[0]));
    if (fs.existsSync(f) && fs.statSync(f).isDirectory()) f = path.join(f, 'index.html');
    const existe = f.startsWith(dist) && fs.existsSync(f) && fs.statSync(f).isFile();
    res.writeHead(existe ? 200 : 404, { 'Content-Type': tipos[path.extname(existe ? f : '404.html')] || 'application/octet-stream' });
    res.end(fs.readFileSync(existe ? f : path.join(dist, '404.html')));
  });
  await new Promise(r => servidor.listen(0, '127.0.0.1', r));
  const base = `http://127.0.0.1:${servidor.address().port}`;
  const browser = await chromium.launch();
  let falhas = 0;
  const mal = m => { falhas++; console.log('  ✗ ' + m); };
  const bem = m => console.log('  ✓ ' + m);

  const medir = () => {
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
    const alvos = [...document.querySelectorAll('a,button,summary')].filter(visivel).map(e => {
      const b = e.getBoundingClientRect(); return { t: (e.textContent || '').trim().slice(0, 30), h: Math.round(b.height) };
    });
    const titulos = [...document.querySelectorAll('h1,h2,h3,h4')].filter(visivel).map(h => +h.tagName[1]);
    return { textos, alvos, titulos, largura: document.documentElement.scrollWidth, janela: innerWidth };
  };

  for (const vista of ['proiecte', 'automatizari', 'servicii']) {
    for (const [nome, vp] of [['360', { width: 360, height: 780 }], ['390', { width: 390, height: 844 }], ['1280', { width: 1280, height: 800 }]]) {
      const ctx = await browser.newContext({ viewport: vp, deviceScaleFactor: 2, reducedMotion: 'reduce', locale: 'ro-RO' });
      const p = await ctx.newPage();
      const erros = [];
      p.on('pageerror', e => erros.push(e.message));
      await p.goto(`${base}/#${vista}`);
      await p.evaluate(() => document.fonts.ready);
      if (vista === 'automatizari') await p.$$eval('details', ds => ds.forEach(d => d.open = true));
      const r = await p.evaluate(medir);
      console.log(`\n#${vista} · ${nome} px`);
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
      if (capturas && nome !== '360') {
        await p.evaluate(() => Promise.all([...document.images].map(i => i.decode().catch(() => {}))));
        await p.screenshot({ path: path.join(capturas, `site-${vista}-${nome}.png`), fullPage: true });
      }
      await ctx.close();
    }
  }

  // separadores, automatizações e ligações — com JavaScript
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1, locale: 'ro-RO' });
  const p = await ctx.newPage();
  await p.goto(base + '/');
  const vis = id => p.$eval('#' + id, el => getComputedStyle(el).display !== 'none');
  console.log('\nNAVEGAÇÃO');
  if (!(await vis('proiecte')) || await vis('automatizari') || await vis('servicii')) mal('estado inicial: devia mostrar só #proiecte');
  else bem('início: só #proiecte visível');
  await p.click('.tabs a[href="#automatizari"]');
  if (!(await vis('automatizari')) || await vis('proiecte')) mal('separador Automatizări não trocou a vista');
  else bem('separador Automatizări → só #automatizari visível');
  const atual = await p.$eval('.tabs a[href="#automatizari"]', a => a.getAttribute('aria-current'));
  if (atual !== 'page') mal('aria-current não passou para Automatizări');
  const n = await p.$$eval('details.auto', ds => ds.length);
  if (n !== 8) mal(`esperava 8 automatizações, encontrei ${n}`); else bem('8 automatizações');
  await p.click('details.auto:nth-of-type(1) summary');
  const aberto = await p.$eval('details.auto:nth-of-type(1)', d => d.open);
  if (!aberto) mal('a primeira automatização não abriu ao tocar'); else bem('automatização abre ao tocar');
  await p.click('details.auto:nth-of-type(1) .chips a');
  await p.waitForTimeout(300);
  const abertoAlvo = await p.evaluate(() => { const d = document.querySelector(location.hash); return d && d.tagName === 'DETAILS' && d.open; });
  if (!abertoAlvo) mal('a ligação «Merge bine cu» não abriu a automatização apontada'); else bem('ligação entre automatizações abre a apontada e mantém a vista');
  if (!(await vis('automatizari'))) mal('a vista mudou ao seguir uma ligação interna');
  await p.click('.tabs a[href="#servicii"]');
  if (!(await vis('servicii')) || await vis('automatizari')) mal('separador Ce mai facem não trocou a vista'); else bem('separador Ce mai facem → só #servicii visível');
  await p.click('.tabs a[href="#proiecte"]');
  if (!(await vis('proiecte')) || await vis('servicii')) mal('voltar a Proiecte falhou'); else bem('voltar a Proiecte');

  // quadrados: cada ligação tem de existir em dist/ (ou ser externa)
  const hrefs = await p.$$eval('.grelha .q', as => as.map(a => a.getAttribute('href')));
  const externosSemNovoSep = await p.$$eval('.grelha .q[href^=http]', as => as.filter(a => a.target !== '_blank').length);
  if (externosSemNovoSep) mal(`${externosSemNovoSep} ligações externas sem target=_blank`);
  let faltam = 0;
  for (const h of hrefs) {
    if (h.startsWith('#')) continue;
    if (/^https?:/.test(h)) continue;
    const f = path.join(dist, h.replace(/^\//, ''), 'index.html');
    if (!fs.existsSync(f)) { faltam++; mal(`quadrado aponta para ${h} mas não existe em dist/`); }
  }
  if (!faltam) bem(`${hrefs.length} quadrados, todas as ligações existem`);

  // botão «Înapoi» dentro de um site copiado
  await p.click('.grelha .q[href^="/p/"]');
  await p.waitForLoadState('load');
  const url1 = p.url();
  const temPilula = await p.$('#ps-inapoi');
  if (!temPilula) mal('a cópia do site não tem o botão «Înapoi»');
  else {
    const h = await p.$eval('#ps-inapoi', a => Math.round(a.getBoundingClientRect().height));
    if (h < 44) mal(`botão «Înapoi» com ${h}px de altura`);
    await p.click('#ps-inapoi');
    await p.waitForLoadState('load');
    if (!/\/(#proiecte)?$/.test(p.url()) || p.url() === url1) mal('o botão «Înapoi» não voltou à página: ' + p.url());
    else bem('site copiado tem «Înapoi» e volta aos projetos');
  }
  const noindex = await p.evaluate(async u => { const t = await (await fetch(u)).text(); return /name="robots" content="noindex/.test(t); }, url1);
  if (!noindex) mal('a cópia do site não tem noindex'); else bem('cópias dos sites com noindex');

  // 404
  const r404 = await p.goto(base + '/nao-existe');
  if (r404.status() !== 404 || !(await p.$('text=/nu există/i'))) mal('404 não serviu a página romena'); else bem('404 em romeno');
  if (capturas) await p.screenshot({ path: path.join(capturas, 'site-404.png') });

  // barra fixa
  await p.goto(base + '/');
  await p.waitForTimeout(300);
  const antes = await p.$eval('#barra', b => b.classList.contains('visivel'));
  await p.evaluate(() => window.scrollTo(0, innerHeight * 1.5));
  await p.waitForTimeout(400);
  const depois = await p.$eval('#barra', b => b.classList.contains('visivel') && !b.hasAttribute('inert'));
  await p.evaluate(() => document.getElementById('contact').scrollIntoView());
  await p.waitForTimeout(500);
  const fim = await p.$eval('#barra', b => b.classList.contains('visivel'));
  if (antes || !depois || fim) mal(`barra fixa: no topo=${antes}, a meio=${depois}, no contacto=${fim}`); else bem('barra fixa: escondida no topo, visível a meio, escondida no contacto');
  await ctx.close();

  // sem JavaScript: os separadores continuam a trocar a vista (:target)
  const ctx2 = await browser.newContext({ viewport: { width: 390, height: 844 }, javaScriptEnabled: false });
  const p2 = await ctx2.newPage();
  await p2.goto(base + '/#servicii');
  const semJs = await p2.evaluate(() => [getComputedStyle(document.getElementById('servicii')).display, getComputedStyle(document.getElementById('proiecte')).display]);
  if (semJs[0] === 'none' || semJs[1] !== 'none') mal('sem JavaScript, #servicii não substituiu #proiecte'); else bem('sem JavaScript, os separadores funcionam (:target)');
  await ctx2.close();

  await browser.close();
  servidor.close();
  console.log(falhas ? `\n${falhas} problema(s).` : '\n✓ Sem problemas.');
  process.exit(falhas ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
