#!/usr/bin/env python3
"""Plano de 30 dias para a Obiectiv Imobiliare (RO para o dono, PT para o Tomás), 1.000 €.

Uso: python3 plan30.py  →  obiectiv-plan-30-zile-ro.pdf e obiectiv-plan-30-dias-pt.pdf (A4 deitado).
Reutiliza a identidade e os ajudantes de gerar.py.
"""
import os, subprocess
from gerar import AQUI, FONTES, CSS, CHROME, esc, rod, rota_svg

RO = dict(
    marca="PACHECO STUDIOS · PLAN DE 30 DE ZILE PENTRU OBIECTIV IMOBILIARE · OCTOMBRIE 2026",
    capa_k="Obiectiv Imobiliare · Piatra-Neamț · Plan de 30 de zile",
    capa_t="O organizare mai eficientă. În 30 de zile.",
    capa_s="Ați spus clar ce căutați: «o organizare mai eficientă». Acesta este planul: diagnosticul complet, problema principală rezolvată și o față nouă a brandului, în 30 de zile, cu rezultate pe care le vedeți.",
    capa_pasi=["Problema", "30 de zile", "Ce primiți", "Rezultate", "Website", "După", "Investiție"],
    # 2 problema
    pro_k="Problema", pro_t="Ce înseamnă «organizare eficientă» la Obiectiv.",
    pro_azi="Astăzi (ipoteza noastră, de confirmat în diagnostic)", pro_maine="La 30 de zile",
    pro_a=["4 agenți, 538 de anunțuri, 6 canale de intrare, 9 servicii: fiecare fir trăiește în telefonul cuiva",
           "O cerere, o vizionare, un dosar: statusul e în capul agentului, nu într-un loc comun",
           "După ora 17 și sâmbăta, cine preia? Proprietarul află când întreabă",
           "Managementul vede rezultatul la final de lună, nu blocajul din ziua respectivă"],
    pro_b=["Un singur tablou: fiecare cerere, vizionare, ofertă și dosar are status, responsabil și termen",
           "Nimic nu depinde de memoria unei persoane: predarea între agenți durează un minut",
           "Răspunsul și urmărirea merg 7 zile din 7, cu agentul în control",
           "Dimineața, în 5 minute, se vede ce e blocat și cine are nevoie de ajutor"],
    pro_conc="Nu schimbăm oamenii, nici felul în care vând. Schimbăm locul în care trăiește informația și regula după care circulă.",
    # 3 calendar
    cal_k="Cele 30 de zile", cal_t="Patru săptămâni, fiecare cu un livrabil.",
    cal=[("Săptămâna 1", "Diagnostic", "Interviuri cu voi și cu cei 4 agenți, observăm fluxurile reale, numărăm cererile și timpii. Harta tuturor blocajelor, cu priorități. Pornim site-ul nou."),
         ("Săptămâna 2", "Sistemul de organizare", "Construim tabloul comun: cerere, vizionare, ofertă, dosar, cu responsabil și status. Pornesc cele 3 quick wins (răspuns în 5 minute, feedback către proprietar, dosar urmărit)."),
         ("Săptămâna 3", "Echipa lucrează în el", "Agenții folosesc sistemul pe cazuri reale; ajustăm regulile cu ei, nu pentru ei. Site-ul nou intră online."),
         ("Săptămâna 4", "Măsurare și decizie", "Prezentăm rezultatele față de săptămâna 1, diagnosticul final și planul de implementare cu preț. Voi decideți dacă mergem mai departe.")],
    cal_gantt=[("Diagnostic", 0, 1), ("Website nou", 0, 3), ("Tablou și quick wins", 1, 3), ("Echipa în sistem", 2, 4), ("Măsurare și plan", 3, 4)],
    cal_conc="La final de săptămână, de fiecare dată, un lucru vizibil: harta, tabloul, site-ul, rezultatele.",
    # 4 livrabile
    liv_k="Ce primiți", liv_t="Trei lucruri care rămân ale voastre, orice ați decide după.",
    liv=[("01", "Diagnosticul complet", "Toate blocajele firmei, de la primul mesaj la semnare, cu prioritățile și impactul estimat al fiecăruia. Documentul pe baza căruia se decide orice implementare."),
         ("02", "Problema principală rezolvată", "Organizarea: tabloul comun în funcțiune, folosit de echipă, cu reguli scrise și responsabili. Plus cele 3 quick wins pornite."),
         ("03", "O față nouă pentru brand", "Website nou, construit pe ce aveți deja (anunțurile, aplicația, Alesia rămân), care spune clar de ce un proprietar din Neamț vinde cu Obiectiv.")],
    liv_plus="La care se adaugă planul de implementare cu preț, pentru pasul următor.",
    # 5 rezultate
    rez_k="Rezultate vizuale așteptate", rez_t="Ce vedeți în fiecare dimineață, din săptămâna 2.",
    rez_col=["Cereri noi", "În discuție", "Vizionare programată", "Ofertă", "Dosar", "Semnat"],
    rez_cards=[["Ap. 2 cam. · Dărmănești", "Casă · Bistrița", "Teren · Roman"], ["Ap. 3 cam. · Precista", "Spațiu · Centru"], ["Ap. 2 cam. · Orion", "Casă · Gârcina", "Garsonieră · Mărăței"], ["Casă · Dumbrava Roșie"], ["Ap. 3 cam. · Centru", "Ap. 2 cam. · Dărmănești"], ["Ap. 4 cam. · Precista"]],
    rez_ind=[("Timp de răspuns", "jos"), ("Cereri fără răspuns", "jos"), ("Vizionări per cerere", "sus"), ("Proprietari informați după vizionare", "sus"), ("Dosare blocate", "jos"), ("Recomandări după semnare", "sus")],
    rez_nota="Exemple de carduri, nu date reale. Cifrele de pornire le măsurăm în săptămâna 1; cele de la 30 de zile le vedeți în raportul final.",
    # 6 website
    web_k="Website nou", web_t="O față nouă, pe fundația pe care o aveți.",
    web_lista=["Pentru proprietari: de ce vinzi cu Obiectiv, în 6 pași, cu promisiunea de răspuns și de informare după fiecare vizionare",
               "Echipa și felul în care lucrează, cu oamenii pe care îi suni direct",
               "Rapoartele voastre de piață pe cartiere, ca motiv de revenire și de încredere",
               "Cerere de evaluare și de vizionare care intră direct în tabloul comun, fără cont obligatoriu",
               "Anunțurile, aplicația și Alesia rămân și se leagă de noul site"],
    web_conc="Site-ul nu este scopul. Este prima față vizibilă a organizării din spate.",
    # 7 după
    dup_k="După cele 30 de zile", dup_t="Dacă vedeți rezultate, trecem la implementarea reală.",
    dup_obj_k="Obiectivul implementării", dup_obj="Cel puțin dublarea numărului de case vândute în același interval de timp de astăzi. Este obiectivul pe care îl urmărim și îl măsurăm, nu o garanție.",
    dup_cum=[("Prețul implementării", "Se stabilește pe baza diagnosticului: știm exact ce blocaje atacăm și ce valoare au."),
             ("Abonamentul lunar", "Începe după prima lună de implementare, în care însoțim soluția și punerea ei în funcțiune. Valoarea se stabilește odată cu planul."),
             ("Dacă nu continuați", "Păstrați diagnosticul cu toate blocajele și prioritățile, site-ul nou și problema principală rezolvată.")],
    dup_conc="Decizia o luați cu rezultatele pe masă, nu cu promisiuni.",
    # 8 investiție
    inv_k="Investiție", inv_t="1.000 € pentru cele 30 de zile.",
    inv_incl=["Diagnosticul complet, cu toate blocajele și prioritățile", "Problema principală rezolvată: organizarea, cu tabloul comun și 3 quick wins", "Website nou, o față nouă pentru brand", "Planul de implementare cu preț, pentru pasul următor"],
    inv_pas_k="Pasul următor", inv_pas="Confirmați și stabilim ziua 1: o întâlnire cu voi și cu cei 4 agenți, la birou sau online.",
    inv_livram_k="Ce livrăm", inv_livram="Găsim scurgerea. Proiectăm sistemul. Dovedim impactul.",
    inv_contact=["Tomás Pacheco · Pacheco Studios", "WhatsApp +40 723 098 556", "ro.pachecost.com"],
)

