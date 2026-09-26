// Testes do site com o Chromium do Playwright, sobre dist/ servido como o Netlify serviria os DOIS domínios:
// pachecost.com (PT em /, EN em /en/) e ro.pachecost.com (RO). O _redirects de dist/ é lido e aplicado aqui
// (regras por domínio, 200! de reescrita, 301/302, 404 por língua), por isso os testes apanham erros nas regras.
// Uso: NODE_PATH=/opt/node22/lib/node_modules node verificar.cjs <dist> [pasta-capturas]
//  1. QR do cartão: HTTPS://RO.PACHECOST.COM/C → página romena. Endereços antigos e de cada língua.
//  2. Em 360, 390 e 1280 px, nas 3 línguas e nas 3 vistas: sem scroll horizontal, letra ≥ 12 px, contraste,
//     alvos ≥ 44 px, títulos por ordem.
//  3. Seletor PT · EN · RO, canonical e hreflang; separadores (com e sem JavaScript), automatizações, quadrados,
//     cópia da Toda Chic com «voltar» em cada língua, 404 em cada língua, privacidade, barra fixa, faixa de cookies.
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const dist = path.resolve(process.argv[2] || 'dist');
  const capturas = process.argv[3];
  const PT = 'https://pachecost.com', RO = 'https://ro.pachecost.com';
  const tipos = { '.html': 'text/html; charset=utf-8', '.webp': 'image/webp', '.png': 'image/png', '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg', '.svg': 'image/svg+xml', '.mp4': 'video/mp4', '.webm': 'video/webm', '.json': 'application/json',
    '.txt': 'text/plain', '.xml': 'application/xml', '.woff2': 'font/woff2', '.css': 'text/css', '.js': 'text/javascript' };

  // ——— emulador das regras do Netlify (o subconjunto que o gerador escreve) ———
  const regras = fs.readFileSync(path.join(dist, '_redirects'), 'utf8').split('\n')
    .map(l => l.trim()).filter(l => l && !l.startsWith('#')).map(l => {
      const [de, para, est] = l.split(/\s+/);
      const m = de.match(/^https?:\/\/([^/]+)(\/.*)$/);
      return { host: m ? m[1] : null, de: m ? m[2] : de, para, estado: parseInt(est, 10), forcar: est.endsWith('!') };
    });
  const ficheiro = p => {
    let f = path.join(dist, decodeURIComponent(p));
    if (!f.startsWith(dist)) return null;
    if (fs.existsSync(f) && fs.statSync(f).isDirectory()) f = path.join(f, 'index.html');
    return fs.existsSync(f) && fs.statSync(f).isFile() ? f : null;
  };
  const casa = (padrao, p) => {
    if (padrao.endsWith('/*')) { const b = padrao.slice(0, -1); if (p.startsWith(b)) return p.slice(b.length); if (p === b.slice(0, -1)) return ''; return null; }
    return padrao === p ? '' : null;
  };
  function responder(url) {
    const u = new URL(url);
    for (const r of regras) {
      if (r.host && r.host !== u.host) continue;
      const splat = casa(r.de, u.pathname);
      if (splat === null) continue;
      const alvo = r.para.replace(':splat', splat);
      if (r.estado === 301 || r.estado === 302) {
        const loc = /^https?:/.test(alvo) ? alvo : alvo; // relativo: o browser resolve no mesmo domínio
        return { status: r.estado, headers: { location: loc }, body: '' };
      }
      if (!r.forcar && ficheiro(u.pathname)) break; // regras não forçadas não tapam ficheiros que existem
      const f = ficheiro(alvo.split('?')[0]);
      if (f) return { status: r.estado, headers: { 'content-type': tipos[path.extname(f)] || 'application/octet-stream' }, body: fs.readFileSync(f) };
    }
    const f = ficheiro(u.pathname);
    if (f) return { status: 200, headers: { 'content-type': tipos[path.extname(f)] || 'application/octet-stream' }, body: fs.readFileSync(f) };
    return { status: 404, headers: { 'content-type': 'text/html; charset=utf-8' }, body: fs.readFileSync(path.join(dist, '404.html')) };
  }

  // sem proxy: os dois domínios são servidos aqui (route.fulfill) e o resto é cortado; nada sai para a rede
  const browser = await chromium.launch({ args: ['--no-proxy-server'] });
  let falhas = 0;
  const mal = m => { falhas++; console.log('  ✗ ' + m); };
  const bem = m => console.log('  ✓ ' + m);
  // consent: 'nao' = já respondeu (faixa escondida), null = primeira visita
  async function contexto(opcoes = {}, consent = 'nao') {
    const ctx = await browser.newContext({ deviceScaleFactor: 1, ...opcoes });
    await ctx.route('**/*', async rota => {
      const u = new URL(rota.request().url());
      if (u.host !== 'pachecost.com' && u.host !== 'ro.pachecost.com') return rota.abort(); // Google Fonts, GoatCounter, Meta, wa.me
      const r = responder(u.href);
      if (r.status === 301 || r.status === 302) {
        // o Chromium não segue um 3xx vindo da interceção (sai para a rede): segue-se aqui, com uma página que troca
        // o endereço. Os códigos 301/302 verificam-se à parte, com cadeia().
        const alvo = new URL(r.headers.location, u.href).href;
        return rota.fulfill({ status: 200, headers: { 'content-type': 'text/html; charset=utf-8' },
          body: `<!doctype html><html data-redirect><script>location.replace(${JSON.stringify(alvo)})</script></html>` });
      }
      await rota.fulfill(r);
    });
    if (consent) await ctx.addInitScript(v => { try { localStorage.setItem('ps-consentimento', v); } catch (e) {} }, consent);
    return ctx;
  }

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
    // exceção da WCAG 2.5.8: uma ligação dentro de uma frase (o email a meio de um parágrafo) tem a altura da linha
    const emFrase = e => getComputedStyle(e).display === 'inline' && e.parentElement.tagName === 'P' &&
      e.parentElement.textContent.trim().length > e.textContent.trim().length + 10;
    const alvos = [...document.querySelectorAll('a,button,summary')].filter(visivel).filter(e => !emFrase(e)).map(e => {
      const b = e.getBoundingClientRect(); return { t: (e.textContent || '').trim().slice(0, 30), h: Math.round(b.height) };
    });
    const titulos = [...document.querySelectorAll('h1,h2,h3,h4')].filter(visivel).map(h => +h.tagName[1]);
    return { textos, alvos, titulos, largura: document.documentElement.scrollWidth, janela: innerWidth };
  };
  const avaliar = (r, rotulo) => {
    if (r.largura > r.janela) mal(`${rotulo}: scroll horizontal ${r.largura} > ${r.janela}`);
    for (const t of r.textos) {
      const grande = t.px >= 24 || (t.px >= 18.66 && t.peso >= 700);
      if (t.px < 12) mal(`${rotulo}: letra ${t.px}px «${t.t}»`);
      if (t.c < (grande ? 3 : 4.5)) mal(`${rotulo}: contraste ${t.c}:1 (${t.px}px) «${t.t}»`);
    }
    for (const a of r.alvos) if (a.h < 44) mal(`${rotulo}: alvo de toque com ${a.h}px «${a.t}»`);
    let ant = 0; for (const h of r.titulos) { if (h > ant + 1) mal(`${rotulo}: título salta de h${ant} para h${h}`); ant = h; }
  };

  // os saltos de um endereço, pelas regras: [[302, '/?origem=cartao'], ..., [200]]
  function cadeia(url) {
    const saltos = [];
    for (let i = 0; i < 6; i++) {
      const r = responder(url);
      if (r.status !== 301 && r.status !== 302) { saltos.push([r.status]); break; }
      saltos.push([r.status, r.headers.location]);
      url = new URL(r.headers.location, url).href;
    }
    return { saltos, final: url };
  }

  const LINGUAS = { pt: { url: PT + '/', lang: 'pt-PT' }, en: { url: PT + '/en/', lang: 'en' }, ro: { url: RO + '/', lang: 'ro' } };

  // ——— 1. domínios, QR e endereços ———
  console.log('\nDOMÍNIOS E QR');
  {
    const ctx = await contexto({ viewport: { width: 390, height: 844 } });
    const p = await ctx.newPage();
    const ir = async (url, esperaUrl, esperaLang, texto, esperaSalto = null) => {
      const c = cadeia(url);
      await p.goto(url);
      if (p.url() !== esperaUrl) await p.waitForURL(esperaUrl, { timeout: 4000 }).catch(() => {});
      await p.waitForLoadState('load');
      const lang = await p.$eval('html', h => h.lang);
      const salto = c.saltos.length > 1 ? c.saltos[0][0] : null;
      const ok = p.url() === esperaUrl && lang === esperaLang && c.saltos[c.saltos.length - 1][0] === 200 && salto === esperaSalto;
      const via = c.saltos.map(s => s.join(' ')).join(' → ');
      if (ok) bem(`${texto}: ${url.replace('https://', '')} → ${p.url().replace('https://', '')} (${lang}; ${via})`);
      else mal(`${texto}: ${url} → ${p.url()} (lang ${lang}; ${via}); esperava ${esperaUrl} (${esperaLang}, salto ${esperaSalto})`);
    };
    await ir(RO + '/C', RO + '/?origem=cartao', 'ro', 'QR impresso', 302);
    await ir(RO + '/c', RO + '/?origem=cartao', 'ro', 'QR em minúsculas', 302);
    await ir(PT + '/', PT + '/', 'pt-PT', 'site principal abre em português');
    await ir(PT + '/en/', PT + '/en/', 'en', 'inglês');
    await ir(RO + '/', RO + '/', 'ro', 'subdomínio abre em romeno');
    await ir(PT + '/ro/', RO + '/', 'ro', 'pachecost.com/ro/ vai para o subdomínio', 301);
    await ir(PT + '/pt/', PT + '/', 'pt-PT', 'endereço antigo /pt/', 301);
    await ir(RO + '/en/', PT + '/en/', 'en', 'ro.pachecost.com/en/ vai para pachecost.com', 301);
    const cab = await p.evaluate(() => ({ goat: !!document.querySelector('script[data-goatcounter^="https://pachecost.goatcounter.com"]') }));
    if (!cab.goat) mal('falta o GoatCounter'); else bem('GoatCounter carregado (sem cookies), como no site anterior');
    for (const [k, v] of Object.entries(LINGUAS)) {
      await p.goto(v.url);
      const info = await p.evaluate(() => ({
        canonical: document.querySelector('link[rel=canonical]').href,
        alt: Object.fromEntries([...document.querySelectorAll('link[rel=alternate][hreflang]')].map(l => [l.hreflang, l.href])),
        seletor: [...document.querySelectorAll('.linguas a')].map(a => [a.textContent.trim().slice(0, 2), a.href, a.getAttribute('aria-current')]),
        og: document.querySelector('meta[property="og:image"]').content,
      }));
      const erros = [];
      if (info.canonical !== v.url) erros.push(`canonical ${info.canonical}`);
      for (const [kk, vv] of Object.entries(LINGUAS)) if (info.alt[vv.lang] !== vv.url) erros.push(`hreflang ${vv.lang}`);
      if (info.alt['x-default'] !== PT + '/') erros.push('x-default');
      const atuais = info.seletor.filter(s => s[2]).map(s => s[0]);
      if (info.seletor.length !== 3 || atuais.join() !== k.toUpperCase()) erros.push(`seletor ${JSON.stringify(info.seletor)}`);
      if (!/\/media\/og-(pt|en|ro)\.png$/.test(info.og) || !info.og.includes(k)) erros.push(`og:image ${info.og}`);
      const og = responder(info.og);
      if (og.status !== 200) erros.push('og:image não existe');
      if (erros.length) mal(`${k}: ${erros.join(' · ')}`); else bem(`${k}: canonical, hreflang das 3 línguas, seletor com ${k.toUpperCase()} marcado, imagem de partilha`);
      // cada ligação do seletor abre a língua certa
      for (const [sigla, href] of info.seletor) {
        const alvo = Object.values(LINGUAS).find(x => x.url === href);
        if (!alvo) { mal(`${k}: seletor ${sigla} aponta para ${href}`); continue; }
      }
    }
    // navegar pelo seletor, de uma língua para a outra
    await p.goto(PT + '/');
    await p.click('.linguas a[hreflang="ro"]'); await p.waitForLoadState('load');
    const l1 = await p.$eval('html', h => h.lang);
    await p.click('.linguas a[hreflang="en"]'); await p.waitForLoadState('load');
    const l2 = await p.$eval('html', h => h.lang);
    await p.click('.linguas a[hreflang="pt-PT"]'); await p.waitForLoadState('load');
    const l3 = await p.$eval('html', h => h.lang);
    if (`${l1},${l2},${l3}` !== 'ro,en,pt-PT') mal(`seletor: PT→RO→EN→PT deu ${l1},${l2},${l3}`); else bem('seletor: PT → RO → EN → PT, entre os dois domínios');
    // 404 em cada língua
    for (const [url, lang] of [[PT + '/nao-existe', 'pt-PT'], [PT + '/en/nope', 'en'], [RO + '/nu-exista', 'ro']]) {
      const r = await p.goto(url);
      const l = await p.$eval('html', h => h.lang);
      if (r.status() !== 404 || l !== lang) mal(`404 de ${url}: ${r.status()} em ${l}`); else bem(`404 em ${lang}: ${url.replace('https://', '')}`);
    }
    // privacidade
    for (const [url, lang] of [[PT + '/privacidade.html', 'pt-PT'], [PT + '/privacy.html', 'en'], [RO + '/confidentialitate.html', 'ro']]) {
      const r = await p.goto(url);
      const l = await p.$eval('html', h => h.lang);
      const r2 = await p.evaluate(medir);
      avaliar(r2, `privacidade ${lang}`);
      if (r.status() !== 200 || l !== lang) mal(`privacidade ${url}: ${r.status()} ${l}`); else bem(`privacidade em ${lang}`);
    }
    await ctx.close();
  }

  // ——— 2. acessibilidade: 3 línguas × 3 vistas × 3 larguras ———
  for (const [k, v] of Object.entries(LINGUAS)) {
    for (const vista of ['proiecte', 'automatizari', 'servicii']) {
      const linhas = [];
      for (const [nome, vp] of [['360', { width: 360, height: 780 }], ['390', { width: 390, height: 844 }], ['1280', { width: 1280, height: 800 }]]) {
        const ctx = await contexto({ viewport: vp, deviceScaleFactor: 2, reducedMotion: 'reduce' });
        const p = await ctx.newPage();
        const erros = [];
        p.on('pageerror', e => erros.push(e.message));
        await p.goto(`${v.url}#${vista}`);
        if (vista === 'automatizari') await p.$$eval('details', ds => ds.forEach(d => d.open = true));
        const r = await p.evaluate(medir);
        avaliar(r, `${k} #${vista} ${nome}px`);
        if (erros.length) mal(`${k} #${vista} ${nome}px: erros de JavaScript: ${erros.join(' | ')}`);
        linhas.push(`${nome}px: ${r.textos.length} textos, contraste ≥ ${Math.min(...r.textos.map(t => t.c))}:1, letra ≥ ${Math.min(...r.textos.map(t => t.px))}px`);
        if (capturas && nome !== '360' && vista === 'proiecte') {
          await p.evaluate(() => Promise.all([...document.images].map(i => i.decode().catch(() => {}))));
          await p.screenshot({ path: path.join(capturas, `site-${k}-${vista}-${nome}.png`), fullPage: true });
        }
        await ctx.close();
      }
      console.log(`\n${k} #${vista}\n  ${linhas.join('\n  ')}`);
    }
  }

  // ——— 3. navegação, quadrados, cópias, barra fixa ———
  console.log('\nNAVEGAÇÃO');
  const ctx = await contexto({ viewport: { width: 390, height: 844 } });
  const p = await ctx.newPage();
  for (const [k, v] of Object.entries(LINGUAS)) {
    await p.goto(v.url);
    const vis = id => p.$eval('#' + id, el => getComputedStyle(el).display !== 'none');
    const falhasAntes = falhas;
    if (!(await vis('proiecte')) || await vis('automatizari') || await vis('servicii')) mal(`${k}: estado inicial devia mostrar só #proiecte`);
    await p.click('.tabs a[href="#automatizari"]');
    if (!(await vis('automatizari')) || await vis('proiecte')) mal(`${k}: separador das automatizações não trocou a vista`);
    if (await p.$eval('.tabs a[href="#automatizari"]', a => a.getAttribute('aria-current')) !== 'page') mal(`${k}: aria-current não passou`);
    const n = await p.$$eval('details.auto', ds => ds.length);
    if (n !== 8) mal(`${k}: esperava 8 automatizações, encontrei ${n}`);
    await p.click('details.auto:nth-of-type(1) summary');
    if (!(await p.$eval('details.auto:nth-of-type(1)', d => d.open))) mal(`${k}: a primeira automatização não abriu`);
    await p.click('details.auto:nth-of-type(1) .chips a');
    await p.waitForTimeout(250);
    if (!(await p.evaluate(() => { const d = document.querySelector(location.hash); return d && d.tagName === 'DETAILS' && d.open; }))) mal(`${k}: ligação entre automatizações não abriu a apontada`);
    await p.click('.tabs a[href="#servicii"]');
    if (!(await vis('servicii'))) mal(`${k}: separador dos serviços não trocou a vista`);
    await p.click('.tabs a[href="#proiecte"]');
    if (!(await vis('proiecte'))) mal(`${k}: voltar aos projetos falhou`);
    // quadrados e exemplos: cada ligação interna tem de existir
    const hrefs = await p.$$eval('.grelha .q, .link-ex', as => as.map(a => a.getAttribute('href')));
    const semSep = await p.$$eval('.grelha .q[href^=http]', as => as.filter(a => a.target !== '_blank').length);
    if (semSep) mal(`${k}: ${semSep} ligações externas sem target=_blank`);
    for (const h of hrefs) {
      if (h.startsWith('#') || /^https?:/.test(h)) continue;
      if (responder(new URL(h, v.url).href).status !== 200) mal(`${k}: ${h} não existe`);
    }
    const dest = await p.$$eval('.grelha > li.dest .q-nome', ns => ns.map(n => n.textContent));
    if (dest.length !== 3) mal(`${k}: primeira fila com ${dest.length} quadrados`);
    // cópia da Toda Chic: «voltar» na língua da página
    await p.click('.grelha .q[href^="/p/"]');
    await p.waitForLoadState('load');
    const pil = await p.$eval('#ps-inapoi', a => ({ lang: a.lang, t: a.textContent.trim(), h: Math.round(a.getBoundingClientRect().height) })).catch(() => null);
    const noindex = await p.evaluate(() => /noindex/.test((document.querySelector('meta[name=robots]') || {}).content || ''));
    if (!pil) mal(`${k}: a cópia do site não tem o botão de voltar`);
    else {
      if (pil.lang !== v.lang) mal(`${k}: botão de voltar em ${pil.lang}`);
      if (pil.h < 44) mal(`${k}: botão de voltar com ${pil.h}px`);
      await p.click('#ps-inapoi');
      await p.waitForLoadState('load');
      const l = await p.$eval('html', h => h.lang);
      if (l !== v.lang || !p.url().startsWith(v.url)) mal(`${k}: o botão de voltar foi para ${p.url()} (${l})`);
    }
    if (!noindex) mal(`${k}: a cópia do site não tem noindex`);
    if (falhas === falhasAntes) bem(`${k}: separadores, 8 automatizações, ligações, primeira fila (${dest.join(', ')}), Toda Chic com «${pil && pil.t}» a voltar à página ${k.toUpperCase()}`);
  }

  // barra fixa
  await p.goto(LINGUAS.pt.url);
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

  // ——— 4. faixa de cookies (primeira visita) ———
  console.log('\nCOOKIES');
  {
    // ro.pachecost.com (quem lê o QR): sem pixel, logo sem faixa
    const c = await contexto({ viewport: { width: 390, height: 844 } }, null);
    const q = await c.newPage();
    await q.goto(LINGUAS.ro.url);
    const faixa = await q.$eval('#rgpd', f => !f.hidden);
    const semPixel = await q.evaluate(() => !/fbevents|fbq\('init'/.test([...document.scripts].map(x => x.textContent).join('')) || !/var PIXEL = '\d/.test([...document.scripts].map(x => x.textContent).join('')));
    if (faixa || !semPixel) mal(`ro.pachecost.com: faixa=${faixa}, sem pixel=${semPixel}`); else bem('ro.pachecost.com: sem pixel da Meta e sem faixa (o QR abre direto nos projetos)');
    await c.close();
  }
  for (const escolha of ['nao', 'sim']) {
    const c = await contexto({ viewport: { width: 390, height: 844 } }, null);
    const q = await c.newPage();
    await q.goto(LINGUAS.pt.url);
    const aberta = await q.$eval('#rgpd', f => !f.hidden);
    const r = await q.evaluate(medir);
    avaliar(r, 'faixa de cookies');
    const barraEscondida = await q.$eval('#barra', b => getComputedStyle(b).display === 'none');
    await q.click(escolha === 'sim' ? '#rgpdSim' : '#rgpdNao');
    const fechada = await q.$eval('#rgpd', f => f.hidden);
    const guardado = await q.evaluate(() => localStorage.getItem('ps-consentimento'));
    const pixel = await q.evaluate(() => typeof window.fbq === 'function');
    await q.reload();
    const depoisRecarregar = await q.$eval('#rgpd', f => f.hidden);
    if (!aberta || !barraEscondida || !fechada || guardado !== escolha || pixel !== (escolha === 'sim') || !depoisRecarregar)
      mal(`faixa (${escolha}): aberta=${aberta} barra escondida=${barraEscondida} fechou=${fechada} guardou=${guardado} pixel=${pixel} ao recarregar=${depoisRecarregar}`);
    else bem(escolha === 'sim' ? 'pachecost.com, «Aceitar»: a faixa fecha, fica guardado e o pixel da Meta arranca' : 'pachecost.com, «Só o essencial»: a faixa fecha, fica guardado e o pixel nunca carrega');
    await c.close();
  }

  // ——— 5. sem JavaScript: os separadores continuam a trocar a vista (:target) ———
  const ctx2 = await contexto({ viewport: { width: 390, height: 844 }, javaScriptEnabled: false });
  const p2 = await ctx2.newPage();
  await p2.goto(LINGUAS.pt.url + '#servicii');
  const semJs = await p2.evaluate(() => [getComputedStyle(document.getElementById('servicii')).display, getComputedStyle(document.getElementById('proiecte')).display, document.getElementById('rgpd').hidden]);
  if (semJs[0] === 'none' || semJs[1] !== 'none' || !semJs[2]) mal('sem JavaScript: vistas ou faixa de cookies erradas'); else bem('sem JavaScript: separadores funcionam (:target) e a faixa de cookies não aparece');
  await ctx2.close();

  await browser.close();
  console.log(falhas ? `\n${falhas} problema(s).` : '\n✓ Sem problemas.');
  process.exit(falhas ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
