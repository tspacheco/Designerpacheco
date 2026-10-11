#!/usr/bin/env python3
"""Triagem (Micro System Print de 1 página) para o parceiro Iulian Paraschiv, mágico (@iulianparaschivmagician), 11/10/2026.

  python3 research/parceiros/triagens/iulian-paraschiv/gerar.py   → triagem-ro.pdf (para mostrar ao Iulian) e triagem-pt.pdf

Formato pedido pelo Tomás (19h12): não adivinhar o percurso dele; mostrar, etapa a etapa, o caminho que a Pacheco Studios
montaria (eficiente) com uma alternativa «se preferir», para ele tirar as suas ideias. Ele já pede avaliações depois de cada
evento, por isso isso não é quick win. Nada de números inventados nem preços.
"""
import base64, os, subprocess

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", "..", ".."))
CHROMIUM = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

T = {
 "ro": dict(
  lang="ro", supra="Triaj · Micro System Print", data="Octombrie 2026", tel="+40 723 098 556", site="ro.pachecost.com",
  h1="Iulian Paraschiv<br><em>Drumul unei cereri, de la primul mesaj la următorul spectacol.</em>",
  aviso="Nu e un diagnostic al afacerii tale: e drumul pe care l-am construi noi, Pacheco Studios, eficient la fiecare pas. Fiecare om lucrează în felul lui, așa că alege ce ți se potrivește.",
  etapas_t="Drumul Pacheco Studios, pas cu pas", ou="Sau, dacă preferi:",
  etapas=[("Cererea", "Toate canalele (DM, WhatsApp, telefon) ajung într-un singur loc, cu răspuns imediat și cererea înregistrată.",
           "răspuns automat doar noaptea sau în timpul spectacolelor; restul răspunzi tu."),
          ("Întrebările", "Un asistent află data, tipul evenimentului, numărul de invitați, locul și bugetul, și verifică agenda.",
           "primești totul rezumat și porți tu discuția, cu datele în mână."),
          ("Oferta", "Oferta se generează din pachete (durată, zonă, extra) și pleacă în aceeași zi.",
           "sistemul pregătește ciorna, iar tu ajustezi și semnezi fiecare ofertă."),
          ("Avansul", "Link de plată pentru avans; data se blochează când intră avansul, cu factură și contract automate.",
           "reamintire automată clientului dacă avansul nu a intrat până la data stabilită."),
          ("Spectacolul", "În săptămâna evenimentului: confirmare de oră, loc și persoană de contact; fișa evenimentului pe telefon.",
           "doar o listă de verificare (material, drum, contact) în ziua spectacolului."),
          ("După", "Ceri deja recenzii. Pasul următor: fiecare testimonial devine conținut, iar organizatorul e întrebat de următoarea dată sau de un contact.",
           "reamintire anuală pentru același client (aniversare, petrecerea firmei de anul viitor).")],
  qw_t="Cele 3 sugestii ale noastre",
  qw=[("Răspuns automat", "Cererea și întrebările de la pașii 1 și 2: răspuns imediat, chiar în timpul spectacolului, cu agenda verificată."),
      ("Gestionarea clienților", "O singură listă cu fiecare cerere, de la primul mesaj până după spectacol, cu reamintiri."),
      ("Facturi și avansuri", "Pasul 4: link de plată, factură și contract, iar data se blochează singură.")],
  alt="Alte variante: plan pentru surse de clienți (organizatori de nunți, săli de evenimente, firme pentru team building) · conținut din recenziile pe care le strângi deja.",
  perg_t="3 întrebări pentru tine",
  perg=["Ce pași îți place să faci personal: discuția, oferta, altceva?",
        "Ce pas îți ia cel mai mult timp astăzi?",
        "De unde ai vrea mai multe cereri: nunți, firme, petreceri private?"],
  met_t="Ce măsurăm", met=["Timpul până la primul răspuns", "Cereri → ofertă → avans", "Spectacole din recomandări"],
  prox="Pasul următor: poți alege 3 dintre aceste direcții și le implementăm fără niciun cost.<small>Scopul e să-ți dovedim valoarea noastră și, când apare ocazia să ne recomanzi, să se întâmple.</small>",
 ),
 "pt": dict(
  lang="pt-PT", supra="Triagem · Micro System Print", data="Outubro 2026", tel="+351 967 117 357", site="pachecost.com",
  h1="Iulian Paraschiv<br><em>O caminho de um pedido, da primeira mensagem ao próximo espetáculo.</em>",
  aviso="Não é um diagnóstico do teu negócio: é o caminho que nós, Pacheco Studios, montaríamos, eficiente em cada passo. Cada um trabalha à sua maneira; escolhe o que te serve.",
  etapas_t="O caminho Pacheco Studios, passo a passo", ou="Ou, se preferires:",
  etapas=[("Pedido", "Todos os canais (DM, WhatsApp, telefone) caem num só sítio, com resposta imediata e o pedido registado.",
           "resposta automática só à noite ou durante os espetáculos; o resto respondes tu."),
          ("Perguntas", "Um assistente recolhe data, tipo de evento, convidados, local e orçamento, e verifica a agenda.",
           "recebes tudo resumido e fazes tu a conversa, já com os dados na mão."),
          ("Orçamento", "A proposta sai de pacotes (duração, zona, extras) e é enviada no mesmo dia.",
           "o sistema prepara o rascunho e tu ajustas e assinas cada orçamento."),
          ("Sinal", "Link de pagamento do sinal; a data fica bloqueada quando o sinal entra, com fatura e contrato automáticos.",
           "lembrete automático ao cliente se o sinal não entrar até à data combinada."),
          ("Espetáculo", "Na semana do evento: confirmação de hora, local e contacto; a ficha do evento no telemóvel.",
           "só uma checklist (material, viagem, contacto) no dia do espetáculo."),
          ("Depois", "Já pedes avaliações. Passo seguinte: cada testemunho vira conteúdo e o organizador é convidado a marcar a próxima data.",
           "lembrete anual ao mesmo cliente (aniversário, festa de empresa do ano seguinte).")],
  qw_t="As nossas 3 sugestões",
  qw=[("Atendimento automático", "Passos 1 e 2: resposta imediata, mesmo durante o espetáculo, com a agenda verificada."),
      ("Gestão de clientes", "Uma só lista com cada pedido, da primeira mensagem até depois do espetáculo, com lembretes."),
      ("Faturas e sinais", "Passo 4: link de pagamento, fatura e contrato, e a data bloqueia-se sozinha.")],
  alt="Outras vertentes: plano para escalar fontes de leads (organizadores de casamentos, salas de eventos, empresas para team building) · conteúdo a partir das avaliações que já recolhes.",
  perg_t="3 perguntas para ti",
  perg=["Que passos gostas de fazer pessoalmente?",
        "Que passo te ocupa mais tempo hoje?",
        "De onde queres mais pedidos: casamentos, empresas, festas?"],
  met_t="O que medimos", met=["Tempo até à primeira resposta", "Pedidos → orçamento → sinal", "Espetáculos vindos de recomendações"],
  prox="Próximo passo: tu podes escolher 3 destas vertentes e implementamos sem qualquer custo.<small>O intuito é provar o nosso valor e, quando houver oportunidade de nos recomendares, fazer acontecer.</small>",
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
.etapas{display:grid;grid-template-columns:repeat(3,1fr);gap:3mm}
.etapas div{background:var(--c);color:var(--o);border-radius:8px;padding:3.5mm;display:flex;flex-direction:column}
.etapas i{font:700 7.4pt/1 'Space Mono';color:var(--c);background:var(--l);padding:3px 5px;border-radius:3px;font-style:normal;align-self:flex-start}
.etapas b{display:block;font:400 11pt/1 'Archivo Black';text-transform:uppercase;color:var(--l);margin:2.5mm 0 1.8mm}
.etapas span{font-size:8.4pt;color:#E6E0D7;line-height:1.42}
.etapas em{font-style:normal;font-size:7.9pt;color:var(--sc);line-height:1.4;margin-top:auto;padding-top:2.5mm;border-top:1px solid #3A3631;margin-top:3mm}
.etapas em strong{color:var(--o);font-weight:600}
.topo{padding:7mm 14mm 6mm}.topo .sup{margin:5mm 0 2mm}h1{font-size:18pt}h1 em{font-size:12.5pt}
.corpo{gap:3.6mm;padding-top:5mm}.etapas div{padding:3mm}.etapas span{font-size:8pt}.etapas em{font-size:7.6pt}
.qw div{padding:3mm}.qw span{font-size:8pt}.prox{margin-bottom:5mm;padding:3.5mm 5mm}.prox small{display:block;font:400 8.8pt/1.4 'Inter';margin-top:1.2mm}
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
    etapas = "".join(f'<div><i>0{i+1}</i><b>{a}</b><span>{b}</span><em><strong>{t["ou"]}</strong> {c}</em></div>'
                     for i, (a, b, c) in enumerate(t["etapas"]))
    qw = "".join(f"<div><i>0{i+1}</i><b>{a}</b><span>{b}</span></div>" for i, (a, b) in enumerate(t["qw"]))
    perg = "".join(f"<li>{x}</li>" for x in t["perg"])
    met = "".join(f"<li>{x}</li>" for x in t["met"])
    return f"""<!doctype html><html lang="{t['lang']}"><head><meta charset="utf-8"><title>Triagem Iulian Paraschiv</title>
<style>{FONTES}{CSS}</style></head><body><section class="pag">
<div class="topo"><div class="l1"><span class="marca">Pacheco Studios<i></i></span><span class="mono">{t['data']}</span></div>
<span class="mono sup">{t['supra']}</span><h1>{t['h1']}</h1><p class="aviso">{t['aviso']}</p></div>
<div class="corpo">
<div><h3>{t['etapas_t']}</h3><div class="etapas">{etapas}</div></div>
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