PT = dict(
    marca="PACHECO STUDIOS · PLANO DE 30 DIAS PARA A OBIECTIV IMOBILIARE · OUTUBRO 2026",
    capa_k="Obiectiv Imobiliare · Piatra-Neamț · Plano de 30 dias",
    capa_t="Uma organização mais eficiente. Em 30 dias.",
    capa_s="Disseram claramente o que procuram: «uma organização mais eficiente». Este é o plano: o diagnóstico completo, o problema principal resolvido e uma cara nova para a marca, em 30 dias, com resultados que se veem.",
    capa_pasi=["Problema", "30 dias", "O que recebem", "Resultados", "Website", "Depois", "Investimento"],
    pro_k="O problema", pro_t="O que significa «organização eficiente» na Obiectiv.",
    pro_azi="Hoje (a nossa hipótese, a confirmar no diagnóstico)", pro_maine="Aos 30 dias",
    pro_a=["4 agentes, 538 anúncios, 6 canais de entrada, 9 serviços: cada fio vive no telemóvel de alguém",
           "Um pedido, uma visita, um processo: o estado está na cabeça do agente, não num sítio comum",
           "Depois das 17 e ao sábado, quem assume? O proprietário sabe quando pergunta",
           "A gestão vê o resultado ao fim do mês, não o bloqueio do próprio dia"],
    pro_b=["Um só quadro: cada pedido, visita, proposta e processo tem estado, dono e prazo",
           "Nada depende da memória de uma pessoa: a passagem entre agentes demora um minuto",
           "Resposta e seguimento correm 7 dias por semana, com o agente no controlo",
           "De manhã, em 5 minutos, vê-se o que está bloqueado e quem precisa de ajuda"],
    pro_conc="Não mudamos as pessoas nem a forma como vendem. Mudamos o sítio onde a informação vive e a regra pela qual circula.",
    cal_k="Os 30 dias", cal_t="Quatro semanas, cada uma com um entregável.",
    cal=[("Semana 1", "Diagnóstico", "Entrevistas convosco e com os 4 agentes, observamos os fluxos reais, contamos pedidos e tempos. Mapa de todos os bloqueios, com prioridades. Arrancamos o site novo."),
         ("Semana 2", "O sistema de organização", "Construímos o quadro comum: pedido, visita, proposta, processo, com dono e estado. Arrancam os 3 quick wins (resposta em 5 minutos, feedback ao proprietário, processo seguido)."),
         ("Semana 3", "A equipa trabalha nele", "Os agentes usam o sistema em casos reais; afinamos as regras com eles, não por eles. O site novo entra no ar."),
         ("Semana 4", "Medição e decisão", "Apresentamos os resultados face à semana 1, o diagnóstico final e o plano de implementação com preço. Vocês decidem se avançamos.")],
    cal_gantt=[("Diagnóstico", 0, 1), ("Website novo", 0, 3), ("Quadro e quick wins", 1, 3), ("Equipa no sistema", 2, 4), ("Medição e plano", 3, 4)],
    cal_conc="Ao fim de cada semana, sempre uma coisa visível: o mapa, o quadro, o site, os resultados.",
    liv_k="O que recebem", liv_t="Três coisas que ficam vossas, decidam o que decidirem depois.",
    liv=[("01", "O diagnóstico completo", "Todos os bloqueios da empresa, da primeira mensagem à assinatura, com as prioridades e o impacto estimado de cada um. O documento com que se decide qualquer implementação."),
         ("02", "O problema principal resolvido", "A organização: o quadro comum a funcionar, usado pela equipa, com regras escritas e donos. Mais os 3 quick wins a correr."),
         ("03", "Uma cara nova para a marca", "Website novo, construído sobre o que já têm (anúncios, app e Alesia ficam), que diz claramente porque é que um proprietário de Neamț vende com a Obiectiv.")],
    liv_plus="A que se junta o plano de implementação com preço, para o passo seguinte.",
    rez_k="Resultados visuais esperados", rez_t="O que veem todas as manhãs, a partir da semana 2.",
    rez_col=["Pedidos novos", "Em conversa", "Visita marcada", "Proposta", "Processo", "Assinado"],
    rez_cards=[["Ap. T2 · Dărmănești", "Casa · Bistrița", "Terreno · Roman"], ["Ap. T3 · Precista", "Loja · Centro"], ["Ap. T2 · Orion", "Casa · Gârcina", "Estúdio · Mărăței"], ["Casa · Dumbrava Roșie"], ["Ap. T3 · Centro", "Ap. T2 · Dărmănești"], ["Ap. T4 · Precista"]],
    rez_ind=[("Tempo de resposta", "jos"), ("Pedidos sem resposta", "jos"), ("Visitas por pedido", "sus"), ("Proprietários informados após visita", "sus"), ("Processos bloqueados", "jos"), ("Recomendações após assinatura", "sus")],
    rez_nota="Cartões de exemplo, não dados reais. Os números de partida medem-se na semana 1; os dos 30 dias veem-se no relatório final.",
    web_k="Website novo", web_t="Uma cara nova, sobre a base que já têm.",
    web_lista=["Para proprietários: porquê vender com a Obiectiv, em 6 passos, com a promessa de resposta e de informação depois de cada visita",
               "A equipa e a forma como trabalha, com as pessoas a quem se liga diretamente",
               "Os vossos relatórios de mercado por bairro, como motivo de regresso e de confiança",
               "Pedido de avaliação e de visita que entra direto no quadro comum, sem conta obrigatória",
               "Anúncios, app e Alesia ficam e ligam-se ao site novo"],
    web_conc="O site não é o objetivo. É a primeira cara visível da organização que está por trás.",
    dup_k="Depois dos 30 dias", dup_t="Se virem resultados, passamos à implementação real.",
    dup_obj_k="Objetivo da implementação", dup_obj="No mínimo duplicar o número de casas vendidas no mesmo intervalo de tempo de hoje. É o objetivo que perseguimos e medimos, não uma garantia.",
    dup_cum=[("Preço da implementação", "Define-se com base no diagnóstico: sabemos exatamente que bloqueios atacamos e quanto valem."),
             ("Mensalidade", "Começa depois do primeiro mês de implementação, em que acompanhamos a solução e a sua entrada em funcionamento. O valor define-se com o plano."),
             ("Se não continuarem", "Ficam com o diagnóstico com todos os bloqueios e prioridades, o site novo e o problema principal resolvido.")],
    dup_conc="A decisão toma-se com os resultados em cima da mesa, não com promessas.",
    inv_k="Investimento", inv_t="1.000 € pelos 30 dias.",
    inv_incl=["Diagnóstico completo, com todos os bloqueios e prioridades", "Problema principal resolvido: a organização, com o quadro comum e 3 quick wins", "Website novo, uma cara nova para a marca", "Plano de implementação com preço, para o passo seguinte"],
    inv_pas_k="Próximo passo", inv_pas="Confirmam e marcamos o dia 1: uma reunião convosco e com os 4 agentes, no escritório ou online.",
    inv_livram_k="O que entregamos", inv_livram="Encontramos a fuga. Desenhamos o sistema. Provamos o impacto.",
    inv_contact=["Tomás Pacheco · Pacheco Studios", "WhatsApp +40 723 098 556", "ro.pachecost.com"],
)

