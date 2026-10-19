(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const saveData = navigator.connection && navigator.connection.saveData;
  const L = document.documentElement.lang.startsWith('en') ? 'en' : 'pt';
  const WA = document.body.dataset.wa || '';

  /* ---------- Vídeo do hero: 16:9 ou 9:16 consoante a orientação ---------- */
  const video = $('#heroVideo');
  const pickOrientation = () => matchMedia('(orientation: portrait)').matches ? 'portrait' : 'landscape';
  let loadedFor = null;
  function loadHero() {
    if (!video || reduced || saveData) { if (video) video.classList.add('is-missing'); return; }
    const o = pickOrientation(); if (o === loadedFor) return; loadedFor = o;
    const k = o === 'portrait' ? 'Portrait' : 'Landscape';
    video.innerHTML = '';
    if (video.dataset['poster' + k]) video.poster = video.dataset['poster' + k];
    const webm = video.dataset['webm' + k], mp4 = video.dataset['src' + k];
    if (webm) { const s = document.createElement('source'); s.src = webm; s.type = 'video/webm'; video.appendChild(s); }
    if (mp4) { const s = document.createElement('source'); s.src = mp4; s.type = 'video/mp4'; video.appendChild(s); }
    video.classList.remove('is-missing', 'is-ready');
    video.load(); video.play().catch(() => {});
    const last = video.querySelector('source:last-child'); if (last) last.addEventListener('error', () => video.classList.add('is-missing'));
  }
  if (video) {
    video.addEventListener('canplay', () => video.classList.add('is-ready'));
    loadHero();
    matchMedia('(orientation: portrait)').addEventListener('change', loadHero);
    new IntersectionObserver(en => en.forEach(e => { if (video.classList.contains('is-ready')) e.isIntersecting ? video.play().catch(() => {}) : video.pause(); })).observe(video);
  }

  /* ---------- Imagens: real vs. placeholder ---------- */
  $$('.media img').forEach(img => {
    const ok = () => img.closest('.media').classList.add('is-real');
    img.addEventListener('load', ok); if (img.complete && img.naturalWidth) ok();
    img.addEventListener('error', () => img.classList.add('is-missing'));
  });

  /* ---------- Header ---------- */
  const header = $('#header');
  const onScroll = () => header && header.classList.toggle('is-scrolled', scrollY > 40);
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  const sheet = $('#sheet'), burger = $('.burger');
  if (sheet && burger) {
    const openSheet = o => { sheet.classList.toggle('is-open', o); sheet.setAttribute('aria-hidden', String(!o)); burger.setAttribute('aria-expanded', String(o)); document.body.style.overflow = o ? 'hidden' : ''; if (o) $('.sheet .close').focus(); else burger.focus(); };
    burger.addEventListener('click', () => openSheet(true));
    $('.sheet .close').addEventListener('click', () => openSheet(false));
    $$('.sheet nav a').forEach(a => a.addEventListener('click', () => openSheet(false)));
    addEventListener('keydown', e => { if (e.key === 'Escape' && sheet.classList.contains('is-open')) openSheet(false); });
  }

  /* ---------- "Hoje": aberto/fechado em hora de Lisboa, sem rede. Todos os dias 10–23 ---------- */
  const OPEN = 10, CLOSE = 23;
  function nowLisbon() {
    const p = new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/Lisbon', weekday: 'short', hour: '2-digit', minute: '2-digit', hour12: false }).formatToParts(new Date());
    const get = t => p.find(x => x.type === t).value;
    return { wd: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].indexOf(get('weekday')), h: +get('hour') % 24, m: +get('minute') };
  }
  function renderStatus() {
    const { wd, h, m } = nowLisbon(); const t = h + m / 60;
    let text, open = false;
    if (t < OPEN) text = L === 'en' ? `Closed · we open today at ${OPEN}:00` : `Fechado · abrimos hoje às ${OPEN}:00`;
    else if (t < CLOSE) { open = true; const left = CLOSE - t; text = left <= 1 ? (L === 'en' ? `Open · closing at ${CLOSE}:00` : `Aberto · fechamos às ${CLOSE}:00`) : (L === 'en' ? `Open now · until ${CLOSE}:00` : `Aberto agora · até às ${CLOSE}:00`); }
    else text = L === 'en' ? `Closed · we open tomorrow at ${OPEN}:00` : `Fechado · abrimos amanhã às ${OPEN}:00`;
    $$('.js-status').forEach(s => { s.classList.toggle('is-open', open); s.classList.toggle('is-closed', !open); });
    $$('.js-status-text').forEach(s => s.textContent = text);
    $$('.hours li').forEach(li => li.classList.toggle('is-today', +li.dataset.day === wd));
    $$('.js-year').forEach(y => y.textContent = new Date().getFullYear());
  }
  renderStatus(); setInterval(renderStatus, 60000);

  /* ---------- Reserva por WhatsApp: mensagem pré-preenchida ---------- */
  const form = $('#bookForm');
  if (form) {
    const d = $('#bDate'); if (d) { const t = new Date(); d.min = t.toISOString().slice(0, 10); if (!d.value) d.value = d.min; }
    form.addEventListener('submit', e => {
      e.preventDefault();
      if (!form.reportValidity()) return;
      const data = new FormData(form);
      const dt = new Date(data.get('data') + 'T12:00:00');
      const when = new Intl.DateTimeFormat(L === 'en' ? 'en-GB' : 'pt-PT', { weekday: 'long', day: 'numeric', month: 'long' }).format(dt);
      const msg = L === 'en'
        ? `Hello! I'd like to book a table at Olá Kathmandu for ${data.get('pessoas')} people on ${when} at ${data.get('hora')}. Name: ${data.get('nome')}. Thank you!`
        : `Olá! Queria reservar uma mesa no Olá Kathmandu para ${data.get('pessoas')} pessoas, ${when}, às ${data.get('hora')}. Nome: ${data.get('nome')}. Obrigado!`;
      open(`https://wa.me/${WA}?text=${encodeURIComponent(msg)}`, '_blank', 'noopener');
    });
  }

  /* ---------- Carta: filtros de alergénios e navegação por secção ---------- */
  const filters = $$('.filters .chip');
  if (filters.length) {
    const apply = () => {
      const on = filters.filter(c => c.getAttribute('aria-pressed') === 'true').map(c => c.dataset.f);
      $$('.dish').forEach(d => {
        const tags = (d.dataset.tags || '').split(' ').filter(Boolean);
        let dim = false;
        on.forEach(f => { if (f === 'veg') { if (!tags.includes('veg')) dim = true; } else if (tags.includes(f)) dim = true; });
        d.classList.toggle('is-dim', dim);
      });
    };
    filters.forEach(c => c.addEventListener('click', () => { c.setAttribute('aria-pressed', c.getAttribute('aria-pressed') === 'true' ? 'false' : 'true'); apply(); }));
  }
  const mnav = $$('.menu-nav a');
  if (mnav.length) {
    const secs = mnav.map(a => $(a.getAttribute('href'))).filter(Boolean);
    const mio = new IntersectionObserver(en => en.forEach(e => { if (e.isIntersecting) mnav.forEach(a => a.classList.toggle('is-active', a.getAttribute('href') === '#' + e.target.id)); }), { rootMargin: '-40% 0px -55% 0px' });
    secs.forEach(sct => mio.observe(sct));
  }

  /* ---------- Cesto de take-away: pedido escrito no WhatsApp (nada sai sem o cliente) ---------- */
  const basket = $('#basket');
  if (basket) {
    const items = new Map(); // id -> {name, price (cêntimos|null), qty}
    const fmt = c => (c / 100).toFixed(2).replace('.', ',') + ' €';
    const parsePrice = s => { const m = (s || '').match(/(\d+)[,.](\d{2})/); return m ? +m[1] * 100 + +m[2] : null; };
    const list = $('.basket-list ul', basket), count = $('.js-count', basket), total = $('.js-total', basket), send = $('.js-send', basket);
    const T = L === 'en'
      ? { one: 'item', many: 'items', tbc: 'price on the menu', open: 'Hello! I would like to order for take-away:', end: 'Pick-up time: ', name: 'Name: ', note: 'Prices to confirm by phone where missing.', extra: 'Some items have no price online' }
      : { one: 'item', many: 'itens', tbc: 'preço na carta', open: 'Olá! Queria encomendar para take-away:', end: 'Hora de recolha: ', name: 'Nome: ', note: 'Preços a confirmar por telefone onde faltam.', extra: 'Alguns itens sem preço online' };
    function render() {
      let n = 0, sum = 0, missing = false; list.innerHTML = '';
      items.forEach((it, id) => {
        n += it.qty; if (it.price == null) missing = true; else sum += it.price * it.qty;
        const li = document.createElement('li');
        li.innerHTML = `<span>${it.name}</span><span class="qty"><button type="button" data-d="-1" aria-label="−"><svg><use href="#i-minus"/></svg></button><span class="num">${it.qty}</span><button type="button" data-d="1" aria-label="+"><svg><use href="#i-plus"/></svg></button></span><span class="p">${it.price == null ? '<small>' + T.tbc + '</small>' : fmt(it.price * it.qty)}</span>`;
        $$('button', li).forEach(b => b.addEventListener('click', () => change(id, it.name, it.price, +b.dataset.d)));
        list.appendChild(li);
      });
      count.textContent = `${n} ${n === 1 ? T.one : T.many}`;
      total.textContent = fmt(sum) + (missing ? ' +' : '');
      $('.js-extra', basket).textContent = missing ? T.extra : '';
      basket.classList.toggle('is-on', n > 0); document.body.classList.toggle('has-basket', n > 0);
      if (!n) basket.classList.remove('is-expanded');
      $$('.dish').forEach(d => { const b = $('.add', d); if (b) b.classList.toggle('is-on', items.has(d.dataset.id)); });
    }
    function change(id, name, price, delta) {
      const cur = items.get(id) || { name, price, qty: 0 }; cur.qty += delta;
      if (cur.qty <= 0) items.delete(id); else items.set(id, cur);
      render();
    }
    $$('.dish').forEach(d => {
      const b = $('.add', d); if (!b) return;
      b.addEventListener('click', () => change(d.dataset.id, $('.name', d).childNodes[0].textContent.trim(), parsePrice($('.price', d) && $('.price', d).textContent), 1));
    });
    $('.js-toggle', basket).addEventListener('click', () => basket.classList.toggle('is-expanded'));
    send.addEventListener('click', () => {
      const lines = []; let sum = 0, missing = false;
      items.forEach(it => { lines.push(`• ${it.qty}× ${it.name}${it.price == null ? ' (' + T.tbc + ')' : ' · ' + fmt(it.price * it.qty)}`); if (it.price == null) missing = true; else sum += it.price * it.qty; });
      const msg = `${T.open}\n${lines.join('\n')}\n${L === 'en' ? 'Total' : 'Total'}: ${fmt(sum)}${missing ? ' + ' + T.tbc : ''}\n${T.end}____\n${T.name}____`;
      open(`https://wa.me/${WA}?text=${encodeURIComponent(msg)}`, '_blank', 'noopener');
    });
  }

  /* ---------- Galeria: lightbox ---------- */
  const lb = $('#lightbox');
  if (lb) {
    const img = $('img', lb), cap = $('.cap', lb);
    const close = () => { lb.classList.remove('is-open'); document.body.style.overflow = ''; };
    $$('.gallery .g').forEach(g => g.addEventListener('click', () => {
      const src = $('img', g); if (!src || src.classList.contains('is-missing')) return;
      img.src = src.currentSrc || src.src; img.alt = src.alt; cap.textContent = src.alt; lb.classList.add('is-open'); document.body.style.overflow = 'hidden';
    }));
    $('.close', lb).addEventListener('click', close);
    lb.addEventListener('click', e => { if (e.target === lb) close(); });
    addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
    $$('.gtabs .chip').forEach(c => c.addEventListener('click', () => {
      $$('.gtabs .chip').forEach(x => x.setAttribute('aria-pressed', 'false')); c.setAttribute('aria-pressed', 'true');
      $$('.gallery .g').forEach(g => g.style.display = (c.dataset.f === 'all' || g.dataset.cat === c.dataset.f) ? '' : 'none');
    }));
  }

  /* ---------- Mapa: só carrega com consentimento ---------- */
  const mapBox = $('.map-embed');
  if (mapBox) $('.consent button', mapBox).addEventListener('click', () => { const f = document.createElement('iframe'); f.src = mapBox.dataset.src; f.loading = 'lazy'; f.referrerPolicy = 'no-referrer-when-downgrade'; f.title = 'Google Maps'; mapBox.appendChild(f); mapBox.classList.add('is-on'); });

  /* ---------- Grupos: pedido por WhatsApp ---------- */
  const ev = $('#groupForm');
  if (ev) {
    $('.js-ev-wa', ev).addEventListener('click', () => {
      const d = new FormData(ev);
      const msg = L === 'en'
        ? `Hello! I'd like to book for a group at Olá Kathmandu: ${d.get('pessoas') || '?'} people, ${d.get('data') || 'date to be set'}. ${d.get('mensagem') || ''} Name: ${d.get('nome') || ''}.`
        : `Olá! Queria reservar para um grupo no Olá Kathmandu: ${d.get('pessoas') || '?'} pessoas, ${d.get('data') || 'data a combinar'}. ${d.get('mensagem') || ''} Nome: ${d.get('nome') || ''}.`;
      open(`https://wa.me/${WA}?text=${encodeURIComponent(msg)}`, '_blank', 'noopener');
    });
  }

  /* ---------- Reveal ---------- */
  const io = new IntersectionObserver(entries => entries.forEach(en => { if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); } }), { rootMargin: '0px 0px -8% 0px' });
  $$('.reveal').forEach(el => io.observe(el));
  const heroEl = $('.hero'); if (heroEl) requestAnimationFrame(() => requestAnimationFrame(() => heroEl.classList.add('is-in')));
  $$('.page-hero').forEach(p => requestAnimationFrame(() => p.classList.add('is-in')));
})();
