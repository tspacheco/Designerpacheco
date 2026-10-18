#!/usr/bin/env python3
"""TopCopias · gerador do site (ES).

  python3 build.py           -> ../site/     (Netlify: URLs bonitas, formulário real)
  python3 build.py preview   -> ../preview/  (links para index.html, formulário em modo demonstração)

Preços em data/precios.json, dados da loja em data/negocio.json.
"""
import json, os, shutil, sys, html

AQUI = os.path.dirname(os.path.abspath(__file__))
MODO = "preview" if len(sys.argv) > 1 and sys.argv[1] == "preview" else "web"
SAIDA = os.path.join(AQUI, "..", "preview" if MODO == "preview" else "site")
P = json.load(open(os.path.join(AQUI, "data", "precios.json"), encoding="utf-8"))
N = json.load(open(os.path.join(AQUI, "data", "negocio.json"), encoding="utf-8"))
DOMINIO = "https://topcopias.com"
T1, T2 = N["tiendas"]
WA = "https://wa.me/" + N["whatsapp"]
e = html.escape


def eur(x, d=2):
    return f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".") + " €"


# ---------- Iconos (trazo 1.8, tinta) ----------
def ico(nombre, cls=""):
    p = {
        "subir": '<path d="M12 15V4m0 0L7.5 8.5M12 4l4.5 4.5"/><path d="M5 14v4.5A1.5 1.5 0 0 0 6.5 20h11a1.5 1.5 0 0 0 1.5-1.5V14"/>',
        "estrella": '<path d="m12 3.5 2.6 5.3 5.9.9-4.3 4.1 1 5.8L12 16.9l-5.2 2.7 1-5.8-4.3-4.1 5.9-.9z" fill="currentColor" stroke="none"/>',
        "gente": '<circle cx="9" cy="8" r="3.2"/><path d="M3.5 19c.6-3.2 2.8-5 5.5-5s4.9 1.8 5.5 5"/><circle cx="17" cy="9" r="2.4"/><path d="M15.6 14.2c2.4-.3 4.3 1.2 4.9 4.3"/>',
        "euro": '<path d="M17 6.5A6.5 6.5 0 1 0 17 17.5"/><path d="M4.5 10.5h9m-9 3h8"/>',
        "apuntes": '<path d="M6 3.5h9l3.5 3.5v13.5H6z"/><path d="M15 3.5V7h3.5M9 11h6.5M9 14h6.5M9 17h4"/>',
        "color": '<circle cx="9" cy="10" r="4.6"/><circle cx="15" cy="10" r="4.6"/><circle cx="12" cy="15" r="4.6"/>',
        "espiral": '<rect x="7" y="4" width="12" height="16" rx="1"/><path d="M4.5 6.5h4m-4 3h4m-4 3h4m-4 3h4"/>',
        "flyer": '<path d="M4 6.5 14 4l1.5 13.5-10 2.5z"/><path d="M15.5 6 20 7l-1.5 12.5-3-.4"/>',
        "tarjeta": '<rect x="3" y="6" width="18" height="12" rx="1.5"/><path d="M7 10.5h6M7 13.5h4"/>',
        "envio": '<path d="M3 7.5h11v9H3zM14 10.5h4l3 3v3h-7z"/><circle cx="7" cy="17.5" r="1.7"/><circle cx="17.5" cy="17.5" r="1.7"/>',
        "wa": '<path d="M12 3.2a8.7 8.7 0 0 0-7.5 13.2L3.3 20.8l4.6-1.2A8.7 8.7 0 1 0 12 3.2z" fill="currentColor" stroke="none"/><path d="M9 8.3c.2-.4.4-.4.7-.4h.5c.2 0 .4 0 .5.4l.7 1.7c.1.2 0 .4-.1.6l-.5.6c-.1.1-.2.3 0 .5.5.9 1.3 1.7 2.3 2.2.2.1.4.1.5-.1l.6-.7c.2-.2.4-.2.6-.1l1.6.8c.2.1.4.2.4.4 0 .5-.2 1.1-.7 1.4-.5.4-1.4.6-2.6.2-1.4-.5-2.9-1.6-3.9-3-.8-1.1-1.1-2.1-1-2.9 0-.7.2-1.2.5-1.6z" fill="#fff" stroke="none"/>',
        "mapa": '<path d="M12 21s-6.5-6-6.5-11a6.5 6.5 0 0 1 13 0c0 5-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.4"/>',
        "tel": '<path d="M6.5 3.5h3l1.5 4-2 1.3a10 10 0 0 0 6.2 6.2l1.3-2 4 1.5v3a2 2 0 0 1-2.2 2A16.5 16.5 0 0 1 4.5 5.7a2 2 0 0 1 2-2.2z"/>',
    }[nombre]
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>'


LOGO_SVG = ('<svg viewBox="0 0 48 48" aria-hidden="true"><g style="mix-blend-mode:multiply">'
            '<circle cx="19" cy="20" r="11" fill="#0094D4"/><circle cx="29" cy="20" r="11" fill="#E2007A" opacity=".92"/>'
            '<circle cx="24" cy="29" r="11" fill="#FFD21F" opacity=".95"/></g>'
            '<path d="M14 14h20v4h-8v17h-4V18h-8z" fill="#141619"/></svg>')