T = {"ro": RO, "pt": PT}

CSS2 = CSS + """
.duo{display:grid;grid-template-columns:1fr 1fr;gap:8mm;width:100%}
.col h4{font-family:"Space Mono",monospace;font-size:8pt;letter-spacing:.1em;text-transform:uppercase;color:var(--t2);padding-bottom:2.5mm;border-bottom:2px solid var(--b);margin-bottom:1mm}
.col.b h4{color:var(--lt);border-color:var(--l)}
.col li{list-style:none;font-size:12.5pt;line-height:1.4;padding:5mm 0 5mm 8mm;border-bottom:1px solid var(--b);position:relative}
.col.a li:before{content:"";position:absolute;left:0;top:6.8mm;width:3.5mm;height:3.5mm;border:1.5px dashed #A5A19B;border-radius:50%}
.col.b li:before{content:"";position:absolute;left:0;top:6.8mm;width:3.5mm;height:3.5mm;background:var(--l);border-radius:50%}
.sem{display:grid;grid-template-columns:repeat(4,1fr);gap:5mm;margin-top:4mm}
.sem div{border-top:3px solid var(--c);padding-top:3mm}
.sem .q{font-family:"Space Mono",monospace;font-size:7.5pt;letter-spacing:.1em;text-transform:uppercase;color:var(--lt)}
.sem h3{font-family:"Archivo Black",sans-serif;font-weight:400;font-size:13pt;margin:1.5mm 0 2mm}
.sem p{font-size:9.3pt;color:var(--t2);line-height:1.38}
.liv{display:grid;grid-template-columns:repeat(3,1fr);gap:6mm;width:100%}
.liv>div{background:#fff;border:1px solid var(--b);padding:6mm;border-top:3mm solid var(--c)}
.liv .n{font-family:"Space Mono",monospace;font-size:9pt;color:var(--l);letter-spacing:.1em}
.liv h3{font-family:"Archivo Black",sans-serif;font-weight:400;font-size:16pt;line-height:1.1;margin:3mm 0 4mm}
.liv p{font-size:10.5pt;line-height:1.4;color:var(--t2)}
.board{display:grid;grid-template-columns:repeat(6,1fr);gap:3mm;background:var(--c);padding:4mm;border-radius:1.5mm}
.board .c h5{font-family:"Space Mono",monospace;font-size:7.5pt;letter-spacing:.08em;text-transform:uppercase;color:var(--o2);margin-bottom:2mm;display:flex;justify-content:space-between}
.board .c h5 b{color:var(--l)}
.board .cd{background:#FAF8F4;border-radius:1mm;padding:3mm 3mm;margin-bottom:2.5mm;font-size:9pt;line-height:1.25;color:var(--c)}
.board .cd small{display:block;font-family:"Space Mono",monospace;font-size:6.8pt;color:var(--t2);margin-top:1mm}
.board .cd i{display:inline-block;width:2.2mm;height:2.2mm;border-radius:50%;background:var(--l);margin-right:1.5mm;vertical-align:0}
.ind{display:grid;grid-template-columns:repeat(6,1fr);gap:4mm;margin-top:8mm}
.ind div{border-top:1px solid var(--b);padding-top:3mm;font-size:10pt;line-height:1.3;color:var(--t2)}
.ind svg{display:block;margin-bottom:1.5mm}
.dup{display:grid;grid-template-columns:repeat(3,1fr);gap:6mm}
.dup div{border-top:2px solid var(--b);padding-top:3mm}
.dup b{display:block;font-family:"Archivo Black",sans-serif;font-weight:400;font-size:15pt;margin-bottom:2mm}
.dup p{font-size:11.5pt;line-height:1.4;color:var(--t2)}
.obj{background:var(--c);color:var(--o);padding:6mm 7mm;border-left:3mm solid var(--l);margin-top:5mm;display:flex;gap:8mm;align-items:center}
.obj .x{font-family:"Archivo Black",sans-serif;font-size:44pt;line-height:1;color:var(--l);flex:none}
.obj p{font-size:14pt;line-height:1.4}
.preco{font-family:"Archivo Black",sans-serif;font-size:64pt;line-height:1;color:var(--o)}
.preco small{font-family:"Space Mono",monospace;font-size:10pt;letter-spacing:.1em;color:var(--o2);display:block;margin-top:3mm}
.incl li{list-style:none;display:flex;gap:3mm;font-size:11pt;line-height:1.35;padding:3mm 0;border-bottom:1px solid #3a3632;color:var(--o)}
.incl li:before{content:"";width:4mm;height:4mm;border-radius:50%;background:var(--l);flex:none;margin-top:1.2mm}
.wire{background:#fff;border:1px solid var(--b);padding:4mm;width:120mm;flex:none}
"""


