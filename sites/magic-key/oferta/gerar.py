#!/usr/bin/env python3
"""Pack de oferta Magic Key (Iași): afiș QR, oferta RO/PT e auditoria (pág. 1-2).

Uso:  python3 gerar.py      -> escreve os .html nesta pasta
      node pdf.js           -> imprime os .pdf com o Chromium do Playwright
"""
import io
import pathlib

import qrcode
import qrcode.constants

AQUI = pathlib.Path(__file__).resolve().parent
FONTES = (AQUI.parent / "_fontes" / "fontes.css").read_text()

# Place ID tirado do link da ficha Google (parâmetro 19s), ver ponte/r3-magic-key-chei-auto-duplicare.txt
PLACE_ID = "ChIJdbn1UCv7ykAR8GfcUXEt81c"
LINK_RECENZIE = "https://search.google.com/local/writereview?placeid=" + PLACE_ID
DATA = "09.10.2026"


def qr_svg(texto, cor="#1C1F22"):
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=0)
    q.add_data(texto)
    q.make(fit=True)
    m = q.get_matrix()
    n = len(m)
    partes = []
    for y, linha in enumerate(m):
        for x, v in enumerate(linha):
            if v:
                partes.append("M%d %dh1v1h-1z" % (x, y))
    return ('<svg class="qr" viewBox="0 0 %d %d" shape-rendering="crispEdges" role="img" aria-label="Cod QR">'
            '<path fill="%s" d="%s"/></svg>') % (n, n, cor, "".join(partes))


BASE_CSS = """
@page{size:A4;margin:0}
:root{--grafit:#1C1F22;--grafit-2:#272B30;--grafit-3:#353A40;--alb:#FAFBF8;--hartie:#EFF2EC;--linie:#DADFD5;
--verde:#3BAA35;--verde-txt:#23801F;--verde-dsc:#86DC78;--verde-pal:#E3F3DF;--ambra:#FFB020;--ambra-2:#E89400;
--text:#121416;--text-2:#4F5650;--pal:#9AA39A;
--f-disp:'Tomorrow',Arial,sans-serif;--f-txt:'Red Hat Text',system-ui,sans-serif;--f-mono:'Xanh Mono',ui-monospace,monospace}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{background:#8A9099;font:500 10pt/1.45 var(--f-txt);color:var(--text);-webkit-print-color-adjust:exact;print-color-adjust:exact}
.foaie{width:210mm;height:297mm;margin:0 auto;background:var(--alb);position:relative;overflow:hidden;display:flex;flex-direction:column;page-break-after:always;break-after:page}
.foaie:last-child{page-break-after:auto;break-after:auto}
@media screen{.foaie{margin:24px auto;box-shadow:0 20px 60px rgba(0,0,0,.35)}}
@media print{body{background:none}}
h1,h2,h3{font-family:var(--f-disp);font-weight:600;margin:0;line-height:1.1;letter-spacing:-.02em}
.mono{font-family:var(--f-mono)}
.qr{display:block;width:100%;height:auto}
.marcaj{display:inline-block;padding:1px 6px;border-radius:4px;background:#FFE36B;color:#1A1406;font-weight:700;font-size:.85em;outline:1.2px dashed var(--ambra-2);outline-offset:1px;white-space:nowrap}
"""

# Perfil de cheie (bitting) usado como separador: assinatura do pack
def profil(cul="#1C1F22", h=10):
    return ('<svg class="profil" viewBox="0 0 400 20" preserveAspectRatio="none" aria-hidden="true" style="height:%dpx">'
            '<path d="M0 4H40l8 9h20l6-7h22l9 10h18l7-8h26l8 9h24l6-6h30l9 9h22l7-7h134V20H0z" fill="%s"/></svg>') % (h, cul)


# ---------------------------------------------------------------- AFIȘ (RO)
STELE = "".join('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 1.8l3.1 6.6 7.2.9-5.3 5 1.4 7.1L12 17.9l-6.4 3.5 1.4-7.1-5.3-5 7.2-.9z"/></svg>' for _ in range(5))

