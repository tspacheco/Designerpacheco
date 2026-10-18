/* TopCopias · hero imersivo
   Si existen los vídeos del hero (assets/media/hero-*.mp4) se usa el vídeo: horizontal en pantallas
   anchas y vertical en móvil. Mientras no existan, un canvas dibuja hojas que vuelan y se apilan. */
(function () {
  "use strict";
  var hero = document.querySelector(".hero-inm");
  if (!hero) return;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Vídeo ---------- */
  var video = hero.querySelector("video");
  if (video) {
    var vertical = function () { return window.matchMedia("(max-width: 880px)").matches; };
    var elegir = function () {
      var src = vertical() ? video.dataset.vertical : video.dataset.horizontal;
      var pos = vertical() ? video.dataset.posterVertical : video.dataset.posterHorizontal;
      if (pos && video.poster !== pos) video.poster = pos;
      if (src && video.getAttribute("src") !== src) { video.setAttribute("src", src); if (!reduce) video.play().catch(function () {}); }
    };
    elegir();
    var t; window.addEventListener("resize", function () { clearTimeout(t); t = setTimeout(elegir, 250); });
    if (reduce) video.removeAttribute("autoplay");
    return;
  }

  /* ---------- Canvas: hojas al vuelo ---------- */
  var cv = hero.querySelector("canvas.hojas");
  if (!cv) return;
  var ctx = cv.getContext("2d"), W, H, dpr, hojas = [], T0 = performance.now();
  var TINTAS = ["#E2007A", "#0094D4", "#FFD21F"];
  var N = 34, CICLO = 10.5;

  function rnd(a, b) { return a + Math.random() * (b - a); }
  function bez(a, b, c, d, t) { var u = 1 - t; return u * u * u * a + 3 * u * u * t * b + 3 * u * t * t * c + t * t * t * d; }
  function suave(t) { return t < 0 ? 0 : t > 1 ? 1 : t * t * (3 - 2 * t); }

  function medir() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = cv.clientWidth; H = cv.clientHeight;
    cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    crear();
  }

  function crear() {
    var movil = W / H < 0.9;
    var s = Math.min(W, H) * (movil ? 0.26 : 0.2);
    var tx = movil ? W * 0.5 : W * 0.76, ty = movil ? H * 0.84 : H * 0.66;
    hojas = [];
    for (var i = 0; i < N; i++) {
      var lado = Math.random() < 0.5 ? -1 : 1;
      hojas.push({
        w: s, h: s * 1.414,
        x0: tx + lado * rnd(W * 0.35, W * 0.7), y0: rnd(-H * 0.4, H * 0.3),
        c1x: rnd(0, W), c1y: rnd(-H * 0.2, H * 0.6), c2x: tx + rnd(-W * 0.3, W * 0.3), c2y: rnd(0, H * 0.5),
        tx: tx + rnd(-3, 3), ty: ty - i * Math.max(1.6, s * 0.012),
        r0: rnd(-4, 4), rf: rnd(-0.03, 0.03), giros: rnd(1, 3),
        d: 0.05 * i + rnd(0, 0.4), dur: rnd(2.6, 3.4),
        sx: rnd(-1, 1) * W * 0.8, sy: rnd(-H * 0.9, -H * 0.4),
        tinta: Math.random() < 0.22 ? TINTAS[i % 3] : null, lineas: 6 + (i % 5)
      });
    }
  }

  function dibujarHoja(o, x, y, rot, esc, alpha) {
    ctx.save(); ctx.globalAlpha = alpha; ctx.translate(x, y); ctx.rotate(rot); ctx.scale(1, esc);
    var w = o.w, h = o.h;
    ctx.shadowColor = "rgba(20,22,25,.16)"; ctx.shadowBlur = 14; ctx.shadowOffsetY = 6;
    ctx.fillStyle = "#fff"; ctx.fillRect(-w / 2, -h / 2, w, h);
    ctx.shadowColor = "transparent";
    ctx.strokeStyle = "rgba(20,22,25,.08)"; ctx.lineWidth = 1; ctx.strokeRect(-w / 2, -h / 2, w, h);
    ctx.fillStyle = "rgba(20,22,25,.12)";
    for (var l = 0; l < o.lineas; l++) ctx.fillRect(-w * 0.36, -h * 0.38 + l * h * 0.075, w * (l % 3 === 2 ? 0.45 : 0.72), Math.max(1, h * 0.012));
    if (o.tinta) {
      ctx.fillStyle = o.tinta; ctx.globalAlpha = alpha * 0.9;
      ctx.beginPath(); ctx.arc(w * 0.12, h * 0.2, w * 0.17, 0, 7); ctx.fill();
      ctx.beginPath(); ctx.arc(w * 0.3, h * 0.07, w * 0.06, 0, 7); ctx.fill();
      ctx.beginPath(); ctx.arc(-w * 0.05, h * 0.33, w * 0.04, 0, 7); ctx.fill();
    }
    ctx.restore();
  }

  function cuadro(ahora) {
    var t = ((ahora - T0) / 1000) % CICLO;
    ctx.clearRect(0, 0, W, H);
    for (var i = 0; i < hojas.length; i++) {
      var o = hojas[i], x, y, rot, esc, a = 1;
      var p = suave((t - o.d) / o.dur);
      if (t > CICLO - 1.6) {
        // las hojas salen volando para empezar de nuevo
        var q = suave((t - (CICLO - 1.6) - (hojas.length - i) * 0.012) / 1.2);
        x = o.tx + o.sx * q; y = o.ty + o.sy * q; rot = o.rf + q * o.r0; esc = 1 - 0.6 * Math.abs(Math.sin(q * 3)); a = 1 - q;
      } else {
        x = bez(o.x0, o.c1x, o.c2x, o.tx, p); y = bez(o.y0, o.c1y, o.c2y, o.ty, p);
        rot = o.r0 * (1 - p) + o.rf * p; esc = 1 - 0.75 * Math.abs(Math.sin(p * Math.PI * o.giros)) * (1 - p);
        a = Math.min(1, (t - o.d + 0.3) * 2);
        if (a <= 0) continue;
      }
      dibujarHoja(o, x, y, rot, Math.max(0.12, esc), Math.max(0, a));
    }
    if (!reduce && visible) requestAnimationFrame(cuadro);
  }

  var visible = true;
  medir();
  if (reduce) { T0 = performance.now() - 7000; cuadro(performance.now()); }
  else requestAnimationFrame(cuadro);
  var rt; window.addEventListener("resize", function () { clearTimeout(rt); rt = setTimeout(function () { medir(); if (reduce) cuadro(performance.now()); }, 200); });
  if ("IntersectionObserver" in window) new IntersectionObserver(function (e) {
    var v = e[0].isIntersecting; if (v && !visible && !reduce) { visible = true; requestAnimationFrame(cuadro); } visible = v;
  }).observe(hero);
})();