def capa(t):
    deco = ''.join(f'<circle cx="{40 + (i % 9) * 30}" cy="{30 + (i // 9) * 30}" r="1.1" fill="#EFEAE3" fill-opacity=".12"/>' for i in range(54))
    return f'''<section class="p esc">
<svg style="position:absolute;right:-10mm;top:-6mm;width:150mm" viewBox="0 0 300 200">{deco}</svg>
<div class="k"><i></i>{esc(t["capa_k"])}</div>
<h1 style="font-size:48pt;margin-top:10mm;max-width:230mm">{esc(t["capa_t"])}</h1>
<p style="font-size:14pt;color:var(--o2);margin-top:7mm;max-width:185mm;line-height:1.4">{esc(t["capa_s"])}</p>
<div style="margin-top:auto;margin-bottom:10mm">{rota_svg(t["capa_pasi"])}</div>
{rod(t, 1)}</section>'''


def problema(t):
    a = ''.join(f'<li>{esc(x)}</li>' for x in t["pro_a"])
    b = ''.join(f'<li>{esc(x)}</li>' for x in t["pro_b"])
    return f'''<section class="p">
<div class="k"><i></i>{esc(t["pro_k"])}</div><h2>{esc(t["pro_t"])}</h2>
<div class="corpo" style="align-items:flex-start"><div class="duo">
<div class="col a"><h4>{esc(t["pro_azi"])}</h4><ul>{a}</ul></div>
<div class="col b"><h4>{esc(t["pro_maine"])}</h4><ul>{b}</ul></div>
</div></div>
<div class="conc">{esc(t["pro_conc"])}</div>
{rod(t, 2)}</section>'''


