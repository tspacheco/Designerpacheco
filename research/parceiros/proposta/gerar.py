#!/usr/bin/env python3
"""Proposta de parceria (agente 6, «Parceiros que indicam»): uma folha A4 por versão.

  python3 research/parceiros/proposta/gerar.py

Gera parceria-ro.html/.pdf (Iași, lei), parceria-pt-iasi (a mesma em PT, para o Tomás) e parceria-pt-faro (€).
Mostra-se ao parceiro depois de entregues os 3 quick wins (a comissão não vai na 1.ª mensagem).
Os valores vêm de VALORES; mudar a comissão é mudar aí e correr outra vez. Precisa de segno (QR) e do Chromium.
"""
import base64, html, os, subprocess, sys
import segno

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
CHROMIUM = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
DEMO = "https://pachecost.com/demo/la-gioia/"

# Acordo decidido pelo Tomás a 11/10/2026 (fonte: /mnt/project-files/prospecao-instagram/COMISSAO-PARCEIROS.md):
# 3 quick wins grátis → o parceiro mostra o nosso nome → 15 % de cada trabalho recomendado (mensalidades fora).
VALORES = {
    "lei": dict(site="2.500", com_site="375", proj="5.000", com_proj="750", mes="375", moeda="lei"),
    "eur": dict(site="500", com_site="75", proj="1.000", com_proj="150", mes="75", moeda="€"),
}

MENU_RO = ["Afiș cu cod QR pentru recenzii Google", "Fișa Google completă: program, servicii, poze reale, buton de programare",
           "Răspunsuri rapide pe WhatsApp Business și Instagram la cele 5 întrebări care se repetă",
           "Formular de cerere sau programare care ajunge deja ordonat la echipă", "Pagină simplă pentru link-ul din bio: servicii, programare, contact",
           "Mesaj automat după serviciu, care cere o recenzie", "Tabel comun de cereri, cu stadiul și responsabilul fiecăreia"]
MENU_PT = ["Cartaz com QR para avaliações Google", "Ficha Google completa: horário, serviços, fotos reais, botão de marcação",
           "Respostas rápidas no WhatsApp Business e no Instagram às 5 perguntas mais repetidas",
           "Formulário de pedido ou marcação que chega já arrumado à equipa", "Página simples para o link da bio: serviços, marcação, contacto",
           "Mensagem automática depois do serviço a pedir avaliação", "Folha partilhada de pedidos, com estado e responsável de cada um"]

_PT = dict(
    lang="pt-PT", data="11.10.2026",
    h1="Nós ajudamos primeiro.<br><em>Depois recomenda-nos.</em>",
    lead="Implementamos sem custo <strong>3 soluções rápidas</strong> no seu negócio. Em troca, diz quem o ajudou "
         "e recomenda-nos: recebe <strong>15 %</strong> de cada trabalho que vier da sua parte.",
    et_pasi="Como funciona",
    pasi=[("Damos primeiro", "Escolhemos consigo 3 soluções rápidas e deixamo-las a funcionar. Não paga nada."),
          ("Mostra o nosso nome", "Um post ou story com @pachecostudiospt e uma linha no seu site: «Sistemas: Pacheco Studios»."),
          ("Recomenda-nos", "Por cada trabalho que vier da sua recomendação recebe 15 %, até 7 dias depois de o cliente pagar.")],
    et_cine="O acordo",
    voi_t="O parceiro recebe", voi=["<b>3 soluções rápidas</b> implementadas, sem custo",
                                   "<b>15 %</b> de cada trabalho recomendado: site de {site} {moeda} → <b>{com_site} {moeda}</b>; projeto de {proj} {moeda} → <b>{com_proj} {moeda}</b>",
                                   "Pagamento por transferência, até 7 dias depois de o cliente pagar", "Sem limite de recomendações e sem obrigações"],
    ei_t="As 3 soluções saem daqui", ei=MENU_PT,
    ce_t="Como se conta", ce="Os 15 % contam sobre o valor da implementação; as mensalidades ficam de fora. Só conta uma apresentação feita com o "
                            "conhecimento do negócio (sabe quem nos apresenta). Site profissional: <b>{site} {moeda}</b> uma vez + {mes} {moeda}/mês.",
    demo_t="Um exemplo", demo="Demonstração feita para um negócio de Iași, antes de o dono nos conhecer.",
    functie="Fundador", wa_t="WhatsApp", wa="+40 723 098 556", mail="tomas@pachecost.com", site_t="Site", site="ro.pachecost.com",
)

