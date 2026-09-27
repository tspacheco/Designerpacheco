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