def calendar(t):
    w, h = 260, 62; x0 = 52; cw = (w - x0) / 4
    g = ''
    for i in range(4):
        g += f'<text x="{x0 + i * cw + cw / 2:.1f}" y="6" text-anchor="middle" font-size="4.6" fill="#4D4A47" style="font-family:Space Mono;letter-spacing:.08em">{esc(t["cal"][i][0].upper())}</text>'
        g += f'<line x1="{x0 + i * cw:.1f}" y1="9" x2="{x0 + i * cw:.1f}" y2="{h}" stroke="#CFC8BC" stroke-width=".5"/>'
    for j, (nome, a, b) in enumerate(t["cal_gantt"]):
        y = 12 + j * 10
        g += f'<text x="{x0 - 3}" y="{y + 5.2}" text-anchor="end" font-size="5" fill="#141210">{esc(nome)}</text>'
        cor = "#E8622C" if j in (0, 4) else "#141210"
        g += f'<rect x="{x0 + a * cw + 1:.1f}" y="{y}" width="{(b - a) * cw - 2:.1f}" height="7" rx="1" fill="{cor}"/>'
    svg = f'<svg viewBox="0 0 {w} {h}" width="100%">{g}</svg>'
    sem = ''.join(f'<div><div class="q">{esc(q)}</div><h3>{esc(h3)}</h3><p>{esc(p)}</p></div>' for q, h3, p in t["cal"])
    return f'''<section class="p">
<div class="k"><i></i>{esc(t["cal_k"])}</div><h2>{esc(t["cal_t"])}</h2>
<div style="margin-top:5mm">{svg}</div>
<div class="sem">{sem}</div>
<div class="conc">{esc(t["cal_conc"])}</div>
{rod(t, 3)}</section>'''