AFIS_CSS = """
.afis{background:var(--alb);padding:14mm 16mm 0}
.afis .sus{display:flex;justify-content:space-between;align-items:center}
.afis .brand{font:600 15pt/1 var(--f-disp);letter-spacing:.02em;display:flex;align-items:center;gap:3mm}
.afis .brand i{width:5mm;height:5mm;border-radius:50%;background:var(--verde);box-shadow:0 0 0 1.4mm var(--verde-pal)}
.afis .brand small{font:400 11pt/1 var(--f-mono);color:var(--text-2);letter-spacing:0;margin-left:1mm}
.afis .stele{display:flex;gap:1.4mm}
.afis .stele svg{width:7mm;height:7mm;fill:var(--ambra)}
.afis h1{font-size:46pt;line-height:1.02;margin:10mm 0 4mm;letter-spacing:-.035em}
.afis h1 em{font-style:normal;color:var(--verde-txt)}
.afis .lead{font-size:15pt;line-height:1.4;color:var(--text-2);margin:0;max-width:160mm}
.afis .lead b{color:var(--text)}
.afis .scena{display:grid;grid-template-columns:104mm 1fr;gap:9mm;align-items:start;margin-top:8mm}
.cheie{position:relative;width:104mm}
.cap{position:relative;background:linear-gradient(160deg,#30353B,#1C1F22 55%,#111315);border-radius:20mm 20mm 15mm 15mm;padding:10mm 10mm 7mm;box-shadow:0 3mm 8mm -3mm rgba(0,0,0,.45),inset 0 .6mm 0 rgba(255,255,255,.08)}
.cap .placa{background:#fff;border-radius:6mm;padding:6mm;box-shadow:inset 0 0 0 .5mm #DADFD5}
.cap .butoane{display:flex;justify-content:center;gap:5mm;margin-top:5mm}
.cap .butoane span{width:11mm;height:6mm;border-radius:3mm;background:var(--grafit-3);box-shadow:inset 0 .4mm 0 rgba(255,255,255,.1)}
.cap .butoane span.v{background:var(--verde)}
.cap .led{position:absolute;top:5mm;left:50%;width:2.4mm;height:2.4mm;margin-left:-1.2mm;border-radius:50%;background:var(--verde-dsc);box-shadow:0 0 3mm var(--verde)}
.lama{position:relative;width:24mm;height:38mm;margin:0 auto;background:linear-gradient(90deg,#9BA3AB,#E7EBEE 35%,#C5CBD1 60%,#8D959D);border-radius:0 0 3mm 9mm;clip-path:polygon(0 0,100% 0,100% 82%,62% 100%,0 100%)}
.lama::before{content:'';position:absolute;inset:-2mm 0 auto;height:6mm;background:#2A2E33;border-radius:0 0 2mm 2mm}
.lama svg{position:absolute;left:6mm;top:5mm;width:12mm;height:30mm}
.pasi{list-style:none;margin:0;padding:6mm 0 0;display:grid;gap:9mm;counter-reset:p}
.pasi li{counter-increment:p;display:grid;grid-template-columns:12mm 1fr;gap:4mm;align-items:start;font-size:13pt;line-height:1.35;color:var(--text-2)}
.pasi li::before{content:counter(p);width:12mm;height:12mm;border-radius:50%;display:grid;place-items:center;font:600 15pt/1 var(--f-disp);background:var(--grafit);color:var(--ambra)}
.pasi b{display:block;font:600 15pt/1.2 var(--f-disp);color:var(--text);margin-bottom:1mm;letter-spacing:-.01em}
.pasi .link{font:400 9.5pt/1.3 var(--f-mono);color:var(--text-2);word-break:break-all}
.afis .jos{margin:auto -16mm 0;flex:none;background:var(--grafit);color:#D9DED8;padding:8mm 16mm 7mm;display:grid;grid-template-columns:1fr auto;gap:2mm 8mm;align-items:end}
.afis .jos strong{font:600 20pt/1 var(--f-disp);color:#fff;letter-spacing:-.02em}
.afis .jos strong em{font-style:normal;color:var(--verde-dsc)}
.afis .jos p{margin:2.5mm 0 0;font-size:11pt;line-height:1.4}
.afis .jos .tel{font:600 16pt/1 var(--f-disp);color:#fff;text-align:right;white-space:nowrap}
.afis .jos .tel small{display:block;font:400 9.5pt/1.2 var(--f-mono);color:#9AA39A;margin-bottom:2mm}
.afis .jos .semn{grid-column:1/-1;font:400 8pt/1 var(--f-mono);color:#7C857C;border-top:1px solid rgba(255,255,255,.1);padding-top:3mm;margin-top:3mm}
/* A5 x2 numa A4 deitada */
.dublu{width:297mm;height:210mm;display:flex;background:#fff;page-break-after:always;break-after:page;position:relative}
@media screen{.dublu{margin:24px auto;box-shadow:0 20px 60px rgba(0,0,0,.35)}}
.dublu .cel{width:148.5mm;height:210mm;overflow:hidden}
.dublu .cel .foaie{zoom:.7071;margin:0;box-shadow:none}
.dublu::after{content:'';position:absolute;left:50%;top:0;bottom:0;border-left:.3mm dashed #B9C0B8}
"""

LAMA_SVG = ('<svg viewBox="0 0 12 42" aria-hidden="true"><path d="M6 0 C 11 5, 1 9, 6 14 S 11 23, 6 28 S 1 37, 6 42" '
            'fill="none" stroke="#7E868E" stroke-width="2.4" stroke-linecap="round"/></svg>')


def afis_foaie():
    return """
<section class="foaie afis">
  <div class="sus">
    <div class="brand"><i></i>Magic Key <small>chei auto · Iași</small></div>
    <div class="stele">{stele}</div>
  </div>
  <h1>Cheia a pornit<br><em>din prima?</em></h1>
  <p class="lead">Spuneți-le și altora. <b>Scanați codul și lăsați-ne o recenzie pe Google.</b> Durează 30 de secunde și ne ajută enorm.</p>
  <div class="scena">
    <div class="cheie">
      <div class="cap"><span class="led"></span><div class="placa">{qr}</div><div class="butoane"><span></span><span class="v"></span><span></span></div></div>
      <div class="lama">{lama}</div>
    </div>
    <ol class="pasi">
      <li><span><b>Deschideți camera</b>Pe orice telefon, fără aplicație.</span></li>
      <li><span><b>Îndreptați-o spre cod</b>Apăsați pe linkul care apare.</span></li>
      <li><span><b>Alegeți stelele</b>Și, dacă aveți chef, două vorbe despre cheia dumneavoastră.</span></li>
    </ol>
  </div>
  <div class="jos">
    <div><strong>Mulțumim! <em>Drum bun.</em></strong><p>Magic Key · incinta Selgros, Șos. Nicolina 57A, Iași</p></div>
    <div class="tel"><small>Ați pierdut o cheie?</small>0747 979 810</div>
    <div class="semn">Afiș realizat de Pacheco Studios · pachecost.com</div>
  </div>
</section>""".format(stele=STELE, qr=qr_svg(LINK_RECENZIE), lama=LAMA_SVG)