# ---------- Enlaces ----------
def url(destino, prof):
    """destino: '' (inicio), 'imprimir', 'precios'... ; prof: profundidad de la página actual."""
    pre = "../" * prof
    if MODO == "preview":
        return pre + (destino + "/" if destino else "") + "index.html"
    return pre + (destino + "/" if destino else "")


NAV = [("imprimir", "Imprimir online"), ("servicios", "Servicios"), ("precios", "Precios"), ("tiendas", "Tiendas")]


def cabecera(actual, prof):
    items = "".join(
        f'<a href="{url(k, prof)}"{" aria-current=\"page\"" if k == actual else ""}>{v}</a>' for k, v in NAV if k != "imprimir"
    )
    ir = url("", prof) + "#imprimir" if actual == "" else url("imprimir", prof)
    return f'''<a class="sr" href="#contenido">Saltar al contenido</a>
<div class="promo"><div class="wrap"><span>Pide antes de las 13:00 y recógelo hoy</span><span class="promo-sep" aria-hidden="true">·</span><span>Envío gratis a la península desde {eur(P["envio"]["gratis_desde"])}</span></div></div>
<header class="cab"><div class="wrap">
  <a class="logo" href="{url('', prof)}" aria-label="TopCopias, inicio">{LOGO_SVG}<span><b>TopCopias</b><small>Copistería · Zaragoza</small></span></a>
  <button class="menu-btn" type="button" aria-label="Menú" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
  <nav class="nav" id="nav" aria-label="Principal">
    <a href="{url('imprimir', prof)}"{' aria-current="page"' if actual == 'imprimir' else ''}>Imprimir online</a>{items}
    <a class="btn btn--mag" href="{ir}">{ico('subir')}Sube tu PDF</a>
  </nav>
</div></header>'''


def pie(prof):
    tiendas = "".join(f'<li>{e(t["direccion"])}<br>{e(t["cp"])}<br><a href="tel:{t["tel"]}">{t["tel_texto"]}</a></li>' for t in N["tiendas"])
    return f'''<footer class="pie"><div class="wrap">
  <div>
    <a class="logo" href="{url('', prof)}">{LOGO_SVG}<span><b>TopCopias</b><small>Copistería · Zaragoza</small></span></a>
    <p style="margin-top:14px;max-width:34ch">Imprimimos tus apuntes, trabajos y documentos desde hace {N["anios"]} años. Sube el PDF, mira el precio y recógelo listo.</p>
    <div class="tintas-pie"><i></i><i></i><i></i><i></i></div>
  </div>
  <div><h4>Tiendas</h4><ul style="gap:12px">{tiendas}</ul></div>
  <div><h4>Contacto</h4><ul>
    <li><a href="{WA}" target="_blank" rel="noopener">WhatsApp {N["whatsapp_texto"]}</a></li>
    <li><a href="mailto:{N["email_pedidos"]}">{N["email_pedidos"]}</a></li>
    <li><a href="{N["instagram"]}" target="_blank" rel="noopener">Instagram</a></li>
    <li><a href="{N["facebook"]}" target="_blank" rel="noopener">Facebook</a></li>
  </ul></div>
  <div><h4>Web</h4><ul>
    <li><a href="{url('imprimir', prof)}">Imprimir online</a></li>
    <li><a href="{url('servicios', prof)}">Servicios</a></li>
    <li><a href="{url('precios', prof)}">Precios</a></li>
    <li><a href="{url('tiendas', prof)}">Tiendas</a></li>
  </ul></div>
  <div class="legal"><span>© 2026 {N["razon_social"]} · CIF {N["cif"]}</span>
    <span><a href="{url('aviso-legal', prof)}">Aviso legal</a> · <a href="{url('privacidad', prof)}">Privacidad</a> · <a href="{url('cookies', prof)}">Cookies</a></span></div>
</div></footer>
<a class="wa-flot" href="{WA}" target="_blank" rel="noopener" aria-label="Escríbenos por WhatsApp">{ico('wa')}</a>'''


FUENTES = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
           '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,500..900&family=IBM+Plex+Mono:wght@500;600;700&family=Public+Sans:wght@400;600;700&display=swap">')