def livrabile(t):
    liv = ''.join(f'<div><div class="n">{n}</div><h3>{esc(h)}</h3><p>{esc(p)}</p></div>' for n, h, p in t["liv"])
    return f'''<section class="p">
<div class="k"><i></i>{esc(t["liv_k"])}</div><h2>{esc(t["liv_t"])}</h2>
<div class="corpo" style="align-items:center"><div class="liv">{liv}</div></div>
<div class="conc">{esc(t["liv_plus"])}</div>
{rod(t, 4)}</section>'''


def rezultate(t):
    agentes = ["Adina", "Alexandra", "Gabriel C.", "Gabriel L."]
    cols = ''
    k = 0
    for i, (c, cards) in enumerate(zip(t["rez_col"], t["rez_cards"])):
        cds = ''
        for cd in cards:
            cds += f'<div class="cd"><i></i>{esc(cd)}<small>{agentes[k % 4]}</small></div>'
            k += 1
        cols += f'<div class="c"><h5>{esc(c)}<b>{len(cards)}</b></h5>{cds}</div>'
    ind = ''
    for nome, d in t["rez_ind"]:
        pts = "2,14 10,10 18,12 26,6 34,4" if d == "sus" else "2,4 10,8 18,6 26,12 34,14"
        ind += f'<div><svg viewBox="0 0 36 18" width="18mm"><polyline points="{pts}" fill="none" stroke="#E8622C" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round"/></svg>{esc(nome)}</div>'
    return f'''<section class="p">
<div class="k"><i></i>{esc(t["rez_k"])}</div><h2>{esc(t["rez_t"])}</h2>
<div style="margin-top:6mm" class="board">{cols}</div>
<div class="ind">{ind}</div>
<div class="sursa" style="margin-top:auto">{esc(t["rez_nota"])}</div>
{rod(t, 5)}</section>'''


