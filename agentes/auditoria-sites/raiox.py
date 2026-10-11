#!/usr/bin/env python3
"""Agente 3 · Raio-X do primeiro contacto (gatilho grátis da consultoria, decisão do Tomás de 11/10/2026).

Não é uma auditoria (essa é o produto pago) nem vende um site. Mostra, com o que se mede de fora, onde um cliente
novo se perde entre o Google e a primeira mensagem ao negócio, propõe UMA vitória rápida desenhada como System Print
(trigger, fluxo, regra, dono, passagem a uma pessoa, métrica) e pede 20 minutos para ver o que não se vê de fora.

  python3 raiox.py --top 10      os 10 primeiros do ranking (nota Google ≥ 4,4, sem cadeias)
  python3 raiox.py <slug> …      só esses

Saída: raio-x/<slug>/radiografie-<slug>-ro.pdf (dono) e raio-x-<slug>-pt.pdf (Tomás, + notas) e raio-x/ENVIAR.md.
"""
import datetime, html, os, sys
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gerar import (CSS, EXCLUIR, FONTE_GOOGLE, GOOGLE_ABANDONO, RAIZ, RAMO, aud, b64img, escrever_ranking, fraqueza,
                   ler, ler_candidatos, logo_mini, nome_curto, nota_num, pdf, seg, verificacoes, whatsapp, DADOS)

SAIDA = os.path.join(RAIZ, "raio-x")
RAW = f"https://github.com/tspacheco/Designerpacheco/raw/{RAMO}/raio-x"
WHATSAPP_RO = "+40 723 098 556"
WA_LINK = "https://wa.me/40723098556"
MARCAVEL = r"salon|barber|frizer|beauty|nail|unghii|lash|gene|estetic|clinic|masaj|tatu|tattoo|vet|service|restaurant|bistro|pizz|kinetic|fit|cabinet|medic"

