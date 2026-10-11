#!/usr/bin/env python3
"""Triagem (Micro System Print de 1 página) para o parceiro Iulian Paraschiv, mágico (@iulianparaschivmagician), 11/10/2026.

  python3 research/parceiros/triagens/iulian-paraschiv/gerar.py   → triagem-ro.pdf (para mostrar ao Iulian) e triagem-pt.pdf

Feita sem acesso ao perfil (o Instagram pede login à ponte) e sem site próprio encontrado: tudo o que é processo interno
está escrito como hipótese a validar com ele. Nada de números inventados nem preços.
"""
import base64, os, subprocess

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", "..", ".."))
CHROMIUM = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

T = {
 "ro": dict(
  lang="ro", supra="Triaj · Micro System Print", data="Octombrie 2026", tel="+40 723 098 556", site="ro.pachecost.com",
  h1="Iulian Paraschiv<br><em>Nicio cerere de spectacol fără răspuns.</em>",
  aviso="Ipoteză de validat împreună. Nu avem acces la mesajele, agenda sau cifrele tale; am pornit doar de la ce e public.",
  sinais_t="Punctul de plecare",
  sinais=["Instagram-ul (@iulianparaschivmagician) e vitrina principală.",
          "La o căutare după nume nu apare un site sau o pagină de rezervări proprie.",
          "În evenimente, spectacolele sunt de obicei seara și în weekend, adesea exact când vin cererile noi."],
  atual_t="Drumul de azi (de validat)",
  atual=[("Cerere", "DM, WhatsApp sau telefon"), ("Întrebări", "dată, preț, durată, loc"), ("Ofertă", "scrisă de mână"),
         ("Avans", "dată blocată?"), ("Spectacol", ""), ("După", "testimonial? recomandare?")],
  risco="De validat: cine răspunde când ești pe scenă?",
  futuro_t="Sistemul propus",
  futuro=[("Trigger", "Intră o cerere de spectacol, pe orice canal."),
          ("Responsabil", "Un asistent răspunde imediat, întreabă data, tipul evenimentului, numărul de invitați și locul, și verifică agenda."),
          ("Regulă", "Pachete clare pe durată și zonă; data se blochează doar cu avans."),
          ("Predare", "Tu intri pentru evenimente corporate mari, cereri speciale și închidere.")],
  qw_t="3 soluții rapide propuse",
  qw=[("Răspuns automat", "Răspuns în câteva secunde la DM și WhatsApp, cu întrebările potrivite și data verificată, chiar în timpul spectacolului."),
      ("Gestionarea clienților", "O singură listă cu fiecare cerere: cerere → ofertă → avans → spectacol → după, cu reamintiri."),
      ("Recenzii după serviciu", "A doua zi după eveniment: mesaj automat care cere un testimonial, video de la invitați și o recomandare.")],
  alt="Alte variante, după validare: facturi și avansuri automate · plan pentru surse de clienți (organizatori de nunți, săli de evenimente, firme pentru team building) · conținut și calendar din fiecare spectacol.",
  perg_t="3 întrebări pentru validare",
  perg=["Când primești o cerere în timpul unui spectacol, în cât timp răspunzi de obicei?",
        "Unde ții evidența datelor ocupate și a avansurilor?",
        "După eveniment, ceri testimonial sau contactul organizatorului pentru următoarele evenimente?"],
  met_t="Ce măsurăm", met=["Timpul până la primul răspuns", "Cereri → ofertă → avans", "Testimoniale pe eveniment"],
  prox="Pasul următor: validăm harta împreună. Dacă se confirmă, implementăm cele 3 soluții fără cost.",
 ),
 "pt": dict(
  lang="pt-PT", supra="Triagem · Micro System Print", data="Outubro 2026", tel="+351 967 117 357", site="pachecost.com",
  h1="Iulian Paraschiv<br><em>Nenhum pedido de espetáculo sem resposta.</em>",
  aviso="Hipótese para validar com ele. Não temos acesso às mensagens, à agenda nem aos números dele; partimos só do que é público.",
  sinais_t="Ponto de partida",
  sinais=["O Instagram (@iulianparaschivmagician) é a montra principal.",
          "Numa pesquisa pelo nome não aparece site nem página de reservas própria.",
          "Em eventos, os espetáculos são normalmente à noite e ao fim de semana, muitas vezes quando chegam pedidos novos."],
  atual_t="O percurso de hoje (a validar)",
  atual=[("Pedido", "DM, WhatsApp ou telefone"), ("Perguntas", "data, preço, duração, local"), ("Orçamento", "feito à mão"),
         ("Sinal", "data bloqueada?"), ("Espetáculo", ""), ("Depois", "testemunho? recomendação?")],
  risco="A validar: quem responde quando ele está em palco?",
  futuro_t="O sistema proposto",
  futuro=[("Trigger", "Entra um pedido de espetáculo, por qualquer canal."),
          ("Dono", "Um assistente responde logo, pergunta data, tipo de evento, número de convidados e local, e verifica a agenda."),
          ("Regra", "Pacotes claros por duração e zona; a data só fica bloqueada com sinal."),
          ("Handoff", "Ele entra nos eventos corporativos grandes, nos pedidos especiais e no fecho.")],
  qw_t="3 soluções rápidas propostas",
  qw=[("Atendimento automático", "Resposta em segundos a DMs e WhatsApp, com as perguntas certas e a data verificada, mesmo durante o espetáculo."),
      ("Gestão de clientes", "Uma só lista com cada pedido: pedido → orçamento → sinal → espetáculo → depois, com lembretes."),
      ("Avaliações após o serviço", "No dia a seguir ao evento: mensagem automática a pedir testemunho, vídeo dos convidados e uma recomendação.")],
  alt="Outras hipóteses, depois de validar: faturas e sinais automáticos · plano para escalar fontes de leads (organizadores de casamentos, salas de eventos, empresas para team building) · conteúdo e calendário a partir de cada espetáculo.",
  perg_t="3 perguntas de validação",
  perg=["Quando chega um pedido durante um espetáculo, em quanto tempo costuma responder?",
        "Onde regista as datas ocupadas e os sinais?",
        "Depois do evento, pede testemunho ou o contacto do organizador para próximos eventos?"],
  met_t="O que medimos", met=["Tempo até à primeira resposta", "Pedidos → orçamento → sinal", "Testemunhos por evento"],
  prox="Próximo passo: validar o mapa com ele numa reunião. Se se confirmar, implementamos as 3 soluções sem custo.",
 ),
}