def afis_html():
    f = afis_foaie()
    return """<!doctype html><html lang="ro"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Afiș recenzii Google · Magic Key</title><style>{fontes}{base}{css}</style></head><body>
{f}
</body></html>""".format(fontes=FONTES, base=BASE_CSS, css=AFIS_CSS, f=f)


def afis_a5_html():
    f = afis_foaie()
    css = AFIS_CSS + "@page{size:A4 landscape;margin:0}"
    return """<!doctype html><html lang="ro"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Afiș recenzii Google A5 · Magic Key</title><style>{fontes}{base}{css}</style></head><body>
<div class="dublu"><div class="cel">{f}</div><div class="cel">{f}</div></div>
</body></html>""".format(fontes=FONTES, base=BASE_CSS, css=css, f=f)


# ---------------------------------------------------------------- OFERTA
DOC_CSS = """
.antet{background:radial-gradient(120% 140% at 12% 0%,#30353B 0%,#1C1F22 55%,#121416 100%);color:#D9DED8;padding:13mm 15mm 0;position:relative}
.antet .sus{display:flex;justify-content:space-between;align-items:center;margin-bottom:9mm}
.antet .marca{font:600 10pt/1 var(--f-disp);letter-spacing:.12em;text-transform:uppercase;color:#fff;display:flex;gap:8px;align-items:center}
.antet .marca b{font-weight:600;color:var(--verde-dsc)}
.antet .marca i{width:9px;height:9px;border-radius:50%;background:var(--verde);box-shadow:0 0 0 3px rgba(59,170,53,.25)}
.antet .meta{display:flex;gap:8px}
.antet .meta span{font:700 8pt/1 var(--f-txt);letter-spacing:.03em;padding:6px 10px;border-radius:99px;background:rgba(255,255,255,.07);box-shadow:inset 0 0 0 1px rgba(255,255,255,.16)}
.antet .meta b{color:#fff}
.supra{font:400 10pt/1 var(--f-mono);color:var(--ambra);margin:0 0 3.5mm}
.antet h1{font-size:24pt;color:#fff;margin-bottom:4mm}
.antet h1 .mat{color:#AEB6AD}
.antet .situatie{font-size:10.5pt;line-height:1.5;color:#C3C9C2;max-width:165mm;margin:0 0 8mm}
.antet .situatie strong{color:#fff}
.antet .profil{display:block;width:100%;margin-bottom:-1px}
.corp{flex:1;padding:8mm 15mm 0;display:flex;flex-direction:column}
.eticheta{font:400 10pt/1 var(--f-mono);color:var(--verde-txt);margin:0 0 3.5mm;display:flex;align-items:center;gap:8px}
.eticheta::after{content:'';flex:1;height:1px;background:var(--linie)}
.pachet{display:grid;grid-template-columns:1.42fr 1fr;border-radius:14px;overflow:hidden;box-shadow:inset 0 0 0 1px var(--linie),0 10px 26px -16px rgba(18,20,22,.45)}
.pachet .ce{background:#fff;padding:7mm 7mm 6mm}
.pachet h2{font-size:13pt;margin-bottom:1.5mm}
.pachet .ce>p{font-size:8.8pt;color:var(--text-2);margin:0 0 4mm}
.pachet ul{list-style:none;margin:0;padding:0;display:grid;gap:2.6mm;font-size:9.2pt;line-height:1.38}
.pachet li{position:relative;padding-left:16px}
.pachet li::before{content:'';position:absolute;left:0;top:.38em;width:8px;height:8px;border-radius:2px;background:var(--verde);transform:rotate(45deg)}
.pachet li.gratis::before{background:var(--ambra)}
.pachet li b{font-weight:800}
.pachet li small{display:block;color:var(--text-2);font-size:8pt;font-weight:500}
.pachet .tag{display:inline-block;font:800 7pt/1 var(--f-txt);letter-spacing:.1em;text-transform:uppercase;padding:3px 6px;border-radius:4px;background:var(--ambra);color:#1A1406;margin-left:4px;vertical-align:1px}
.pachet .cost{background:radial-gradient(120% 90% at 20% 0%,#30353B 0%,#1C1F22 55%,#121416 100%);color:#D9DED8;padding:9mm 7mm 7mm;display:flex;flex-direction:column;justify-content:center;gap:5.5mm;box-shadow:inset 1.5px 0 0 var(--verde)}
.pachet .ce-e{display:block;font:400 9pt/1 var(--f-mono);color:var(--verde-dsc);margin-bottom:2.5mm}
.pachet .suma{display:block;font:600 25pt/1 var(--f-disp);letter-spacing:-.03em;color:#fff;white-space:nowrap}
.pachet .suma .lei{font:700 11pt/1 var(--f-txt);letter-spacing:.02em;color:var(--ambra);margin-left:5px}
.pachet .det{display:block;font-size:8pt;line-height:1.4;color:#A9B0A8;margin-top:2mm}
.pachet .sep{height:1px;background:rgba(255,255,255,.14)}
.pachet .zero{font:600 10pt/1.3 var(--f-disp);color:#fff}
.pachet .zero small{display:block;font:500 8pt/1.4 var(--f-txt);color:#A9B0A8;margin-top:1mm}
.fara{margin:5mm 0 0;padding:4mm 5mm;border-radius:10px;background:var(--verde-pal);font-size:9pt;line-height:1.45;color:#1E3D1C}
.fara b{color:#0F2A0E}
.urmeaza{margin-top:8mm}
.pasi-o{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,1fr);gap:4mm;counter-reset:p}
.pasi-o li{counter-increment:p;display:flex;gap:3mm;align-items:flex-start;font-size:8.8pt;line-height:1.42;color:var(--text-2)}
.pasi-o li::before{content:counter(p);flex:none;width:7mm;height:7mm;border-radius:50%;display:grid;place-items:center;font:600 9pt/1 var(--f-disp);background:var(--grafit);color:var(--ambra)}
.pasi-o b{display:block;font-weight:800;color:var(--text)}
.demo{margin-top:7mm;display:grid;grid-template-columns:auto 1fr;gap:1.5mm 5mm;align-items:center;padding:4mm 5mm;border-radius:12px;background:var(--hartie);box-shadow:inset 0 0 0 1px var(--linie);font-size:8.8pt;color:var(--text-2)}
.demo b{font:600 9.5pt/1.2 var(--f-disp);color:var(--text)}
.subsol{margin-top:auto;background:var(--grafit);color:#D9DED8;padding:6mm 15mm;display:flex;justify-content:space-between;align-items:center;gap:6mm}
.subsol .cine{font-size:9pt;line-height:1.45}
.subsol .cine strong{display:block;font:600 11pt/1.3 var(--f-disp);color:#fff}
.subsol dl{display:flex;gap:7mm;margin:0;font-size:9pt}
.subsol dt{font:400 8pt/1 var(--f-mono);color:var(--verde-dsc);margin-bottom:1.6mm}
.subsol dd{margin:0;font-weight:700;color:#fff}
.subsol a{color:inherit;text-decoration:none}
"""