def website(t):
    wire = ('<svg viewBox="0 0 120 78" width="100%">'
            '<rect x="0" y="0" width="120" height="78" fill="#FAF8F4"/>'
            '<rect x="0" y="0" width="120" height="7" fill="#141210"/><rect x="4" y="2.5" width="18" height="2" fill="#EFEAE3"/><rect x="92" y="2.5" width="24" height="2" fill="#E8622C"/>'
            '<rect x="6" y="13" width="60" height="6" fill="#141210"/><rect x="6" y="21" width="44" height="3" fill="#141210"/><rect x="6" y="27" width="50" height="1.5" fill="#A5A19B"/><rect x="6" y="30" width="40" height="1.5" fill="#A5A19B"/>'
            '<rect x="6" y="35" width="22" height="5" fill="#E8622C"/>'
            '<rect x="74" y="12" width="40" height="30" fill="#CFC8BC"/>'
            + ''.join(f'<rect x="{6 + i * 18.6}" y="48" width="16" height="12" fill="#fff" stroke="#CFC8BC" stroke-width=".5"/><rect x="{8 + i * 18.6}" y="50" width="4" height="1.5" fill="#E8622C"/><rect x="{8 + i * 18.6}" y="53" width="11" height="1" fill="#A5A19B"/><rect x="{8 + i * 18.6}" y="55" width="9" height="1" fill="#A5A19B"/>' for i in range(6))
            + '<rect x="6" y="65" width="108" height="9" fill="#141210"/><rect x="10" y="68.5" width="30" height="2" fill="#EFEAE3"/><rect x="88" y="67.5" width="22" height="4" fill="#E8622C"/>'
            '</svg>')
    lista = ''.join(f'<li>{esc(x)}</li>' for x in t["web_lista"])
    return f'''<section class="p">
<div class="k"><i></i>{esc(t["web_k"])}</div><h2>{esc(t["web_t"])}</h2>
<div class="corpo" style="gap:12mm;align-items:center">
<div class="wire">{wire}</div>
<ul class="lista" style="flex:1">{lista}</ul>
</div>
<div class="conc">{esc(t["web_conc"])}</div>
{rod(t, 6)}</section>'''


def dupa(t):
    cum = ''.join(f'<div><b>{esc(a)}</b><p>{esc(b)}</p></div>' for a, b in t["dup_cum"])
    return f'''<section class="p">
<div class="k"><i></i>{esc(t["dup_k"])}</div><h2>{esc(t["dup_t"])}</h2>
<div class="obj"><div class="x">2×</div><div><div class="k" style="margin-bottom:2mm">{esc(t["dup_obj_k"])}</div><p>{esc(t["dup_obj"])}</p></div></div>
<div class="dup" style="margin-top:12mm">{cum}</div>
<div class="conc">{esc(t["dup_conc"])}</div>
{rod(t, 7)}</section>'''


def investitie(t):
    incl = ''.join(f'<li>{esc(x)}</li>' for x in t["inv_incl"])
    ct = '<br>'.join(esc(x) for x in t["inv_contact"])
    return f'''<section class="p esc cum">
<div class="k"><i></i>{esc(t["inv_k"])}</div><h2>{esc(t["inv_t"])}</h2>
<div class="corpo" style="gap:16mm;align-items:flex-start;margin-top:8mm">
<div style="width:95mm;flex:none"><div class="preco">1.000 €<small>30 {"DE ZILE" if t is RO else "DIAS"}</small></div>
<div class="k" style="margin-top:10mm">{esc(t["inv_livram_k"])}</div><div class="lv" style="margin-top:2mm;font-size:16pt">{esc(t["inv_livram"])}</div></div>
<div style="flex:1"><ul class="incl">{incl}</ul>
<div class="k" style="margin:7mm 0 3mm">{esc(t["inv_pas_k"])}</div><div class="ctb">{esc(t["inv_pas"])}</div><div class="ct">{ct}</div></div>
</div>
{rod(t, 8)}</section>'''


if __name__ == "__main__":
    for lang, t in T.items():
        html = (f'<!doctype html><html lang="{ {"ro": "ro", "pt": "pt-PT"}[lang] }"><head><meta charset="utf-8"><title>{esc(t["capa_t"])}</title>'
                f'<style>{FONTES}{CSS2}</style></head><body>'
                + capa(t) + problema(t) + calendar(t) + livrabile(t) + rezultate(t) + website(t) + dupa(t) + investitie(t) + '</body></html>')
        nome = {"ro": "obiectiv-plan-30-zile-ro", "pt": "obiectiv-plan-30-dias-pt"}[lang]
        h = os.path.join(AQUI, nome + ".html")
        open(h, "w").write(html)
        pdf = os.path.join(AQUI, nome + ".pdf")
        subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=8000",
                        f"--print-to-pdf={pdf}", "file://" + h], check=True, capture_output=True)
        print(lang, os.path.getsize(pdf) // 1024, "KB")