def fonte(nome, ficheiro, peso):
    b = base64.b64encode(open(os.path.join(RAIZ, "marca", "fontes", ficheiro), "rb").read()).decode()
    return f"@font-face{{font-family:'{nome}';font-weight:{peso};src:url(data:font/woff2;base64,{b}) format('woff2')}}"


FONTES = "\n".join([fonte("Archivo Black", "archivo-black-ro.woff2", 400), fonte("Inter", "inter-400-ro.woff2", 400),
                    fonte("Inter", "inter-600-ro.woff2", 600), fonte("Space Mono", "space-mono-700-ro.woff2", 700)])

CSS = """
@page{size:A4;margin:0}
:root{--c:#141210;--o:#EFEAE3;--o2:#F7F3EE;--l:#E8622C;--lt:#A64923;--sc:#A5A19B;--so:#4D4A47;--li:#D8D1C7}
*{box-sizing:border-box}html,body{margin:0}
body{font:400 9.2pt/1.45 'Inter',sans-serif;color:var(--c);-webkit-print-color-adjust:exact;print-color-adjust:exact}
.pag{width:210mm;height:297mm;background:var(--o);display:flex;flex-direction:column;overflow:hidden}
.mono{font:700 7.2pt/1 'Space Mono',monospace;letter-spacing:.14em;text-transform:uppercase}
.marca{font:400 10pt/1 'Archivo Black';letter-spacing:.06em;text-transform:uppercase}
.marca i{display:inline-block;width:.42em;height:.42em;border-radius:50%;background:var(--l);margin-left:.12em}
.topo{background:var(--c);color:var(--o);padding:9mm 14mm 8mm}
.topo .l1{display:flex;justify-content:space-between}.topo .l1 .mono{color:var(--sc)}
.topo .sup{color:var(--l);margin:7mm 0 2.5mm;display:block}
h1{font:400 20pt/1.12 'Archivo Black';text-transform:uppercase;margin:0}
h1 em{font-style:normal;color:var(--l);display:block;font-size:15pt;margin-top:1.5mm}
.aviso{margin:3mm 0 0;font-size:8.6pt;color:var(--sc)}
.corpo{flex:1;padding:6mm 14mm 0;display:flex;flex-direction:column;gap:5mm}
h3{font:700 7.4pt/1 'Space Mono';letter-spacing:.14em;text-transform:uppercase;color:var(--lt);margin:0 0 2.5mm;display:flex;gap:3mm;align-items:center}
h3::after{content:'';flex:1;height:1px;background:var(--li)}
.sinais{margin:0;padding:0;list-style:none;display:grid;grid-template-columns:repeat(3,1fr);gap:4mm}
.sinais li{border-top:2px solid var(--c);padding-top:2mm;font-size:8.8pt}
.rota{display:flex;gap:1.5mm;align-items:stretch}
.rota div{flex:1;background:var(--o2);box-shadow:inset 0 0 0 1px var(--li);border-radius:6px;padding:2.5mm;position:relative}
.rota b{display:block;font-weight:600;font-size:9pt}.rota span{font-size:7.8pt;color:var(--so)}
.rota div.r{box-shadow:inset 0 0 0 1.5px var(--l)}
.risco{margin-top:2mm;font:700 7.4pt/1.3 'Space Mono';color:var(--lt);text-transform:uppercase;letter-spacing:.1em}
.fut{display:grid;grid-template-columns:repeat(4,1fr);gap:3mm}
.fut div{background:var(--c);color:var(--o);border-radius:8px;padding:3.5mm}
.fut b{display:block;font:400 10pt/1 'Archivo Black';text-transform:uppercase;color:var(--l);margin-bottom:2mm}
.fut span{font-size:8.3pt;color:#D9D3CA;line-height:1.4}
.qw{display:grid;grid-template-columns:repeat(3,1fr);gap:3mm}
.qw div{background:var(--o2);box-shadow:inset 0 0 0 1px var(--li);border-radius:8px;padding:3.5mm}
.qw b{display:block;font-weight:600;font-size:9.6pt;margin:1.5mm 0 1mm}.qw span{font-size:8.3pt;color:var(--so)}
.qw i{font:700 7.4pt/1 'Space Mono';color:var(--o);background:var(--l);padding:3px 5px;border-radius:3px;font-style:normal}
.alt{font-size:8.2pt;color:var(--so);margin:2.5mm 0 0}
.duas{display:grid;grid-template-columns:1.6fr 1fr;gap:5mm}
.duas ol{margin:0;padding-left:4.5mm;display:grid;gap:1.8mm;font-size:8.8pt}
.duas ul{margin:0;padding:0;list-style:none;display:grid;gap:1.8mm;font-size:8.8pt}
.duas ul li::before{content:'';display:inline-block;width:5px;height:5px;border-radius:50%;background:var(--l);margin-right:2mm;vertical-align:1px}
.prox{margin-top:auto;margin-bottom:6mm;background:var(--l);border-radius:8px;padding:4mm 5mm;font:600 10pt/1.35 'Inter'}
.rod{background:var(--c);color:var(--sc);padding:4.5mm 14mm;display:flex;justify-content:space-between;font-size:8pt}
.rod .marca{color:var(--o)}
"""