OFERTA = {
    "ro": dict(
        lang="ro", titulo="Ofertă · Magic Key", data="Data", valid="Valabilă", zile="30 de zile",
        supra="Propunere Pacheco Studios",
        h1='Ofertă pentru<br><span class="mat">Magic Key, chei auto</span>',
        situatie='Aveți <strong>4,5 stele din 53 de recenzii</strong> pe Google și niciun site. Cine își pierde cheia mașinii caută pe telefon, pe loc: <strong>scopul este ca atunci să vă găsească pe dumneavoastră</strong> și să vă poată scrie marca și anul mașinii înainte să sune.',
        et_oferta="Pachetul",
        h2="Site, recenzii și audit",
        sub="Totul pregătit și pus în funcțiune de noi, la atelier.",
        itens=[
            ("", "<b>Site-ul Magic Key</b><small>servicii, mărci, «cerere cheie auto» (marcă, an, ce s-a pierdut), Sună / SMS, harta până la standul din Selgros</small>"),
            ("", "<b>Site-ul legat de profilul Google</b><small>astăzi profilul nu are niciun site</small>"),
            ("", "<b>Afișul cu cod QR pentru recenzii</b><small>gata de printat, îl lăsăm azi la stand</small>"),
            ("gratis", '<b>Auditul complet al afacerii</b><span class="tag">gratuit</span><small>unde se pierd clienți și timp, cu cifrele dumneavoastră</small>'),
            ("", "<b>Implementare cu vizită la atelier</b><small>configurăm totul împreună, la fața locului</small>"),
        ],
        insigna="", inst="Instalare", inst_det="plată unică: site, afiș și implementare",
        lunar="Pe lună", lunar_det="domeniu, găzduire, modificări de texte și prețuri, suport",
        audit_t="Auditul: 0 RON", audit_d="inclus în pachet",
        fara='<b>Fără obligații după audit.</b> Primiți raportul complet. Ce implementăm din el, și dacă implementăm ceva, decideți dumneavoastră.',
        et_urm="Ce urmează",
        pasi=[("Discuția de audit", "20–30 de minute la stand, când vă convine."),
              ("Ajustăm detaliile", 'Prețuri, mărci, program, texte <span class="marcaj">de confirmat</span>.'),
              ("Online în ~7 zile", "De la confirmare, cu vizită pentru implementare.")],
        demo_t="Demo-ul site-ului", demo='<strong>pachecost.com/demo/magic-key</strong> · deschideți-l pe telefon',
        cine="Pacheco Studios · Iași", tel_t="WhatsApp / telefon", web_t="Web",
    ),
    "pt": dict(
        lang="pt-PT", titulo="Proposta · Magic Key", data="Data", valid="Válida", zile="30 dias",
        supra="Proposta Pacheco Studios · cópia PT do Tomás",
        h1='Proposta para<br><span class="mat">Magic Key, chaves auto</span>',
        situatie='Têm <strong>4,5 estrelas em 53 avaliações</strong> no Google e nenhum site. Quem perde a chave do carro procura no telemóvel, na hora: <strong>o objetivo é que nessa altura vos encontre a vocês</strong> e possa escrever a marca e o ano do carro antes de ligar.',
        et_oferta="O pack",
        h2="Site, avaliações e auditoria",
        sub="Tudo preparado e posto a funcionar por nós, na loja.",
        itens=[
            ("", "<b>Site do Magic Key</b><small>serviços, marcas, «pedido de chave auto» (marca, ano, o que se perdeu), Ligar / SMS, mapa até ao stand no Selgros</small>"),
            ("", "<b>Site ligado à ficha Google</b><small>hoje a ficha não tem site nenhum</small>"),
            ("", "<b>Cartaz com QR para avaliações</b><small>pronto a imprimir, fica hoje no stand</small>"),
            ("gratis", '<b>Auditoria completa ao negócio</b><span class="tag">grátis</span><small>onde se perdem clientes e tempo, com os números deles</small>'),
            ("", "<b>Implementação com visita à loja</b><small>configuramos tudo juntos, no local</small>"),
        ],
        insigna="", inst="Instalação", inst_det="pagamento único: site, cartaz e implementação",
        lunar="Por mês", lunar_det="domínio, alojamento, alterações de textos e preços, suporte",
        audit_t="Auditoria: 0 RON", audit_d="incluída no pack",
        fara='<b>Sem obrigação depois da auditoria.</b> Recebem o relatório completo. O que implementamos dele, e se implementamos alguma coisa, decidem eles.',
        et_urm="Próximos passos",
        pasi=[("Conversa de auditoria", "20–30 minutos no stand, quando lhes der jeito."),
              ("Afinamos os detalhes", 'Preços, marcas, horário, textos <span class="marcaj">a confirmar</span>.'),
              ("Online em ~7 dias", "Depois da confirmação, com visita para implementar.")],
        demo_t="Demo do site", demo='<strong>pachecost.com/demo/magic-key</strong> · abrir no telemóvel',
        cine="Pacheco Studios · Iași", tel_t="WhatsApp / telefone", web_t="Web",
    ),
}