def pagina(ruta, actual, titulo, desc, cuerpo, con_pedido=False, extra_head=""):
    prof = 0 if ruta == "" else ruta.count("/") + 1
    a = "../" * prof + "assets/"
    canon = DOMINIO + "/" + (ruta + "/" if ruta else "")
    scripts = f'<script src="{a}precios.js" charset="utf-8"></script><script src="{a}pedido.js" charset="utf-8"></script>' if con_pedido else ""
    head_comun = f'''<title>{e(titulo)}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:title" content="{e(titulo)}"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="website"><meta property="og:locale" content="es_ES">
<meta name="theme-color" content="#FFFFFF">
<link rel="icon" href="{a}favicon.svg" type="image/svg+xml">
{FUENTES}
<link rel="stylesheet" href="{a}site.css">{extra_head}'''
    corpo = f'''{cabecera(actual, prof)}
<main id="contenido">
{cuerpo}
</main>
{pie(prof)}
<script src="{a}site.js"></script>{'<script src="' + a + 'hero.js"></script>' if ruta == '' else ''}{scripts}'''
    if MODO == "preview" and ruta == "":
        # a página principal do artifact é embrulhada pelo próprio visor
        doc = head_comun + "\n" + corpo
    else:
        doc = f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
{head_comun}
</head><body>
{corpo}
</body></html>'''
    destino = os.path.join(SAIDA, ruta, "index.html") if ruta else os.path.join(SAIDA, "index.html")
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    open(destino, "w", encoding="utf-8").write(doc)


# ---------- Bloques ----------
def ticket_ejemplo_estatico():
    # mismo cálculo que pedido.js: 148 págs, 12 en color, doble cara, espiral
    bn, col = 136, 12
    pbn = [p for n, p in P["tramos"]["bn"] if bn >= n][-1]
    pcol = [p for n, p in P["tramos"]["color"] if col >= n][-1]
    hojas = 74
    esp = [p for n, p in P["acabados"]["espiral"]["tramos_hojas"] if hojas <= n][0]
    filas = [(f"B/N · {bn} caras × {eur(pbn, 3)}", bn * pbn), (f"Color · {col} caras × {eur(pcol, 3)}", col * pcol), ("Encuadernado en espiral · 1 ud.", esp)]
    tot = sum(x for _, x in filas)
    h = '<h4><span>Apuntes-Derecho-Civil.pdf</span><span>148 págs</span></h4>'
    h += "".join(f'<div class="fila"><span>{a}</span><span>{eur(b)}</span></div>' for a, b in filas)
    h += f'<div class="fila total"><span>Total</span><span>{eur(tot)}</span></div><div class="tintas"><i></i><i></i><i></i><i></i></div>'
    return h


def chip(nombre, valor, etiqueta, peque="", marcado=False, sw=""):
    i = f"{nombre}-{valor}"
    swh = f'<span class="sw" style="background:{sw}"></span>' if sw else ""
    return (f'<div class="chip"><input type="radio" name="{nombre}" id="{i}" value="{valor}"{" checked" if marcado else ""}>'
            f'<label for="{i}"><span>{swh}{etiqueta}</span>{f"<small>{peque}</small>" if peque else ""}</label></div>')


def herramienta(titulo_nivel="h2"):
    papel = "".join(chip("op_papel", k, v["etiqueta"].split(" · ")[0], v["etiqueta"].split(" · ")[1] + (f' · +{eur(v["por_hoja"])}/hoja' if v["por_hoja"] else " · incluido"), k == "80") for k, v in P["papel"].items())
    acab = []
    for k, v in P["acabados"].items():
        if k == "espiral":
            pr = "desde " + eur(v["tramos_hojas"][0][1])
        else:
            pr = eur(v["precio"]) if v["precio"] else "gratis"
        acab.append(chip("op_acabado", k, v["etiqueta"], f'{v["detalle"]} · {pr}', k == "ninguno"))
    tiendas_opts = "".join(chip("tienda", t["id"], t["nombre"], t["direccion"], i == 0) for i, t in enumerate(N["tiendas"]))
    archivos_ocultos = "".join(f'<input type="file" name="archivo{i}" hidden>' for i in range(1, 6))
    return f'''