T = {
    "ro": dict(
        lang="ro", v="lei", data="11.10.2026", supra="Program de parteneri · Iași",
        h1="Vă ajutăm noi primii.<br><em>Apoi ne recomandați.</em>",
        lead="Implementăm gratuit <strong>3 soluții rapide</strong> în afacerea dumneavoastră. În schimb, spuneți cine v-a ajutat "
             "și ne recomandați: primiți <strong>15%</strong> din fiecare lucrare care vine de la dumneavoastră.",
        et_pasi="Cum funcționează",
        pasi=[("Noi oferim primii", "Alegem împreună 3 soluții rapide și le lăsăm funcționale. Nu plătiți nimic."),
              ("Ne arătați numele", "O postare sau un story cu @pachecostudiospt și un rând pe site-ul dumneavoastră: «Sisteme: Pacheco Studios»."),
              ("Ne recomandați", "Pentru fiecare lucrare care vine din recomandarea dumneavoastră primiți 15%, în 7 zile de la plata clientului.")],
        et_cine="Acordul",
        voi_t="Partenerul primește", voi=["<b>3 soluții rapide</b> implementate, gratuit",
                                         "<b>15%</b> din fiecare lucrare recomandată: site de {site} {moeda} → <b>{com_site} {moeda}</b>; proiect de {proj} {moeda} → <b>{com_proj} {moeda}</b>",
                                         "Plata prin transfer bancar, în 7 zile de la plata clientului", "Fără limită de recomandări și fără obligații"],
        ei_t="Cele 3 soluții se aleg de aici", ei=MENU_RO,
        ce_t="Cum se calculează", ce="Cei 15% se calculează din valoarea implementării; abonamentul lunar nu intră. Contează doar o prezentare făcută cu "
                                    "acordul afacerii (știe cine ne prezintă). Site profesional: <b>{site} {moeda}</b> o singură dată + {mes} {moeda}/lună.",
        demo_t="Un exemplu", demo="Demonstrație făcută pentru o afacere din Iași, înainte ca proprietarul să ne cunoască.",
        functie="Fondator", wa_t="WhatsApp", wa="+40 723 098 556", mail="tomas@pachecost.com", site_t="Site", site="ro.pachecost.com",
        titlu="Program de parteneri — Pacheco Studios"),
    "pt-iasi": dict(_PT, v="lei", supra="Programa de parceiros · Iași", titlu="Programa de parceiros — Pacheco Studios (versão PT de Iași)"),
    "pt-faro": dict(_PT, v="eur", supra="Programa de parceiros · Algarve", wa="+351 967 117 357", site="pachecost.com",
                    demo="Demonstração feita para um negócio do Algarve, antes de o dono nos conhecer.", url_demo="https://pachecost.com/demo/sos-car/",
                    titlu="Programa de parceiros — Pacheco Studios (Algarve)"),
}


def fonte(nome, ficheiro, peso):
    b = base64.b64encode(open(os.path.join(RAIZ, "marca", "fontes", ficheiro), "rb").read()).decode()
    return f"@font-face{{font-family:'{nome}';font-weight:{peso};src:url(data:font/woff2;base64,{b}) format('woff2')}}"


FONTES = "\n".join([fonte("Archivo Black", "archivo-black-ro.woff2", 400), fonte("Inter", "inter-400-ro.woff2", 400),
                    fonte("Inter", "inter-600-ro.woff2", 600), fonte("Space Mono", "space-mono-700-ro.woff2", 700)])