def oferta_html(t):
    itens = "".join('<li class="%s">%s</li>' % (c, h) for c, h in t["itens"])
    pasi = "".join("<li><span><b>%s</b>%s</span></li>" % p for p in t["pasi"])
    corpo = """
<main class="foaie">
  <header class="antet">
    <div class="sus"><div class="marca"><i></i>Pacheco <b>Studios</b></div>
      <div class="meta"><span>{data} <b>{dia}</b></span><span>{valid} <b>{zile}</b></span></div></div>
    <p class="supra">{supra}</p>
    <h1>{h1}</h1>
    <p class="situatie">{situatie}</p>
    {profil}
  </header>
  <div class="corp">
    <p class="eticheta">{et_oferta}</p>
    <section class="pachet">
      <div class="ce"><h2>{h2}</h2><p>{sub}</p><ul>{itens}</ul></div>
      <div class="cost">
        <div><span class="ce-e">{inst}</span><span class="suma">2.500<span class="lei">RON</span></span><span class="det">{inst_det}</span></div>
        <div class="sep"></div>
        <div><span class="ce-e">{lunar}</span><span class="suma">300<span class="lei">RON</span></span><span class="det">{lunar_det}</span></div>
        <div class="sep"></div>
        <div class="zero">{audit_t}<small>{audit_d}</small></div>
      </div>
    </section>
    <p class="fara">{fara}</p>
    <section class="urmeaza"><p class="eticheta">{et_urm}</p><ol class="pasi-o">{pasi}</ol></section>
    <p class="demo"><b>{demo_t}</b><span>{demo}</span></p>
  </div>
  <footer class="subsol">
    <div class="cine"><strong>Tomás Pacheco</strong>{cine}</div>
    <dl><div><dt>{tel_t}</dt><dd><a href="https://wa.me/40723098556">+40 723 098 556</a></dd></div><div><dt>{web_t}</dt><dd>pachecost.com</dd></div></dl>
  </footer>
</main>""".format(dia=DATA, itens=itens, pasi=pasi, profil=profil("#FAFBF8", 14), **{k: v for k, v in t.items() if k not in ("itens", "pasi")})
    return """<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{titulo}</title><style>{fontes}{base}{css}</style></head><body>{corpo}</body></html>""".format(
        lang=t["lang"], titulo=t["titulo"], fontes=FONTES, base=BASE_CSS, css=DOC_CSS, corpo=corpo)


