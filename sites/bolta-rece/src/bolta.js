/* "Sub boltă" — a pivniță de cărămidă em 3D (Three.js). A câmara avança pelo túnel conforme o scroll. */
(function () {
  "use strict";
  var sec = document.querySelector(".bolta");
  if (!sec) return;
  var stage = sec.querySelector(".bolta__stage");
  var caps = Array.prototype.slice.call(sec.querySelectorAll(".bolta__cap"));
  var reduzido = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var movel = window.matchMedia("(max-width: 820px)").matches;

  var alvo = 0;
  function legendas() {                       // a legenda muda com o scroll, com ou sem WebGL
    var r = sec.getBoundingClientRect(), total = r.height - stage.offsetHeight;
    alvo = total > 0 ? Math.min(1, Math.max(0, -r.top / total)) : 0;
    var idx = Math.min(caps.length - 1, Math.floor(alvo * caps.length));
    caps.forEach(function (c, i) { c.classList.toggle("on", reduzido || i === idx); });
  }
  window.addEventListener("scroll", legendas, { passive: true });
  legendas();
  function fallback() { sec.classList.add("bolta--fallback"); if (reduzido) caps.forEach(function (c) { c.classList.add("on"); }); }
  if (typeof THREE === "undefined") { fallback(); return; }

  var renderer;
  try {
    renderer = new THREE.WebGLRenderer({ antialias: !movel, powerPreference: "high-performance" });
  } catch (e) { fallback(); return; }
  var gl = renderer.getContext();
  if (!gl) { fallback(); return; }
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, movel ? 1.5 : 2));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;
  stage.insertBefore(renderer.domElement, stage.firstChild);

  var scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0d0906);
  scene.fog = new THREE.Fog(0x0d0906, 3, movel ? 20 : 26);
  var camera = new THREE.PerspectiveCamera(58, 1, 0.1, 80);

  /* geometria da boltă: arco de cărămidă (raio R) sobre paredes de altura H, ao longo de L metros */
  var R = 2.7, H = 1.25, L = 44, passoZ = 0.235, passoArco = 0.245;
  var comprimento = 0.44, altura = 0.2, profundidade = 0.2;
  var nArco = Math.round(Math.PI * R / passoArco);          // tijolos por arco
  var nParede = Math.round(H / altura);                        // fiadas de parede
  var filas = Math.round(L / passoZ);
  var salto = movel ? 2 : 1;                                   // no telemóvel, metade das fiadas
  var total = Math.ceil(filas / salto) * (nArco + 2 * nParede);
  var geo = new THREE.BoxGeometry(comprimento, altura, profundidade);
  var mat = new THREE.MeshStandardMaterial({ roughness: 0.94, metalness: 0.0, vertexColors: false });
  var bricks = new THREE.InstancedMesh(geo, mat, total);
  var m = new THREE.Matrix4(), q = new THREE.Quaternion(), pos = new THREE.Vector3(), sc = new THREE.Vector3(1, 1, 1);
  var cor = new THREE.Color(), base = new THREE.Color(0x8e3b26);
  var seed = 7;
  function rnd() { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }
  var k = 0;
  for (var f = 0; f < filas; f += salto) {
    var z = -f * passoZ;
    var desloc = (f % 2) * passoArco * 0.5;                   // aparelho alternado
    for (var i = 0; i < nArco; i++) {
      var a = (i + 0.5) * Math.PI / nArco + desloc / R;        // 0 → π, da esquerda para a direita
      pos.set(-Math.cos(a) * R, H + Math.sin(a) * R, z);
      q.setFromAxisAngle(new THREE.Vector3(0, 0, 1), a - Math.PI / 2);
      m.compose(pos, q, sc); bricks.setMatrixAt(k, m);
      cor.copy(base).offsetHSL((rnd() - 0.5) * 0.03, (rnd() - 0.5) * 0.12, (rnd() - 0.55) * 0.16);
      if (rnd() < 0.08) cor.multiplyScalar(0.55);                // tijolo enegrecido
      bricks.setColorAt(k, cor); k++;
    }
    for (var lado = -1; lado <= 1; lado += 2) {
      for (var j = 0; j < nParede; j++) {
        pos.set(lado * R, (j + 0.5) * altura, z + (j % 2) * 0.05);
        q.setFromAxisAngle(new THREE.Vector3(0, 0, 1), lado * Math.PI / 2);
        m.compose(pos, q, sc); bricks.setMatrixAt(k, m);
        cor.set(0x6e5a4a).offsetHSL(0, (rnd() - 0.5) * 0.08, (rnd() - 0.5) * 0.14);   // pedra das paredes
        bricks.setColorAt(k, cor); k++;
      }
    }
  }
  bricks.count = k;
  bricks.instanceMatrix.needsUpdate = true;
  if (bricks.instanceColor) bricks.instanceColor.needsUpdate = true;
  scene.add(bricks);

  var chao = new THREE.Mesh(new THREE.PlaneGeometry(R * 2.2, L + 6), new THREE.MeshStandardMaterial({ color: 0x2a201a, roughness: 1 }));
  chao.rotation.x = -Math.PI / 2; chao.position.set(0, 0, -L / 2 + 2); scene.add(chao);
  /* a luz ao fundo do túnel */
  var tela = document.createElement("canvas"); tela.width = tela.height = 256;
  var ctx = tela.getContext("2d"), grad = ctx.createRadialGradient(128, 128, 0, 128, 128, 128);
  grad.addColorStop(0, "rgba(255,232,180,1)"); grad.addColorStop(0.35, "rgba(243,213,154,.55)"); grad.addColorStop(1, "rgba(243,213,154,0)");
  ctx.fillStyle = grad; ctx.fillRect(0, 0, 256, 256);
  var fim = new THREE.Sprite(new THREE.SpriteMaterial({ map: new THREE.CanvasTexture(tela), blending: THREE.AdditiveBlending, depthWrite: false, toneMapped: false, transparent: true }));
  fim.scale.set(R * 3.2, R * 3.2, 1); fim.position.set(0, H + R * 0.3, -L - 1.2); scene.add(fim);
  var fimLuz = new THREE.PointLight(0xf3d59a, 3.5, 22, 2); fimLuz.position.set(0, H + 1, -L + 2); scene.add(fimLuz);

  scene.add(new THREE.AmbientLight(0x6b4a2a, 0.35));
  var felinare = [];
  for (var n = 0; n < 5; n++) {
    var luz = new THREE.PointLight(0xe7b86a, 2.6, 11, 2);
    var lado2 = n % 2 ? 1 : -1;
    luz.position.set(lado2 * (R - 0.45), H + 0.6, -5 - n * 8);
    scene.add(luz);
    var bulbo = new THREE.Mesh(new THREE.SphereGeometry(0.075, 10, 10), new THREE.MeshBasicMaterial({ color: 0xffe3a6, toneMapped: false }));
    bulbo.position.copy(luz.position); scene.add(bulbo);
    felinare.push({ luz: luz, base: 2.6, fase: n * 1.7 });
  }
  var lanterna = new THREE.PointLight(0xe7b86a, 1.1, 9, 2); scene.add(lanterna);

  var progresso = 0, tempo = 0, visivel = false, ultimo = 0;
  function medir() {
    var w = stage.clientWidth, h = stage.clientHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w / h; camera.updateProjectionMatrix();
  }
  function desenhar(t) {
    var dt = Math.min(0.05, (t - ultimo) / 1000 || 0.016); ultimo = t; tempo += dt;
    progresso += (alvo - progresso) * (reduzido ? 1 : Math.min(1, dt * 6));
    var z = -progresso * (L - 4);
    camera.position.set(Math.sin(progresso * 9) * 0.12, H + 0.45 + Math.sin(progresso * 14) * 0.035, z);
    camera.lookAt(Math.sin(progresso * 9 + 1) * 0.06, H + 0.35, z - 7);
    lanterna.position.set(camera.position.x + 0.3, camera.position.y + 0.3, z - 0.6);
    felinare.forEach(function (f) { f.luz.intensity = f.base + Math.sin(tempo * 7 + f.fase) * 0.22 + Math.sin(tempo * 13.3 + f.fase) * 0.12; });
    renderer.render(scene, camera);
  }
  function ciclo(t) { if (!visivel) return; desenhar(t); requestAnimationFrame(ciclo); }

  var obs = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      var antes = visivel; visivel = e.isIntersecting;
      if (visivel && !antes && !reduzido) requestAnimationFrame(ciclo);
    });
  }, { rootMargin: "20% 0px" });
  obs.observe(sec);

  window.addEventListener("resize", function () { medir(); if (reduzido) desenhar(performance.now()); });
  medir();
  if (reduzido) { alvo = progresso = 0.4; desenhar(performance.now()); caps.forEach(function (c) { c.classList.add("on"); }); }
})();
