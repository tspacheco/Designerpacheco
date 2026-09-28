/* Casa Bolta Rece — comportamentos partilhados (nav, revelação, herói, cards, galeria) */
(function () {
  "use strict";
  var reduzido = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var pointerFino = window.matchMedia("(hover: hover) and (pointer: fine)").matches;

  /* nav: fundo sólido ao rolar */
  var nav = document.querySelector(".nav");
  function aoRolar() { if (nav) nav.classList.toggle("scrolled", window.scrollY > 24); }
  window.addEventListener("scroll", aoRolar, { passive: true });
  aoRolar();

  /* burger + menu de ecrã inteiro */
  var burger = document.querySelector(".burger");
  var menu = document.getElementById("menu");
  function abrirMenu(aberto) {
    if (!burger || !menu) return;
    burger.setAttribute("aria-expanded", aberto ? "true" : "false");
    burger.setAttribute("aria-label", aberto ? "Închide meniul" : "Deschide meniul");
    menu.classList.toggle("open", aberto);
    document.documentElement.style.overflow = aberto ? "hidden" : "";
  }
  if (burger && menu) {
    burger.addEventListener("click", function () { abrirMenu(burger.getAttribute("aria-expanded") !== "true"); });
    menu.querySelectorAll("a").forEach(function (a) { a.addEventListener("click", function () { abrirMenu(false); }); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") abrirMenu(false); });
  }

  /* revelação no scroll */
  var io = new IntersectionObserver(function (entradas) {
    entradas.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add("is-in"); io.unobserve(e.target); }
    });
  }, { rootMargin: "0px 0px -10% 0px", threshold: 0.12 });
  document.querySelectorAll(".rv, .feluri, .poezie").forEach(function (el) { io.observe(el); });

  /* herói: coreografia de entrada + parallax da fotografia */
  var hero = document.querySelector(".hero");
  if (hero) {
    var foto = hero.querySelector(".hero__photo img");
    var entrar = function () { hero.classList.add("is-in"); };
    if (document.getElementById("cb-intro")) {
      window.addEventListener("cb-intro:done", entrar, { once: true });
      setTimeout(entrar, 9000); // rede de segurança
    } else {
      requestAnimationFrame(function () { requestAnimationFrame(entrar); });
    }
    if (foto && !reduzido) {
      var agendado = false;
      var parallax = function () {
        agendado = false;
        var y = Math.min(window.scrollY, window.innerHeight);
        foto.style.setProperty("--py", (y * 0.22) + "px");
      };
      window.addEventListener("scroll", function () {
        if (!agendado) { agendado = true; requestAnimationFrame(parallax); }
      }, { passive: true });
    }
  }

  /* poveste: percurso horizontal comandado pelo scroll vertical (masa → vin → vers) */
  var pov = document.querySelector(".poveste");
  if (pov && !reduzido) {
    var stage = pov.querySelector(".poveste__stage"), track = pov.querySelector(".poveste__track");
    var paineis = Array.prototype.slice.call(pov.querySelectorAll(".poveste__panel"));
    var imagens = paineis.map(function (p) { return p.querySelector(".poveste__img"); });
    var caps = Array.prototype.slice.call(pov.querySelectorAll(".poveste__cap"));
    var passos = Array.prototype.slice.call(pov.querySelectorAll(".poveste__nav li"));
    var navP = pov.querySelector(".poveste__nav");
    var n = paineis.length, PAUSA = 0.15, DESLIZE = (1 - n * PAUSA) / (n - 1);
    var alvo = 0, pos = 0, maxX = 0, visivel = false, aCorrer = false, ultimo = 0, idxAtual = -1;
    var suave = function (x) { return x * x * (3 - 2 * x); };
    var curva = function (p) {                       // 0..1 → posição 0..n-1, com paragem em cada capítulo
      for (var k = 0; k < n - 1; k++) {
        var ini = PAUSA * (k + 1) + DESLIZE * k, fim = ini + DESLIZE;
        if (p < ini) return k;
        if (p < fim) return k + suave((p - ini) / DESLIZE);
      }
      return n - 1;
    };
    var medir = function () { maxX = track.clientWidth * (n - 1); };
    var aplicar = function () {
      track.style.transform = "translate3d(" + (-pos / (n - 1) * maxX).toFixed(2) + "px,0,0)";
      imagens.forEach(function (img, i) { img.style.setProperty("--px", ((pos - i) * 8).toFixed(2) + "%"); });   // a foto anda mais devagar do que a moldura
      var idx = Math.round(pos);
      if (idx !== idxAtual) {
        idxAtual = idx;
        caps.forEach(function (c, i) { c.classList.toggle("on", i === idx); });
        passos.forEach(function (li, i) { li.classList.toggle("on", i === idx); });
      }
    };
    var ciclo = function (t) {
      if (!visivel) { aCorrer = false; return; }
      var dt = Math.min(0.05, (t - ultimo) / 1000 || 0.016); ultimo = t;
      var destino = curva(alvo);
      pos += (destino - pos) * Math.min(1, dt * 7);
      if (Math.abs(destino - pos) < 0.0005) pos = destino;
      aplicar();
      if (pos === destino) { aCorrer = false; return; }   // parado: nada a animar até ao próximo scroll
      requestAnimationFrame(ciclo);
    };
    var acordar = function () {
      if (visivel && !aCorrer) { aCorrer = true; ultimo = performance.now(); requestAnimationFrame(ciclo); }
    };
    var aoScroll = function () {
      var r = pov.getBoundingClientRect(), total = r.height - stage.offsetHeight;
      alvo = total > 0 ? Math.min(1, Math.max(0, -r.top / total)) : 0;
      if (navP) navP.style.setProperty("--p", alvo.toFixed(3));   // a linha segue o scroll; os painéis têm as pausas
      acordar();
    };
    new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        var antes = visivel; visivel = e.isIntersecting;
        if (visivel && !antes) { medir(); aoScroll(); pos = curva(alvo); aplicar(); acordar(); }   // entra já no sítio certo
      });
    }, { rootMargin: "10% 0px" }).observe(pov);
    window.addEventListener("scroll", aoScroll, { passive: true });
    window.addEventListener("resize", function () { medir(); aoScroll(); aplicar(); });
    /* foco por teclado numa legenda escondida: leva o scroll até ao capítulo dela */
    pov.addEventListener("focusin", function (e) {
      var i = caps.indexOf(e.target.closest(".poveste__cap"));
      if (i < 0 || i === idxAtual) return;
      var meio = PAUSA * (i + 0.5) + DESLIZE * i;
      window.scrollTo({ top: pov.offsetTop + meio * (pov.offsetHeight - stage.offsetHeight), behavior: "instant" });
    });
    medir(); aoScroll(); pos = curva(alvo); aplicar();
  }

  /* cards: inclinação 3D e felinar que segue o cursor */
  if (pointerFino && !reduzido) {
    document.querySelectorAll(".card").forEach(function (card) {
      card.addEventListener("pointermove", function (e) {
        var r = card.getBoundingClientRect();
        var px = (e.clientX - r.left) / r.width, py = (e.clientY - r.top) / r.height;
        card.style.setProperty("--ry", ((px - 0.5) * 12).toFixed(2) + "deg");
        card.style.setProperty("--rx", ((0.5 - py) * 10).toFixed(2) + "deg");
        card.style.setProperty("--gx", (px * 100).toFixed(1) + "%");
        card.style.setProperty("--gy", (py * 100).toFixed(1) + "%");
      });
      card.addEventListener("pointerleave", function () {
        card.style.setProperty("--rx", "0deg"); card.style.setProperty("--ry", "0deg");
      });
    });
  }

  /* galeria: caixa de luz */
  var galerias = document.querySelectorAll(".galerie");
  var lb = document.getElementById("lightbox");
  if (galerias.length && lb && lb.showModal) {
    var botoes = Array.prototype.slice.call(document.querySelectorAll(".galerie button"));
    var img = lb.querySelector("img"), atual = 0;
    var mostrar = function (i) {
      atual = (i + botoes.length) % botoes.length;
      var src = botoes[atual].querySelector("img");
      img.src = src.getAttribute("data-full") || src.src; img.alt = src.alt;
    };
    botoes.forEach(function (b, i) { b.addEventListener("click", function () { mostrar(i); lb.showModal(); }); });
    lb.querySelector("[data-prev]").addEventListener("click", function () { mostrar(atual - 1); });
    lb.querySelector("[data-next]").addEventListener("click", function () { mostrar(atual + 1); });
    lb.querySelector("[data-close]").addEventListener("click", function () { lb.close(); });
    lb.addEventListener("click", function (e) { if (e.target === lb) lb.close(); });
    document.addEventListener("keydown", function (e) {
      if (!lb.open) return;
      if (e.key === "ArrowRight") mostrar(atual + 1);
      if (e.key === "ArrowLeft") mostrar(atual - 1);
    });
  }

  /* formulário: só feedback local (envio via Netlify Forms quando alojado lá) */
  var form = document.querySelector("form.form");
  if (form && !form.hasAttribute("data-netlify")) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var ok = form.querySelector(".form__ok");
      if (ok) ok.hidden = false;
    });
  }

  var ano = document.getElementById("ano");
  if (ano) ano.textContent = new Date().getFullYear();
})();
