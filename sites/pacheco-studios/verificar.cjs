// Testes do site com o Chromium do Playwright, sobre dist/ servido como o Netlify serviria os DOIS domínios:
// pachecost.com (PT em /, EN em /en/) e ro.pachecost.com (RO). O _redirects de dist/ é lido e aplicado aqui
// (regras por domínio, 200! de reescrita, 301/302, 404 por língua), por isso os testes apanham erros nas regras.
// Uso: NODE_PATH=/opt/node22/lib/node_modules node verificar.cjs <dist> [pasta-capturas]
//  1. QR do cartão: HTTPS://RO.PACHECOST.COM/C → página romena. Endereços antigos e de cada língua.
//  2. Em 360, 390 e 1280 px, nas 3 línguas e nas 4 vistas: sem scroll horizontal, letra ≥ 12 px, contraste,
//     alvos ≥ 44 px, títulos por ordem.
//  3. Seletor PT · EN · RO, canonical e hreflang; separadores (com e sem JavaScript), automatizações, sites em destaque e
//     por tipo de negócio (cada site ativo num deles, sem grelha com todos),
//     cópia da Toda Chic com «voltar» em cada língua, 404 em cada língua, privacidade e cookies, barra fixa, pixel sem faixa (desliga-se na página Cookies).
//  4. Esquemas: «Ver o esquema» abre cada um dos 8 num cartão no meio do ecrã (Esc, X e tocar fora fecham), o
//     endereço #esquema-… abre-o direto, e sem JavaScript mostra-o na mesma.
//  5. Intro: na 1.ª visita da sessão o carro passa pelos dois portais com as três fotografias e o ecrã sobe; um toque
//     ou Esc saltam-na; ao recarregar, com movimento reduzido ou sem JavaScript não aparece.
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
    // URLs bonitos do Netlify: /cartaz serve cartaz.html
    const f = ficheiro(u.pathname) || (!path.extname(u.pathname) && !u.pathname.endsWith('/') ? ficheiro(u.pathname + '.html') : null);
    if (f) return { status: 200, headers: { 'content-type': tipos[path.extname(f)] || 'application/octet-stream' }, body: fs.readFileSync(f) };
    return { status: 404, headers: { 'content-type': 'text/html; charset=utf-8' }, body: fs.readFileSync(path.join(dist, '404.html')) };
  }

  // sem proxy: os dois domínios são servidos aqui (route.fulfill) e o resto é cortado; nada sai para a rede
  const browser = await chromium.launch({ args: ['--no-proxy-server'] });
  let falhas = 0;
  const mal = m => { falhas++; console.log('  ✗ ' + m); };
  const bem = m => console.log('  ✓ ' + m);
  // consent: 'nao' = pixel desligado na página Cookies, null = primeira visita (pixel carrega sozinho)
  // intro: false = a sessão já a viu (não aparece); true = primeira visita, aparece
  async function contexto(opcoes = {}, consent = 'nao', intro = false) {
    const ctx = await browser.newContext({ deviceScaleFactor: 1, ...opcoes });
    if (!intro) await ctx.addInitScript(() => { try { sessionStorage.setItem('ps-intro', '1'); } catch (e) {} });
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

  // raiz: só dentro deste elemento (um esquema aberto); sem raiz, a página toda
  const medir = (raiz) => {
    const base = raiz ? document.querySelector(raiz) : document.body;
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
    const w = document.createTreeWalker(base, NodeFilter.SHOW_TEXT);
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
    const alvos = [...base.querySelectorAll('a,button,summary')].filter(visivel).filter(e => !emFrase(e)).map(e => {
      const b = e.getBoundingClientRect(); return { t: (e.textContent || '').trim().slice(0, 30), h: Math.round(b.height) };
    });
    const titulos = [...base.querySelectorAll('h1,h2,h3,h4')].filter(visivel).map(h => +h.tagName[1]);
    return { textos, alvos, titulos, largura: document.documentElement.scrollWidth, janela: innerWidth };
  };
  // nivel: o título acima da raiz medida (1 para um esquema: o h1 da página)
  const avaliar = (r, rotulo, nivel = 0) => {
    if (r.largura > r.janela) mal(`${rotulo}: scroll horizontal ${r.largura} > ${r.janela}`);
    for (const t of r.textos) {
      const grande = t.px >= 24 || (t.px >= 18.66 && t.peso >= 700);
      if (t.px < 12) mal(`${rotulo}: letra ${t.px}px «${t.t}»`);
      if (t.c < (grande ? 3 : 4.5)) mal(`${rotulo}: contraste ${t.c}:1 (${t.px}px) «${t.t}»`);
    }
    for (const a of r.alvos) if (a.h < 44) mal(`${rotulo}: alvo de toque com ${a.h}px «${a.t}»`);
    let ant = nivel; for (const h of r.titulos) { if (h > ant + 1) mal(`${rotulo}: título salta de h${ant} para h${h}`); ant = h; }
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

  const portfolio = JSON.parse(fs.readFileSync(path.join(__dirname, 'portfolio.json'), 'utf8'));
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
    for (const [url, lang] of [[PT + '/privacidade.html', 'pt-PT'], [PT + '/privacy.html', 'en'], [RO + '/confidentialitate.html', 'ro'],
                               [PT + '/cookies.html', 'pt-PT'], [PT + '/en/cookies.html', 'en'], [RO + '/cookie-uri.html', 'ro']]) {
      const r = await p.goto(url);
      const l = await p.$eval('html', h => h.lang);
      const r2 = await p.evaluate(medir);
      avaliar(r2, `privacidade ${lang}`);
      if (r.status() !== 200 || l !== lang) mal(`privacidade ${url}: ${r.status()} ${l}`); else bem(`privacidade em ${lang}`);
    }
    await ctx.close();
  }

  // ——— 2. acessibilidade: 3 línguas × 4 vistas × 3 larguras ———
  for (const [k, v] of Object.entries(LINGUAS)) {
    for (const vista of ['consultanta', 'cazuri', 'automatizari', 'proiecte']) {
      const linhas = [];
      for (const [nome, vp] of [['360', { width: 360, height: 780 }], ['390', { width: 390, height: 844 }], ['1280', { width: 1280, height: 800 }]]) {
        const ctx = await contexto({ viewport: vp, deviceScaleFactor: 2, reducedMotion: 'reduce' });
        const p = await ctx.newPage();
        const erros = [];
        p.on('pageerror', e => erros.push(e.message));
        await p.goto(`${v.url}#${vista}`);
        // abre todos os cartões (sem o «name», senão o navegador deixa só um aberto) para medir o que está lá dentro
        await p.$$eval('details', ds => ds.forEach(d => { d.removeAttribute('name'); d.open = true; }));
        const r = await p.evaluate(medir);
        avaliar(r, `${k} #${vista} ${nome}px`);
        if (erros.length) mal(`${k} #${vista} ${nome}px: erros de JavaScript: ${erros.join(' | ')}`);
        linhas.push(`${nome}px: ${r.textos.length} textos, contraste ≥ ${Math.min(...r.textos.map(t => t.c))}:1, letra ≥ ${Math.min(...r.textos.map(t => t.px))}px`);
        if (capturas && nome !== '360') {
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
    if (!(await vis('consultanta')) || await vis('cazuri') || await vis('automatizari') || await vis('proiecte')) mal(`${k}: estado inicial devia mostrar só #consultanta`);
    if (await p.$eval('.tabs a[href="#consultanta"]', a => a.getAttribute('aria-current')) !== 'page') mal(`${k}: a Consultoria não está marcada no início`);
    // consultoria: um só botão de diagnóstico no herói, que vai ao WhatsApp, e três números que levam a casos que existem
    const heroi = await p.$$eval('.heroi a.botao[href^="https://wa.me/"]', as => as.length);
    const nums = await p.$$eval('#consultanta .numeros a', as => as.map(a => a.getAttribute('href')));
    if (heroi !== 1) mal(`${k}: o herói devia ter um botão de WhatsApp (tem ${heroi})`);
    for (const h of nums) if (!(await p.$(h + '.caso'))) mal(`${k}: o número da Consultoria aponta para ${h}, que não é um caso`);
    if (nums.length !== 3) mal(`${k}: a Consultoria devia mostrar 3 números de casos (mostra ${nums.length})`);
    // casos: só o depoimento e 3 números; sem nome, sem tipo de negócio, sem ligações para fora, sem «próximo caso»
    await p.click('.tabs a[href="#cazuri"]');
    if (!(await vis('cazuri')) || await vis('consultanta')) mal(`${k}: separador dos casos não trocou a vista`);
    const nomes = JSON.parse(fs.readFileSync(path.join(__dirname, 'conteudo', 'casos.json'), 'utf8')).itens.map(x => x.empresa);
    const casos = await p.$$eval('.caso', cs => cs.map(c => ({ id: c.id, depo: (c.querySelector('.caso-depo') || {}).textContent || '',
      n: c.querySelectorAll('.caso-num li').length, fora: c.querySelectorAll('a[href^="http"]').length, txt: c.textContent })));
    if (casos.length !== nomes.length) mal(`${k}: ${casos.length} casos (esperava ${nomes.length})`);
    for (const c of casos) {
      if (c.depo.trim().length < 20 || c.n !== 3 || c.fora) mal(`${k}: caso mal montado ${JSON.stringify(c)}`);
    }
    const pagina = await p.evaluate(() => document.body.innerText);
    const comNome = nomes.filter(x => pagina.includes(x));
    if (comNome.length) mal(`${k}: o site mostra o nome de empresas dos casos: ${comNome.join(', ')}`);
    if (await p.$('.caso.vazio')) mal(`${k}: ainda há a caixa «o próximo caso»`);
    await p.click('.tabs a[href="#automatizari"]');
    if (!(await vis('automatizari')) || await vis('proiecte')) mal(`${k}: separador das automatizações não trocou a vista`);
    if (await p.$eval('.tabs a[href="#automatizari"]', a => a.getAttribute('aria-current')) !== 'page') mal(`${k}: aria-current não passou`);
    const n = await p.$$eval('details.auto', ds => ds.length);
    if (n !== 8) mal(`${k}: esperava 8 automatizações, encontrei ${n}`);
    await p.click('details.auto:nth-of-type(1) summary');
    if (!(await p.$eval('details.auto:nth-of-type(1)', d => d.open))) mal(`${k}: a primeira automatização não abriu`);
    await p.click('details.auto:nth-of-type(1) .chips a[href^="#a-"]');
    await p.waitForTimeout(250);
    if (!(await p.evaluate(() => { const d = document.querySelector(location.hash); return d && d.tagName === 'DETAILS' && d.open; }))) mal(`${k}: ligação entre automatizações não abriu a apontada`);
    // «O que mais fazemos» vive no fim das Soluções
    if (!(await p.$('#automatizari #servicii .svc'))) mal(`${k}: «O que mais fazemos» não está no fim das Soluções`);
    await p.click('.tabs a[href="#proiecte"]');
    if (!(await vis('proiecte')) || await vis('consultanta')) mal(`${k}: separador dos sites falhou`);
    // sites em destaque, sites dentro de cada tipo de negócio e exemplos: cada ligação interna tem de existir
    const hrefs = await p.$$eval('.grelha .q, .grelha-mais .q, .exemplos a, .link-ex', as => as.map(a => a.getAttribute('href')));
    const semSep = await p.$$eval('.grelha .q[href^=http], .grelha-mais .q[href^=http], .exemplos a[href^=http]', as => as.filter(a => a.target !== '_blank').length);
    // sem grelha com todos, sem «O teu negócio?»: cada site ativo aparece uma vez num tipo de negócio
    const setores = await p.$$eval('details.setor', ds => ds.map(d => ({ id: d.id, n: d.querySelectorAll('.exemplos a').length,
      qa: d.querySelectorAll('.perguntas dt').length, combina: d.querySelectorAll('.chips a').length })));
    const nosSetores = await p.$$eval('.exemplos a', as => as.map(a => a.getAttribute('href')));
    const ativos = portfolio.itens.filter(x => x.ativo && !x.demo && (x.url || x.pasta));
    const emFalta = ativos.filter(x => !nosSetores.some(h => x.url ? h === x.url : h.startsWith(`/p/${x.slug}/`))).map(x => x.slug);
    if (setores.length !== 4 || setores.some(x => !x.qa || !x.combina)) mal(`${k}: tipos de negócio ${JSON.stringify(setores)}`);
    if (emFalta.length || nosSetores.length !== ativos.length) mal(`${k}: sites fora dos tipos de negócio: ${emFalta.join(', ')} (${nosSetores.length}/${ativos.length})`);
    if (await p.$('.q.teu, .grelha > li:not(.dest)')) mal(`${k}: a grelha ainda tem mais do que os três em destaque`);
    // «Mais sites»: todos os outros sites ativos, sem o quadrado de contacto
    const mais = await p.$$eval('.grelha-mais .q', as => as.map(a => a.getAttribute('href')));
    if (mais.length !== ativos.length - 3 || await p.$('.grelha-mais .teu')) mal(`${k}: «Mais sites» com ${mais.length} sites (esperava ${ativos.length - 3})`);
    // «Combina com» leva à automação e abre-a
    await p.click('.tabs a[href="#proiecte"]');
    await p.click('#s-restauracao summary');
    await p.click('#s-restauracao .chips a');
    await p.waitForTimeout(250);
    if (!(await p.evaluate(() => { const d = document.querySelector(location.hash); return d && d.tagName === 'DETAILS' && d.open && !!d.closest('#automatizari'); })))
      mal(`${k}: «Combina com» não abriu a automação`);
    await p.click('.tabs a[href="#proiecte"]');
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
    if (falhas === falhasAntes) bem(`${k}: separadores, consultoria, ${casos.length} casos só com depoimento e resultados (sem nomes), 8 automatizações, ligações, em destaque (${dest.join(', ')}), 4 tipos de negócio com os ${ativos.length} sites, Toda Chic com «${pil && pil.t}» a voltar à página ${k.toUpperCase()}`);
  }

  // diagnóstico: «Conhece-nos» abre a conversa; 8 respostas; no fim, a mensagem para o WhatsApp leva tudo
  for (const [k, v] of Object.entries(LINGUAS)) {
    await p.goto(v.url);
    // o GoatCounter está cortado no teste: um substituto apanha os eventos
    await p.evaluate(() => { window.__gc = []; window.goatcounter = { count: o => window.__gc.push(o.path) }; });
    await p.click('.heroi [data-diagnostico]');
    const g = JSON.parse(fs.readFileSync(path.join(__dirname, 'conteudo', k + '.json'), 'utf8')).diagnostico;
    // quem faz o diagnóstico: a foto do Tomás carregada, com nome e papel na língua da página
    const cara = await p.evaluate(() => { const i = document.querySelector('.diag-quem img');
      return { foto: !!i && i.complete && i.naturalWidth > 100, alt: i && i.alt, nome: (document.querySelector('.diag-quem b') || {}).textContent,
        papel: (document.querySelector('.diag-quem small') || {}).textContent }; });
    if (!cara.foto || cara.nome !== g.quem_nome || cara.papel !== g.quem_papel || ![g.quem_alt, 'Pacheco Studios'].includes(cara.alt)) mal(`${k}: diagnóstico sem a cara do Tomás: ${JSON.stringify(cara)}`);
    // 1.º ecrã: a foto, o porquê e logo o campo do nome (sem «Começar»)
    const ecra1 = await p.evaluate(() => ({ nome: !!document.getElementById('diag-in'), comecar: !!document.getElementById('diag-comecar'),
      foto: !!document.querySelector('.diag-quem img'), foco: document.activeElement && document.activeElement.id }));
    if (!ecra1.nome || ecra1.comecar || !ecra1.foto || ecra1.foco === 'diag-in') mal(`${k}: 1.º ecrã do diagnóstico ${JSON.stringify(ecra1)}`);
    const respostas = [];
    for (const q of g.perguntas) {
      if (q.tipo === 'texto' || q.tipo === 'tel' || q.tipo === 'email') {
        await p.waitForSelector('#diag-in', { timeout: 8000 });
        const t = q.tipo === 'tel' ? '+351 900 000 000' : q.tipo === 'email' ? 'teste@exemplo.pt' : `Teste ${q.id}`;
        await p.fill('#diag-in', t); await p.press('#diag-in', 'Enter'); respostas.push(t);
        // depois de cada resposta, o Tomás «está a escrever…» antes da mensagem seguinte
        if (q.id === 'nome' && !(await p.evaluate(() => !!document.querySelector('.diag-pensa')))) mal(`${k}: falta o «a escrever…» depois do nome`);
      } else if (q.outro) {
        // «Outro»: abre um campo; o que se escreve é a resposta
        await p.waitForSelector('.diag-op', { timeout: 8000 });
        await p.click(`.diag-op:nth-child(${q.opcoes.indexOf(q.outro) + 1})`);
        await p.waitForSelector('#diag-in', { timeout: 8000 });
        const t = `Teste ${q.id} escrito`;
        await p.fill('#diag-in', t); await p.press('#diag-in', 'Enter'); respostas.push(t);
      } else {
        await p.waitForSelector('.diag-op', { timeout: 8000 });
        await p.click('.diag-op'); respostas.push(q.opcoes[0]);
        if (q.tipo === 'multi') await p.click('#diag-seg');
      }
      await p.waitForTimeout(350);
    }
    await p.waitForSelector('#diag-enviar', { timeout: 10000 });
    // os ganchos: cada pergunta vem com uma frase que reage à resposta anterior (o nome do negócio, a dor escolhida…)
    const conversa = await p.evaluate(() => document.getElementById('diag-palco').textContent);
    const ganchos = g.perguntas.filter(q => q.gancho).map(q => {
      const antes = g.perguntas.find(x => x.id === q.gancho_de), v = respostas[g.perguntas.indexOf(antes)];
      const i = antes.opcoes ? antes.opcoes.indexOf(v) : -1;
      return (q.gancho[String(i)] || q.gancho['*']).replace(/\{(\w+)\}/g, (m, id) => id === 'nome' ? 'Teste' : respostas[g.perguntas.findIndex(x => x.id === id)]);
    });
    const semGancho = ganchos.filter(t => !conversa.includes(t));
    if (semGancho.length) mal(`${k}: ganchos em falta na conversa: ${semGancho.join(' | ')}`);
    else bem(`${k}: conversa com «a escrever…» e ${ganchos.length} ganchos que reagem às respostas`);
    const fim = await p.evaluate(() => ({ href: decodeURIComponent(document.getElementById('diag-enviar').href),
      n: document.getElementById('diag-n').textContent, aberto: document.getElementById('diagnostico').open }));
    const falta = respostas.filter(t => !fim.href.includes(t));
    // o número que recebe o diagnóstico: o romeno no ro.pachecost.com, o português no resto (marca/dados.json)
    const numDiag = k === 'ro' ? 'https://wa.me/40723098556?' : 'https://wa.me/351967117357?';
    if (!fim.href.startsWith(numDiag)) mal(`${k}: o diagnóstico vai para ${fim.href.split('?')[0]} e devia ir para ${numDiag.slice(0, -1)}`);
    else bem(`${k}: o diagnóstico é enviado para ${numDiag.slice(14, -1)}`);
    // os contactos do fim da página: o número romeno no RO, o português no resto
    const cont = await p.evaluate(() => { const s = document.getElementById('contact');
      return { txt: s.textContent, tel: (s.querySelector('a[href^="tel:"]') || {}).href, wa: (s.querySelector('.contactos a[href^="https://wa.me"]') || {}).href }; });
    const [numTxt, numTel] = k === 'ro' ? ['+40 723 098 556', 'tel:+40723098556'] : ['+351 967 117 357', 'tel:+351967117357'];
    if (!cont.txt.includes(numTxt) || cont.tel !== numTel || !cont.wa.startsWith(numDiag)) mal(`${k}: contactos do fim da página ${JSON.stringify({ tel: cont.tel, wa: cont.wa && cont.wa.split('?')[0] })}`);
    else bem(`${k}: contactos do fim da página com ${numTxt}`);
    // no ro.pachecost.com só o número romeno, em todos os botões e no JSON-LD (pedido do Tomás, 09/10)
    const outro = await p.evaluate(n => { const h = document.documentElement.outerHTML;
      return (h.match(new RegExp(n.join('|'), 'g')) || []).length; }, k === 'ro' ? ['351967117357', '967 117 357'] : ['40723098556', '723 098 556']);
    if (outro) mal(`${k}: ${outro} vezes o número ${k === 'ro' ? 'português' : 'romeno'} na página`);
    else bem(`${k}: só aparece o número ${k === 'ro' ? 'romeno' : 'português'} na página`);
    await p.evaluate(() => { const a = document.getElementById('diag-enviar'); a.addEventListener('click', e => e.preventDefault()); a.click(); });
    const avatar = await p.evaluate(() => !!document.querySelector('.diag-bot img'));
    if (!avatar) mal(`${k}: o fim do diagnóstico devia ter a foto do Tomás`);
    const ev = await p.evaluate(() => window.__gc);
    const pq = g.perguntas.map((q, i) => `diagnostico/pergunta-${String(i + 1).padStart(2, '0')}-${q.id}`);
    const esperado = ['diagnostico/aberto', pq[0], 'diagnostico/comecou', ...pq.slice(1), 'diagnostico/fim', 'diagnostico/enviado'];
    if (JSON.stringify(ev) !== JSON.stringify(esperado)) mal(`${k}, eventos do diagnóstico: ${ev.join(' ')}`);
    else bem(`${k}: 1.º ecrã com foto e nome; eventos no GoatCounter por ordem: aberto, pergunta 1, começou, as outras perguntas, fim, enviado`);
    await p.keyboard.press('Escape');
    const fechou = await p.evaluate(() => !document.getElementById('diagnostico').open);
    const fat = g.perguntas.find(q => q.id === 'faturacao');
    const moeda = fat && fat.opcoes.slice(0, -1).every(o => o.includes(k === 'ro' ? 'lei' : '€'));
    if (falta.length || +fim.n !== g.perguntas.length || !fim.aberto || !fechou || !moeda) mal(`${k}, diagnóstico: ${JSON.stringify({ falta, fim, fechou, moeda })}`);
    else bem(`${k}: diagnóstico com a ficha, ${g.perguntas.length} respostas (e-mail na 3.ª, faturação em ${k === 'ro' ? 'lei' : '€'}), todas na mensagem para o WhatsApp; Esc fecha`);
  }

  // anúncio de sites: entra nos Sites; sem utm, entra na Consultoria
  await p.goto(LINGUAS.ro.url + '?utm_source=meta&utm_content=web-bolta');
  await p.waitForTimeout(200);
  const doAnuncio = await p.evaluate(() => ({ h: location.hash, s: getComputedStyle(document.getElementById('proiecte')).display !== 'none' }));
  if (doAnuncio.h !== '#proiecte' || !doAnuncio.s) mal(`anúncio de sites: ${JSON.stringify(doAnuncio)}`); else bem('anúncio de sites (utm_content=web-…): abre nos Sites');

  // barra fixa
  await p.goto(LINGUAS.pt.url);
  await p.waitForTimeout(300);
  const antes = await p.$eval('#barra', b => b.classList.contains('visivel'));
  await p.evaluate(() => window.scrollTo(0, innerHeight * 1.5));
  await p.waitForTimeout(400);
  const depois = await p.$eval('#barra', b => b.classList.contains('visivel') && !b.hasAttribute('inert'));
  await p.evaluate(() => document.getElementById('contact').scrollIntoView({ behavior: 'instant' }));
  await p.waitForTimeout(500);
  const fim = await p.$eval('#barra', b => b.classList.contains('visivel'));
  if (antes || !depois || fim) mal(`barra fixa: no topo=${antes}, a meio=${depois}, no contacto=${fim}`); else bem('barra fixa: escondida no topo, visível a meio, escondida no contacto');
  await ctx.close();

  // ——— 4. esquemas: «Ver o esquema» abre o cartão no meio do ecrã ———
  console.log('\nESQUEMAS');
  for (const [k, v] of Object.entries(LINGUAS)) {
    const linhas = [];
    for (const [nome, vp] of [['360', { width: 360, height: 780 }], ['1280', { width: 1280, height: 800 }]]) {
      const c = await contexto({ viewport: vp, deviceScaleFactor: 2, reducedMotion: 'reduce' });
      const q = await c.newPage();
      const erros = [];
      q.on('pageerror', e => erros.push(e.message));
      await q.goto(v.url + '#automatizari');
      const falhasAntes = falhas;
      const ids = await q.$$eval('details.auto', ds => ds.map(d => d.id.slice(2)));
      const botoes = await q.$$eval('details.auto .corpo > .ver-esquema:first-child', as => as.length);
      const dialogos = await q.$$eval('dialog.esquema', ds => ds.length);
      if (ids.length !== 8 || botoes !== 8 || dialogos !== 8)
        mal(`${k} ${nome}px: ${ids.length} automatizações, ${botoes} botões «ver o esquema» no início do cartão, ${dialogos} esquemas`);
      // o GoatCounter real não carrega aqui: regista-se o que lhe seria enviado
      await q.evaluate(() => { window.__ev = []; if (window.goatcounter) window.goatcounter.count = o => window.__ev.push(o.path); });
      let caixas = 0, contraste = Infinity, letra = Infinity;
      for (const id of ids) {
        const rot = `${k} esquema ${id} ${nome}px`;
        await q.click(`#a-${id} summary`);
        await q.click(`#a-${id} .ver-esquema`);
        const e = await q.evaluate(id => {
          const d = document.getElementById('esquema-' + id), b = d.getBoundingClientRect();
          const tela = d.querySelector('.tela').getBoundingClientRect();
          // as portas (::before e ::after) saem da caixa de propósito: mede-se a caixa na tela e o texto na caixa
          const fora = [...d.querySelectorAll('.n, .pilula')].filter(n => {
            const r = n.getBoundingClientRect(), t = (n.querySelector('.tx') || n).getBoundingClientRect();
            return r.left < tela.left - 1 || r.right > tela.right + 1 || t.left < r.left - 1 || t.right > r.right + 1;
          }).length;
          const titulo = document.getElementById(d.getAttribute('aria-labelledby'));
          return { modal: d.open && d.matches(':modal'), abertos: document.querySelectorAll('dialog[open]').length,
            dentro: b.left >= 0 && b.top >= 0 && b.right <= innerWidth && b.bottom <= innerHeight,
            foco: d.contains(document.activeElement), nome: !!(titulo && d.contains(titulo) && titulo.textContent.trim()),
            caixas: d.querySelectorAll('.n').length, fora, lado: d.scrollWidth > d.clientWidth + 1, hash: location.hash };
        }, id);
        if (!e.modal || e.abertos !== 1) mal(`${rot}: não abriu como cartão (modal=${e.modal}, abertos=${e.abertos})`);
        if (!e.dentro) mal(`${rot}: o cartão sai do ecrã`);
        if (!e.foco) mal(`${rot}: o foco não entrou no cartão`);
        if (!e.nome) mal(`${rot}: o cartão não tem nome acessível`);
        if (e.fora || e.lado) mal(`${rot}: ${e.fora} caixa(s) a sair da tela${e.lado ? ', scroll horizontal no cartão' : ''}`);
        if (e.hash !== '#automatizari') mal(`${rot}: o botão mudou o endereço para ${e.hash}`);
        const r = await q.evaluate(medir, `#esquema-${id}`);
        avaliar(r, rot, 1);
        caixas += e.caixas;
        contraste = Math.min(contraste, ...r.textos.map(t => t.c));
        letra = Math.min(letra, ...r.textos.map(t => t.px));
        if (capturas && id === 'lead') await q.screenshot({ path: path.join(capturas, `esquema-${k}-${nome}.png`) });
        await q.keyboard.press('Escape');
        if (await q.$eval(`#esquema-${id}`, d => d.open)) mal(`${rot}: Esc não fechou o cartão`);
      }
      // fechar com o X e tocando fora; pelo teclado, Enter abre e Esc devolve o foco ao botão
      const id0 = ids[0], d0 = `#esquema-${id0}`;
      await q.click(`#a-${id0} summary`);
      await q.click(`#a-${id0} .ver-esquema`);
      await q.click(`${d0} .fechar`);
      const x = await q.$eval(d0, d => !d.open && location.hash === '#automatizari');
      await q.click(`#a-${id0} .ver-esquema`);
      await q.mouse.click(4, 4);
      const fora = await q.$eval(d0, d => !d.open);
      await q.focus(`#a-${id0} .ver-esquema`);
      await q.keyboard.press('Enter');
      const teclado = await q.$eval(d0, d => d.open);
      await q.keyboard.press('Escape');
      const focoVolta = await q.evaluate(() => !!document.activeElement && document.activeElement.matches('.ver-esquema'));
      const ev = await q.evaluate(() => window.__ev);
      if (!x) mal(`${k} ${nome}px: o X não fechou o cartão (ou mudou o endereço)`);
      if (!fora) mal(`${k} ${nome}px: tocar fora não fechou o cartão`);
      if (!teclado || !focoVolta) mal(`${k} ${nome}px: teclado: Enter abriu=${teclado}, foco voltou ao botão=${focoVolta}`);
      if (!ids.every(id => ev.includes('esquema/' + id))) mal(`${k} ${nome}px: eventos do GoatCounter ${JSON.stringify(ev)}`);
      // endereço partilhado: #esquema-… abre o cartão; ao fechar, fica-se na automação dele, aberta
      const q2 = await c.newPage();
      q2.on('pageerror', e => erros.push(e.message));
      const id2 = ids[3];
      await q2.goto(`${v.url}#esquema-${id2}`);
      const dl = await q2.evaluate(id => ({ aberto: document.getElementById('esquema-' + id).open,
        vista: getComputedStyle(document.getElementById('automatizari')).display !== 'none' }), id2);
      await q2.keyboard.press('Escape');
      await q2.waitForTimeout(200);
      const dl2 = await q2.evaluate(id => ({ hash: location.hash, aberta: document.getElementById('a-' + id).open,
        fechado: !document.getElementById('esquema-' + id).open,
        vista: getComputedStyle(document.getElementById('automatizari')).display !== 'none' }), id2);
      if (!dl.aberto || !dl.vista) mal(`${k} ${nome}px: #esquema-${id2} não abriu o cartão (aberto=${dl.aberto}, vista=${dl.vista})`);
      if (!dl2.fechado || dl2.hash !== `#a-${id2}` || !dl2.aberta || !dl2.vista)
        mal(`${k} ${nome}px: depois de fechar #esquema-${id2}: ${JSON.stringify(dl2)}`);
      if (erros.length) mal(`${k} ${nome}px: erros de JavaScript: ${erros.join(' | ')}`);
      if (falhas === falhasAntes) linhas.push(`${nome}px: 8 esquemas, ${caixas} caixas, contraste ≥ ${contraste}:1, letra ≥ ${letra}px`);
      await c.close();
    }
    if (linhas.length === 2) bem(`${k}: ${linhas.join(' · ')}; Esc, X e tocar fora fecham; teclado e endereço direto`);
  }

  // ——— 5. cookies: nada aparece ao abrir; o pixel carrega sozinho em pachecost.com e desliga-se na página Cookies ———
  console.log('\nCOOKIES');
  const temPixel = q => q.evaluate(() => typeof window.fbq === 'function');
  {
    // ro.pachecost.com (quem lê o QR): sem pixel
    const c = await contexto({ viewport: { width: 390, height: 844 } }, null);
    const q = await c.newPage();
    await q.goto(LINGUAS.ro.url);
    const faixa = await q.$('#rgpd');
    const px = await temPixel(q);
    const rod = await q.$$eval('.rodape a', as => as.map(a => a.getAttribute('href')));
    if (faixa || px || !rod.includes('/cookie-uri.html')) mal(`ro.pachecost.com: faixa=${!!faixa} pixel=${px} rodapé=${rod}`);
    else bem('ro.pachecost.com: nada ao abrir, sem pixel da Meta; rodapé liga à política de cookie-uri');
    await c.close();
  }
  {
    const c = await contexto({ viewport: { width: 390, height: 844 } }, null);
    const q = await c.newPage();
    await q.goto(LINGUAS.pt.url);
    const faixa = await q.$('#rgpd');
    const px = await temPixel(q);
    const rod = await q.$$eval('.rodape a', as => as.map(a => a.getAttribute('href')));
    if (faixa || !px || !rod.includes('/cookies.html') || !rod.includes('/privacidade.html'))
      mal(`pachecost.com, 1.ª visita: faixa=${!!faixa} pixel=${px} rodapé=${rod}`);
    else bem('pachecost.com, 1.ª visita: nada aparece, o pixel carrega sozinho e o rodapé liga à privacidade e aos cookies');
    // página Cookies: desligar e voltar a ligar
    await q.goto(PT + '/cookies.html');
    const t1 = await q.$eval('#pixel-txt', e => e.textContent);
    await q.click('#pixel-btn');
    const guardado = await q.evaluate(() => localStorage.getItem('ps-consentimento'));
    const t2 = await q.$eval('#pixel-txt', e => e.textContent);
    await q.goto(LINGUAS.pt.url);
    const pxDesligado = await temPixel(q);
    await q.goto(PT + '/cookies.html');
    await q.click('#pixel-btn');
    await q.goto(LINGUAS.pt.url);
    const pxReligado = await temPixel(q);
    if (guardado !== 'nao' || t1 === t2 || pxDesligado || !pxReligado)
      mal(`página Cookies: guardou=${guardado} texto mudou=${t1 !== t2} pixel desligado=${pxDesligado} religado=${pxReligado}`);
    else bem('página Cookies: «Desligar o pixel» fica guardado e o site deixa de o carregar; «Voltar a ligar» repõe');
    await c.close();
  }
  {
    // sinal Global Privacy Control do navegador: o pixel não carrega
    const c = await contexto({ viewport: { width: 390, height: 844 } }, null);
    await c.addInitScript(() => Object.defineProperty(Navigator.prototype, 'globalPrivacyControl', { get: () => true }));
    const q = await c.newPage();
    await q.goto(LINGUAS.pt.url);
    if (await temPixel(q)) mal('GPC: o pixel carregou'); else bem('navegador com Global Privacy Control: o pixel não carrega');
    await c.close();
  }

  // ——— 5b. herói: o vídeo em fotogramas (16:9 em ecrãs deitados, recorte 9:16 ao alto) avança com o scroll ———
  console.log('\nHERÓI');
  // a ordem a seguir ao herói é a mesma nas três línguas: veredito (3D), depois a caixa da consultoria
  for (const [k, f] of [['pt', 'index.html'], ['en', 'en/index.html'], ['ro', 'ro/index.html']]) {
    const h = fs.readFileSync(path.join(dist, f), 'utf8');
    const ordem = ['class="heroi-bg"', 'class="veredito seccao"', 'class="envolver seccao consultoria"', 'class="envolver seccao ia-bloco"'].map(x => h.indexOf(x));
    if (ordem.some(x => x < 0) || ordem.some((x, i) => i && x <= ordem[i - 1])) mal(`${k}: ordem das secções a seguir ao herói ${JSON.stringify(ordem)}`);
    else bem(`${k}: a seguir ao herói vem o veredito e depois a consultoria`);
  }
  const comVideo = fs.readFileSync(path.join(dist, 'index.html'), 'utf8').includes('id="heroi-quadros"');
  if (!comVideo) {
    // desligado no gerar.py (HEROI_VIDEO = False): imagem parada, o scroll desce normalmente
    for (const [w, h] of [[1280, 800], [390, 844]]) {
      const c = await contexto({ viewport: { width: w, height: h } });
      const q = await c.newPage();
      await q.goto(LINGUAS.pt.url);
      await q.waitForTimeout(800);
      const r = await q.evaluate(() => ({ rolo: document.querySelector('.heroi-bg').classList.contains('rolo'), cv: !!document.querySelector('.heroi-cv'),
        pedidos: performance.getEntriesByType('resource').filter(x => x.name.includes('/heroi-hd/')).length,
        img: !!document.querySelector('.heroi-img') }));
      if (r.rolo || r.cv || r.pedidos || !r.img) mal(`herói ${w}px: vídeo desligado mas ${JSON.stringify(r)}`);
      else bem(`herói ${w}px: vídeo desligado; imagem parada e o scroll desce normalmente`);
      await c.close();
    }
  }
  for (const [w, h, conj] of (comVideo ? [[1280, 800, 'd'], [390, 844, 'v']] : [])) {
    const c = await contexto({ viewport: { width: w, height: h } });
    const q = await c.newPage();
    await q.goto(LINGUAS.pt.url);
    await q.waitForTimeout(1500);
    const pedidos = await q.evaluate(() => performance.getEntriesByType('resource').map(r => r.name).filter(n => n.includes('/heroi-hd/')));
    const certo = pedidos.length > 1 && pedidos.every(n => n.includes(`/heroi-hd/${pedidos[0].includes('/v/') ? 'v' : 'd'}/`)) && pedidos[0].includes(`/${conj}/`);
    const rolo = await q.$eval('.heroi-bg', b => b.classList.contains('rolo'));
    await q.evaluate(() => { const b = document.querySelector('.heroi-bg'); window.scrollTo(0, (b.offsetHeight - innerHeight) * .5); });
    await q.waitForTimeout(500);
    const pinta = await q.evaluate(() => { const cv = document.querySelector('.heroi-cv'); const d = cv.getContext('2d').getImageData(0, 0, cv.width, cv.height).data; let s = 0; for (let i = 0; i < d.length; i += 400) s += d[i] + d[i + 1] + d[i + 2]; return s; });
    if (!certo || !rolo || !pinta) mal(`herói ${w}px: conjunto ${conj} certo=${certo} (${pedidos.length} pedidos) rolo=${rolo} desenha=${!!pinta}`);
    else bem(`herói ${w}px: fotogramas ${conj === 'd' ? '16:9' : '9:16'} (${pedidos.length} carregados), preso ao ecrã e desenhado a meio do scroll`);
    await c.close();
  }

  // ——— 6. intro: 1.ª vez na sessão, com as três fotografias; salta com um toque ou Esc; nunca com movimento reduzido ———
  console.log('\nINTRO');
  const comIntro = fs.readFileSync(path.join(dist, 'index.html'), 'utf8').includes('id="intro"');
  if (!comIntro) {
    // desligada no gerar.py (INTRO_LIGADA = False): na 1.ª visita não aparece e a página abre ativa
    for (const [k, v] of Object.entries(LINGUAS)) {
      const c = await contexto({ viewport: { width: 390, height: 844 } }, 'nao', true);
      const q = await c.newPage();
      await q.goto(v.url);
      const r = await q.evaluate(() => ({ vai: document.documentElement.classList.contains('intro-vai'), existe: !!document.getElementById('intro'),
        inerte: document.querySelector('main').hasAttribute('inert'), rola: getComputedStyle(document.documentElement).overflow !== 'hidden' }));
      if (r.vai || r.existe || r.inerte || !r.rola) mal(`${k}: intro desligada mas ${JSON.stringify(r)}`);
      else bem(`${k}: intro desligada; a 1.ª visita abre direta no site`);
      await c.close();
    }
  }
  if (comIntro) {
  for (const n of [1, 2, 3]) {
    const r = responder(PT + '/media/intro-' + n + '.webp');
    if (r.status !== 200 || r.headers['content-type'] !== 'image/webp') mal(`/media/intro-${n}.webp: ${r.status}`);
  }
  const conteudo = k => JSON.parse(fs.readFileSync(path.join(__dirname, 'conteudo', k + '.json'), 'utf8'));
  for (const [k, v] of Object.entries(LINGUAS)) {
    for (const largura of (k === 'pt' ? [390, 1280] : [390])) {
      const c = await contexto({ viewport: { width: largura, height: largura === 390 ? 844 : 720 } }, 'nao', true);
      const q = await c.newPage();
      const erros = []; q.on('pageerror', e => erros.push(e.message));
      const t0 = Date.now();
      await q.goto(v.url);
      const i = conteudo(k).intro, esperados = [i.saltar, i.p1, i.p2, ...i.legendas];
      const antes = await q.evaluate(() => ({ vai: document.documentElement.classList.contains('intro-vai'),
        mostra: getComputedStyle(document.getElementById('intro')).display === 'grid', guardado: sessionStorage.getItem('ps-intro'),
        inerte: [...document.body.children].filter(el => el.id !== 'intro' && el.tagName !== 'SCRIPT').every(el => el.hasAttribute('inert')),
        textos: [...document.querySelectorAll('#intro-rot1, #intro-rot2, .intro-legenda span, #intro-saltar')].map(e => e.textContent.trim()),
        slogan: document.querySelector('.intro-slogan').textContent.trim() }));
      avaliar(await q.evaluate(medir, '#intro'), `${k} ${largura}px: intro`);
      await q.waitForTimeout(1200);
      // a meio: as três fotografias já no palco, e o palco todo dentro do ecrã
      const meio = await q.evaluate(() => {
        const caixa = document.querySelector('.intro-palco').getBoundingClientRect();
        return { fotos: [...document.querySelectorAll('#intro image')].map(x => x.getAttribute('href')),
          dentro: caixa.top >= 0 && caixa.bottom <= innerHeight && caixa.left >= 0 && caixa.right <= innerWidth };
      });
      await q.waitForFunction(() => !document.documentElement.classList.contains('intro-vai'), null, { timeout: 8000 });
      const durou = Date.now() - t0;
      const depois = await q.evaluate(() => ({ inerte: document.querySelector('main').hasAttribute('inert'),
        escondida: getComputedStyle(document.getElementById('intro')).display === 'none', legenda: document.querySelector('.intro-legenda p.ativa').id }));
      await q.reload();
      const segunda = await q.evaluate(() => getComputedStyle(document.getElementById('intro')).display);
      const slogan = conteudo(k).og.slogan.join(' ').replace(/\*/g, '');
      const fotos = meio.fotos.join() === '/media/intro-1.webp,/media/intro-2.webp,/media/intro-3.webp';
      if (!antes.vai || !antes.mostra || antes.guardado !== '1' || !antes.inerte || antes.textos.join('|') !== esperados.join('|') || antes.slogan !== slogan
          || !fotos || !meio.dentro || durou < 4000 || depois.inerte || !depois.escondida || depois.legenda !== 'intro-l3' || segunda !== 'none' || erros.length)
        mal(`${k} ${largura}px, intro: ${JSON.stringify({ antes, meio, durou, depois, segunda, erros })}`);
      else bem(`${k} ${largura}px: intro na 1.ª visita (${(durou / 1000).toFixed(1)} s, 3 fotografias, textos certos, página inerte), sobe no fim e não volta ao recarregar`);
      await c.close();
    }
  }
  for (const modo of ['toque', 'Esc']) {
    const c = await contexto({ viewport: { width: 390, height: 844 } }, 'nao', true);
    const q = await c.newPage();
    await q.goto(LINGUAS.pt.url);
    const t0 = Date.now();
    if (modo === 'toque') await q.click('#intro-saltar'); else await q.keyboard.press('Escape');
    await q.waitForFunction(() => !document.documentElement.classList.contains('intro-vai'), null, { timeout: 3000 });
    const r = await q.evaluate(() => ({ inerte: document.querySelector('main').hasAttribute('inert'), guardado: sessionStorage.getItem('ps-intro'),
      escondida: getComputedStyle(document.getElementById('intro')).display === 'none' }));
    const durou = Date.now() - t0;
    if (r.inerte || r.guardado !== '1' || !r.escondida || durou > 1500) mal(`intro, ${modo}: ${JSON.stringify(r)} em ${durou} ms`);
    else bem(`intro: ${modo === 'toque' ? 'o botão «Saltar»' : 'a tecla Esc'} salta-a em ${durou} ms e a página volta a estar ativa`);
    await c.close();
  }
  {
    const c = await contexto({ viewport: { width: 390, height: 844 }, reducedMotion: 'reduce' }, 'nao', true);
    const q = await c.newPage();
    await q.goto(LINGUAS.ro.url);
    const r = await q.evaluate(() => ({ vai: document.documentElement.classList.contains('intro-vai'), mostra: getComputedStyle(document.getElementById('intro')).display,
      inerte: document.querySelector('main').hasAttribute('inert'), guardado: sessionStorage.getItem('ps-intro') }));
    if (r.vai || r.mostra !== 'none' || r.inerte || r.guardado) mal(`intro com movimento reduzido: ${JSON.stringify(r)}`);
    else bem('intro: com movimento reduzido não aparece e a página abre direta');
    await c.close();
  }
  }
  // ligação direta dos anúncios, na 1.ª visita: sem intro, diagnóstico aberto e utilizável; fechar limpa o #diagnostico
  // os links que estão nos anúncios da Meta (campanhas de outubro) e o #diagnostico do cartão
  const anuncio = (camp, cont) => `?utm_source=meta&utm_medium=paid&utm_campaign=${camp}&utm_content=${cont}`;
  for (const [lg, sufixo] of [['pt', '#diagnostico'], ['pt', anuncio('ps-pt-out26', 'diag-video-b')], ['en', anuncio('ps-en-out26', 'diag-video-b')],
                              ['ro', anuncio('ps-ro-out26', 'diag-video-b')], ['ro', '#diagnostico']]) {
    const c = await contexto({ viewport: { width: 390, height: 844 } }, 'nao', true);
    await c.addInitScript(() => { window.__gc = []; const stub = { count: o => window.__gc.push(o.path) };
      Object.defineProperty(window, 'goatcounter', { get: () => stub, set: () => {}, configurable: true }); });
    const q = await c.newPage();
    await q.goto(LINGUAS[lg].url.replace(/\/$/, '') + '/' + sufixo);
    await q.waitForTimeout(300);
    const r = await q.evaluate(() => ({ vai: document.documentElement.classList.contains('intro-vai'), lang: document.documentElement.lang,
      aberto: document.getElementById('diagnostico').open, comecar: !!document.getElementById('diag-in'),
      foto: !!document.querySelector('.diag-quem img'), gc: window.__gc.slice() }));
    let ok = !r.vai && r.aberto && r.comecar && r.foto && r.lang === LINGUAS[lg].lang && r.gc.includes('diagnostico/aberto');
    if (ok) { await q.fill('#diag-in', 'Teste Link'); await q.press('#diag-in', 'Enter'); await q.waitForTimeout(200);
      ok = await q.evaluate(() => window.__gc.includes('diagnostico/comecou') && window.__gc.includes('diagnostico/pergunta-02-negocio')); }
    if (ok) { await q.keyboard.press('Escape'); await q.waitForTimeout(100);
      ok = await q.evaluate(() => !document.getElementById('diagnostico').open && location.hash === ''); }
    if (!ok) mal(`ligação direta ao diagnóstico (${lg} ${sufixo}): ${JSON.stringify(r)}`);
    else bem(`${lg}: ${sufixo} abre o diagnóstico com a foto, o nome logo no 1.º ecrã; conta «aberto» e «começou» no GoatCounter; fechar limpa o endereço`);
    await c.close();
  }

  { // os anúncios de web design (utm_content=web-…) continuam a abrir o site, sem o diagnóstico
    const c = await contexto({ viewport: { width: 390, height: 844 } }, 'nao', true);
    const q = await c.newPage();
    await q.goto(RO + '/?utm_source=meta&utm_medium=paid-video&utm_campaign=ps-prospecao-out26-ro&utm_content=web-bolta');
    await q.waitForTimeout(300);
    const aberto = await q.evaluate(() => document.getElementById('diagnostico').open);
    if (aberto) mal('anúncio web-bolta abriu o diagnóstico'); else bem('ro: o anúncio web-bolta abre o site, sem o diagnóstico');
    await c.close();
  }

  // ——— 7. sem JavaScript: os separadores e os esquemas continuam a funcionar (:target) ———
  // movimento reduzido: sem o scroll suave, o Playwright não toca a meio do deslizar
  const ctx2 = await contexto({ viewport: { width: 390, height: 844 }, javaScriptEnabled: false, reducedMotion: 'reduce' }, 'nao', true);
  const p2 = await ctx2.newPage();
  await p2.goto(LINGUAS.pt.url + '#cazuri');
  const semJs = await p2.evaluate(() => [getComputedStyle(document.getElementById('cazuri')).display, getComputedStyle(document.getElementById('consultanta')).display, !document.getElementById('rgpd'), document.getElementById('intro') ? getComputedStyle(document.getElementById('intro')).display : 'none']);
  if (semJs[0] === 'none' || semJs[1] !== 'none' || !semJs[2] || semJs[3] !== 'none') mal('sem JavaScript: vistas, faixa de cookies ou intro erradas'); else bem('sem JavaScript: separadores funcionam (:target), a faixa de cookies e a intro não aparecem');
  // o esquema: abre-se a automação (<details> nativo), «Ver o esquema» mostra o cartão e o X volta à automação
  await p2.goto(LINGUAS.pt.url + '#automatizari');
  await p2.click('#a-lead summary');
  await p2.click('#a-lead .ver-esquema');
  const nj = await p2.evaluate(() => {
    const d = document.getElementById('esquema-lead'), cs = getComputedStyle(d), b = d.getBoundingClientRect();
    return { hash: location.hash, mostra: cs.display !== 'none' && cs.position === 'fixed',
      dentro: b.left >= 0 && b.top >= 0 && b.right <= innerWidth && b.bottom <= innerHeight,
      outros: [...document.querySelectorAll('dialog.esquema')].filter(x => x !== d && getComputedStyle(x).display !== 'none').length,
      vista: getComputedStyle(document.getElementById('automatizari')).display !== 'none' };
  });
  await p2.click('#esquema-lead .fechar');
  const nj2 = await p2.evaluate(() => ({ hash: location.hash, escondido: getComputedStyle(document.getElementById('esquema-lead')).display === 'none',
    aberta: document.getElementById('a-lead').open }));
  if (nj.hash !== '#esquema-lead' || !nj.mostra || !nj.dentro || nj.outros || !nj.vista || nj2.hash !== '#a-lead' || !nj2.escondido || !nj2.aberta)
    mal(`sem JavaScript, esquema: ${JSON.stringify(nj)} → ${JSON.stringify(nj2)}`);
  else bem('sem JavaScript: «Ver o esquema» mostra o cartão (:target) e o X volta à automação');
  await ctx2.close();

  // ——— cartaz grátis de avaliações (pachecost.com/cartaz, ro.pachecost.com/afis, pachecost.com/en/poster) ———
  console.log('\nCARTAZ GRÁTIS');
  {
    const ctx = await contexto();
    for (const [lg, sufixo] of [['pt', '/cartaz'], ['en', '/en/poster'], ['ro', '/afis']]) {
      const p = await ctx.newPage();
      await p.goto(LINGUAS[lg].url, { waitUntil: 'domcontentloaded' });
      const href = await p.evaluate(() => { const a = [...document.querySelectorAll('.rodape a')].find(x => /\/(cartaz|afis|poster)$/.test(x.getAttribute('href'))); return a && a.getAttribute('href'); });
      const r = href === sufixo ? responder(new URL(sufixo, LINGUAS[lg].url).href) : { status: 0 };
      let ok = r.status === 200 && /<title>[^<]*(avalia|review|recenz)/i.test(r.body.toString());
      if (ok) { await p.click(`.rodape a[href="${sufixo}"]`); await p.waitForLoadState('domcontentloaded');
        ok = await p.evaluate(l => document.documentElement.lang.startsWith(l === 'pt' ? 'pt' : l), lg); }
      if (!ok) mal(`${lg}: cartaz grátis no rodapé (${href} → ${r.status})`);
      else bem(`${lg}: o rodapé leva ao cartaz grátis em ${new URL(sufixo, LINGUAS[lg].url).href}`);
      await p.close();
    }
    await ctx.close();
  }

  await browser.close();
  console.log(falhas ? `\n${falhas} problema(s).` : '\n✓ Sem problemas.');
  process.exit(falhas ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