T = {
    "ro": {
        "lang": "ro", "nome": "Radiografia primului contact", "etiq": "Gratuit · ce se vede din afară",
        "lead": "Am urmărit pe telefon drumul unui client nou, de la Google până la primul mesaj către voi. Iată unde se rupe.",
        "elogio": "{nota}★ pe Google{aval}. Cei care ajung la voi sunt mulțumiți. Întrebarea e câți se pierd pe drum.",
        "aval": " din {n} de recenzii",
        "medido": "Măsurat pe {d}, pe telefon (Lighthouse, motorul Google PageSpeed, și un iPhone simulat).",
        "teu": "Ce vede clientul azi", "drumul": "Drumul clientului nou",
        "leg": [("r", "se pierde"), ("a", "încetinește"), ("v", "merge"), ("g", "nu se vede din afară")],
        "n_maps": "Vă găsește pe Google Maps", "n_maps_t": "{nota}★{aval}. Aici totul e bine.",
        "n_site": "Deschide pagina voastră",
        "n_site_r": "Conținutul principal apare după {x} s pe telefon.", "n_site_a": "Conținutul principal apare după {x} s.",
        "n_site_v": "Se deschide repede: {x} s.",
        "n_cont": "Vrea să vă contacteze",
        "n_cont_r": "Numărul e doar text: trebuie găsit, copiat și lipit ({p} pași).",
        "n_cont_a": "Butonul de apel nu e în primul ecran{wa}.", "n_cont_a2": "Se poate suna dintr-o apăsare, dar nu există WhatsApp.",
        "n_cont_v": "Sună sau scrie dintr-o apăsare.", "sem_wa": " și nu există WhatsApp",
        "n_marc": "Vrea o programare", "n_marc_r": "Doar la telefon, doar în program.", "n_marc_v": "Se poate programa online.",
        "n_resp": "Cine răspunde și în cât timp?", "n_resp_t": "Nu se vede din afară. Asta e ce vrem să înțelegem cu voi.",
        "medimos": "Ce am măsurat", "pasos": "Pași până la un apel",
        "cats": {"performance": "Viteză pe telefon", "lcp": "Conținut principal", "peso": "Cât descarcă telefonul"},
        "sim": "Da", "nao": "Nu",
        "chk": {
            "https": "Conexiune securizată (lacătul din browser)", "viewport": "Pagina e făcută pentru telefon",
            "cabe": "Încape pe ecran, fără să alunece în lateral", "tel": "Buton care formează numărul",
            "tel1": "Telefonul e vizibil din primul ecran", "whatsapp": "WhatsApp dintr-o apăsare",
            "marcacao": "Programare sau rezervare online", "mapa": "Hartă / «Cum ajungi»",
            "jsonld": "Fișa pentru Google (program, adresă, tip de afacere)",
            "descricao": "Textul care apare sub numele vostru în Google", "ano": "Anul din subsol e la zi",
        },
        "google": "Google a măsurat că, atunci când o pagină se încarcă în {x} s în loc de 1 s, șansa ca omul să plece înainte să vadă ceva crește cu {p} %.",
        "fonte": "Sursa",
        "qw": "Un câștig rapid", "qw_sub": "Un singur lucru, mic și măsurabil, care închide prima ruptură. Desenat ca sistem: ce îl pornește, cine răspunde și ce numărăm.",
        "pr": {"trig": "Pornește când", "flux": "Ce se întâmplă", "regra": "Regula", "dono": "Cine răspunde", "hand": "Când intră un om", "metr": "Ce numărăm"},
        "naovemos": "Ce nu se vede din afară",
        "perg": ["Ce se întâmplă cu un mesaj primit la 21:00?", "Cine răspunde la cererile noi și, de obicei, în cât timp?",
                 "Câte cereri noi aveți pe săptămână și câte devin clienți?"],
        "cta_t": "20 de minute, gratuit", "cta": "Ne spuneți cum lucrați azi. Vă spunem sincer dacă merită mers mai departe și de unde am începe.",
        "cta_wa": "Scrieți-ne pe WhatsApp", "assin": "Pacheco Studios · sisteme cu IA pentru afaceri de servicii · ro.pachecost.com",
        "marca": "Găsim unde se pierde. Desenăm sistemul. Dovedim impactul.",
        "honesta": "Totul a fost măsurat pe pagina voastră, în ziua indicată. Ce nu se poate măsura din afară e marcat ca atare.",
        "pag": "Pagina", "morto": "Linkul din Google duce la o eroare",
        "morto_t": "Cine apasă «Site» în fișa voastră Google nu ajunge nicăieri.",
    },
    "pt": {
        "lang": "pt-PT", "nome": "Raio-X do primeiro contacto", "etiq": "Grátis · o que se vê de fora",
        "lead": "Seguimos no telemóvel o caminho de um cliente novo, do Google até à primeira mensagem para vocês. É aqui que se parte.",
        "elogio": "{nota}★ no Google{aval}. Quem chega até vocês fica satisfeito. A pergunta é quantos se perdem pelo caminho.",
        "aval": " em {n} avaliações",
        "medido": "Medido a {d}, no telemóvel (Lighthouse, o motor do Google PageSpeed, e um iPhone simulado).",
        "teu": "O que o cliente vê hoje", "drumul": "O caminho do cliente novo",
        "leg": [("r", "perde-se"), ("a", "abranda"), ("v", "funciona"), ("g", "não se vê de fora")],
        "n_maps": "Encontra-vos no Google Maps", "n_maps_t": "{nota}★{aval}. Aqui está tudo bem.",
        "n_site": "Abre a vossa página",
        "n_site_r": "O conteúdo principal aparece ao fim de {x} s no telemóvel.", "n_site_a": "O conteúdo principal aparece ao fim de {x} s.",
        "n_site_v": "Abre depressa: {x} s.",
        "n_cont": "Quer contactar-vos",
        "n_cont_r": "O número é só texto: tem de ser encontrado, copiado e colado ({p} passos).",
        "n_cont_a": "O botão de ligar não está no primeiro ecrã{wa}.", "n_cont_a2": "Dá para ligar com um toque, mas não há WhatsApp.",
        "n_cont_v": "Liga ou escreve com um toque.", "sem_wa": " e não há WhatsApp",
        "n_marc": "Quer marcar", "n_marc_r": "Só por telefone, só no horário.", "n_marc_v": "Dá para marcar online.",
        "n_resp": "Quem responde e em quanto tempo?", "n_resp_t": "Não se vê de fora. É isto que queremos perceber convosco.",
        "medimos": "O que medimos", "pasos": "Passos até uma chamada",
        "cats": {"performance": "Velocidade no telemóvel", "lcp": "Conteúdo principal", "peso": "Quanto o telemóvel descarrega"},
        "sim": "Sim", "nao": "Não",
        "chk": {
            "https": "Ligação segura (o cadeado do browser)", "viewport": "A página está feita para telemóvel",
            "cabe": "Cabe no ecrã, sem deslizar para o lado", "tel": "Botão que marca o número",
            "tel1": "Telefone visível no primeiro ecrã", "whatsapp": "WhatsApp com um toque",
            "marcacao": "Marcação ou reserva online", "mapa": "Mapa / «Como chegar»",
            "jsonld": "Ficha para o Google (horário, morada, tipo de negócio)",
            "descricao": "O texto que aparece debaixo do nome no Google", "ano": "O ano do rodapé está atualizado",
        },
        "google": "A Google mediu que, quando uma página carrega em {x} s em vez de 1 s, a probabilidade de a pessoa sair antes de ver alguma coisa aumenta {p} %.",
        "fonte": "Fonte",
        "qw": "Uma vitória rápida", "qw_sub": "Uma só coisa, pequena e mensurável, que fecha a primeira quebra. Desenhada como sistema: o que a dispara, quem responde e o que contamos.",
        "pr": {"trig": "Dispara quando", "flux": "O que acontece", "regra": "A regra", "dono": "Quem responde", "hand": "Quando entra uma pessoa", "metr": "O que contamos"},
        "naovemos": "O que não se vê de fora",
        "perg": ["O que acontece a uma mensagem que chega às 21h?", "Quem responde aos pedidos novos e, normalmente, em quanto tempo?",
                 "Quantos pedidos novos têm por semana e quantos viram clientes?"],
        "cta_t": "20 minutos, sem custo", "cta": "Contam-nos como trabalham hoje. Dizemos com franqueza se vale a pena avançar e por onde começaríamos.",
        "cta_wa": "Falem connosco no WhatsApp", "assin": "Pacheco Studios · sistemas com IA para negócios de serviços · pachecost.com",
        "marca": "Encontramos a fuga. Desenhamos o sistema. Provamos o impacto.",
        "honesta": "Tudo foi medido na vossa página, no dia indicado. O que não se mede de fora está marcado como tal.",
        "pag": "Página", "morto": "O link do Google dá erro",
        "morto_t": "Quem carrega em «Site» na vossa ficha Google não chega a lado nenhum.",
    },
}