CSS = """
@page{size:A4;margin:0}
:root{--carvao:#141210;--osso:#EFEAE3;--laranja:#E8622C;--l-txt:#A64923;--sec-c:#A5A19B;--sec-o:#4D4A47;--linha:#D8D1C7}
*{box-sizing:border-box}html,body{margin:0}
body{background:#6d6862;font:400 9.6pt/1.45 'Inter',system-ui,sans-serif;color:var(--carvao);-webkit-print-color-adjust:exact;print-color-adjust:exact}
.folha{width:210mm;height:297mm;margin:0 auto;background:var(--osso);display:flex;flex-direction:column;overflow:hidden;position:relative}
@media screen{.folha{margin:24px auto;box-shadow:0 20px 60px rgba(0,0,0,.35)}}
@media print{body{background:none}}
.mono{font:700 7.4pt/1 'Space Mono',monospace;letter-spacing:.14em;text-transform:uppercase}
/* cabeçalho */
.cab{flex:none;background:var(--carvao);color:var(--osso);padding:12mm 15mm 11mm;position:relative;overflow:hidden}
.cab .topo{display:flex;justify-content:space-between;align-items:center;margin-bottom:10mm}
.marca{font:400 10pt/1 'Archivo Black';letter-spacing:.06em;text-transform:uppercase}
.marca i{display:inline-block;width:.42em;height:.42em;border-radius:50%;background:var(--laranja);margin-left:.12em}
.cab .data{color:var(--sec-c)}
.supra{color:var(--laranja);margin:0 0 4mm}
h1{font:400 25pt/1.08 'Archivo Black';text-transform:uppercase;letter-spacing:-.005em;margin:0 0 5mm;max-width:165mm}
h1 em{font-style:normal;color:var(--laranja)}
.lead{font-size:10.6pt;line-height:1.5;color:#D9D3CA;max-width:160mm;margin:0}
.lead strong{color:#fff;font-weight:600}
/* corpo */
.corpo{flex:1;padding:8mm 15mm 0;display:flex;flex-direction:column;gap:6.5mm}
.et{color:var(--l-txt);display:flex;align-items:center;gap:3mm;margin:0 0 3.5mm}
.et::after{content:'';flex:1;height:1px;background:var(--linha)}
.pasi{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,1fr);gap:5mm;counter-reset:p}
.pasi li{counter-increment:p;position:relative;padding-top:10mm}
.pasi li::before{content:'0' counter(p);position:absolute;top:0;left:0;font:700 9pt/1 'Space Mono';color:var(--osso);background:var(--carvao);padding:4px 7px;border-radius:3px}
.pasi li:not(:last-child)::after{content:'';position:absolute;top:3.4mm;left:13mm;right:-4mm;height:1.5px;background:repeating-linear-gradient(90deg,#D35A29 0 4px,transparent 4px 8px)}
.pasi b{display:block;font-weight:600;font-size:10pt;margin-bottom:1.2mm}
.pasi span{color:var(--sec-o);font-size:8.9pt}
.duas{display:grid;grid-template-columns:1fr 1fr;gap:5mm}
.cx{border-radius:10px;padding:5.5mm 5.5mm 5mm;background:#F7F3EE;box-shadow:inset 0 0 0 1px var(--linha)}
.cx.forte{background:var(--carvao);color:var(--osso);box-shadow:inset 0 0 0 1.5px var(--laranja)}
.cx h2{font:700 7.6pt/1 'Space Mono';letter-spacing:.14em;text-transform:uppercase;margin:0 0 3.5mm;color:var(--l-txt)}
.cx.forte h2{color:var(--laranja)}
.cx ul{list-style:none;margin:0;padding:0;display:grid;gap:2.2mm}
.cx li{position:relative;padding-left:4.5mm;font-size:9.2pt;line-height:1.4}
.cx li::before{content:'';position:absolute;left:0;top:.5em;width:5px;height:5px;border-radius:50%;background:var(--laranja)}
.cx.forte li{color:#D9D3CA}.cx.forte li b{color:#fff;font-weight:600}
.cx li b{font-weight:600}
.cx.menu ul{gap:1.6mm}.cx.menu li{font-size:8.6pt;line-height:1.35}
.ce{font-size:9.2pt;line-height:1.5;margin:0;color:var(--sec-o)}
.ce b{color:var(--carvao);font-weight:600}
.rec{margin:0;padding:4mm 5mm;border-left:3px solid var(--laranja);background:#F7F3EE;font-size:9.2pt;color:var(--sec-o)}
.rec b{color:var(--carvao);font-weight:600}
.demo{display:flex;align-items:center;gap:5mm}
.demo svg{flex:none;width:24mm;height:24mm;border-radius:4px}
.demo p{margin:0;font-size:9pt;color:var(--sec-o)}
.demo a{display:block;font:700 9pt/1.3 'Space Mono';color:var(--l-txt);text-decoration:none;margin-top:1.5mm}
/* rodapé */
.rod{margin-top:auto;background:var(--carvao);color:var(--osso);padding:6.5mm 15mm;display:flex;justify-content:space-between;align-items:center;gap:6mm}
.rod .quem strong{display:block;font:400 11pt/1.2 'Archivo Black';text-transform:uppercase;letter-spacing:.02em}
.rod .quem span{color:var(--sec-c);font-size:8.6pt}
.rod dl{display:flex;gap:7mm;margin:0}
.rod dt{color:var(--laranja);margin-bottom:1.8mm}
.rod dd{margin:0;font-weight:600;font-size:9.2pt}
"""

