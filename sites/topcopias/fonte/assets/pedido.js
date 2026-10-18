/* TopCopias · pedido online
   Lee el PDF en el navegador (pdf.js), cuenta páginas, detecta qué páginas llevan color,
   calcula el precio con assets/precios.js y envía el pedido por Netlify Forms. */
(function () {
  "use strict";
  var P = window.TC_PRECIOS, N = window.TC_NEGOCIO, MODO = window.TC_MODO || "web";
  if (!P) return;

  var BASE = (function () {
    var s = document.querySelector('script[src*="pedido.js"]');
    return s ? s.src.replace(/pedido\.js.*$/, "") : "assets/";
  })();
  var LIMITE_ENVIO = 8 * 1024 * 1024;   // Netlify Forms: 8 MB por envío
  var MAX_ANALISIS = 600;                // páginas analizadas para color

  var eur = function (n) { return n.toLocaleString("es-ES", { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + " €"; };
  var eur3 = function (n) { return n.toLocaleString("es-ES", { minimumFractionDigits: 3, maximumFractionDigits: 3 }) + " €"; };
  var mb = function (b) { return b < 1048576 ? Math.max(1, Math.round(b / 1024)) + " KB" : (b / 1048576).toLocaleString("es-ES", { maximumFractionDigits: 1 }) + " MB"; };
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ---------- Cálculo ---------- */
  function tramo(lista, n) { var p = lista[0][1]; for (var i = 0; i < lista.length; i++) if (n >= lista[i][0]) p = lista[i][1]; return p; }
  function precioEspiral(hojas) { var t = P.acabados.espiral.tramos_hojas; for (var i = 0; i < t.length; i++) if (hojas <= t[i][0]) return t[i][1]; return null; }

  // docs: [{pages, colorPages, copies}] · op: {color, caras, pps, formato, papel, acabado, entrega}
  function calcular(docs, op) {
    var bnCaras = 0, colCaras = 0, hojasTot = 0, acabadoTot = 0, avisos = [], copiasTot = 0;
    var ac = P.acabados[op.acabado];
    docs.forEach(function (d) {
      if (!d.pages) return;
      var colP = op.color === "bn" ? 0 : op.color === "color" ? d.pages : (d.colorPages || 0);
      var caras = Math.ceil(d.pages / op.pps);
      var colC = Math.min(caras, Math.ceil(colP / op.pps));
      var bnC = caras - colC;
      var hojas = op.caras === "doble" ? Math.ceil(caras / 2) : caras;
      bnCaras += bnC * d.copies; colCaras += colC * d.copies; hojasTot += hojas * d.copies; copiasTot += d.copies;
      if (op.acabado === "espiral") {
        var pe = precioEspiral(hojas);
        if (pe === null) { avisos.push("«" + d.name + "» tiene " + hojas + " hojas: para espiral de más de 400 hojas te damos precio en tienda."); pe = P.acabados.espiral.tramos_hojas.slice(-1)[0][1]; }
        acabadoTot += pe * d.copies;
      } else if (ac && ac.precio) {
        if (ac.max_hojas && hojas > ac.max_hojas) avisos.push("«" + d.name + "» tiene " + hojas + " hojas y el " + ac.etiqueta.toLowerCase() + " admite hasta " + ac.max_hojas + ". Te recomendamos espiral.");
        acabadoTot += ac.precio * d.copies;
      }
    });
    var mult = P.formato[op.formato].multiplicador;
    var pBn = tramo(P.tramos.bn, bnCaras) * mult, pCol = tramo(P.tramos.color, colCaras) * mult;
    var papel = P.papel[op.papel].por_hoja * mult * hojasTot;
    var lineas = [];
    if (bnCaras) lineas.push(["B/N · " + bnCaras + " caras × " + eur3(pBn), bnCaras * pBn]);
    if (colCaras) lineas.push(["Color · " + colCaras + " caras × " + eur3(pCol), colCaras * pCol]);
    if (papel) lineas.push(["Papel " + op.papel + " g · " + hojasTot + " hojas", papel]);
    if (acabadoTot) lineas.push([ac.etiqueta + " · " + copiasTot + " ud.", acabadoTot]);
    var sub = lineas.reduce(function (s, l) { return s + l[1]; }, 0);
    if (op.entrega === "envio" && sub > 0) {
      var gratis = sub >= P.envio.gratis_desde;
      lineas.push([gratis ? "Envío península · gratis" : "Envío península", gratis ? 0 : P.envio.precio]);
      if (!gratis) sub += P.envio.precio;
    }
    return { lineas: lineas, total: Math.round(sub * 100) / 100, hojas: hojasTot, bn: bnCaras, col: colCaras, avisos: avisos };
  }
  window.TC_calcular = calcular;

  function htmlTicket(r, titulo, extra) {
    var h = '<h4><span>' + titulo + '</span><span>' + (extra || "") + '</span></h4>';
    r.lineas.forEach(function (l) { h += '<div class="fila"><span>' + l[0] + '</span><span>' + eur(l[1]) + '</span></div>'; });
    h += '<div class="fila total"><span>Total</span><span>' + eur(r.total) + '</span></div>';
    return h;
  }

  /* ---------- Ticket de ejemplo del hero ---------- */
  var ej = $("#ticket-ejemplo");
  if (ej) {
    var r0 = calcular([{ name: "ejemplo", pages: 148, colorPages: 12, copies: 1 }], { color: "auto", caras: "doble", pps: 1, formato: "A4", papel: "80", acabado: "espiral", entrega: "tienda" });
    ej.querySelector(".cuerpo").innerHTML = htmlTicket(r0, "Apuntes-Derecho-Civil.pdf", "148 págs") + '<div class="tintas"><i></i><i></i><i></i><i></i></div>';
  }

  /* ---------- Herramienta ---------- */
  var raiz = $("#pedido");
  var docs = [], uid = 0;

  function leerOpciones() {
    var v = function (n) { var e = $('input[name="' + n + '"]:checked', raiz); return e ? e.value : null; };
    return { color: v("op_color"), caras: v("op_caras"), pps: +v("op_pps"), formato: v("op_formato"), papel: v("op_papel"), acabado: v("op_acabado"), entrega: v("entrega") || "tienda" };
  }

  var pdfjsPromesa = null;
  function cargarPdfjs() {
    if (window.pdfjsLib) return Promise.resolve(window.pdfjsLib);
    if (!pdfjsPromesa) pdfjsPromesa = new Promise(function (ok, ko) {
      var s = document.createElement("script");
      s.src = BASE + "vendor/pdf.min.js";
      s.onload = function () { window.pdfjsLib.GlobalWorkerOptions.workerSrc = BASE + "vendor/pdf.worker.min.js"; ok(window.pdfjsLib); };
      s.onerror = ko; document.head.appendChild(s);
    });
    return pdfjsPromesa;
  }

  function esColor(ctx, w, h) {
    var d = ctx.getImageData(0, 0, w, h).data, n = 0, tot = w * h;
    for (var i = 0; i < d.length; i += 4) {
      var mx = Math.max(d[i], d[i + 1], d[i + 2]), mn = Math.min(d[i], d[i + 1], d[i + 2]);
      if (mx - mn > 48) n++;
    }
    return n / tot > 0.002;
  }

  function analizarPdf(doc) {
    return cargarPdfjs().then(function (lib) {
      return doc.file.arrayBuffer().then(function (buf) { return lib.getDocument({ data: buf }).promise; });
    }).then(function (pdf) {
      doc.pages = pdf.numPages; doc.colorPages = 0; doc.analizadas = 0; pintar();
      var lim = Math.min(pdf.numPages, MAX_ANALISIS), i = 1;
      var cv = document.createElement("canvas"), ctx = cv.getContext("2d", { willReadFrequently: true });
      function siguiente() {
        if (i > lim || doc.quitado) { doc.analizando = false; if (pdf.numPages > lim) doc.parcial = true; pintar(); return; }
        return pdf.getPage(i).then(function (pg) {
          var vp0 = pg.getViewport({ scale: 1 });
          var esc = (i === 1 ? 112 : 60) / vp0.width, vp = pg.getViewport({ scale: esc });
          cv.width = Math.ceil(vp.width); cv.height = Math.ceil(vp.height);
          ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, cv.width, cv.height);
          return pg.render({ canvasContext: ctx, viewport: vp }).promise.then(function () {
            if (i === 1) doc.thumb = cv.toDataURL("image/jpeg", .7);
            if (esColor(ctx, cv.width, cv.height)) doc.colorPages++;
            doc.analizadas = i; i++;
            if (i % 8 === 0 || i > lim) pintar();
            return siguiente();
          });
        });
      }
      return siguiente();
    }).catch(function () {
      doc.analizando = false; doc.error = "No hemos podido leer este PDF. Indica el número de páginas."; doc.manual = true; pintar();
    });
  }

  function analizarImagen(doc) {
    var url = URL.createObjectURL(doc.file), img = new Image();
    img.onload = function () {
      var cv = document.createElement("canvas"), w = 80, h = Math.round(80 * img.height / img.width) || 100;
      cv.width = w; cv.height = h; var ctx = cv.getContext("2d", { willReadFrequently: true });
      ctx.drawImage(img, 0, 0, w, h);
      doc.thumb = cv.toDataURL("image/jpeg", .7); doc.pages = 1; doc.colorPages = esColor(ctx, w, h) ? 1 : 0;
      doc.analizando = false; URL.revokeObjectURL(url); pintar();
    };
    img.onerror = function () { doc.analizando = false; doc.manual = true; pintar(); };
    img.src = url;
  }

  function anadir(files) {
    Array.prototype.forEach.call(files, function (f) {
      var d = { id: ++uid, file: f, name: f.name, size: f.size, copies: 1, pages: 0, colorPages: 0, analizando: true };
      docs.push(d);
      if (/pdf$/i.test(f.type) || /\.pdf$/i.test(f.name)) analizarPdf(d);
      else if (/^image\//.test(f.type)) analizarImagen(d);
      else { d.analizando = false; d.manual = true; }
    });
    pintar();
  }
  window.TC_anadir = anadir;

  function pintar() {
    if (!raiz) return;
    var lista = $("#lista-archivos", raiz);
    lista.innerHTML = "";
    docs.forEach(function (d) {
      var el = document.createElement("div"); el.className = "archivo";
      var det = d.analizando ? (d.pages ? "Analizando color " + (d.analizadas || 0) + "/" + Math.min(d.pages, MAX_ANALISIS) + "…" : "Leyendo páginas…")
        : d.manual ? (d.error || "Indica el número de páginas")
        : d.pages + (d.pages === 1 ? " página" : " páginas") + (d.colorPages ? ' · <span class="c">' + d.colorPages + " en color</span>" : " · todo B/N") + (d.parcial ? " (color analizado en las " + MAX_ANALISIS + " primeras)" : "");
      el.innerHTML =
        (d.thumb ? '<img class="mini" alt="" src="' + d.thumb + '">' : '<div class="mini" aria-hidden="true"></div>') +
        '<div style="min-width:0"><div class="nom"></div><div class="det">' + det + " · " + mb(d.size) + "</div>" +
        (d.manual ? '<label class="paginas-manual">Páginas <input type="number" min="1" inputmode="numeric" data-pag="' + d.id + '" value="' + (d.pages || "") + '"></label>' : "") + "</div>" +
        '<div class="acc"><div class="copias" role="group" aria-label="Copias"><button type="button" data-menos="' + d.id + '" aria-label="Una copia menos">−</button><input type="number" min="1" inputmode="numeric" aria-label="Copias" data-cop="' + d.id + '" value="' + d.copies + '"><button type="button" data-mas="' + d.id + '" aria-label="Una copia más">+</button></div><button type="button" class="quitar" data-quitar="' + d.id + '">Quitar</button></div>';
      el.querySelector(".nom").textContent = d.name;
      lista.appendChild(el);
    });
    $("#zona-vacia", raiz).hidden = docs.length > 0;
    $("#zona-mas", raiz).hidden = docs.length === 0;
    recalcular();
  }

  function buscar(id) { for (var i = 0; i < docs.length; i++) if (docs[i].id === +id) return docs[i]; }

  function recalcular() {
    if (!raiz) return;
    var op = leerOpciones(), r = calcular(docs, op), box = $("#resumen-ticket", raiz);
    var listos = docs.filter(function (d) { return d.pages > 0; });
    var analizando = docs.some(function (d) { return d.analizando; });
    $("#envio-campos", raiz).hidden = op.entrega !== "envio";
    $("#tienda-campos", raiz).hidden = op.entrega === "envio";
    $$('[data-solo-envio]', raiz).forEach(function (e) { e.required = op.entrega === "envio"; });
    var avisoAcabado = $("#aviso-acabado", raiz);
    avisoAcabado.textContent = r.avisos.join(" "); avisoAcabado.hidden = !r.avisos.length;
    if (!listos.length) {
      box.innerHTML = '<h4><span>Tu pedido</span><span></span></h4><p class="vacio">' + (analizando ? "Leyendo tu archivo…" : "Sube un PDF y aquí verás el precio exacto, línea a línea, antes de enviar nada.") + "</p>";
    } else {
      var paginas = listos.reduce(function (s, d) { return s + d.pages * d.copies; }, 0);
      box.innerHTML = htmlTicket(r, listos.length === 1 ? listos[0].name : listos.length + " archivos", paginas + " págs · " + r.hojas + " hojas") + '<div class="tintas"><i></i><i></i><i></i><i></i></div>';
    }
    var barra = $("#barra-total");
    if (barra) {
      $(".mono", barra).textContent = eur(r.total);
      $("small", barra).textContent = listos.length ? r.hojas + " hojas · IVA incl." : "";
      var ver = listos.length > 0 && !(window.__formVisible);
      barra.classList.toggle("visible", ver); document.body.classList.toggle("con-barra", ver);
    }
    var btn = $("#btn-enviar", raiz);
    btn.disabled = !listos.length || analizando;
    $("#btn-enviar-txt", raiz).textContent = listos.length ? "Enviar pedido · " + eur(r.total) : "Enviar pedido";
    var peso = docs.reduce(function (s, d) { return s + d.size; }, 0), avP = $("#aviso-peso", raiz);
    avP.hidden = peso <= LIMITE_ENVIO;
    avP.textContent = "Tus archivos pesan " + mb(peso) + ". Enviaremos el pedido con el precio y te pediremos los archivos por WhatsApp o en " + N.email_pedidos + " indicando tu código de pedido.";
    return r;
  }

  if (raiz) {
    raiz.addEventListener("change", function (e) {
      var t = e.target;
      if (t.matches('input[type="file"][data-subir]')) { anadir(t.files); t.value = ""; return; }
      if (t.dataset.cop) { var d = buscar(t.dataset.cop); d.copies = Math.max(1, Math.min(999, parseInt(t.value, 10) || 1)); pintar(); return; }
      if (t.dataset.pag) { var d2 = buscar(t.dataset.pag); d2.pages = Math.max(0, parseInt(t.value, 10) || 0); d2.colorPages = 0; recalcular(); return; }
      recalcular();
    });
    raiz.addEventListener("click", function (e) {
      var t = e.target.closest("button"); if (!t) return;
      if (t.dataset.mas) { buscar(t.dataset.mas).copies++; pintar(); }
      if (t.dataset.menos) { var d = buscar(t.dataset.menos); d.copies = Math.max(1, d.copies - 1); pintar(); }
      if (t.dataset.quitar) { var q = buscar(t.dataset.quitar); q.quitado = true; docs = docs.filter(function (x) { return x !== q; }); pintar(); }
    });
    $$(".dropzone", raiz).forEach(arrastre);
    var formEl = $("#form-pedido");
    if ("IntersectionObserver" in window && formEl) {
      new IntersectionObserver(function (en) { window.__formVisible = en[0].isIntersecting; recalcular(); }, { threshold: .1 }).observe(formEl);
    }
    pintar();
  }

  function arrastre(z) {
    ["dragenter", "dragover"].forEach(function (ev) { z.addEventListener(ev, function (e) { e.preventDefault(); z.classList.add("encima"); }); });
    ["dragleave", "drop"].forEach(function (ev) { z.addEventListener(ev, function (e) { e.preventDefault(); z.classList.remove("encima"); }); });
    z.addEventListener("drop", function (e) {
      if (!e.dataTransfer || !e.dataTransfer.files.length) return;
      if (raiz) { anadir(e.dataTransfer.files); if (!raiz.contains(z)) irAPedido(); }
    });
  }

  // Zona de subida del hero: los archivos pasan a la herramienta de la misma página
  var hero = $("#subida-hero");
  if (hero) {
    arrastre(hero);
    var inp = $("input", hero);
    inp.addEventListener("change", function () { if (raiz && inp.files.length) { anadir(inp.files); irAPedido(); } inp.value = ""; });
  }
  function irAPedido() { var s = $("#imprimir"); if (s) s.scrollIntoView({ behavior: "smooth", block: "start" }); }

  /* ---------- Envío del pedido ---------- */
  function codigo() {
    var f = new Date(), a = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789", c = "";
    for (var i = 0; i < 4; i++) c += a[Math.floor(Math.random() * a.length)];
    return "TC-" + ("0" + f.getDate()).slice(-2) + ("0" + (f.getMonth() + 1)).slice(-2) + "-" + c;
  }

  function resumenTexto(r, op) {
    var t = [];
    docs.filter(function (d) { return d.pages; }).forEach(function (d) {
      t.push("• " + d.name + " — " + d.pages + " págs (" + (op.color === "auto" ? d.colorPages + " en color" : op.color === "bn" ? "todo B/N" : "todo color") + ") × " + d.copies + " copia(s)");
    });
    t.push("Opciones: " + op.formato + ", " + (op.caras === "doble" ? "doble cara" : "una cara") + ", " + op.pps + " pág/cara, papel " + op.papel + " g, " + P.acabados[op.acabado].etiqueta + ", color: " + op.color);
    r.lineas.forEach(function (l) { t.push(l[0] + ": " + eur(l[1])); });
    t.push("TOTAL: " + eur(r.total) + " (IVA incl., precios de referencia)");
    return t.join("\n");
  }

  var form = $("#form-pedido");
  if (form) form.addEventListener("submit", function (e) {
    e.preventDefault();
    var err = $("#form-error"); err.hidden = true;
    if (!form.checkValidity()) { form.reportValidity(); return; }
    var op = leerOpciones(), r = recalcular(), cod = codigo();
    $("#f-codigo").value = cod; $("#f-total").value = eur(r.total); $("#f-resumen").value = resumenTexto(r, op);
    var fd = new FormData(form), peso = 0, conArchivos = docs.reduce(function (s, d) { return s + d.size; }, 0) <= LIMITE_ENVIO;
    if (conArchivos) docs.slice(0, 5).forEach(function (d, i) { fd.set("archivo" + (i + 1), d.file, d.name); peso += d.size; });
    if (docs.length > 5) conArchivos = false;
    fd.set("archivos_adjuntos", conArchivos ? "sí" : "no: pedir por WhatsApp/email");
    var btn = $("#btn-enviar"); btn.disabled = true; $("#btn-enviar-txt").textContent = "Enviando…";
    var envio = MODO === "preview" ? new Promise(function (ok) { setTimeout(ok, 700); }) :
      fetch(form.getAttribute("action") || "/", { method: "POST", body: fd }).then(function (res) { if (!res.ok) throw new Error(res.status); });
    envio.then(function () { exito(cod, r, op, conArchivos, fd.get("nombre"), fd.get("tienda")); })
      .catch(function () {
        err.hidden = false; err.textContent = "No se ha podido enviar. Revisa tu conexión y vuelve a intentarlo, o escríbenos por WhatsApp al " + N.whatsapp_texto + ".";
        btn.disabled = false; recalcular();
      });
  });

  function exito(cod, r, op, conArchivos, nombre, tiendaId) {
    var t = N.tiendas.filter(function (x) { return x.id === tiendaId; })[0] || N.tiendas[0];
    var msg = "Hola, soy " + nombre + ". Acabo de hacer el pedido " + cod + " (" + eur(r.total) + ") en la web." + (conArchivos ? "" : " Os mando aquí los archivos.");
    var box = $("#exito");
    box.innerHTML =
      '<p class="eyebrow">Pedido recibido' + (MODO === "preview" ? " · demostración, no se ha enviado" : "") + "</p>" +
      "<h2>Gracias, " + escapar(nombre.split(" ")[0]) + ". Ya estamos con ello.</h2>" +
      '<div><span class="codigo">' + cod + "</span></div>" +
      "<p>" + (op.entrega === "envio" ? "Te avisaremos cuando salga hacia tu dirección." : "Te escribiremos por WhatsApp cuando esté listo para recoger en <b>" + t.direccion + "</b>. Pagas al recoger.") + "</p>" +
      (conArchivos ? "" : '<p class="aviso">Tus archivos pesan más de lo que admite el formulario. Envíanoslos por WhatsApp o a <b>' + N.email_pedidos + "</b> con el código " + cod + ".</p>") +
      '<div class="ticket">' + htmlTicket(r, cod, r.hojas + " hojas") + "</div>" +
      '<div class="hero-cta"><a class="btn btn--wa" href="https://wa.me/' + N.whatsapp + "?text=" + encodeURIComponent(msg) + '" target="_blank" rel="noopener">Confirmar por WhatsApp</a></div>';
    $("#form-pedido").hidden = true; box.hidden = false;
    var barra = $("#barra-total"); if (barra) { barra.classList.remove("visible"); document.body.classList.remove("con-barra"); }
    box.scrollIntoView({ behavior: "smooth", block: "start" });
  }
  function escapar(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  var irForm = $("#barra-ir");
  if (irForm) irForm.addEventListener("click", function () { $("#form-pedido").scrollIntoView({ behavior: "smooth", block: "start" }); });
})();