# ---------------------------------------------------------------- AUDITORIA (pág. 1 e 2)
AUD_CSS = """
.antet.mic{padding-top:11mm}
.antet.mic .sus{margin-bottom:6mm}
.antet.mic h1{font-size:20pt}
.antet.mic .situatie{margin-bottom:6mm}
.fise{display:grid;grid-template-columns:repeat(4,1fr);gap:3mm;margin-bottom:6mm}
.fisa{background:#fff;border-radius:10px;box-shadow:inset 0 0 0 1px var(--linie);padding:3.5mm 4mm}
.fisa span{display:block;font:400 8.5pt/1 var(--f-mono);color:var(--text-2);margin-bottom:2mm}
.fisa b{display:block;font:600 15pt/1.05 var(--f-disp);letter-spacing:-.02em}
.fisa small{display:block;font-size:7.8pt;color:var(--text-2);margin-top:1.2mm;line-height:1.3}
.fisa.rau b{color:#B4261A}
.motoare{display:grid;grid-template-columns:repeat(3,1fr);gap:3.5mm}
.motor{border-radius:12px;background:#fff;box-shadow:inset 0 0 0 1px var(--linie);padding:4.5mm 4.5mm 4mm}
.motor h3{font-size:10.5pt;margin-bottom:.8mm}
.motor .ce{font:400 8.5pt/1.2 var(--f-mono);color:var(--text-2);margin:0 0 3mm}
.motor ul{list-style:none;margin:0;padding:0;display:grid;gap:2.2mm;font-size:8.4pt;line-height:1.38}
.motor li{position:relative;padding-left:13px}
.motor li::before{content:'';position:absolute;left:0;top:.35em;width:7px;height:7px;border-radius:50%;background:var(--verde)}
.motor li.a::before{background:var(--ambra)}
.motor li.r::before{background:#D23B2A}
.legenda{display:flex;gap:5mm;font-size:7.8pt;color:var(--text-2);margin:3mm 0 0}
.legenda i{display:inline-block;width:7px;height:7px;border-radius:50%;margin-right:4px;vertical-align:0}
.voce{margin-top:6mm;display:grid;grid-template-columns:repeat(3,1fr);gap:3.5mm}
.voce blockquote{margin:0;padding:3.5mm 4mm;border-left:2px solid var(--verde);background:var(--hartie);border-radius:0 8px 8px 0;font-size:8.4pt;line-height:1.42;color:var(--text)}
.voce cite{display:block;font:400 8pt/1 var(--f-mono);color:var(--text-2);margin-top:2mm;font-style:normal}
.urm{margin-top:auto;padding:5mm 0 7mm;font-size:8.6pt;color:var(--text-2);line-height:1.45}
.urm b{color:var(--text)}
.intrebari{display:grid;grid-template-columns:1fr 1fr;gap:4mm 6mm}
.bloc h3{font-size:11.5pt;margin:2mm 0 3mm;display:flex;gap:6px;align-items:baseline}
.bloc h3 span{font:400 8.5pt/1 var(--f-mono);color:var(--verde-txt)}
.bloc ol{margin:0;padding-left:5mm;display:grid;gap:2.4mm;font-size:9.6pt;line-height:1.4}
.bloc li::marker{font-weight:700;color:var(--text-2)}
.bloc li.e{font-weight:700}
.cifre{margin-top:6mm;border-radius:12px;box-shadow:inset 0 0 0 1px var(--linie);background:#fff;padding:4mm 5mm}
.cifre table{width:100%;border-collapse:collapse;font-size:9.4pt}
.cifre td{padding:3.6mm 0;border-bottom:1px solid var(--linie)}
.cifre td:last-child{width:46mm;border-bottom:1px solid #9AA39A}
.cifre tr:last-child td{border-bottom:0}
.cifre tr:last-child td:last-child{border-bottom:1px solid #9AA39A}
.nota{font-size:8pt;color:var(--text-2);margin:3mm 0 0}
.nr-pag{position:absolute;right:15mm;bottom:8mm;font:400 8pt/1 var(--f-mono);color:var(--pal)}
"""