<section class="seccion herramienta" id="imprimir" aria-labelledby="t-imprimir"><div class="wrap">
  <div class="seccion-cab">
    <p class="eyebrow">Imprimir online · recoger en tienda</p>
    <{titulo_nivel} id="t-imprimir">Sube tu PDF y mira el precio al momento</{titulo_nivel}>
    <p>Contamos las páginas y detectamos cuáles llevan color: solo pagas color donde hay color. Tu archivo no sale de tu móvil hasta que envías el pedido.</p>
  </div>
  <div class="pedido" id="pedido">
    <div class="panel">
      <div class="grupo">
        <h3><span class="mono">1</span> Tus archivos</h3>
        <label class="dropzone corte" id="zona-vacia">
          <input type="file" data-subir accept="application/pdf,.pdf,image/*" multiple aria-label="Elegir archivos para imprimir">
          {ico('subir', 'ico')}
          <strong><span class="solo-raton">Arrastra aquí tu PDF</span><span class="solo-tactil">Toca y elige tu PDF</span></strong>
          <span>o toca para elegirlo · PDF o imágenes, varios a la vez</span>
        </label>
        <div class="archivos" id="lista-archivos" aria-live="polite"></div>
        <label class="dropzone dropzone--mini" id="zona-mas" hidden>
          <input type="file" data-subir accept="application/pdf,.pdf,image/*" multiple aria-label="Añadir más archivos">
          {ico('subir', 'ico')}<span><strong>Añadir otro archivo</strong></span>
        </label>
      </div>

      <div class="opciones">
        <h3><span class="mono">2</span> Cómo lo quieres</h3>
        <fieldset class="grupo"><legend>Color</legend><div class="chips">
          {chip("op_color", "auto", "Automático", "Color solo donde hay color", True, "conic-gradient(#0094D4 0 33%,#E2007A 0 66%,#FFD21F 0)")}
          {chip("op_color", "bn", "Todo en B/N", "Lo más barato")}
          {chip("op_color", "color", "Todo en color", "Cada página a color")}
        </div></fieldset>
        <fieldset class="grupo"><legend>Caras</legend><div class="chips">
          {chip("op_caras", "doble", "Doble cara", "Mitad de hojas", True)}
          {chip("op_caras", "una", "Una cara")}
        </div></fieldset>
        <fieldset class="grupo"><legend>Páginas por cara</legend><div class="chips">
          {chip("op_pps", "1", "1 página", "Tamaño normal", True)}
          {chip("op_pps", "2", "2 páginas", "Ideal para apuntes y diapositivas")}
        </div></fieldset>
        <fieldset class="grupo"><legend>Tamaño</legend><div class="chips">
          {chip("op_formato", "A4", "A4", "21 × 29,7 cm", True)}
          {chip("op_formato", "A3", "A3", "29,7 × 42 cm · precio doble")}
        </div></fieldset>
        <fieldset class="grupo"><legend>Papel</legend><div class="chips">{papel}</div></fieldset>
        <fieldset class="grupo"><legend>Acabado (por copia)</legend><div class="chips">{"".join(acab)}</div>
          <p class="nota-op alerta" id="aviso-acabado" hidden></p></fieldset>
      </div>

      <form class="form" id="form-pedido" name="pedido" method="POST" action="/" data-netlify="true" netlify-honeypot="empresa" enctype="multipart/form-data">
        <h3><span class="mono">3</span> Tus datos y la recogida</h3>
        <input type="hidden" name="form-name" value="pedido">
        <p class="sr"><label>No rellenar <input name="empresa"></label></p>
        <input type="hidden" name="codigo" id="f-codigo"><input type="hidden" name="total" id="f-total">
        <input type="hidden" name="resumen" id="f-resumen"><input type="hidden" name="archivos_adjuntos">
        {archivos_ocultos}
        <fieldset class="grupo"><legend>Entrega</legend><div class="chips">
          {chip("entrega", "tienda", "Recoger en tienda", "Gratis · pagas al recoger", True)}
          {chip("entrega", "envio", "Envío a casa", f'Península · {P["envio"]["texto"]}, gratis desde {eur(P["envio"]["gratis_desde"])}')}
        </div></fieldset>
        <fieldset class="grupo" id="tienda-campos"><legend>¿En qué tienda?</legend><div class="chips">{tiendas_opts}</div>
          <p class="nota-op">Los pedidos que entran antes de las 13:00 se preparan el mismo día (según volumen). Te avisamos por WhatsApp.</p></fieldset>
        <div class="campos">
          <div class="campo"><label for="f-nombre">Nombre</label><input id="f-nombre" name="nombre" autocomplete="name" required></div>
          <div class="campo"><label for="f-tel">Móvil (WhatsApp)</label><input id="f-tel" name="telefono" type="tel" inputmode="tel" autocomplete="tel" required pattern="[+0-9 ]{{9,16}}"></div>
          <div class="campo campo--ancho"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
          <div class="campo campo--ancho" id="tienda-cuando"><label for="f-cuando">¿Cuándo lo recoges?</label>
            <select id="f-cuando" name="recogida"><option>En cuanto esté listo</option><option>Mañana</option><option>Otro día (lo indico en notas)</option></select></div>
        </div>
        <div class="campos" id="envio-campos" hidden>
          <div class="campo campo--ancho"><label for="f-dir">Dirección de envío</label><input id="f-dir" name="direccion" autocomplete="street-address" data-solo-envio></div>
          <div class="campo"><label for="f-cp">Código postal</label><input id="f-cp" name="cp" inputmode="numeric" autocomplete="postal-code" data-solo-envio></div>
          <div class="campo"><label for="f-ciudad">Población</label><input id="f-ciudad" name="ciudad" autocomplete="address-level2" data-solo-envio></div>
        </div>
        <div class="campo"><label for="f-notas">Notas para la tienda <span style="font-weight:400;color:var(--gris)">(opcional)</span></label>
          <textarea id="f-notas" name="notas" placeholder="Por ejemplo: imprimir solo de la página 3 a la 40, portada en color…"></textarea></div>
        <label class="check"><input type="checkbox" id="f-priv" name="acepto_privacidad" required> <span>He leído la <a href="{url('privacidad', 0 if titulo_nivel == 'h2' else 1)}" target="_blank">política de privacidad</a> y acepto que TopCopias use mis datos y archivos solo para preparar este pedido.</span></label>
        <p class="nota-op alerta" id="aviso-peso" hidden></p>
        <p class="error" id="form-error" hidden role="alert"></p>
        <button class="btn btn--mag" id="btn-enviar" type="submit" disabled style="min-height:56px;font-size:1.06rem">{ico('subir')}<span id="btn-enviar-txt">Enviar pedido</span></button>
        <p class="nota-op">No pagas nada ahora. Pagas al recoger, cuando hayas visto tus copias.</p>
      </form>
      <div class="gracias" id="exito" hidden aria-live="polite"></div>
    </div>

    <aside class="resumen" aria-label="Resumen del precio">
      <div class="ticket corte" id="resumen-ticket"></div>
      <p class="aviso-precio">Precios con IVA incluido. Si tu archivo necesita algo especial (márgenes, páginas en blanco, formatos raros) te lo decimos antes de imprimir.</p>
    </aside>
  </div>
</div></section>
<div class="barra-total" id="barra-total" aria-hidden="true"><div><span class="mono">0,00 €</span><small></small></div><button class="btn btn--mag" type="button" id="barra-ir">Continuar</button></div>'''


def pasos():
    return '''
<section class="seccion" aria-labelledby="t-como"><div class="wrap">
  <div class="seccion-cab"><p class="eyebrow">Cómo funciona</p><h2 id="t-como">Tres pasos y sin colas</h2></div>
  <ol class="pasos limpia" style="list-style:none;margin:0;padding:0">
    <li class="paso"><span class="n">PASO 1</span><h3>Sube tu PDF</h3><p>Desde el móvil o el ordenador. Puedes subir varios archivos y elegir copias de cada uno.</p></li>
    <li class="paso"><span class="n">PASO 2</span><h3>Mira el precio exacto</h3><p>Elige B/N o color, doble cara, papel y encuadernación. El total cambia al momento, línea a línea.</p></li>
    <li class="paso"><span class="n">PASO 3</span><h3>Recógelo listo</h3><p>Te avisamos por WhatsApp cuando esté preparado. Entras, das tu código y te lo llevas. Pagas al recoger.</p></li>
  </ol>
