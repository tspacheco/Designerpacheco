/* Casa Bolta Rece — o percurso da página inicial, da rua até à mesa.
 *
 * 1) De porta em porta (fotografias reais, 2D). A câmara aproxima-se da abertura de cada foto
 *    (poarta, ușa, arcul) e a divisão seguinte já lá está dentro, recortada com a forma dessa abertura:
 *    retas e de madeira lá fora, em arco cá dentro. A divisão do fundo cresce mais devagar do que a
 *    abertura (paralaxe), por isso lê-se como espaço e não como uma foto colada.
 * 2) Sub boltă (Three.js). A descida pela crama e pelas pivnițe com as fotografias reais da cave.
 *    Cada foto tem um mapa de profundidade (media/profundidade-*.png): a malha é deslocada por ele e a
 *    câmara entra na foto com paralaxe verdadeira. A paragem seguinte nasce no ponto de fuga da anterior
 *    enquanto o que está perto passa por nós. Os candeeiros das fotos tremeluzem; há pó no ar.
 *    No fim, a luz do fundo da boltă enche o ecrã e dá lugar à secção seguinte.
 * Sem WebGL, a descida faz-se com as mesmas fotografias em 2D. Sem JS ou com movimento reduzido,
 * o CSS empilha tudo (fotografias e legendas) e este script não corre.
 */