# Uma vitória rápida por tipo de quebra, escrita como System Print (PLAYBOOK de consultoria, secção 5).
VITORIAS = {
    "contacto": {
        "ro": dict(titulo="Niciun mesaj nou fără răspuns",
                   trig="Clientul apasă «WhatsApp» pe pagina voastră sau în Google.",
                   flux=["Mesajul pleacă deja scris, cu serviciul ales.", "Ajunge pe WhatsApp-ul vostru, nu într-un formular.",
                         "Primește pe loc o confirmare, semnată ca asistent.", "O persoană numită de voi preia conversația."],
                   regra="Confirmarea doar spune că mesajul a ajuns și când răspundeți. Nu dă prețuri și nu promite ore.",
                   dono="O persoană de la voi, aleasă împreună.",
                   hand="Orice întrebare care trece de confirmare merge direct la persoana numită.",
                   metr="Timpul până la primul răspuns, măsurat din prima săptămână."),
        "pt": dict(titulo="Nenhuma mensagem nova sem resposta",
                   trig="O cliente carrega em «WhatsApp» na vossa página ou no Google.",
                   flux=["A mensagem sai já escrita, com o serviço escolhido.", "Chega ao vosso WhatsApp, não a um formulário.",
                         "Recebe logo uma confirmação, assinada como assistente.", "Uma pessoa escolhida por vocês pega na conversa."],
                   regra="A confirmação só diz que a mensagem chegou e quando respondem. Não dá preços nem promete horas.",
                   dono="Uma pessoa vossa, escolhida em conjunto.",
                   hand="Qualquer pergunta que passe da confirmação vai direta para a pessoa escolhida.",
                   metr="Tempo até à primeira resposta, medido desde a primeira semana."),
    },
    "marcacao": {
        "ro": dict(titulo="Programări primite și când sunteți închiși",
                   trig="Clientul vrea o programare seara sau în weekend.",
                   flux=["Apasă «Programează» pe pagină sau în Google.", "Vede doar orele libere din agenda voastră.",
                         "Primește confirmarea și un memento cu o zi înainte.", "Dimineața, programarea e deja în agendă."],
                   regra="Se pot alege doar orele libere. Serviciile speciale cer confirmarea voastră.",
                   dono="Cine ține agenda (recepția sau voi).",
                   hand="Cereri neobișnuite și anulări în ultima oră merg la o persoană.",
                   metr="Programări făcute în afara programului, numărate din prima săptămână."),
        "pt": dict(titulo="Marcações que entram mesmo com a porta fechada",
                   trig="O cliente quer marcar à noite ou ao fim de semana.",
                   flux=["Carrega em «Marcar» na página ou no Google.", "Vê só as horas livres da vossa agenda.",
                         "Recebe a confirmação e um lembrete na véspera.", "De manhã, a marcação já está na agenda."],
                   regra="Só se escolhem horas livres. Serviços especiais pedem a vossa confirmação.",
                   dono="Quem gere a agenda (receção ou vocês).",
                   hand="Pedidos fora do normal e cancelamentos de última hora vão para uma pessoa.",
                   metr="Marcações feitas fora do horário, contadas desde a primeira semana."),
    },
    "entrada": {
        "ro": dict(titulo="Primul ecran duce direct la contact",
                   trig="Clientul deschide pagina voastră din Google Maps.",
                   flux=["Pagina de intrare se deschide în sub 3 s pe telefon.", "Primul ecran spune ce faceți, unde, și are un buton de contact.",
                         "Fiecare apăsare pe «Sună» sau «WhatsApp» e numărată, fără date personale.", "Vedeți în fiecare săptămână câți au ajuns la voi."],
                   regra="Voi aprobați fiecare text. Nu se colectează date personale.",
                   dono="Voi, cu un raport scurt în fiecare luni.",
                   hand="Mesajele ajung la voi ca și azi; nu răspunde nimeni în locul vostru.",
                   metr="Câți vizitatori apasă «Sună» sau «WhatsApp» pe săptămână."),
        "pt": dict(titulo="O primeiro ecrã leva direto ao contacto",
                   trig="O cliente abre a vossa página a partir do Google Maps.",
                   flux=["A página de entrada abre em menos de 3 s no telemóvel.", "O primeiro ecrã diz o que fazem, onde, e tem um botão de contacto.",
                         "Cada toque em «Ligar» ou «WhatsApp» é contado, sem dados pessoais.", "Veem todas as semanas quantos chegaram até vocês."],
                   regra="Vocês aprovam cada texto. Não se recolhem dados pessoais.",
                   dono="Vocês, com um relatório curto todas as segundas.",
                   hand="As mensagens chegam-vos como hoje; ninguém responde no vosso lugar.",
                   metr="Quantos visitantes carregam em «Ligar» ou «WhatsApp» por semana."),
    },
}