</div></section>'''


def servicios_grid(prof):
    bn0 = P["tramos"]["bn"][-1][1]; col0 = P["tramos"]["color"][-1][1]
    esp0 = P["acabados"]["espiral"]["tramos_hojas"][0][1]; ter = P["acabados"]["termico"]["precio"]
    items = [
        ("apuntes", "Apuntes y temarios", "Blanco y negro a doble cara, con 2 páginas por cara si quieres ahorrar papel. Para todo el cuatrimestre.", f"desde <b>{eur(bn0, 3)}</b> la cara"),
        ("color", "Impresión en color", "Impresoras láser de alta calidad para trabajos, presentaciones y portadas que tienen que verse bien.", f"desde <b>{eur(col0, 2)}</b> la cara"),
        ("espiral", "Encuadernación", "Espiral con tapa transparente para el día a día, o térmica con acabado de libro para el TFG.", f"espiral desde <b>{eur(esp0)}</b> · térmica <b>{eur(ter)}</b>"),
        ("flyer", "Flyers y folletos", "Panfletos, folletos y carteles para tu negocio, tu asociación o tu evento.", "precio según cantidad"),
        ("tarjeta", "Tarjetas de visita", "Tarjetas con la máxima calidad de impresión, listas para repartir.", "precio según diseño y cantidad"),
        ("envio", "Envío a toda la península", f"¿No estás en Zaragoza? Te lo mandamos a casa. {P['envio']['texto']}, gratis desde {eur(P['envio']['gratis_desde'])}.", "24 a 48 horas"),
    ]
    h = "".join(f'<article class="serv">{ico(i)}<h3>{t}</h3><p>{d}</p><p class="desde">{p}</p></article>' for i, t, d, p in items)
    return f'<div class="servicios">{h}</div>'


def banda():
    return f'''<section class="banda" aria-label="TopCopias en cifras"><div class="wrap">
  <div class="dato"><b>{N["anios"]}</b><span>años imprimiendo en Zaragoza</span></div>
  <div class="dato"><b>+{N["clientes"]}</b><span>clientes atendidos</span></div>
  <div class="dato"><b>{N["google"]["nota"]}★</b><span>{N["google"]["resenas"]} reseñas en Google</span></div>
  <div class="dato"><b>2</b><span>tiendas en el 50009</span></div>
</div></section>'''


def tiendas_bloque(prof, h="h2"):
    a = "../" * prof + "assets/"
    cards = ""
    for i, t in enumerate(N["tiendas"]):
        cards += f'''<article class="tienda">{'<span class="principal">Tienda principal</span>' if i == 0 else ''}
      <h3>{e(t["nombre"])}</h3>
      <p class="dir">{e(t["direccion"])}<br>{e(t["cp"])}</p>
      <div class="meta"><span>{e(t["horario"])}</span><span>Tel. <a href="tel:{t["tel"]}">{t["tel_texto"]}</a> · <a href="mailto:{t["email"]}">{t["email"]}</a></span></div>
      <div class="acciones"><a class="btn btn--borde" href="{t["mapa"]}" target="_blank" rel="noopener">{ico('mapa')}Cómo llegar</a><a class="btn btn--borde" href="tel:{t["tel"]}">{ico('tel')}Llamar</a></div>
    </article>'''
    return f'''
<section class="seccion" id="tiendas" aria-labelledby="t-tiendas"><div class="wrap tiendas">
  <div class="fotos">
    <figure><img src="{a}img/fachada.jpg" width="530" height="704" alt="Fachada de TopCopias en el Paseo de Fernando el Católico, 30, con la pared amarilla y el letrero de colores" loading="lazy"><figcaption>P.º Fernando el Católico, 30</figcaption></figure>
    <figure><img src="{a}img/interior.jpg" width="528" height="704" alt="Interior de la tienda con el mostrador y las impresoras al fondo" loading="lazy"><figcaption>Mostrador y máquinas</figcaption></figure>
  </div>
  <div style="display:grid;gap:22px;min-width:0">
    <div class="seccion-cab" style="margin:0"><p class="eyebrow">Dónde recoger</p><{h} id="t-tiendas">Dos tiendas en el centro de Zaragoza</{h}>
      <p>Busca la fachada amarilla con el letrero de colores. Dinos tu código de pedido en el mostrador y te lo damos preparado.</p></div>
    <div class="lista-tiendas">{cards}</div>
  </div>