def html(t):
    sinais = "".join(f"<li>{x}</li>" for x in t["sinais"])
    rota = "".join(f'<div class="{"r" if i == 0 else ""}"><b>{a}</b><span>{b}</span></div>' for i, (a, b) in enumerate(t["atual"]))
    fut = "".join(f"<div><b>{a}</b><span>{b}</span></div>" for a, b in t["futuro"])
    qw = "".join(f"<div><i>0{i+1}</i><b>{a}</b><span>{b}</span></div>" for i, (a, b) in enumerate(t["qw"]))
    perg = "".join(f"<li>{x}</li>" for x in t["perg"])
    met = "".join(f"<li>{x}</li>" for x in t["met"])
    return f"""<!doctype html><html lang="{t['lang']}"><head><meta charset="utf-8"><title>Triagem Iulian Paraschiv</title>
<style>{FONTES}{CSS}</style></head><body><section class="pag">
<div class="topo"><div class="l1"><span class="marca">Pacheco Studios<i></i></span><span class="mono">{t['data']}</span></div>
<span class="mono sup">{t['supra']}</span><h1>{t['h1']}</h1><p class="aviso">{t['aviso']}</p></div>
<div class="corpo">
<div><h3>{t['sinais_t']}</h3><ul class="sinais">{sinais}</ul></div>
<div><h3>{t['atual_t']}</h3><div class="rota">{rota}</div><p class="risco">{t['risco']}</p></div>
<div><h3>{t['futuro_t']}</h3><div class="fut">{fut}</div></div>
<div><h3>{t['qw_t']}</h3><div class="qw">{qw}</div><p class="alt">{t['alt']}</p></div>
<div class="duas"><div><h3>{t['perg_t']}</h3><ol>{perg}</ol></div><div><h3>{t['met_t']}</h3><ul>{met}</ul></div></div>
<div class="prox">{t['prox']}</div>
</div><footer class="rod"><span class="marca">Pacheco Studios<i></i></span><span>Tomás Pacheco · {t['tel']} · {t['site']}</span></footer>
</section></body></html>"""


for lingua, t in T.items():
    h = os.path.join(AQUI, f"triagem-{lingua}.html")
    open(h, "w", encoding="utf-8").write(html(t))
    p = h[:-5] + ".pdf"
    subprocess.run([CHROMIUM, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={p}", "file://" + h], check=True, capture_output=True)
    print("ok", os.path.relpath(p, RAIZ))