CSS_RX = """
.lead{font:500 12.5pt/1.4 var(--corpo);margin-top:3mm;max-width:50ch}
.p1{display:grid;grid-template-columns:58mm 1fr;gap:8mm;margin-top:7mm;flex:1;align-items:start}
.p1 .tel{width:58mm;height:122mm}
.p1 .cap{font:700 7pt/1 var(--corpo);letter-spacing:.14em;text-transform:uppercase;color:var(--cinza);margin-bottom:3mm;text-align:center}
.rota h3{font:400 12pt/1 var(--display);text-transform:uppercase;margin-bottom:4mm}
.no{position:relative;padding:0 0 4.2mm 9mm}
.no:before{content:"";position:absolute;left:2.6mm;top:5mm;bottom:0;border-left:1.4px dashed var(--linha)}
.no:last-child:before{display:none}
.no i{position:absolute;left:0;top:.6mm;width:5.6mm;height:5.6mm;border-radius:50%;border:1.6px solid}
.no.sr i{background:#F7E1DD;border-color:var(--mau)}.no.sa i{background:#F8EBD3;border-color:var(--medio)}
.no.sv i{background:#E3F0E9;border-color:var(--bom)}.no.sg i{background:#fff;border-color:#9C958B;border-style:dashed}
.no b{display:block;font:700 10.5pt/1.25 var(--corpo)}
.no span{display:block;font-size:9pt;color:#3C3832;margin-top:.6mm}
.no.sr span{color:var(--mau)}
.leg{display:flex;flex-wrap:wrap;gap:2mm 5mm;font-size:7.5pt;color:var(--cinza);margin-top:2mm}
.leg span{display:flex;align-items:center;gap:1.5mm}
.leg i{width:3mm;height:3mm;border-radius:50%;border:1.3px solid;display:inline-block}
.leg .sr{background:#F7E1DD;border-color:var(--mau)}.leg .sa{background:#F8EBD3;border-color:var(--medio)}
.leg .sv{background:#E3F0E9;border-color:var(--bom)}.leg .sg{border-color:#9C958B;border-style:dashed}
.print{border:1.4px solid var(--carvao);border-radius:6px;background:#fff;overflow:hidden;margin-bottom:6mm}
.print header{background:var(--carvao);color:var(--osso);padding:4mm 5mm}
.print header small{display:block;font:700 6.5pt/1 var(--corpo);letter-spacing:.16em;text-transform:uppercase;color:var(--laranja);margin-bottom:1.5mm}
.print header b{font:400 13pt/1.1 var(--display);text-transform:uppercase}
.print .corpo{padding:4mm 5mm;display:grid;grid-template-columns:30mm 1fr;gap:2.4mm 4mm;font-size:9.5pt}
.print dt{font:700 6.8pt/1.5 var(--corpo);letter-spacing:.12em;text-transform:uppercase;color:var(--cinza);padding-top:.4mm}
.print ol{margin:0;padding-left:4.5mm;display:grid;gap:1mm}
.print dd.m{font-weight:700;color:var(--bom)}
.perg{display:grid;gap:2.2mm;margin-bottom:6mm;counter-reset:q}
.perg p{background:var(--osso);border-radius:5px;padding:3mm 4mm 3mm 11mm;position:relative;font:600 10pt/1.35 var(--corpo)}
.perg p:before{counter-increment:q;content:counter(q);position:absolute;left:4mm;top:2.6mm;font:400 12pt/1 var(--display);color:var(--laranja)}
.marca-l{font:400 8.5pt/1.2 var(--display);text-transform:uppercase;letter-spacing:.02em;color:var(--laranja);margin-top:3mm}
"""