</div></section>'''


FAQ = [
    ("¿Cuánto tarda mi pedido?", "Los pedidos que entran antes de las 13:00 se preparan el mismo día, salvo tiradas muy grandes. Te avisamos por WhatsApp en cuanto esté listo para recoger."),
    ("¿Tengo que pagar online?", "No. Envías el pedido sin pagar y pagas en la tienda cuando recoges tus copias."),
    ("¿Cómo sabéis qué páginas van en color?", "Al subir el PDF, la web mira cada página en tu propio dispositivo y cuenta las que tienen color. Con la opción «Automático» solo pagas color en esas páginas. Si prefieres todo en blanco y negro, elígelo y el precio baja al momento."),
    ("¿El precio que veo es el final?", "Sí, con IVA incluido, para las opciones que eliges. Si tu archivo necesita algún ajuste especial te lo decimos antes de imprimir, nunca después."),
    ("¿Qué archivos puedo subir?", "PDF e imágenes (JPG, PNG). Si tienes un Word o un PowerPoint, guárdalo como PDF antes de subirlo: así se imprime exactamente como lo ves."),
    ("Mi archivo es muy grande, ¿qué hago?", f"El formulario admite hasta 8 MB por pedido. Si pesa más, envía el pedido igualmente y mándanos los archivos por WhatsApp al {N['whatsapp_texto']} o a {N['email_pedidos']} con tu código."),
    ("¿Qué pasa con mis archivos después?", "Solo los usamos para imprimir tu pedido y los borramos cuando lo recoges. No los compartimos con nadie."),
]


def faq_bloque(h="h2"):
    items = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in FAQ)
    return f'''<section class="seccion" aria-labelledby="t-faq" style="padding-top:0"><div class="wrap">
  <div class="seccion-cab"><p class="eyebrow">Preguntas frecuentes</p><{h} id="t-faq">Lo que nos preguntáis en el mostrador</{h}></div>
  <div class="faq">{items}</div></div></section>'''


def cierre(prof, inicio=False):
    ir = "#imprimir" if inicio else url("imprimir", prof)
    return f'''<section class="cierre"><div class="wrap"><h2>¿Lo tienes en PDF? En dos minutos está pedido.</h2>
  <div class="hero-cta"><a class="btn btn--mag" href="{ir}">{ico('subir')}Sube tu PDF</a><a class="btn btn--borde" href="{WA}" target="_blank" rel="noopener">{ico('wa')}WhatsApp</a></div></div></section>'''


def cab_pag(eyebrow, h1, lead):
    return f'<section class="cab-pag"><div class="wrap"><p class="eyebrow">{eyebrow}</p><h1>{h1}</h1><p class="lead" style="max-width:52ch">{lead}</p></div></section>'


# ---------- Páginas ----------
def construir():
    if os.path.isdir(SAIDA):
        shutil.rmtree(SAIDA)
    os.makedirs(SAIDA)
    shutil.copytree(os.path.join(AQUI, "assets"), os.path.join(SAIDA, "assets"))
    with open(os.path.join(SAIDA, "assets", "precios.js"), "w", encoding="utf-8") as f:
        f.write("/* Generado por build.py desde data/precios.json y data/negocio.json */\n")
        f.write("window.TC_PRECIOS=" + json.dumps(P, ensure_ascii=False) + ";\n")
        f.write("window.TC_NEGOCIO=" + json.dumps(N, ensure_ascii=False) + ";\n")
        f.write(f'window.TC_MODO="{MODO}";\n')
    with open(os.path.join(SAIDA, "assets", "favicon.svg"), "w") as f:
        f.write(LOGO_SVG.replace('<svg viewBox', '<svg xmlns="http://www.w3.org/2000/svg" viewBox'))

    bn0 = P["tramos"]["bn"][-1][1]
    ld = {
        "@context": "https://schema.org", "@type": "LocalBusiness", "name": "Copistería TopCopias", "url": DOMINIO,
        "telephone": T1["tel"], "email": N["email_pedidos"], "priceRange": "€",
        "address": {"@type": "PostalAddress", "streetAddress": T1["direccion"], "postalCode": "50009", "addressLocality": "Zaragoza", "addressCountry": "ES"},
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.5", "reviewCount": N["google"]["resenas"]},
        "sameAs": [N["instagram"], N["facebook"]],
    }
    ld_tag = '\n<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>"

    # Inicio
    tiene_video = os.path.exists(os.path.join(AQUI, "assets", "media", "hero-h.mp4"))
    if tiene_video:
        fondo = ('<video class="hero-fondo" muted autoplay loop playsinline preload="metadata" aria-hidden="true" '
                 'data-horizontal="assets/media/hero-h.mp4" data-vertical="assets/media/hero-v.mp4" '
                 'data-poster-horizontal="assets/media/hero-h.jpg" data-poster-vertical="assets/media/hero-v.jpg"></video>')
    else:
        fondo = '<canvas class="hero-fondo hojas" aria-hidden="true"></canvas>'
    col0 = P["tramos"]["color"][-1][1]
    hero = f'''
<section class="hero-inm" aria-labelledby="t-hero">
  {fondo}
  <div class="hero-velo" aria-hidden="true"></div>
  <div class="wrap hero-inm-in">
    <div class="hero-txt">
      <a class="chip-google" href="{N["google"]["url"]}" target="_blank" rel="noopener">{ico('estrella')}<b>{N["google"]["nota"]}</b> · {N["google"]["resenas"]} reseñas en Google</a>
      <h1 class="titular" id="t-hero"><span class="reg">Sube tu PDF.</span><br><span class="reg">Recógelo <em>listo</em>.</span></h1>
      <p class="lead">La copistería de Zaragoza que imprime mientras tú vienes. Ves el precio al momento, te avisamos por WhatsApp y lo recoges sin esperar.</p>
      <label class="subida-pill" id="subida-hero">
        <input type="file" accept="application/pdf,.pdf,image/*" multiple aria-label="Elegir PDF para calcular el precio">
        <span class="pill-ico">{ico('subir')}</span>
        <span class="pill-txt"><b><span class="solo-raton">Suelta aquí tu PDF</span><span class="solo-tactil">Elige tu PDF</span></b><small>y mira el precio al instante</small></span>
        <span class="pill-btn">Subir</span>
      </label>
      <ul class="precios-hero limpia">
        <li><span>B/N desde</span><b class="mono">{eur(bn0, 3)}</b></li>
        <li><span>Color desde</span><b class="mono">{eur(col0, 2)}</b></li>
        <li><span>Listo hoy si pides antes de las</span><b class="mono">13:00</b></li>
      </ul>
    </div>
  </div>