AUD = {
    "ro": dict(
        lang="ro", titulo="Audit · Magic Key", supra="Auditul afacerii · partea 1 din 3",
        h1='Magic Key, <span class="mat">văzut din afară</span>',
        situatie='Ce vede un client care vă caută azi pe Google, înainte de prima discuție. <strong>Partea 2 se completează la întâlnire</strong>, cu cifrele dumneavoastră; partea 3 este planul.',
        fise=[("Recenzii Google", "4,5 ★", "din 53 de recenzii", ""),
              ("Site", "lipsă", "profilul spune «Adaugă un site»", "rau"),
              ("Program", "L–V 9–17", "S 9–14 · D închis", ""),
              ("Fotografii", "38", "pe profilul Google", "")],
        et1="Cele 3 motoare ale afacerii",
        motoare=[
            ("Clienți noi", "cum vă găsesc",
             [("", "Profil Google cu adresă clară: incinta Selgros, Șos. Nicolina 57A."),
              ("r", "Fără site: cine caută «chei auto Iași» nu vede mărci, servicii sau prețuri orientative."),
              ("a", "Categoria principală e «duplicare chei»; cheile auto cu cip nu apar ca serviciu."),
              ("a", 'Pagina de Facebook e pe numele AG KeyLine, nu Magic Key <span class="marcaj">de confirmat</span>.')]),
            ("Lucrarea", "cererea și cheia",
             [("a", "Tot ce e despre o cheie auto (marcă, an, ce s-a pierdut) se află doar la telefon."),
              ("a", "Un client a sunat când nu erați la stand și a revenit mai târziu: cererile din afara standului depind de apel."),
              ("", "Clienții laudă viteza: «rezolvat rapid, la preț bun».")]),
            ("Revenire", "recenzii și recomandări",
             [("", "Recenziile vorbesc de seriozitate și de rezolvarea cazurilor grele."),
              ("a", "53 de recenzii în câțiva ani: fără o cerere la casă, majoritatea clienților mulțumiți nu scriu."),
              ("a", 'Răspunsurile la recenzii <span class="marcaj">de confirmat</span>.')]),
        ],
        leg=("bine", "de verificat / timp pierdut", "clienți pierduți"),
        et2="Ce spun clienții (Google)",
        voce=[("Recomand! Am facut niste chei duplicat si domnul care se ocupa a rezolvat rapid, la pret bun. Multumesc.", "Mihai · acum 5 luni"),
              ("Cheie nouă făcută rapid și fără bătăi de cap – recomand cu încredere!", "Ionut Hrisca · acum un an"),
              ("Deși mă așteptam să nu mă poată ajuta, am incercat totuși…", "Laurentiu Gaina · acum 2 luni")],
        urm='<b>Primele câștiguri, deja în pachet:</b> afișul QR pentru recenzii și site-ul legat de profilul Google. Restul (cât valorează fiecare problemă în lei pe lună) iese din partea 2.',
        supra2="Auditul afacerii · partea 2 din 3",
        h1b='Întâlnirea: <span class="mat">ce vă întrebăm</span>',
        sit2='O discuție de 20–30 de minute. <strong>Întrebările îngroșate sunt esențiale</strong>; restul, dacă avem timp. Fără răspunsuri corecte sau greșite: ne interesează ziua reală.',
        blocuri=[
            ("1", "Ziua de ieri", [("e", "Povestiți-mi ziua de ieri, de la deschidere. Și apoi?"),
                                    ("e", "Câte telefoane primiți într-o zi obișnuită? Câte sunt pentru chei auto?"),
                                    ("", "Ce faceți când sună cineva și sunteți ocupat cu o cheie?")]),
            ("2", "Clienții noi", [("e", "De unde vin clienții noi: Google, Selgros, recomandări?"),
                                    ("", "Ce întrebare auziți cel mai des la telefon? (preț, marcă, «puteți face pentru…?»)"),
                                    ("", "Ce mărci sau modele refuzați sau trimiteți în altă parte?")]),
            ("3", "Lucrarea", [("e", "Cât durează o cheie cu cip, de la cerere până o predați?"),
                                ("", "Mergeți la mașina clientului când nu mai are nicio cheie? Cât costă?"),
                                ("", "Ce se pierde vineri seara sau duminica, când standul e închis?")]),
            ("4", "Revenire și obiective", [("e", "Ce ar trebui să se schimbe în 3 luni ca să spuneți că a meritat?"),
                                             ("", "Cereți clienților recenzii? Cum?"),
                                             ("", "Lucrați cu service-uri sau parcuri auto care vă trimit clienți?")]),
        ],
        et3="Cifrele (le notăm împreună)",
        cifre=["Apeluri pe zi (toate / pentru chei auto)", "Cheie auto: preț mediu (RON)", "Chei auto pe săptămână",
               "Cereri pierdute pe săptămână (apel nepreluat, închis, refuzat)", "Ore pe săptămână la telefon"],
        nota="Cu aceste cifre calculăm cât valorează fiecare problemă în lei pe lună și ce rezolvăm întâi. Partea 3: planul pe 90 de zile.",
    ),
    "pt": dict(
        lang="pt-PT", titulo="Auditoria · Magic Key", supra="Auditoria ao negócio · parte 1 de 3 · cópia PT do Tomás",
        h1='Magic Key, <span class="mat">visto de fora</span>',
        situatie='O que vê um cliente que os procura hoje no Google, antes da primeira conversa. <strong>A parte 2 preenche-se na reunião</strong>, com os números deles; a parte 3 é o plano.',
        fise=[("Avaliações Google", "4,5 ★", "em 53 avaliações", ""),
              ("Site", "nenhum", "a ficha diz «Adicionar um site»", "rau"),
              ("Horário", "2.ª–6.ª 9–17", "sáb. 9–14 · dom. fechado", ""),
              ("Fotografias", "38", "na ficha Google", "")],
        et1="Os 3 motores do negócio",
        motoare=[
            ("Clientes novos", "como os encontram",
             [("", "Ficha Google com morada clara: dentro do Selgros, Șos. Nicolina 57A."),
              ("r", "Sem site: quem procura «chei auto Iași» não vê marcas, serviços nem preços indicativos."),
              ("a", "A categoria principal é «duplicação de chaves»; as chaves auto com chip não aparecem como serviço."),
              ("a", 'A página de Facebook está em nome da AG KeyLine, não Magic Key <span class="marcaj">a confirmar</span>.')]),
            ("O trabalho", "o pedido e a chave",
             [("a", "Tudo sobre uma chave auto (marca, ano, o que se perdeu) só se sabe ao telefone."),
              ("a", "Um cliente ligou quando o dono não estava no stand e voltou mais tarde: os pedidos fora do stand dependem da chamada."),
              ("", "Os clientes elogiam a rapidez: «resolveu rápido, a bom preço».")]),
            ("Retorno", "avaliações e indicações",
             [("", "As avaliações falam de seriedade e de resolver casos difíceis."),
              ("a", "53 avaliações em vários anos: sem pedido ao balcão, a maioria dos clientes satisfeitos não escreve."),
              ("a", 'Respostas às avaliações <span class="marcaj">a confirmar</span>.')]),
        ],
        leg=("bem", "a verificar / tempo perdido", "clientes perdidos"),
        et2="O que dizem os clientes (Google, traduzido)",
        voce=[("Recomendo! Fiz umas cópias de chaves e o senhor que trata disso resolveu rápido, a bom preço. Obrigado.", "Mihai · há 5 meses"),
              ("Chave nova feita rápido e sem dores de cabeça – recomendo com confiança!", "Ionut Hrisca · há um ano"),
              ("Apesar de esperar que não me conseguisse ajudar, tentei mesmo assim…", "Laurentiu Gaina · há 2 meses")],
        urm='<b>Primeiras vitórias, já no pack:</b> o cartaz QR para avaliações e o site ligado à ficha Google. O resto (quanto vale cada problema em lei por mês) sai da parte 2.',
        supra2="Auditoria ao negócio · parte 2 de 3",
        h1b='A reunião: <span class="mat">o que perguntar</span>',
        sit2='Conversa de 20–30 minutos. <strong>As perguntas a negrito são essenciais</strong>; o resto, se houver tempo. O dono aparece numa avaliação como George Boariu: confirmar o nome antes de o usar.',
        blocuri=[
            ("1", "O dia de ontem", [("e", "Conte-me o dia de ontem, desde que abriu. E depois?"),
                                     ("e", "Quantas chamadas recebe num dia normal? Quantas são de chaves auto?"),
                                     ("", "O que faz quando alguém liga e está ocupado com uma chave?")]),
            ("2", "Clientes novos", [("e", "De onde vêm os clientes novos: Google, Selgros, indicações?"),
                                      ("", "Que pergunta ouve mais ao telefone? (preço, marca, «conseguem fazer para…?»)"),
                                      ("", "Que marcas ou modelos recusa ou manda para outro lado?")]),
            ("3", "O trabalho", [("e", "Quanto demora uma chave com chip, do pedido à entrega?"),
                                  ("", "Vai ao carro do cliente quando já não há chave nenhuma? Quanto custa?"),
                                  ("", "O que se perde à sexta à noite ou ao domingo, com o stand fechado?")]),
            ("4", "Retorno e objetivos", [("e", "O que teria de mudar em 3 meses para dizer que valeu a pena?"),
                                           ("", "Pede avaliações aos clientes? Como?"),
                                           ("", "Trabalha com oficinas ou frotas que lhe mandam clientes?")]),
        ],
        et3="Os números (anotar juntos)",
        cifre=["Chamadas por dia (todas / de chaves auto)", "Chave auto: preço médio (RON)", "Chaves auto por semana",
               "Pedidos perdidos por semana (chamada sem resposta, fechado, recusado)", "Horas por semana ao telefone"],
        nota="Com estes números calcula-se quanto vale cada problema em lei por mês e o que se resolve primeiro. Parte 3: o plano de 90 dias.",
    ),
}