def estado(d, c, L):
    """Os nós do caminho do cliente, com cor medida: r (perde-se), a (abranda), v (funciona), g (não se vê de fora)."""
    aval = L["aval"].format(n=c["avaliacoes"]) if c.get("avaliacoes") else ""
    nos = [("v", L["n_maps"], L["n_maps_t"].format(nota=c.get("nota"), aval=aval))]
    if d.get("erro_pagina") and not d.get("notas"):
        nos.append(("r", L["morto"], L["morto_t"]))
        nos.append(("g", L["n_resp"], L["n_resp_t"]))
        return nos
    lcp = seg(aud(d, "largest-contentful-paint"))
    if lcp is not None:
        k = "r" if lcp >= 5 else ("a" if lcp >= 3 else "v")
        nos.append((k, L["n_site"], L[f"n_site_{k}"].format(x=lcp)))
    chk = dict(verificacoes(d, c))
    if not chk.get("tel"):
        nos.append(("r", L["n_cont"], L["n_cont_r"].format(p=passos(d))))
    elif not chk.get("tel1"):
        nos.append(("a", L["n_cont"], L["n_cont_a"].format(wa="" if chk.get("whatsapp") else L["sem_wa"])))
    elif not chk.get("whatsapp"):
        nos.append(("a", L["n_cont"], L["n_cont_a2"]))
    else:
        nos.append(("v", L["n_cont"], L["n_cont_v"]))
    if "marcacao" in chk:
        nos.append(("v" if chk["marcacao"] else "r", L["n_marc"], L["n_marc_v"] if chk["marcacao"] else L["n_marc_r"]))
    nos.append(("g", L["n_resp"], L["n_resp_t"]))
    return nos