(function () {
  "use strict";
  var sec = document.querySelector(".bolta");
  var raiz = document.documentElement;
  if (!sec || !raiz.classList.contains("js") || raiz.classList.contains("rm")) return;

  var stage = sec.querySelector(".bolta__stage");
  var locEl = sec.querySelector(".bolta__loc");
  var locNome = sec.querySelector(".bolta__loc-nume");
  var bara = sec.querySelector(".bolta__bara");
  var hint = sec.querySelector(".bolta__hint");
  var ancora = sec.querySelector(".bolta__ancora");
  var movel = window.matchMedia("(max-width: 820px)").matches;
  var luzFim = document.createElement("div");
  luzFim.className = "bolta__fim"; luzFim.setAttribute("aria-hidden", "true");
  stage.appendChild(luzFim);

  function nums(s) { return String(s || "").trim().split(/[\s,]+/).filter(Boolean).map(Number); }
  function clamp(x, a, b) { return x < a ? a : x > b ? b : x; }
  function lerp(a, b, t) { return a + (b - a) * t; }
  function suave(t) { t = clamp(t, 0, 1); return t * t * (3 - 2 * t); }
  function inOut(t) { t = clamp(t, 0, 1); return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }

  /* abertura em coordenadas da foto (0–1):
     "r x0 y0 x1 y1" retângulo (porta, portão) · "a x0 x1 topo nascença base" arco de volta perfeita
     "z x y" sem abertura: aproximação a esse ponto e fusão com a foto seguinte */
  function forma(s) {
    var t = String(s || "").trim().split(/\s+/), k = t.shift(), v = t.map(Number), pts = [];
    if (k === "z") pts = [[v[0], v[1]]];
    else if (k === "r") pts = [[v[0], v[1]], [v[2], v[1]], [v[2], v[3]], [v[0], v[3]]];
    else if (k === "a") {
      var cx = (v[0] + v[1]) / 2, rx = (v[1] - v[0]) / 2, ry = v[3] - v[2];
      pts.push([v[0], v[4]]);
      for (var n = 0; n <= 24; n++) { var a = Math.PI - n * Math.PI / 24; pts.push([cx + Math.cos(a) * rx, v[3] - Math.sin(a) * ry]); }
      pts.push([v[1], v[4]]);
    }
    return pts;
  }

  var pasi = [].slice.call(sec.querySelectorAll(".cadru")).map(function (f, i) {
    var p = {
      i: i, vel: f.querySelector(".cadru__img"), img: f.querySelector("img"), cap: f.querySelector(".cadru__cap"),
      tip: f.getAttribute("data-tip"), nume: f.getAttribute("data-nume") || "", foco: nums(f.getAttribute("data-foco") || ".5 .5")
    };
    if (p.tip === "prag") {
      p.modo = String(f.getAttribute("data-op") || "z").trim().charAt(0);
      p.abre = f.getAttribute("data-abre") || "";
      p.op = forma(f.getAttribute("data-op"));
      var x0 = 1, y0 = 1, x1 = 0, y1 = 0;
      p.op.forEach(function (q) { x0 = Math.min(x0, q[0]); y0 = Math.min(y0, q[1]); x1 = Math.max(x1, q[0]); y1 = Math.max(y1, q[1]); });
      p.opC = [(x0 + x1) / 2, (y0 + y1) / 2];
    } else {
      var z = nums(f.getAttribute("data-z")), l = nums(f.getAttribute("data-luz"));
      p.vp = nums(f.getAttribute("data-vp")); p.perto = z[0]; p.longe = z[1];
      p.avanco = (+f.getAttribute("data-avanco") || 2) * (movel ? 0.75 : 1); p.rel = f.getAttribute("data-rel");
      p.luzes = []; for (var k = 0; k + 2 < l.length; k += 3) p.luzes.push(l.slice(k, k + 3));
    }
    return p;
  });
  if (!pasi.length) return;
  var ultimo = pasi.length - 1;

  /* legenda de cada paragem: a última figcaption até ela (as paragens sem legenda herdam a anterior) */
  var capDe = [], u0 = -1;
  pasi.forEach(function (p, i) { if (p.cap) u0 = i; capDe[i] = u0; });

  /* linha do tempo: cada paragem ocupa um troço do scroll; as da cave são um pouco mais longas */
  var PESO = { prag: 0.9, bolta: 1.1 }, inicio = [], total = 0, primBolta = -1, andado = [], soma = 0;
  pasi.forEach(function (p, i) {
    inicio.push(total); total += PESO[p.tip] || 1;
    if (p.tip === "bolta") { if (primBolta < 0) primBolta = i; andado[i] = soma; soma += p.avanco; }
  });
  function onde(a) {
    var pos = clamp(a, 0, 1) * total, k = pasi.length - 1;
    while (k > 0 && inicio[k] > pos) k--;
    return { k: k, t: clamp((pos - inicio[k]) / (PESO[pasi[k].tip] || 1), 0, 1) };
  }

  /* ---------- medidas (lidas só no resize: o scroll não lê o layout) ---------- */
  var W = 1, H = 1, topo = 0, curso = 1, diag = 1;
  function M(p, u, v) { return [p.L + u * p.w, p.T + v * p.h]; }
  function dentro(pt, poli) {
    var x = pt[0], y = pt[1], d = false;
    for (var i = 0, j = poli.length - 1; i < poli.length; j = i++) {
      var xi = poli[i][0], yi = poli[i][1], xj = poli[j][0], yj = poli[j][1];
      if ((yi > y) !== (yj > y) && x < (xj - xi) * (y - yi) / (yj - yi) + xi) d = !d;
    }
    return d;
  }
  function escalaFinal(p) {        // menor zoom (com a abertura já ao centro) em que a abertura cobre o ecrã todo
    var C = [W / 2, H / 2], rel = p.op.map(function (q) { var m = M(p, q[0], q[1]); return [m[0] - p.A[0], m[1] - p.A[1]]; });
    var pontos = [[0, 0], [W, 0], [W, H], [0, H], [W / 2, 0], [W / 2, H], [0, H / 2], [W, H / 2]];
    function cobre(S) {
      var poli = rel.map(function (q) { return [C[0] + S * q[0], C[1] + S * q[1]]; });
      return pontos.every(function (c) { return dentro(c, poli); });
    }
    var lo = 1, hi = 300;
    if (!cobre(hi)) return hi;
    for (var n = 0; n < 36; n++) { var m = Math.sqrt(lo * hi); if (cobre(m)) hi = m; else lo = m; }
    return hi * 1.03;
  }
  function medir() {
    W = stage.clientWidth || window.innerWidth; H = stage.clientHeight || window.innerHeight;
    diag = Math.sqrt(W * W + H * H);
    topo = sec.getBoundingClientRect().top + (window.scrollY || window.pageYOffset);
    curso = Math.max(1, sec.offsetHeight - H);
    pasi.forEach(function (p) {
      if (W / H > 1.5) { p.w = W; p.h = W / 1.5; } else { p.h = H; p.w = H * 1.5; }     // object-fit: cover
      p.L = (W - p.w) * p.foco[0]; p.T = (H - p.h) * p.foco[1];                         // object-position: foco
      p.img.style.width = p.w + "px"; p.img.style.height = p.h + "px";
      if (p.op) { p.A = M(p, p.opC[0], p.opC[1]); p.Sfim = p.modo === "z" ? 2.1 : escalaFinal(p); }
      if (p.vp) p.V = M(p, p.vp[0], p.vp[1]);
      p.tf = null;
    });
    if (ancora && primBolta >= 0) ancora.style.top = Math.round(inicio[primBolta] / total * curso) + "px";
    if (g3) g3.medir();
  }

  /* ---------- camada 2D (fotografias no DOM) ---------- */
  function colocar(p, S, P, ref) {       // o ponto ref (px, foto sem zoom) vai para P, com escala S
    var tx = P[0] + S * (p.L - ref[0]), ty = P[1] + S * (p.T - ref[1]);
    var v = "translate3d(" + tx.toFixed(2) + "px," + ty.toFixed(2) + "px,0) scale(" + S.toFixed(5) + ")";
    if (v !== p.tf) { p.tf = v; p.img.style.transform = v; }
  }
  function ver(p, sim) { if (p.visto !== sim) { p.visto = sim; p.vel.classList.toggle("vis", sim); } }
  function recortar(p, poli) {
    var v = poli ? "polygon(" + poli.map(function (q) { return q[0].toFixed(1) + "px " + q[1].toFixed(1) + "px"; }).join(",") + ")" : "none";
    if (v !== p.clip) { p.clip = v; p.vel.style.clipPath = v; p.vel.style.webkitClipPath = v; }
  }
  function opacidade(p, o) { var v = o >= 0.999 ? "" : o.toFixed(3); if (v !== p.opa) { p.opa = v; p.vel.style.opacity = v; } }

  var REPOUSO = 0.18;                  // início de cada paragem do tour: quase parado, para ver a foto
  function pragDOM(k, t) {
    var p = pasi[k], q = pasi[k + 1], C = [W / 2, H / 2];
    var tau = clamp((t - REPOUSO) / (1 - REPOUSO), 0, 1);
    var S = t < REPOUSO ? 1 + 0.025 * suave(t / REPOUSO) : 1.025 * Math.pow(p.Sfim / 1.025, inOut(tau));
    var e = suave(tau) * (p.modo === "z" ? 0.6 : 1), P = [lerp(p.A[0], C[0], e), lerp(p.A[1], C[1], e)];
    colocar(p, S, P, p.A); recortar(p, null); opacidade(p, 1); ver(p, true);
    if (!q || tau <= 0) return false;
    if (p.modo === "z") {                 // sem abertura: aproxima-se e a foto seguinte entra por cima, a assentar
      if (tau <= 0.3) return false;
      colocar(q, 1 + 0.16 * (1 - suave(tau)), C, C); recortar(q, null);
      opacidade(q, suave((tau - 0.3) / 0.55)); ver(q, true);
      return true;
    }
    var poli = p.op.map(function (o) { var m = M(p, o[0], o[1]); return [P[0] + S * (m[0] - p.A[0]), P[1] + S * (m[1] - p.A[1])]; });
    var x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
    poli.forEach(function (c) { x0 = Math.min(x0, c[0]); y0 = Math.min(y0, c[1]); x1 = Math.max(x1, c[0]); y1 = Math.max(y1, c[1]); });
    /* a foto seguinte, centrada no meio da abertura: tem de cobrir a parte visível da abertura
       e cresce mais devagar do que ela (está mais longe) */
    var r0 = Math.max(0, x0), r1 = Math.min(W, x1), s0 = Math.max(0, y0), s1 = Math.min(H, y1);
    var cob = Math.max(2 * (P[0] - r0) / W, 2 * (r1 - P[0]) / W, 2 * (P[1] - s0) / H, 2 * (s1 - P[1]) / H);
    var par = Math.pow(Math.min(1, Math.max((x1 - x0) / W, (y1 - y0) / H)), 0.72);
    var sig = tau >= 1 ? 1 : Math.max(cob + 0.01, par) * (1 + 0.06 * (1 - suave(tau)));
    colocar(q, sig, P, C);
    if (p.abre && tau < 1) {             // porta ou portão: a abertura abre-se como as folhas da porta
      var w = suave(tau / 0.28), ax = p.abre === "esq" ? x0 : p.abre === "dir" ? x1 : (x0 + x1) / 2;
      poli = poli.map(function (c) { return [ax + (c[0] - ax) * w, c[1]]; });
    }
    recortar(q, tau >= 1 ? null : poli);
    opacidade(q, p.abre ? 1 : suave(tau / 0.08));
    ver(q, true);
    return true;
  }
  function boltaDOM(k, t) {             // descida sem WebGL: as mesmas fotos, zoom para o fundo e fusão
    var p = pasi[k], q = pasi[k + 1];
    colocar(p, 1 + 0.32 * Math.pow(t, 1.4), p.V, p.V); recortar(p, null); opacidade(p, 1); ver(p, true);
    if (!q || t <= 0.55) return false;
    var f = suave((t - 0.55) / 0.45);
    colocar(q, 1 + 0.12 * (1 - f), q.V, q.V); recortar(q, null); opacidade(q, f); ver(q, true);
    return true;
  }

  /* ---------- camada 3D (Three.js): a cave com profundidade ---------- */
  var g3 = null;
  function criar3D() {
    if (typeof THREE === "undefined" || !window.Promise) return null;
    var renderer;
    try { renderer = new THREE.WebGLRenderer({ antialias: false, alpha: false, powerPreference: "high-performance" }); }
    catch (e) { return null; }
    if (!renderer || !renderer.getContext()) return null;
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, movel ? 1.5 : 2));
    renderer.autoClear = false;
    renderer.setClearColor(0x0d0906, 1);
    var tela = renderer.domElement;
    tela.className = "bolta__gl"; tela.setAttribute("aria-hidden", "true");
    stage.insertBefore(tela, stage.firstChild);
    var webgl2 = renderer.capabilities.isWebGL2;
    var TX = Math.tan(42 * Math.PI / 180), TY = TX / 1.5;       // fotos a ~84° de campo horizontal
    var COLS = movel ? 160 : 270, ROWS = Math.round(COLS / 1.5);
    var cam = new THREE.PerspectiveCamera(60, 1, 0.05, 90), compilado = false;
    var camPo = new THREE.PerspectiveCamera(60, 1, 0.05, 90);

    var VS = [
      "attribute float aresta;",
      "varying vec2 vUv; varying float vProf; varying float vAr;",
      "void main(){ vUv = uv; vAr = aresta; vec4 mv = modelViewMatrix * vec4(position, 1.0); vProf = -mv.z; gl_Position = projectionMatrix * mv; }"
    ].join("\n");
    var FS = [
      "uniform sampler2D mapa; uniform float corte; uniform float macio; uniform float afasta; uniform float borda;",
      "uniform vec3 luz[3]; uniform float cint[3];",
      "varying vec2 vUv; varying float vProf; varying float vAr;",
      "void main(){",
      "  vec3 c = texture2D(mapa, vUv).rgb;",
      "  vec3 quente = vec3(1.0, 0.72, 0.40);",
      "  for (int i = 0; i < 3; i++) {",
      "    if (luz[i].z > 0.0) {",
      "      vec2 d = (vUv - vec2(luz[i].x, 1.0 - luz[i].y)) * vec2(1.5, 1.0);",
      "      float r2 = luz[i].z * luz[i].z;",
      "      float nucleo = exp(-dot(d, d) / r2);",
      "      float halo = exp(-dot(d, d) / (r2 * 10.0));",
      "      c *= 1.0 + (cint[i] - 0.5) * 0.12 * halo;",
      "      c += quente * (nucleo * (0.08 + 0.20 * cint[i]) + halo * 0.04 * cint[i]);",
      "    }",
      "  }",
      "  c *= 1.0 - 0.6 * smoothstep(0.10, 0.40, vAr) * afasta;",
      "  c *= mix(1.0, smoothstep(0.12, 1.15, vProf), afasta);   // o que passa junto a nós fica no escuro",
      "  float bd = min(min(vUv.x, 1.0 - vUv.x) * 1.5, min(vUv.y, 1.0 - vUv.y));",
      "  c *= mix(1.0, smoothstep(0.0, 0.16, bd), borda);            // a sala que nasce ao fundo não tem arestas duras",
      "  float a = 1.0 - smoothstep(corte - macio, corte + macio, vProf);",
      "  gl_FragColor = vec4(c, a);",
      "}"
    ].join("\n");

    /* pó no ar, em espaço de câmara: vem ao nosso encontro à medida que se anda */
    var nPo = movel ? 130 : 240, base = new Float32Array(nPo * 3), semente = 11;
    function rnd() { semente = (semente * 16807) % 2147483647; return (semente - 1) / 2147483646; }
    for (var n = 0; n < nPo; n++) { base[n * 3] = rnd() * 2 - 1; base[n * 3 + 1] = rnd() * 2 - 1; base[n * 3 + 2] = rnd(); }
    var poGeo = new THREE.BufferGeometry();
    poGeo.setAttribute("position", new THREE.BufferAttribute(base, 3));
    var poMat = new THREE.ShaderMaterial({
      uniforms: { viagem: { value: 0 }, tempo: { value: 0 }, px: { value: 1 }, forca: { value: 0 } },
      vertexShader: [
        "uniform float viagem; uniform float tempo; uniform float px; varying float vA;",
        "void main(){",
        "  float z = fract(position.z - viagem * 0.11);",
        "  float prof = mix(0.35, 7.0, z);",
        "  vec3 p = vec3(position.x * 0.95 * prof, position.y * 0.62 * prof, -prof);",
        "  p.x += sin(tempo * 0.35 + position.z * 37.0) * 0.06;",
        "  p.y += sin(tempo * 0.27 + position.x * 23.0) * 0.05;",
        "  gl_Position = projectionMatrix * vec4(p, 1.0);",
        "  gl_PointSize = px * (0.9 + fract(position.x * 91.0) * 1.6) * 3.2 / prof;",
        "  vA = smoothstep(0.0, 0.12, z) * (1.0 - smoothstep(0.75, 1.0, z));",
        "}"
      ].join("\n"),
      fragmentShader: [
        "uniform float forca; varying float vA;",
        "void main(){ vec2 c = gl_PointCoord - 0.5; float d = dot(c, c); if (d > 0.25) discard;",
        "  gl_FragColor = vec4(vec3(1.0, 0.82, 0.58) * (1.0 - d * 4.0) * vA * forca * 0.5, 1.0); }"
      ].join("\n"),
      transparent: true, depthTest: false, depthWrite: false, blending: THREE.AdditiveBlending
    });
    var po = new THREE.Points(poGeo, poMat); po.frustumCulled = false;
    var cenaPo = new THREE.Scene(); cenaPo.add(po);

    function carregarImg(img) {
      return new Promise(function (ok, erro) {
        if (img.complete && img.naturalWidth) { ok(img); return; }
        img.loading = "eager";
        img.addEventListener("load", function () { ok(img); }, { once: true });
        img.addEventListener("error", erro, { once: true });
      });
    }
    function carregarRel(src) {
      return new Promise(function (ok, erro) { var i = new Image(); i.onload = function () { ok(i); }; i.onerror = erro; i.src = src; });
    }
    function bitmap(img) {                 // descodifica fora da thread principal quando o browser deixa
      if (!window.createImageBitmap) return Promise.resolve(null);
      return createImageBitmap(img, { imageOrientation: "flipY" }).catch(function () { return null; });
    }
    function fatias(total, porFatia, fazer) {   // trabalho pesado aos bocados, sem tarefas longas
      return new Promise(function (ok) {
        var i = 0;
        (function passo() { var fim = Math.min(total, i + porFatia); for (; i < fim; i++) fazer(i); if (i < total) setTimeout(passo, 0); else ok(); })();
      });
    }
    function construir(p, rel, bmp) {
      var cv = document.createElement("canvas"); cv.width = rel.naturalWidth; cv.height = rel.naturalHeight;
      var c2 = cv.getContext("2d"); c2.drawImage(rel, 0, 0);
      var px = c2.getImageData(0, 0, cv.width, cv.height).data, rw = cv.width, rh = cv.height;
      function disp(u, v) {                               // disparidade (1 = perto), bilinear
        var x = u * (rw - 1), y = v * (rh - 1), xa = Math.floor(x), ya = Math.floor(y);
        var xb = Math.min(rw - 1, xa + 1), yb = Math.min(rh - 1, ya + 1), fx = x - xa, fy = y - ya;
        var a = px[(ya * rw + xa) * 4], b = px[(ya * rw + xb) * 4], c = px[(yb * rw + xa) * 4], d = px[(yb * rw + xb) * 4];
        return ((a + (b - a) * fx) + ((c + (d - c) * fx) - (a + (b - a) * fx)) * fy) / 255;
      }
      var ka = 1 / p.perto - 1 / p.longe, kb = 1 / p.longe, L1 = COLS + 1;
      var nV = L1 * (ROWS + 1), pos = new Float32Array(nV * 3), uv = new Float32Array(nV * 2);
      var lz = new Float32Array(nV), ar = new Float32Array(nV);
      var idx = new (nV > 65535 ? Uint32Array : Uint16Array)(COLS * ROWS * 6);
      return fatias(ROWS + 1, 24, function (j) {
        for (var i = 0, n = j * L1; i <= COLS; i++, n++) {
          var u = i / COLS, v = j / ROWS, z = 1 / (disp(u, v) * ka + kb);
          pos[n * 3] = (2 * u - 1) * TX * z; pos[n * 3 + 1] = (1 - 2 * v) * TY * z; pos[n * 3 + 2] = -z;
          uv[n * 2] = u; uv[n * 2 + 1] = 1 - v; lz[n] = Math.log(z);
        }
      }).then(function () {
        return fatias(ROWS + 1, 30, function (j) {           // costuras: saltos de profundidade entre vizinhos
          for (var i = 0, n = j * L1; i <= COLS; i++, n++) {
            var m = 0, l0 = lz[n];
            if (i > 0) m = Math.max(m, Math.abs(l0 - lz[n - 1]));
            if (i < COLS) m = Math.max(m, Math.abs(l0 - lz[n + 1]));
            if (j > 0) m = Math.max(m, Math.abs(l0 - lz[n - L1]));
            if (j < ROWS) m = Math.max(m, Math.abs(l0 - lz[n + L1]));
            ar[n] = m;
            if (i < COLS && j < ROWS) {
              var k = (j * COLS + i) * 6;
              idx[k] = n; idx[k + 1] = n + L1; idx[k + 2] = n + 1;
              idx[k + 3] = n + 1; idx[k + 4] = n + L1; idx[k + 5] = n + L1 + 1;
            }
          }
        });
      }).then(function () {
      var geo = new THREE.BufferGeometry();
      geo.setAttribute("position", new THREE.BufferAttribute(pos, 3));
      geo.setAttribute("uv", new THREE.BufferAttribute(uv, 2));
      geo.setAttribute("aresta", new THREE.BufferAttribute(ar, 1));
      geo.setIndex(new THREE.BufferAttribute(idx, 1));
      var tex = new THREE.Texture(bmp || p.img);
      if (bmp) tex.flipY = false;                            // o bitmap já vem virado
      tex.generateMipmaps = webgl2;
      tex.minFilter = webgl2 ? THREE.LinearMipmapLinearFilter : THREE.LinearFilter;
      tex.magFilter = THREE.LinearFilter;
      tex.wrapS = tex.wrapT = THREE.ClampToEdgeWrapping;
      tex.anisotropy = Math.min(8, renderer.capabilities.getMaxAnisotropy());
      tex.needsUpdate = true;
      var luzes = [0, 1, 2].map(function (k) { var l = p.luzes[k]; return new THREE.Vector3(l ? l[0] : 0, l ? l[1] : 0, l ? l[2] : 0); });
      p.mat = new THREE.ShaderMaterial({
        uniforms: { mapa: { value: tex }, corte: { value: 1e4 }, macio: { value: 1 }, afasta: { value: 0 }, borda: { value: 0 }, luz: { value: luzes }, cint: { value: [0.5, 0.5, 0.5] } },
        vertexShader: VS, fragmentShader: FS, side: THREE.DoubleSide, transparent: true
      });
      p.cena = new THREE.Scene();
      var malha = new THREE.Mesh(geo, p.mat); malha.frustumCulled = false; p.cena.add(malha);
      p.dir = new THREE.Vector3((2 * p.vp[0] - 1) * TX, (1 - 2 * p.vp[1]) * TY, -1).normalize();
      renderer.initTexture(tex);                             // sobe já para a GPU, fora do scroll
      if (!compilado) { compilado = true; renderer.compile(p.cena, cam); }   // o shader compila agora e não no 1.º quadro
      p.pronto = true;
      });
    }
    function carregarTudo() {
      var cadeia = Promise.resolve();
      pasi.forEach(function (p) {
        if (p.tip !== "bolta") return;
        cadeia = cadeia.then(function () { return Promise.all([carregarImg(p.img), carregarRel(p.rel)]); })
          .then(function (r) { return bitmap(r[0]).then(function (b) { return construir(p, r[1], b); }); })
          .catch(function () { p.pronto = false; });
      });
    }

    function janela(p) {                 // parte da foto que o ecrã mostra (cover + foco), em 0–1
      var a = W / H, ww, wh;
      if (a > 1.5) { ww = 1; wh = 1.5 / a; } else { wh = 1; ww = a / 1.5; }
      return { l: (1 - ww) * p.foco[0], t: (1 - wh) * p.foco[1], w: ww, h: wh };
    }
    function projetar(c, j) {
      var nr = 0.05;
      c.projectionMatrix.makePerspective((-1 + 2 * j.l) * TX * nr, (-1 + 2 * (j.l + j.w)) * TX * nr,
        (1 - 2 * j.t) * TY * nr, (1 - 2 * (j.t + j.h)) * TY * nr, nr, 90);
      c.projectionMatrixInverse.copy(c.projectionMatrix).invert();
    }
    function cintila(t, s) {
      return clamp(0.55 + 0.25 * Math.sin(t * 6.1 + s * 1.7) + 0.15 * Math.sin(t * 13.7 + s * 3.1) + 0.08 * Math.sin(t * 29.3 + s), 0, 1);
    }
    function estacao(p, j, d, corte, afasta, tempo, borda) {
      var bob = Math.min(1, d / 0.6);
      cam.position.copy(p.dir).multiplyScalar(d);
      cam.position.x += Math.sin(tempo * 0.7) * 0.02 * bob;
      cam.position.y += Math.sin(tempo * 1.1) * 0.012 * bob;
      cam.updateMatrixWorld(true);
      projetar(cam, j);
      var u = p.mat.uniforms;
      u.corte.value = corte; u.macio.value = 0.2 + Math.min(corte, 50) * 0.18; u.afasta.value = afasta; u.borda.value = borda || 0;
      for (var k = 0; k < 3; k++) u.cint.value[k] = cintila(tempo, p.i * 3 + k);
      renderer.render(p.cena, cam);
    }
    function desenhar(k, t, tempo) {
      var A = pasi[k], B = pasi[k + 1];
      renderer.clear(true, true, true);
      var jA = janela(A), dA = A.avanco * Math.pow(t, k === ultimo ? 1.25 : 1.6);
      var tr = B && B.tip === "bolta" ? clamp((t - 0.55) / 0.45, 0, 1) : 0;
      if (tr > 0 && B.pronto) {
        /* a paragem seguinte nasce no ponto de fuga desta e cresce até encher o ecrã */
        var jB = janela(B), PA = [(A.vp[0] - jA.l) / jA.w, (A.vp[1] - jA.t) / jA.h], VB = [(B.vp[0] - jB.l) / jB.w, (B.vp[1] - jB.t) / jB.h];
        var e = inOut(tr), s = Math.pow(0.3, 1 - e), Pt = [lerp(PA[0], VB[0], e), lerp(PA[1], VB[1], e)];
        estacao(B, { l: jB.l - Pt[0] * jB.w / s + VB[0] * jB.w, t: jB.t - Pt[1] * jB.h / s + VB[1] * jB.h, w: jB.w / s, h: jB.h / s }, 0, 1e4, 0, tempo, 1 - e);
        renderer.clearDepth();
      }
      /* o que está longe desaparece primeiro; o que está perto passa por nós */
      var corte = tr > 0 ? A.longe * 1.15 * Math.pow(1 - tr, 1.5) + 0.02 : 1e4;
      estacao(A, jA, dA, corte, clamp(dA / 1.2, 0, 1), tempo);
      camPo.projectionMatrix.copy(cam.projectionMatrix);
      camPo.projectionMatrixInverse.copy(cam.projectionMatrixInverse);
      poMat.uniforms.viagem.value = andado[k] + dA;
      poMat.uniforms.tempo.value = tempo;
      poMat.uniforms.forca.value = 1;
      renderer.render(cenaPo, camPo);
    }
    function medir3D() {
      renderer.setSize(W, H, false);
      poMat.uniforms.px.value = renderer.getPixelRatio() * clamp(H / 800, 0.6, 1.6);
    }
    var ligado = false;
    function mostrar(sim) { if (sim !== ligado) { ligado = sim; tela.classList.toggle("on", sim); } }
    medir3D();
    carregarTudo();
    return { medir: medir3D, desenhar: desenhar, mostrar: mostrar };
  }

  /* ---------- um quadro ---------- */
  var capAtual = -2, nomeAtual = null, fimAtual = -1, pAtual = -1;
  function aplicar(a) {
    var o = onde(a), k = o.k, t = o.t, p = pasi[k], q = pasi[k + 1], vis = {}, em3D = false;
    vis[k] = true;
    if (p.tip === "prag") { if (pragDOM(k, t)) vis[k + 1] = true; }
    else {
      em3D = !!(g3 && p.pronto && (!q || t <= 0.55 || q.pronto));
      if (em3D) g3.desenhar(k, t, tempo);
      else if (boltaDOM(k, t)) vis[k + 1] = true;
    }
    if (g3) g3.mostrar(em3D);
    pasi.forEach(function (x, i) { if (!vis[i] || em3D) ver(x, false); });

    var ci = k;
    if (q && (p.tip === "prag" ? t > REPOUSO + (1 - REPOUSO) * 0.55 : t > 0.78)) ci = k + 1;
    var fim = k === ultimo ? suave((t - 0.6) / 0.36) : 0;
    var cap = fim > 0.4 ? -1 : capDe[ci];
    if (cap !== capAtual) {
      if (capAtual >= 0) pasi[capAtual].cap.classList.remove("on");
      capAtual = cap;
      if (cap >= 0) pasi[cap].cap.classList.add("on");
    }
    if (pasi[ci].nume !== nomeAtual) { nomeAtual = pasi[ci].nume; locNome.textContent = nomeAtual; }
    var pv = Math.round(a * 1000) / 1000;
    if (pv !== pAtual) { pAtual = pv; bara.style.setProperty("--p", String(pv)); }
    hint.classList.toggle("fora", a > 0.012);
    locEl.classList.toggle("fora", fim > 0.3);
    /* no fim, a luz do fundo da boltă enche o ecrã */
    var fr = Math.round(fim * 500) / 500;
    if (fr !== fimAtual) {
      fimAtual = fr;
      stage.style.setProperty("--fim", String(fr));
      if (fr <= 0) luzFim.style.background = "none";
      else {
        var V = pasi[ultimo].V, r1 = diag * (0.12 + 1.5 * fr), r0 = r1 * (0.15 + 0.85 * fr * fr), al = Math.min(1, fr * 1.6);
        luzFim.style.background = "radial-gradient(circle at " + V[0].toFixed(1) + "px " + V[1].toFixed(1) + "px,rgba(252,240,214," + al.toFixed(3) + ") 0," +
          "rgba(244,238,226," + al.toFixed(3) + ") " + r0.toFixed(1) + "px,rgba(244,238,226,0) " + r1.toFixed(1) + "px)";
      }
    }
  }

  /* ---------- ciclo: só corre com a secção à vista ---------- */
  var alvo = 0, prog = 0, correr = false, ultimoT = 0, tempo = 0;
  function quadro(agora) {
    if (!correr) return;
    var dt = Math.min(0.05, (agora - ultimoT) / 1000 || 0.016); ultimoT = agora; tempo += dt;
    alvo = clamp(((window.scrollY || window.pageYOffset) - topo) / curso, 0, 1);
    prog += (alvo - prog) * Math.min(1, dt * 7);
    if (Math.abs(alvo - prog) < 0.00004) prog = alvo;
    aplicar(prog);
    window.requestAnimationFrame(quadro);
  }
  new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (e.isIntersecting && !correr) { correr = true; ultimoT = performance.now(); window.requestAnimationFrame(quadro); }
      else if (!e.isIntersecting) correr = false;
    });
  }, { rootMargin: "10% 0px" }).observe(sec);

  /* as fotos e a cave 3D preparam-se antes de a secção chegar */
  var preparado = false;
  function preparar() {
    if (preparado) return; preparado = true;
    pasi.forEach(function (p) { p.img.loading = "eager"; });
    g3 = criar3D();
    if (g3) g3.medir();
  }
  new IntersectionObserver(function (es, obs) {
    if (es.some(function (e) { return e.isIntersecting; })) { obs.disconnect(); preparar(); }
  }, { rootMargin: "150% 0px" }).observe(sec);

  var pendente = false;
  window.addEventListener("resize", function () {
    if (pendente) return; pendente = true;
    window.requestAnimationFrame(function () { pendente = false; medir(); if (!correr) aplicar(prog); });
  });
  window.addEventListener("load", function () { medir(); });
  medir();
  alvo = prog = clamp(((window.scrollY || window.pageYOffset) - topo) / curso, 0, 1);
  sec.classList.add("pronto");
  aplicar(prog);
})();
