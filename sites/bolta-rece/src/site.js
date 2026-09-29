/* Casa Bolta Rece — comportamentos partilhados (nav, revelação, herói, galeria, widget de rezervări) */
(function () {
  "use strict";
  var reduzido = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

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
    form.addEventListener("input", function () { err.hidden = true; });
    form.addEventListener("change", function () { err.hidden = true; });
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var ok = form.querySelector(".form__ok");
      if (ok) ok.hidden = false;
    });
  }

  /* rezervări: widget ziua · ora · persoane · locul · date.
     window.BOLTA (em src/rezervare.html) liga-o a um sistema: endpoint (POST JSON), disponibilitate (GET ?data=).
     Sem endpoint, no Netlify, a cerere vai para o painel Forms (formulário "rezervare"). Sem nenhum dos dois,
     a pessoa envia-a por e-mail ou telefone com os dados já preenchidos. Nunca se inventa disponibilidade. */
  var rw = document.getElementById("rw");
  if (rw) {
    var B = window.BOLTA || {};
    var CFG = {
      endpoint: B.endpoint || null,
      disponibilitate: B.disponibilitate || null,
      netlify: B.netlify !== false,
      telefon: B.telefon || "+40752589881",
      whatsapp: B.whatsapp || "",
      email: B.email || "casaboltareceiasi@gmail.com",
      pranz: B.pranz || ["12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30"],
      seara: B.seara || ["18:00", "18:30", "19:00", "19:30", "20:00", "20:30", "21:00"],
      zile: B.zile || 21
    };
    var ZILE = ["dum", "lun", "mar", "mie", "joi", "vin", "sâm"], ZILE_L = ["duminică", "luni", "marți", "miercuri", "joi", "vineri", "sâmbătă"];
    var LUNI = ["ian", "feb", "mar", "apr", "mai", "iun", "iul", "aug", "sep", "oct", "nov", "dec"];
    var LUNI_L = ["ianuarie", "februarie", "martie", "aprilie", "mai", "iunie", "iulie", "august", "septembrie", "octombrie", "noiembrie", "decembrie"];
    var LOC_L = { oriunde: "oriunde", crama: "în cramă", salon: "în salon", "sala-rustica": "în sala rustică", terasa: "pe terasă" };
    var el = function (id) { return document.getElementById(id); };
    var cZile = el("rw-zile"), cPranz = el("rw-pranz"), cSeara = el("rw-seara"), outN = el("rw-n"), rez = el("rw-rezumat");
    var form = el("rw-form"), err = el("rw-eroare"), ok = el("rw-ok");
    var sel = { data: null, ora: null, interval: null, persoane: 2, zona: "oriunde" }, libere = null, pedido = 0;
    rw.hidden = false;
    [].forEach.call(document.querySelectorAll(".rw-simplu"), function (f) { f.hidden = true; });

    var esc = function (s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); };
    var telL = function (t) { return /^\+40\d{9}$/.test(t) ? "+40 " + t.slice(3, 6) + " " + t.slice(6, 9) + " " + t.slice(9) : t; };
    var persL = function (n) { return n === 1 ? "1 persoană" : n + (n >= 20 ? " de persoane" : " persoane"); };
    function acum() {                          // a hora de Iași, seja qual for o fuso de quem reserva
      try {
        var g = {};
        new Intl.DateTimeFormat("en-GB", { timeZone: "Europe/Bucharest", year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", hourCycle: "h23" })
          .formatToParts(new Date()).forEach(function (x) { g[x.type] = x.value; });
        return { y: +g.year, m: +g.month, d: +g.day, min: (+g.hour % 24) * 60 + (+g.minute) };
      } catch (e) { var n = new Date(); return { y: n.getFullYear(), m: n.getMonth() + 1, d: n.getDate(), min: n.getHours() * 60 + n.getMinutes() }; }
    }
    var iso = function (dt) { return dt.getUTCFullYear() + "-" + String(dt.getUTCMonth() + 1).padStart(2, "0") + "-" + String(dt.getUTCDate()).padStart(2, "0"); };
    var zi = function (s) { var p = s.split("-"); return new Date(Date.UTC(+p[0], p[1] - 1, +p[2])); };
    var ziL = function (s) { var d = zi(s); return ZILE_L[d.getUTCDay()] + " " + d.getUTCDate() + " " + LUNI_L[d.getUTCMonth()]; };
    var minute = function (h) { var p = h.split(":"); return +p[0] * 60 + (+p[1]); };
    var A = acum(), azi = iso(new Date(Date.UTC(A.y, A.m - 1, A.d)));
    var trecuta = function (h) { return sel.data === azi && minute(h) < A.min + 60; };   // hoje: pelo menos uma hora antes

    for (var i = 0; i < CFG.zile; i++) {
      var d = new Date(Date.UTC(A.y, A.m - 1, A.d + i)), b = document.createElement("button");
      b.type = "button"; b.className = "rw__zi"; b.dataset.data = iso(d); b.setAttribute("aria-pressed", "false");
      b.setAttribute("aria-label", (i === 0 ? "azi, " : i === 1 ? "mâine, " : "") + ziL(iso(d)));
      b.innerHTML = "<small>" + (i === 0 ? "azi" : i === 1 ? "mâine" : ZILE[d.getUTCDay()]) + "</small><b>" + d.getUTCDate() + "</b><em>" + LUNI[d.getUTCMonth()] + "</em>";
      b.addEventListener("click", function () { sel.data = this.dataset.data; sel.ora = null; sel.interval = null; cereDisponibilitate(); pinta(); });
      cZile.appendChild(b);
    }
    function cereDisponibilitate() {
      libere = null;
      if (!CFG.disponibilitate || !sel.data) return;
      var n = ++pedido;
      fetch(CFG.disponibilitate + (CFG.disponibilitate.indexOf("?") < 0 ? "?" : "&") + "data=" + sel.data)
        .then(function (r) { return r.ok ? r.json() : null; })
        .then(function (j) { if (n === pedido && j && typeof j === "object") { libere = j; el("rw-legenda").hidden = false; pinta(); } })
        .catch(function () {});
    }
    function stare(h) {
      if (trecuta(h)) return "trecut";
      if (!libere || libere[h] == null) return "";
      var l = +libere[h];
      return l <= 0 ? "plin" : l <= 3 ? "putine" : "liber";
    }
    function eticheta(s, h) {
      return s === "trecut" ? "prea curând" : s === "plin" ? "complet · listă de așteptare" : s === "putine" ? (+libere[h] === 1 ? "o masă" : libere[h] + " mese") : s === "liber" ? "liber" : "";
    }
    function pintaOre(cont, lista, interval) {
      cont.innerHTML = "";
      lista.forEach(function (h) {
        var s = sel.data ? stare(h) : "", e = sel.data ? eticheta(s, h) : "", b = document.createElement("button");
        b.type = "button"; b.className = "rw__ora"; b.dataset.ora = h; b.dataset.interval = interval;
        if (s) b.dataset.stare = s;
        b.disabled = !sel.data || s === "trecut";
        b.setAttribute("aria-pressed", sel.ora === h ? "true" : "false");
        b.innerHTML = "<b>" + h + "</b>" + (e ? "<span>" + e + "</span>" : "");
        b.addEventListener("click", function () { sel.ora = this.dataset.ora; sel.interval = this.dataset.interval; pinta(); });
        cont.appendChild(b);
      });
    }
    function pinta() {
      err.hidden = true;                          // qualquer escolha nova apaga o aviso anterior
      [].forEach.call(cZile.children, function (b) { b.setAttribute("aria-pressed", b.dataset.data === sel.data ? "true" : "false"); });
      pintaOre(cPranz, CFG.pranz, "pranz"); pintaOre(cSeara, CFG.seara, "seara");
      outN.textContent = sel.persoane;
      el("rw-nota-pers").textContent = sel.persoane > 12 ? "Pentru " + persL(sel.persoane) + ", masa și meniul se stabilesc la confirmare." : "Pentru grupuri mari, stabilim masa împreună la confirmare.";
      [].forEach.call(el("rw-locuri").children, function (b) { b.setAttribute("aria-pressed", b.dataset.loc === sel.zona ? "true" : "false"); });
      var nota = el("rw-nota-ora");
      if (sel.data === azi && CFG.pranz.concat(CFG.seara).every(trecuta)) nota.innerHTML = 'Pentru astăzi nu mai sunt ore disponibile online. Sunați: <a href="tel:' + CFG.telefon + '">' + telL(CFG.telefon) + "</a>.";
      else nota.textContent = (sel.data === azi ? "Pentru astăzi, cu cel puțin o oră înainte. " : "") + "Orele sunt orientative: restaurantul confirmă ora exactă.";
      if (sel.data && sel.ora) {
        rez.innerHTML = "<b>" + persL(sel.persoane) + "</b> · <b>" + ziL(sel.data) + "</b> · <b>ora " + sel.ora + "</b> · " + LOC_L[sel.zona] + (stare(sel.ora) === "plin" ? " · <b>listă de așteptare</b>" : "");
      } else rez.textContent = sel.data ? "Acum alegeți ora." : "Alegeți ziua și ora.";
    }
    el("rw-minus").addEventListener("click", function () { sel.persoane = Math.max(1, sel.persoane - 1); pinta(); });
    el("rw-plus").addEventListener("click", function () { sel.persoane = Math.min(30, sel.persoane + 1); pinta(); });
    [].forEach.call(el("rw-locuri").children, function (b) { b.addEventListener("click", function () { sel.zona = this.dataset.loc; pinta(); }); });
    pinta();

    form.addEventListener("submit", function (e) {
      e.preventDefault(); err.hidden = true;
      var nume = form.nume.value.trim(), tel = form.telefon.value.trim(), email = form.email.value.trim(), foc = null, problema = "";
      if (!sel.data) { problema = "Alegeți ziua."; foc = cZile.querySelector(".rw__zi"); }
      else if (!sel.ora) { problema = "Alegeți ora."; foc = rw.querySelector(".rw__ora:not(:disabled)"); }
      else if (!nume) { problema = "Scrieți-ne numele."; foc = form.nume; }
      else if (tel.replace(/\D/g, "").length < 9) { problema = "Lăsați-ne un număr de telefon, ca restaurantul să vă poată confirma."; foc = form.telefon; }
      else if (email && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) { problema = "Adresa de e-mail nu pare corectă."; foc = form.email; }
      else if (!el("rw-acord").checked) { problema = "Bifați acordul pentru folosirea datelor."; foc = el("rw-acord"); }
      if (problema) { err.textContent = problema; err.hidden = false; if (foc) foc.focus(); return; }
      var c = { data: sel.data, ora: sel.ora, interval: sel.interval, persoane: sel.persoane, zona: sel.zona, nume: nume, telefon: tel, email: email,
                observatii: form.observatii.value.trim(), lista_asteptare: stare(sel.ora) === "plin", limba: "ro", sursa: "web" };
      var btn = el("rw-trimite"); btn.disabled = true; btn.textContent = "Se trimite…";
      trimite(c).then(function (r) { btn.disabled = false; btn.textContent = "Trimite cererea"; arata(c, r); });
    });
    function trimite(c) {
      if (CFG.endpoint) {
        return fetch(CFG.endpoint, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(c) })
          .then(function (r) { return r.ok; }).catch(function () { return false; });
      }
      if (CFG.netlify && /^https?:$/.test(location.protocol)) {
        var campuri = { "form-name": "rezervare", "adresa-web": "" };
        Object.keys(c).forEach(function (k) { campuri[k] = typeof c[k] === "boolean" ? (c[k] ? "da" : "nu") : String(c[k]); });
        return fetch("/", { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body: new URLSearchParams(campuri).toString() })
          .then(function (r) { return r.ok; }).catch(function () { return false; });
      }
      return Promise.resolve(null);
    }
    function arata(c, r) {
      var date = [["Ziua", ziL(c.data)], ["Ora", c.ora], ["Persoane", String(c.persoane)], ["Locul", LOC_L[c.zona]], ["Nume", c.nume], ["Telefon", c.telefon]];
      if (c.email) date.push(["E-mail", c.email]);
      if (c.lista_asteptare) date.push(["Stare", "listă de așteptare: vă anunțăm dacă se eliberează o masă"]);
      if (c.observatii) date.push(["Observații", c.observatii]);
      el("rw-ok-date").innerHTML = date.map(function (x) { return "<dt>" + x[0] + "</dt><dd>" + esc(x[1]) + "</dd>"; }).join("");
      el("rw-ok-t").textContent = r === true ? "Cererea a fost trimisă" : r === false ? "Cererea nu a plecat" : "Mai e un pas";
      el("rw-ok-p").textContent = r === true ? "Restaurantul vă confirmă rezervarea prin telefon sau e-mail. Pentru un răspuns imediat, sunați."
        : r === false ? "Nu am putut trimite cererea de pe site. Trimiteți-o pe e-mail sau sunați: datele de mai jos sunt deja completate."
        : "Trimiteți cererea pe e-mail sau sunați: datele de mai jos sunt deja completate.";
      var mesaj = "Bună ziua! Aș dori să rezerv o masă la Casa Bolta Rece: " + ziL(c.data) + ", ora " + c.ora + ", " + persL(c.persoane) + (c.zona !== "oriunde" ? ", " + LOC_L[c.zona] : "") +
        ". Nume: " + c.nume + ". Telefon: " + c.telefon + (c.observatii ? ". Observații: " + c.observatii : "") + (c.lista_asteptare ? " (listă de așteptare)" : "") + ".";
      var acts = el("rw-ok-acts"); acts.innerHTML = "";
      var link = function (cls, txt, href, rel) { var a = document.createElement("a"); a.className = "btn " + cls; a.textContent = txt; a.href = href; if (rel) a.rel = rel; acts.appendChild(a); };
      if (r !== true) link("btn--primary", "Trimiteți pe e-mail", "mailto:" + CFG.email + "?subject=" + encodeURIComponent("Rezervare: " + ziL(c.data) + ", ora " + c.ora) + "&body=" + encodeURIComponent(mesaj));
      link(r === true ? "btn--primary" : "btn--ghost", "Sunați: " + telL(CFG.telefon), "tel:" + CFG.telefon);
      if (CFG.whatsapp && r !== true) link("btn--ghost", "Trimiteți pe WhatsApp", "https://wa.me/" + CFG.whatsapp.replace(/\D/g, "") + "?text=" + encodeURIComponent(mesaj), "noopener");
      if (r !== true) {
        var cp = document.createElement("button"); cp.type = "button"; cp.className = "btn btn--ghost"; cp.textContent = "Copiați cererea";
        cp.addEventListener("click", function () { if (navigator.clipboard) navigator.clipboard.writeText(mesaj).then(function () { cp.textContent = "Copiată"; }); });
        acts.appendChild(cp);
        var mod = document.createElement("button"); mod.type = "button"; mod.className = "rw__modifica"; mod.textContent = "Modificați cererea";
        mod.addEventListener("click", function () { rw.removeAttribute("data-faza"); ok.classList.remove("on"); form.nume.focus(); });
        acts.appendChild(mod);
      }
      rw.setAttribute("data-faza", "ok"); ok.classList.add("on");
      rw.scrollIntoView({ behavior: reduzido ? "auto" : "smooth", block: "start" });
      ok.focus({ preventScroll: true });
    }
  }

  var ano = document.getElementById("ano");
  if (ano) ano.textContent = new Date().getFullYear();
})();