def passos(d):
    p = d.get("pagina") or {}
    return 1 if p.get("tel_no_1o_ecra") else (2 if p.get("tel") else 5)


def tipo_vitoria(d, c):
    chk = dict(verificacoes(d, c))
    if not chk.get("tel1"):
        return "contacto"  # nem ligar é fácil: é a primeira quebra
    if chk.get("marcacao") is False:
        return "marcacao"
    return "contacto" if not chk.get("whatsapp") else "entrada"


def system_print(v, L):
    pr = L["pr"]
    passos_ = "".join(f"<li>{html.escape(x)}</li>" for x in v["flux"])
    return (f'<div class="print"><header><small>System Print</small><b>{html.escape(v["titulo"])}</b></header><dl class="corpo">'
            f'<dt>{pr["trig"]}</dt><dd>{html.escape(v["trig"])}</dd><dt>{pr["flux"]}</dt><dd><ol>{passos_}</ol></dd>'
            f'<dt>{pr["regra"]}</dt><dd>{html.escape(v["regra"])}</dd><dt>{pr["dono"]}</dt><dd>{html.escape(v["dono"])}</dd>'
            f'<dt>{pr["hand"]}</dt><dd>{html.escape(v["hand"])}</dd><dt>{pr["metr"]}</dt><dd class="m">{html.escape(v["metr"])}</dd></dl></div>')


def mensagem_ro(c):
    return (f"Bună ziua! Sunt Tomás, de la Pacheco Studios (Iași). {nome_curto(c)} are {c.get('nota')}★ pe Google, așa că am urmărit pe telefon "
            f"drumul unui client nou, de la Google până la primul mesaj către voi, și am notat unde se rupe. Vi-l trimit gratuit, în PDF (3 pagini). "
            f"Ce nu se vede din afară e ce se întâmplă după ce mesajul ajunge la voi. Dacă vreți, discutăm 20 de minute. Mulțumesc!")


def mensagem_morto(c):
    dom = urlparse(c["site"]).netloc.replace("www.", "")
    return (f"Bună ziua! Sunt Tomás, de la Pacheco Studios (Iași). {nome_curto(c)} are {c.get('nota')}★ pe Google. "
            f"Vă scriu pentru că linkul de site din fișa voastră Google ({dom}) duce la o eroare, deci clienții noi care apasă pe el se pierd chiar la primul pas. "
            f"Dacă vreți, discutăm 20 de minute despre cum ajung azi clienții noi la voi și unde se pierd. Mulțumesc!")