def pagina(t):
    v = VALORES[t["v"]]
    f = lambda s: s.format(**v)
    pasi = "".join(f"<li><b>{f(a)}</b><span>{f(b)}</span></li>" for a, b in t["pasi"])
    voi = "".join(f"<li>{f(x)}</li>" for x in t["voi"])
    ei = "".join(f"<li>{f(x)}</li>" for x in t["ei"])
    demo = t.get("url_demo", DEMO)
    qr = segno.make(demo, error="m").svg_inline(scale=3, dark="#141210", light="#EFEAE3", border=2)
    return f"""<!doctype html>
<html lang="{t['lang']}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(t['titlu'])}</title><style>{FONTES}{CSS}</style></head>
<body><main class="folha">
<header class="cab">
  <div class="topo"><span class="marca">Pacheco Studios<i></i></span><span class="mono data">{t['data']}</span></div>
  <p class="mono supra">{t['supra']}</p>
  <h1>{f(t['h1'])}</h1>
  <p class="lead">{f(t['lead'])}</p>
</header>
<div class="corpo">
  <section><p class="mono et">{t['et_pasi']}</p><ol class="pasi">{pasi}</ol></section>
  <section><p class="mono et">{t['et_cine']}</p>
    <div class="duas"><div class="cx forte"><h2>{t['voi_t']}</h2><ul>{voi}</ul></div>
    <div class="cx menu"><h2>{t['ei_t']}</h2><ul>{ei}</ul></div></div></section>
  <section><p class="mono et">{t['ce_t']}</p><p class="ce">{f(t['ce'])}</p></section>
  <section><p class="mono et">{t['demo_t']}</p>
    <div class="demo">{qr}<p>{t['demo']}<a href="{demo}">{demo.replace('https://', '')}</a></p></div></section>
</div>
<footer class="rod">
  <div class="quem"><strong>Tomás Pacheco</strong><span>{t['functie']} · Pacheco Studios</span></div>
  <dl><div><dt class="mono">{t['wa_t']}</dt><dd>{t['wa']}</dd></div><div><dt class="mono">E-mail</dt><dd>{t['mail']}</dd></div>
  <div><dt class="mono">{t['site_t']}</dt><dd>{t['site']}</dd></div></dl>
</footer>
</main></body></html>"""


for nome, t in T.items():
    h = os.path.join(AQUI, f"parceria-{nome}.html")
    open(h, "w", encoding="utf-8").write(pagina(t))
    pdf = h[:-5] + ".pdf"
    subprocess.run([CHROMIUM, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf}", "file://" + h], check=True, capture_output=True)
    print("ok", os.path.relpath(pdf, RAIZ), os.path.getsize(pdf) // 1024, "KB")
