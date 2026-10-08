#!/usr/bin/env python3
"""Proposta de parceria (agente 6, «Parceiros que indicam»): uma folha A4 por versão.

  python3 research/parceiros/proposta/gerar.py

Gera parceria-ro.html/.pdf (Iași, lei), parceria-pt-iasi (a mesma em PT, para o Tomás) e parceria-pt-faro (€).
Os valores vêm de VALORES; mudar a comissão é mudar aí e correr outra vez. Precisa de segno (QR) e do Chromium.
"""
import base64, html, os, subprocess, sys
import segno

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
CHROMIUM = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
DEMO = "https://pachecost.com/demo/la-gioia/"

# Comissão por omissão (proposta a 08/10/2026; decisão final é do Tomás): 20 % da primeira fatura.
VALORES = {
    "lei": dict(site="2.500", mes="375", com_site="500", com_sis="250", moeda="lei"),
    "eur": dict(site="500", mes="75", com_site="100", com_sis="50", moeda="€"),
}

T = {
    "ro": dict(
        lang="ro", v="lei", data="08.10.2026", supra="Program de parteneri · Iași",
        h1="Recomandați-ne o afacere.<br><em>Primiți {com_site} {moeda}.</em>",
        lead="Vedeți în fiecare săptămână firme care abia încep: deschid, închiriază un spațiu, își fac cărți de vizită. "
             "Multe nu au încă site. Noi îl facem; dumneavoastră primiți <strong>{com_site} {moeda}</strong> pentru fiecare client care plătește.",
        et_pasi="Cum funcționează",
        pasi=[("Ne trimiteți un contact", "Numele afacerii și telefonul, pe WhatsApp. Sau le dați numărul nostru și ne spun că vin de la dumneavoastră."),
              ("Le arătăm site-ul lor", "Facem gratuit o demonstrație cu numele afacerii, înainte să plătească ceva. Nu insistăm."),
              ("Primiți comisionul", "{com_site} {moeda} prin transfer bancar, în 7 zile de la plata clientului.")],
        et_cine="Ce primește fiecare",
        voi_t="Dumneavoastră", voi=["<b>{com_site} {moeda}</b> pentru fiecare site vândut", "<b>{com_sis} {moeda}</b> pentru fiecare sistem AI vândut aceluiași client",
                                   "Fără limită de clienți și fără obligații", "Lista clienților recomandați și stadiul lor, oricând cereți"],
        ei_t="Clientul recomandat", ei=["<b>Prima lună de întreținere gratuită</b> ({mes} {moeda}): recomandarea dumneavoastră chiar valorează ceva",
                                        "Demonstrația gratuită, înainte de orice plată", "Auditul complet al afacerii, inclus"],
        ce_t="Ce vindem", ce="Site profesional: <b>{site} {moeda}</b> o singură dată + <b>{mes} {moeda}/lună</b> (domeniu, găzduire, modificări, suport). "
                             "Apoi, dacă proprietarul vrea, sisteme AI: programări, răspunsuri automate, recenzii Google.",
        reciproc="<b>Și noi recomandăm.</b> Clienții noștri au nevoie de contabil, tipografie, spațiu, casă de marcat. Partenerii noștri sunt primii pe listă.",
        demo_t="Un exemplu", demo="Demonstrație făcută pentru o afacere din Iași, înainte ca proprietarul să ne cunoască.",
        functie="Fondator", wa_t="WhatsApp", wa="+40 723 098 556", mail="tomas@pachecost.com", site_t="Site", site="ro.pachecost.com",
        titlu="Program de parteneri — Pacheco Studios"),
    "pt-iasi": dict(
        lang="pt-PT", v="lei", data="08.10.2026", supra="Programa de parceiros · Iași",
        h1="Recomende-nos um negócio.<br><em>Recebe {com_site} {moeda}.</em>",
        lead="Vê todas as semanas empresas que estão a começar: abrem, arrendam um espaço, fazem cartões de visita. "
             "Muitas ainda não têm site. Nós fazemo-lo; o senhor recebe <strong>{com_site} {moeda}</strong> por cada cliente que paga.",
        et_pasi="Como funciona",
        pasi=[("Envia-nos um contacto", "Nome do negócio e telefone, por WhatsApp. Ou dá-lhes o nosso número e dizem que vêm da sua parte."),
              ("Mostramos-lhes o site deles", "Fazemos grátis uma demonstração com o nome do negócio, antes de pagarem o que quer que seja. Sem insistir."),
              ("Recebe a comissão", "{com_site} {moeda} por transferência, até 7 dias depois de o cliente pagar.")],
        et_cine="O que recebe cada um",
        voi_t="O parceiro", voi=["<b>{com_site} {moeda}</b> por cada site vendido", "<b>{com_sis} {moeda}</b> por cada sistema de IA vendido ao mesmo cliente",
                                "Sem limite de clientes e sem obrigações", "Lista dos clientes indicados e do estado de cada um, sempre que pedir"],
        ei_t="O cliente indicado", ei=["<b>Primeiro mês de manutenção grátis</b> ({mes} {moeda}): a sua recomendação vale mesmo alguma coisa",
                                       "Demonstração grátis, antes de qualquer pagamento", "Auditoria completa do negócio, incluída"],
        ce_t="O que vendemos", ce="Site profissional: <b>{site} {moeda}</b> uma vez + <b>{mes} {moeda}/mês</b> (domínio, alojamento, alterações, suporte). "
                                  "Depois, se o dono quiser, sistemas de IA: marcações, respostas automáticas, avaliações Google.",
        reciproc="<b>Nós também recomendamos.</b> Os nossos clientes precisam de contabilista, gráfica, espaço, máquina registadora. Os parceiros são os primeiros da lista.",
        demo_t="Um exemplo", demo="Demonstração feita para um negócio de Iași, antes de o dono nos conhecer.",
        functie="Fundador", wa_t="WhatsApp", wa="+40 723 098 556", mail="tomas@pachecost.com", site_t="Site", site="ro.pachecost.com",
        titlu="Programa de parceiros — Pacheco Studios (versão PT de Iași)"),
    "pt-faro": dict(
        lang="pt-PT", v="eur", data="08.10.2026", supra="Programa de parceiros · Algarve",
        h1="Recomende-nos um negócio.<br><em>Recebe {com_site} {moeda}.</em>",
        lead="Vê todas as semanas empresas que estão a começar: abrem, arrendam um espaço, fazem cartões de visita. "
             "Muitas ainda não têm site. Nós fazemo-lo; o senhor recebe <strong>{com_site} {moeda}</strong> por cada cliente que paga.",
        et_pasi="Como funciona",
        pasi=[("Envia-nos um contacto", "Nome do negócio e telefone, por WhatsApp. Ou dá-lhes o nosso número e dizem que vêm da sua parte."),
              ("Mostramos-lhes o site deles", "Fazemos grátis uma demonstração com o nome do negócio, antes de pagarem o que quer que seja. Sem insistir."),
              ("Recebe a comissão", "{com_site} {moeda} por transferência, até 7 dias depois de o cliente pagar.")],
        et_cine="O que recebe cada um",
        voi_t="O parceiro", voi=["<b>{com_site} {moeda}</b> por cada site vendido", "<b>{com_sis} {moeda}</b> por cada sistema de IA vendido ao mesmo cliente",
                                "Sem limite de clientes e sem obrigações", "Lista dos clientes indicados e do estado de cada um, sempre que pedir"],
        ei_t="O cliente indicado", ei=["<b>Primeiro mês de manutenção grátis</b> ({mes} {moeda}): a sua recomendação vale mesmo alguma coisa",
                                       "Demonstração grátis, antes de qualquer pagamento", "Auditoria completa do negócio, incluída"],
        ce_t="O que vendemos", ce="Site profissional: <b>{site} {moeda}</b> uma vez + <b>{mes} {moeda}/mês</b> (domínio, alojamento, alterações, suporte). "
                                  "Depois, se o dono quiser, sistemas de IA: marcações, respostas automáticas, avaliações Google.",
        reciproc="<b>Nós também recomendamos.</b> Os nossos clientes precisam de contabilista, gráfica, espaço, software de faturação. Os parceiros são os primeiros da lista.",
        demo_t="Um exemplo", demo="Demonstração feita para um negócio do Algarve, antes de o dono nos conhecer.", url_demo="https://pachecost.com/demo/sos-car/",
        functie="Fundador", wa_t="WhatsApp", wa="+351 967 117 357", mail="tomas@pachecost.com", site_t="Site", site="pachecost.com",
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
.cab{background:var(--carvao);color:var(--osso);padding:12mm 15mm 11mm;position:relative;overflow:hidden}
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
    <div class="cx"><h2>{t['ei_t']}</h2><ul>{ei}</ul></div></div></section>
  <section><p class="mono et">{t['ce_t']}</p><p class="ce">{f(t['ce'])}</p></section>
  <p class="rec">{t['reciproc']}</p>
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