</section>
<div class="cinta" aria-hidden="true"><div class="cinta-in">{"".join(f"<span>{s}</span><i></i>" for s in ["Apuntes", "TFG encuadernado", "Color láser", "Doble cara", "Espiral", "Flyers", "Tarjetas de visita", "A3", "Envíos a la península"] * 2)}</div></div>'''
    servicios_home = f'''<section class="seccion" style="padding-top:0" aria-labelledby="t-serv"><div class="wrap">
  <div class="seccion-cab"><p class="eyebrow">Qué imprimimos</p><h2 id="t-serv">Del apunte de mañana al TFG encuadernado</h2></div>
  {servicios_grid(0)}</div></section>'''
    pagina("", "", "TopCopias · Copistería en Zaragoza", f"Sube tu PDF, mira el precio al momento y recógelo listo en P.º Fernando el Católico, 30. Copias B/N desde {eur(bn0, 3)}, color, encuadernación y envío a la península.",
           hero + pasos() + herramienta() + servicios_home + banda() + tiendas_bloque(0) + faq_bloque() + cierre(0, True), con_pedido=True, extra_head=ld_tag)

    # Imprimir online
    pagina("imprimir", "imprimir", "Imprimir online · TopCopias Zaragoza", "Sube tu PDF, calcula el precio con B/N o color, doble cara y encuadernación, y recógelo listo en tienda. Pagas al recoger.",
           herramienta("h1").replace('class="seccion herramienta"', 'class="seccion herramienta" style="padding-top:clamp(28px,5vw,56px)"') + pasos() + faq_bloque() , con_pedido=True)

    # Servicios
    pagina("servicios", "servicios", "Servicios · TopCopias Zaragoza", "Apuntes, impresión en color, encuadernación en espiral y térmica, flyers, tarjetas de visita y envíos a la península.",
           cab_pag("Servicios", "Todo lo que sale de nuestras máquinas", "Imprimimos para estudiantes, opositores, profesores y negocios del barrio. Lo que se pide online se recoge listo en tienda.")
           + f'<section class="seccion"><div class="wrap">{servicios_grid(1)}</div></section>' + banda() + cierre(1))

    # Precios
    def tabla(clave, nombre):
        filas = P["tramos"][clave]
        trs = ""
        for i, (desde, pr) in enumerate(filas):
            hasta = filas[i + 1][0] - 1 if i + 1 < len(filas) else None
            rango = f"{desde} – {hasta}" if hasta else f"{desde} o más"
            trs += f'<tr><td>{rango} caras</td><td class="n">{eur(pr, 3)}</td><td class="n">{eur(pr * 2, 3)}</td></tr>'
        return f'<div class="tabla-wrap"><table class="precios"><caption class="sr">{nombre}</caption><thead><tr><th>{nombre} · caras en el pedido</th><th class="n">A4 / cara</th><th class="n">A3 / cara</th></tr></thead><tbody>{trs}</tbody></table></div>'
    esp = P["acabados"]["espiral"]["tramos_hojas"]
    prev = 0; esp_tr = ""
    for h, pr in esp:
        esp_tr += f'<tr><td>Espiral · {prev + 1} – {h} hojas</td><td class="n">{eur(pr)}</td></tr>'; prev = h
    otros = "".join(f'<tr><td>{v["etiqueta"]}{" · hasta " + str(v["max_hojas"]) + " hojas" if v.get("max_hojas") else ""}</td><td class="n">{eur(v["precio"])}</td></tr>' for k, v in P["acabados"].items() if k not in ("ninguno", "espiral"))
    papel_tr = "".join(f'<tr><td>{v["etiqueta"]}</td><td class="n">{"incluido" if not v["por_hoja"] else "+" + eur(v["por_hoja"]) + " / hoja"}</td></tr>' for v in P["papel"].values())
    aviso = '' if P.get("confirmado") else '<p class="aviso" data-pendiente>Tabla de referencia pendiente de confirmar por TopCopias antes de publicar.</p>'
    precios_html = cab_pag("Precios", "Precios claros, por cara impresa", f"Cuantas más caras lleva tu pedido, menos pagas por cada una. Todos los precios con IVA incluido.") + f'''