def pagina(slug, c, lang, notas=False):
    L = T[lang]
    d = ler(slug)
    n = d.get("notas") or {}
    data = (d.get("medido_em") or "")[:10]
    data_fmt = ".".join(reversed(data.split("-"))) if data else "?"
    aval = L["aval"].format(n=c["avaliacoes"]) if c.get("avaliacoes") else ""
    dom = urlparse(c["site"]).netloc.replace("www.", "")
    shot = os.path.join(DADOS, f"{slug}.jpg")
    img = f'<img src="{b64img(shot)}" alt="">' if os.path.exists(shot) else ""
    topo = f'<div class="topo"><span class="marca">{logo_mini()}Pacheco Studios</span><span>{L["nome"]} · {html.escape(dom)}</span></div>'
    rod = lambda txt, i, tot=3: f'<div class="rodape" style="margin-top:auto"><span>{txt}</span><span>{L["pag"]} {i}/{tot}</span></div>'

    nos = "".join(f'<div class="no s{k}"><i></i><b>{html.escape(t)}</b><span>{html.escape(s)}</span></div>' for k, t, s in estado(d, c, L))
    leg = "".join(f'<span><i class="s{k}"></i>{t}</span>' for k, t in L["leg"])
    p1 = (f'<section class="folha">{topo}<span class="etiqueta">{L["etiq"]}</span>'
          f'<h1 style="font-size:{30 if len(nome_curto(c)) <= 18 else 24}pt">{html.escape(nome_curto(c))}</h1>'
          f'<p class="lead">{L["lead"]}</p><p class="elogio" style="font-size:10.5pt;font-weight:400">{L["elogio"].format(nota=c.get("nota"), aval=aval)}</p>'
          f'<p class="medido">{L["medido"].format(d=data_fmt)}</p>'
          f'<div class="p1"><div><p class="cap">{L["teu"]}</p><div class="tel">{img}</div></div>'
          f'<div class="rota"><h3>{L["drumul"]}</h3>{nos}<div class="leg">{leg}</div></div></div>'
          f'{rod(L["honesta"], 1)}</section>')

    lcp, peso = seg(aud(d, "largest-contentful-paint")), aud(d, "total-byte-weight") or 0
    tiles = [(f"{n.get('performance', '—')}/100", L["cats"]["performance"]), (f"{lcp} s", L["cats"]["lcp"]),
             (f"{peso / 1048576:.1f} MB", L["cats"]["peso"]), (str(passos(d)), L["pasos"])]
    numeros = "".join(f"<div><b>{a}</b><span>{b}</span></div>" for a, b in tiles)
    tabela = "".join(f'<tr><td>{L["chk"][k]}</td><td class="r"><span class="pill {"s" if ok else "n"}">{L["sim"] if ok else L["nao"]}</span></td></tr>'
                     for k, ok in verificacoes(d, c))
    pct = next((p for lim, p in GOOGLE_ABANDONO if lcp and lcp >= lim), None)
    lim = next((lim for lim, p in GOOGLE_ABANDONO if lcp and lcp >= lim), None)
    google = (f'<div class="clientes" style="margin-top:7mm"><p class="grande">{L["google"].format(x=lim, p=pct)}</p>'
              f'<p class="fonte">{L["fonte"]}: {FONTE_GOOGLE}.</p></div>') if pct else ""
    p2 = (f'<section class="folha">{topo}<h2>{L["medimos"]}</h2><div class="numeros">{numeros}</div>'
          f'<table class="chk">{tabela}</table>{google}{rod(L["honesta"], 2)}</section>')

    v = VITORIAS[tipo_vitoria(d, c)][lang]
    perg = "".join(f"<p>{html.escape(q)}</p>" for q in L["perg"])
    p3 = (f'<section class="folha">{topo}<h2>{L["qw"]}</h2><p style="margin:-2mm 0 5mm;color:var(--cinza);max-width:60ch">{L["qw_sub"]}</p>'
          f'{system_print(v, L)}<h2>{L["naovemos"]}</h2><div class="perg">{perg}</div>'
          f'<div class="cta"><div><h3>{L["cta_t"]}</h3><p>{L["cta"]}</p><p class="marca-l">{L["marca"]}</p></div>'
          f'<a href="{WA_LINK}">{L["cta_wa"]}<small>{WHATSAPP_RO}</small></a></div>{rod(L["assin"], 3)}</section>')

    p4 = ""
    if notas:
        p4 = (f'<section class="folha">{topo}<h2>Notas para o Tomás</h2><div class="notas">'
              f'<p><b>{html.escape(c["nome"])}</b> · {html.escape(c.get("categoria", ""))} · {html.escape(c.get("morada", "") or "morada a confirmar")}</p>'
              f'<p>Telefone {html.escape(c.get("telefone", ""))} · WhatsApp: {whatsapp(c)} · Google {c.get("nota")}'
              f'{" · " + c["avaliacoes"] + " avaliações" if c.get("avaliacoes") else ""} · fraqueza do site {fraqueza(d, c)}/100</p>'
              f'<h3>Mensagem (RO), com o PDF romeno</h3><pre>{html.escape(mensagem_ro(c))}</pre>'
              f'<h3>PDF para o dono</h3><pre>{RAW}/{slug}/radiografie-{slug}-ro.pdf</pre>'
              f'<h3>Os 20 minutos (triagem curta, playbook §4)</h3><pre>O objetivo é decidir se há um problema vivo que justifique a Auditoria de Sistemas com IA.\n'
              f'1. Seguir o caminho do PDF no telemóvel do dono e parar no ponto cinzento: o que acontece depois de a mensagem chegar?\n'
              f'2. Perguntas de qualificação: resultado a melhorar em 90 dias; onde entra o pedido; onde abranda ou desaparece; quem é dono da próxima ação; '
              f'o que já se mede; quem aprova.\n3. Se houver fuga viva: propor a auditoria. Se não houver: dizê-lo com franqueza.\n'
              f'4. Nada de preço por mensagem. Não falar de site novo: a vitória rápida é o gatilho, não o produto.</pre></div>'
              f'<div class="rodape" style="margin-top:auto"><span>Interno · não enviar</span><span>4/4</span></div></section>')

    titulo = f'{L["nome"]} · {nome_curto(c)}'
    return (f'<!doctype html><html lang="{L["lang"]}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<meta name="robots" content="noindex"><title>{html.escape(titulo)}</title>'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Archivo:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">'
            f'<style>{CSS}{CSS_RX}</style></head><body>{p1}{p2}{p3}{p4}</body></html>')


