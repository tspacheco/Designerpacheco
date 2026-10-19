(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const saveData = navigator.connection && navigator.connection.saveData;

  /* ---------- Cortina de azulejos (entrada): 48 ou 60 peças com atraso em diagonal ---------- */
  const curtain = $('.curtain');
  if (curtain && !reduced) {
    const cols = innerWidth >= 768 ? 10 : 6, rows = innerWidth >= 768 ? 6 : 8;
    const frag = document.createDocumentFragment();
    for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) { const i = document.createElement('i'); i.style.setProperty('--d', String(r + c)); frag.appendChild(i); }
    curtain.appendChild(frag);
  } else if (curtain) { curtain.remove(); }

  /* ---------- Vídeo do hero: 16:9 ou 9:16 consoante a orientação; nunca com reduced-motion / Save-Data ---------- */
  const video = $('#heroVideo');
  const pickOrientation = () => matchMedia('(orientation: portrait)').matches ? 'portrait' : 'landscape';
  let loadedFor = null;
  function loadHero() {
    if (!video || reduced || saveData) { if (video) video.classList.add('is-missing'); return; }
    const o = pickOrientation(); if (o === loadedFor) return; loadedFor = o;
    video.innerHTML = '';
    const poster = video.dataset['poster' + (o === 'portrait' ? 'Portrait' : 'Landscape')];
    if (poster) video.poster = poster;
    const webm = video.dataset['webm' + (o === 'portrait' ? 'Portrait' : 'Landscape')];
    const mp4 = video.dataset['src' + (o === 'portrait' ? 'Portrait' : 'Landscape')];
    if (webm) { const s = document.createElement('source'); s.src = webm; s.type = 'video/webm'; video.appendChild(s); }
    if (mp4) { const s = document.createElement('source'); s.src = mp4; s.type = 'video/mp4'; video.appendChild(s); }
    video.classList.remove('is-missing', 'is-ready');
    video.load();
    video.play().catch(() => {});
  }
  if (video) {
    video.addEventListener('canplay', () => video.classList.add('is-ready'));
    // Se nenhuma source carregar, o placeholder fica (sem flash, sem ícone partido)
    video.addEventListener('error', () => video.classList.add('is-missing'), true);
    video.addEventListener('loadedmetadata', () => { /* poster já visível; vídeo faz fade-in no canplay */ });
    const lastSource = () => video.querySelector('source:last-child');
    video.addEventListener('DOMNodeInserted', () => {}, { once: true });
    loadHero();
    matchMedia('(orientation: portrait)').addEventListener('change', loadHero);
    // Pausa fora do ecrã (poupa bateria)
    new IntersectionObserver(en => en.forEach(e => { if (video.classList.contains('is-ready')) e.isIntersecting ? video.play().catch(() => {}) : video.pause(); })).observe(video);
    // Fonte final falhou: esconder
    setTimeout(() => { const s = lastSource(); if (s) s.addEventListener('error', () => video.classList.add('is-missing')); }, 0);
  }

  /* ---------- Imagens em falta: deixar o placeholder SVG ---------- */
  document.addEventListener('error', e => { const t = e.target; if (t.matches && t.matches('.media img')) t.classList.add('is-missing'); }, true);

  /* ---------- Header ---------- */
  const header = $('#header');
  const onScroll = () => header.classList.toggle('is-scrolled', scrollY > 40);
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  const sheet = $('#sheet'), burger = $('.burger');
  const L = document.documentElement.lang === 'en' ? 'en' : 'ro';
  const openSheet = o => { sheet.classList.toggle('is-open', o); sheet.setAttribute('aria-hidden', String(!o)); burger.setAttribute('aria-expanded', String(o)); document.body.style.overflow = o ? 'hidden' : ''; if (o) $('.sheet .close').focus(); else burger.focus(); };
  burger.addEventListener('click', () => openSheet(true));
  $('.sheet .close').addEventListener('click', () => openSheet(false));
  $$('.sheet nav a').forEach(a => a.addEventListener('click', () => openSheet(false)));
  addEventListener('keydown', e => { if (e.key === 'Escape' && sheet.classList.contains('is-open')) openSheet(false); });

  /* ---------- "Astăzi": aberto/fechado em hora de Iași (Europe/Bucharest), sem rede ---------- */
  const HOURS = { 0: [12, 20], 1: null, 2: [12, 22], 3: [12, 22], 4: [12, 22], 5: [12, 22], 6: [12, 22] }; // 0 = duminică
  const RO_DAYS = ['duminică', 'luni', 'marți', 'miercuri', 'joi', 'vineri', 'sâmbătă'];
  function nowInIasi() {
    const p = new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/Bucharest', weekday: 'short', hour: '2-digit', minute: '2-digit', hour12: false }).formatToParts(new Date());
    const get = t => p.find(x => x.type === t).value;
    const wd = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].indexOf(get('weekday'));
    return { wd, h: +get('hour') % 24, m: +get('minute') };
  }
  function renderStatus() {
    const { wd, h, m } = nowInIasi(); const t = h + m / 60; const today = HOURS[wd];
    let text, open = false;
    const EN_DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    const DAYS = L === 'en' ? EN_DAYS : RO_DAYS;
    if (!today) { text = L === 'en' ? 'Closed on Mondays · we open Tuesday at 12:00' : 'Luni închis · deschidem marți la 12:00'; }
    else if (t < today[0]) { text = L === 'en' ? `Opening today at ${today[0]}:00` : `Deschidem azi la ${today[0]}:00`; }
    else if (t < today[1]) { open = true; text = L === 'en' ? `Open now · until ${today[1]}:00` : `Deschis acum · până la ${today[1]}:00`; }
    else { let n = (wd + 1) % 7; while (!HOURS[n]) n = (n + 1) % 7; const tm = n === (wd + 1) % 7; text = L === 'en' ? `Closed now · we open ${tm ? 'tomorrow' : DAYS[n]} at ${HOURS[n][0]}:00` : `Închis acum · deschidem ${tm ? 'mâine' : DAYS[n]} la ${HOURS[n][0]}:00`; }
    $$('.hours li').forEach(li => li.classList.toggle('is-today', +li.dataset.day === wd));
    $$('.js-status').forEach(el => { el.classList.toggle('is-closed', !open); $('.js-status-text', el).textContent = text; });
  }
  renderStatus(); setInterval(renderStatus, 60000);
  $$('.js-year').forEach(el => el.textContent = new Date().getFullYear());

  /* ---------- Reserva por WhatsApp: mensagem pré-preenchida ---------- */
  const form = $('#bookForm');
  if (form) {
    const d = $('#bDate'); const today = new Date(); d.min = today.toISOString().slice(0, 10);
    const dflt = new Date(today); dflt.setDate(dflt.getDate() + 1); d.value = dflt.toISOString().slice(0, 10);
    form.addEventListener('submit', e => {
      e.preventDefault();
      if (!form.reportValidity()) return;
      const data = new FormData(form);
      const dt = new Date(data.get('data') + 'T12:00:00');
      const when = new Intl.DateTimeFormat(L === 'en' ? 'en-GB' : 'ro-RO', { weekday: 'long', day: 'numeric', month: 'long' }).format(dt);
      const msg = L === 'en'
        ? `Hello! I'd like to book a table at Andalu for ${data.get('persoane')} people on ${when} at ${data.get('ora')}. Name: ${data.get('nume')}. Thank you!`
        : `Bună! Aș vrea să rezerv o masă la Andalu pentru ${data.get('persoane')} persoane, ${when}, la ${data.get('ora')}. Numele: ${data.get('nume')}. Mulțumesc!`;
      open(`https://wa.me/40752803443?text=${encodeURIComponent(msg)}`, '_blank', 'noopener');
    });
  }

  /* ---------- Menu: filtros de alergénios e navegação por secção ---------- */
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

  /* ---------- Mapa: só carrega com consentimento (sem cookies do Google antes do clique) ---------- */
  const mapBox = $('.map-embed');
  if (mapBox) $('.consent button', mapBox).addEventListener('click', () => { const f = document.createElement('iframe'); f.src = mapBox.dataset.src; f.loading = 'lazy'; f.referrerPolicy = 'no-referrer-when-downgrade'; f.title = 'Google Maps'; mapBox.appendChild(f); mapBox.classList.add('is-on'); });

  /* ---------- Evento: pedido por WhatsApp (botão secundário) ---------- */
  const ev = $('#eventForm');
  if (ev) {
    $('.js-ev-wa', ev).addEventListener('click', () => {
      const d = new FormData(ev);
      const msg = L === 'en'
        ? `Hello! I'd like a quote for an event at Andalu: ${d.get('tip') || 'event'}, ${d.get('persoane') || '?'} people, ${d.get('data') || 'date to be set'}. ${d.get('mesaj') || ''} Name: ${d.get('nume') || ''}.`
        : `Bună! Aș vrea o ofertă pentru un eveniment la Andalu: ${d.get('tip') || 'eveniment'}, ${d.get('persoane') || '?'} persoane, ${d.get('data') || 'data de stabilit'}. ${d.get('mesaj') || ''} Numele: ${d.get('nume') || ''}.`;
      open(`https://wa.me/40752803443?text=${encodeURIComponent(msg)}`, '_blank', 'noopener');
    });
  }

  /* ---------- Reveal ---------- */
  const io = new IntersectionObserver(entries => entries.forEach(en => { if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); } }), { rootMargin: '0px 0px -8% 0px' });
  $$('.reveal').forEach(el => io.observe(el));
  const heroEl = $('.hero'); if (heroEl) requestAnimationFrame(() => requestAnimationFrame(() => heroEl.classList.add('is-in')));
  // Depois da cortina: remover do DOM (não bloqueia nada, mas limpa)
  if (curtain) setTimeout(() => curtain.remove(), 2600);
})();