def aud_html(t):
    fise = "".join('<div class="fisa %s"><span>%s</span><b>%s</b><small>%s</small></div>' % (c, a, b, s) for a, b, s, c in t["fise"])
    mot = ""
    for h, ce, itens in t["motoare"]:
        li = "".join('<li class="%s">%s</li>' % (c, x) for c, x in itens)
        mot += '<div class="motor"><h3>%s</h3><p class="ce">%s</p><ul>%s</ul></div>' % (h, ce, li)
    leg = ('<p class="legenda"><span><i style="background:var(--verde)"></i>%s</span><span><i style="background:var(--ambra)"></i>%s</span>'
           '<span><i style="background:#D23B2A"></i>%s</span></p>') % t["leg"]
    voce = "".join("<blockquote>«%s»<cite>%s</cite></blockquote>" % v for v in t["voce"])
    blocuri = ""
    for n, h, qs in t["blocuri"]:
        li = "".join('<li class="%s">%s</li>' % (c, q) for c, q in qs)
        blocuri += '<div class="bloc"><h3><span>%s</span>%s</h3><ol>%s</ol></div>' % (n, h, li)
    cifre = "".join("<tr><td>%s</td><td></td></tr>" % c for c in t["cifre"])
    antet = """<header class="antet mic"><div class="sus"><div class="marca"><i></i>Pacheco <b>Studios</b></div>
      <div class="meta"><span>Magic Key · Iași</span><span><b>{dia}</b></span></div></div>
      <p class="supra">{supra}</p><h1>{h1}</h1><p class="situatie">{sit}</p>{profil}</header>"""
    p1 = """<main class="foaie">{antet}<div class="corp">
      <div class="fise">{fise}</div>
      <p class="eticheta">{et1}</p><div class="motoare">{mot}</div>{leg}
      <p class="eticheta" style="margin-top:6mm">{et2}</p><div class="voce" style="margin-top:0">{voce}</div>
      <p class="urm">{urm}</p></div><span class="nr-pag">1</span></main>""".format(
        antet=antet.format(dia=DATA, supra=t["supra"], h1=t["h1"], sit=t["situatie"], profil=profil("#FAFBF8", 12)),
        fise=fise, et1=t["et1"], mot=mot, leg=leg, et2=t["et2"], voce=voce, urm=t["urm"])
    p2 = """<main class="foaie">{antet}<div class="corp">
      <div class="intrebari">{blocuri}</div>
      <div class="cifre"><p class="eticheta">{et3}</p><table>{cifre}</table></div>
      <p class="nota">{nota}</p></div><span class="nr-pag">2</span></main>""".format(
        antet=antet.format(dia=DATA, supra=t["supra2"], h1=t["h1b"], sit=t["sit2"], profil=profil("#FAFBF8", 12)),
        blocuri=blocuri, et3=t["et3"], cifre=cifre, nota=t["nota"])
    return """<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{titulo}</title><style>{fontes}{base}{css}{aud}</style></head><body>{p1}{p2}</body></html>""".format(
        lang=t["lang"], titulo=t["titulo"], fontes=FONTES, base=BASE_CSS, css=DOC_CSS, aud=AUD_CSS, p1=p1, p2=p2)


if __name__ == "__main__":
    saidas = {
        "afis-recenzii-a4.html": afis_html(),
        "afis-recenzii-a5x2.html": afis_a5_html(),
        "oferta-ro.html": oferta_html(OFERTA["ro"]),
        "oferta-pt.html": oferta_html(OFERTA["pt"]),
        "audit-ro.html": aud_html(AUD["ro"]),
        "auditoria-pt.html": aud_html(AUD["pt"]),
    }
    for nome, html in saidas.items():
        (AQUI / nome).write_text(html)
        print("ok", nome)
    print("QR ->", LINK_RECENZIE)