def gerar(slug, cands):
    pasta = os.path.join(SAIDA, slug)
    os.makedirs(pasta, exist_ok=True)
    for lang, nome, notas in (("ro", f"radiografie-{slug}-ro", False), ("pt", f"raio-x-{slug}-pt", True)):
        h = os.path.join(pasta, nome + ".html")
        open(h, "w", encoding="utf-8").write(pagina(slug, cands[slug], lang, notas))
        pdf(h, os.path.join(pasta, nome + ".pdf"))
    print("ok", slug)


def escrever_envio(escolhidos, cands):
    data = datetime.date.today().strftime("%d/%m/%Y")
    out = [f"# Agente 3 · Raio-X do primeiro contacto para enviar ({data})", "",
           "Gatilho grátis da consultoria: mostra onde um cliente novo se perde entre o Google e a primeira mensagem e pede 20 minutos "
           "(triagem curta). Não é a auditoria paga e não vende site. Sem preço.", "",
           "Mandar pelo WhatsApp Business RO: mensagem + PDF romeno (link raw, descarrega no telemóvel). WhatsApp dos donos: «?» nos telemóveis "
           "(sem prova pública), «não» nos fixos. Se a mensagem não entregar, ligar ou visitar com a morada; nos fixos, ligar e pedir onde mandar o PDF.", ""]
    for i, s in enumerate(escolhidos, 1):
        c = cands[s]
        out += [f"## {i}. {nome_curto(c)} · {c.get('categoria', '')}", "",
                f"- Telefone {c.get('telefone')} · WhatsApp: {whatsapp(c)} · Google {c.get('nota')}{' · ' + c['avaliacoes'] + ' avaliações' if c.get('avaliacoes') else ''}",
                f"- Morada: {c.get('morada') or 'a confirmar'} · site {c['site']}",
                f"- Vitória rápida proposta: {VITORIAS[tipo_vitoria(ler(s), c)]['pt']['titulo']}",
                f"- PDF RO (dono): {RAW}/{s}/radiografie-{s}-ro.pdf",
                f"- PDF PT (Tomás): {RAW}/{s}/raio-x-{s}-pt.pdf", "", "```", mensagem_ro(c), "```", ""]
    mortos = [(s, c) for s, c in cands.items() if (ler(s) or {}).get("erro_pagina") and not (ler(s) or {}).get("notas")]
    if mortos:
        out += ["## O link do Google dá erro (o cliente novo perde-se no primeiro passo)", "", "Sem PDF: a mensagem chega.", ""]
        for s, c in mortos:
            out += [f"### {nome_curto(c)} · {c.get('categoria', '')}", "",
                    f"- Telefone {c.get('telefone')} · WhatsApp: {whatsapp(c)} · Google {c.get('nota')} · morada {c.get('morada') or 'a confirmar'}",
                    f"- Erro medido: {(ler(s).get('erro_pagina') or '').splitlines()[0][:120]}", "", "```", mensagem_morto(c), "```", ""]
    open(os.path.join(SAIDA, "ENVIAR.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")


def main():
    cands = ler_candidatos()
    a = sys.argv[1:] or ["--top", "10"]
    if a[0] == "--top":
        escolhidos = [s for fr, s, c, d, n in escrever_ranking(cands)
                      if s not in EXCLUIR and nota_num(c) >= 4.4 and d.get("notas") and aud(d, "largest-contentful-paint") is not None][:int(a[1])]
    else:
        escolhidos = a
    os.makedirs(SAIDA, exist_ok=True)
    for s in escolhidos:
        gerar(s, cands)
    escrever_envio(escolhidos, cands)


if __name__ == "__main__":
    main()