<section class="seccion"><div class="wrap precios-grid">
  {aviso}
  <div class="seccion-cab" style="margin:0"><h2>Blanco y negro</h2><p>El tramo se calcula con el total de caras del pedido: todas las copias de todos tus archivos.</p></div>
  {tabla("bn", "Blanco y negro")}
  <div class="seccion-cab" style="margin:0"><h2>Color</h2><p>Con la opción «Automático» solo pagas color en las páginas que lo llevan.</p></div>
  {tabla("color", "Color")}
  <div class="seccion-cab" style="margin:0"><h2>Papel y acabados</h2></div>
  <div class="tabla-wrap"><table class="precios"><thead><tr><th>Papel</th><th class="n">Precio</th></tr></thead><tbody>{papel_tr}</tbody></table></div>
  <div class="tabla-wrap"><table class="precios"><thead><tr><th>Acabado, por copia</th><th class="n">Precio</th></tr></thead><tbody>{esp_tr}{otros}</tbody></table></div>
  <div class="tabla-wrap"><table class="precios"><thead><tr><th>Entrega</th><th class="n">Precio</th></tr></thead><tbody>
    <tr><td>Recoger en tienda</td><td class="n">gratis</td></tr>
    <tr><td>Envío a la península ({P["envio"]["texto"]})</td><td class="n">{eur(P["envio"]["precio"])}</td></tr>
    <tr><td>Envío en pedidos desde {eur(P["envio"]["gratis_desde"])}</td><td class="n">gratis</td></tr></tbody></table></div>
  <div class="hero-cta"><a class="btn btn--mag" href="{url('imprimir', 1)}">{ico('subir')}Calcular con mi PDF</a></div>
</div></section>''' + cierre(1)
    pagina("precios", "precios", "Precios · TopCopias Zaragoza", f"Precios de impresión por cara: blanco y negro desde {eur(bn0, 3)}, color, papel, encuadernación y envío.", precios_html)

    # Tiendas
    pagina("tiendas", "tiendas", "Tiendas · TopCopias Zaragoza", "TopCopias en P.º de Fernando el Católico, 30 y Calle Arzobispo Apaolaza, 3 (50009 Zaragoza). Teléfonos, WhatsApp y cómo llegar.",
           cab_pag("Tiendas y contacto", "Ven a recoger, o pregúntanos lo que quieras", f"Escríbenos por WhatsApp al {N['whatsapp_texto']} o a {N['email_pedidos']}. Respondemos en horario de tienda.")
           + tiendas_bloque(1, "h2") + cierre(1))

    # Legales
    def legal(ruta, titulo, cuerpo):
        pagina(ruta, "", f"{titulo} · TopCopias", f"{titulo} de TopCopias.", cab_pag("Información legal", titulo, "") + f'<section class="seccion"><div class="wrap texto-legal">{cuerpo}</div></section>')
    ident = f'<p><b>{N["razon_social"]}</b> · CIF {N["cif"]} · {N["domicilio_fiscal"]} · {N["email_pedidos"]}</p>'
    legal("aviso-legal", "Aviso legal", ident + '''
<h2>Objeto</h2><p>Esta web informa de los servicios de copistería e impresión de TopCopias y permite enviar pedidos de impresión para recoger en tienda o recibir en casa.</p>
<h2>Pedidos</h2><p>El precio mostrado al subir un archivo es el precio del pedido con las opciones elegidas, IVA incluido. Si un archivo necesita ajustes, te contactamos antes de imprimir. El pago se hace al recoger en tienda.</p>
<h2>Propiedad intelectual</h2><p>Quien sube un archivo declara tener derecho a reproducirlo. TopCopias no imprime material que infrinja derechos de terceros.</p>''')
    legal("privacidad", "Política de privacidad", ident + '''
<h2>Qué datos tratamos</h2><p>Nombre, móvil, email, dirección (solo si pides envío) y los archivos que subes para imprimir.</p>
<h2>Para qué</h2><p>Para preparar tu pedido, avisarte cuando esté listo y, si lo pides, enviártelo. Base legal: ejecución del pedido que solicitas.</p>
<h2>Cuánto tiempo</h2><p>Los archivos se borran cuando recoges o recibes el pedido. Los datos del pedido se guardan el tiempo que exige la normativa fiscal.</p>
<h2>Con quién</h2><p>Con nadie, salvo el proveedor de alojamiento de la web y, en envíos, la empresa de transporte.</p>
<h2>Tus derechos</h2><p>Puedes pedir acceso, rectificación o supresión escribiendo a ''' + N["email_pedidos"] + '''. También puedes reclamar ante la Agencia Española de Protección de Datos.</p>''')
    legal("cookies", "Política de cookies", '<p>Esta web no usa cookies de publicidad ni de analítica. Las fuentes tipográficas se cargan desde Google Fonts. Si en el futuro añadimos analítica, te pediremos permiso antes.</p>')

    # 404 + Netlify
    if MODO == "web":
        net = os.path.join(AQUI, "netlify")
        for f in os.listdir(net):
            shutil.copy(os.path.join(net, f), os.path.join(SAIDA, f))
        pagina("404tmp", "", "Página no encontrada · TopCopias", "", cab_pag("Error 404", "Esta página no existe", "Puede que el enlace sea antiguo. Desde aquí puedes subir tu PDF o ver nuestras tiendas.") + cierre(1))
        shutil.move(os.path.join(SAIDA, "404tmp", "index.html"), os.path.join(SAIDA, "404.html")); os.rmdir(os.path.join(SAIDA, "404tmp"))
        with open(os.path.join(SAIDA, "sitemap.xml"), "w") as f:
            urls = ["", "imprimir/", "servicios/", "precios/", "tiendas/"]
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{DOMINIO}/{u}</loc></url>" for u in urls) + "</urlset>\n")
        with open(os.path.join(SAIDA, "robots.txt"), "w") as f:
            f.write(f"User-agent: *\nAllow: /\nSitemap: {DOMINIO}/sitemap.xml\n")
    print("ok ->", os.path.abspath(SAIDA), MODO)


if __name__ == "__main__":
    construir()
