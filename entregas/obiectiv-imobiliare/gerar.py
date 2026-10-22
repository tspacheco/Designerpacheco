#!/usr/bin/env python3
"""Apresentação para a Obiectiv Imobiliare (Piatra-Neamț), RO para o dono e PT para o Tomás.

Uso: python3 gerar.py  →  obiectiv-imobiliare-ro.pdf e -pt.pdf (A4 deitado) e os .html correspondentes.
Dados: site obiectivimobiliare.ro (lido pela PONTE a 22/10/2026), blog da própria agência (ANCPI, mai 2026),
ANCPI, Guvern (Noua Casă 2026, TVA), INS (recensământ 2021), Storia/OLX (2026), InsideSales/MIT (Lead Response).
"""
import os, subprocess

AQUI = os.path.dirname(os.path.abspath(__file__))
FONTES = open(os.path.join(AQUI, "fonts.css")).read()
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

RO = dict(
    marca="PACHECO STUDIOS · PREZENTARE PENTRU OBIECTIV IMOBILIARE · OCTOMBRIE 2026",
    capa_k="Obiectiv Imobiliare · Piatra-Neamț",
    capa_t="Ce urmează după o vitrină bună.",
    capa_s="Ce am văzut din exterior, cum arată piața din Neamț în 2026, unde se pierd clienți între mesaj și semnătură, și ce construim ca să creșteți cota într-o piață care nu crește.",
    capa_pasi=["Ce am văzut", "Piața", "Drumul clientului", "Viteza", "3 quick wins", "Scalare", "Cum lucrăm"],
    # 2
    vaz_k="Ce am văzut la voi", vaz_t="La vitrină sunteți înaintea pieței.",
    vaz_stats=[("575", "proprietăți în portofoliu"), ("4", "agenți dedicați"), ("9", "servicii sub același acoperiș"), ("5,0", "pe Google · 370 recenzii")],
    vaz_lista=["Site propriu cu aplicație mobilă și cont de client", "Alesia, agent AI, disponibilă pe site", "Blog cu analize lunare din datele ANCPI", "WhatsApp și e-mail 7 zile din 7, 09–20",
               "Anunțuri verificate, tur video, calculator de rate", "Credite, cadastru, acte și dosar: tot sub un acoperiș"],
    vaz_conc="Întrebarea nu mai este cum arătați. Întrebarea este ce se întâmplă în spate, după primul mesaj al unui client.",
    # 3
    pia_k="Piața · județul Neamț", pia_t="Piața nu crește. Cota voastră poate.",
    pia_c1="Tranzacții în județul Neamț, luna mai", pia_c2="Top localități, mai 2026", pia_c3="Tipuri de imobile, mai 2026",
    pia_fapte=[("11.003", "imobile vândute în Neamț în 2025, din care 4.328 cu ipotecă (ANCPI)"),
               ("500 mil. lei", "plafon de garanții Noua Casă 2026: cerere finanțată, dosare de făcut"),
               ("TVA 21 %", "la locuințe noi din august 2025: avantaj pentru second-hand, adică portofoliul vostru"),
               ("79.679", "locuitori în Piatra-Neamț la recensământ (−6,3 % față de 2011, INS)")],
    pia_sursa="Surse: ANCPI, prelucrate în blogul Obiectiv Imobiliare (01.07.2026); Guvernul României; INS. Cifrele agenției: site-ul vostru, 22.10.2026.",
    pia_conc="Mai puține tranzacții pe an, același număr de agenții. Câștigă cine răspunde primul și cine ține proprietarul aproape.",
    # 4
    dru_k="Drumul clientului", dru_t="Unde se pierd clienți între mesaj și semnătură.",
    dru_pasi=["Cerere", "Răspuns", "Vizionare", "Ofertă", "Acte", "Semnare", "Recomandare"],
    dru_vede="Se vede din exterior", dru_nuvede="Nu se vede din exterior (verificăm în audit)",
    dru_ipoteze=[("6 canale × 538 anunțuri × 4 agenți", "Site, aplicație, Alesia, WhatsApp, telefon, portaluri. Cine vede toate firele într-un singur loc?"),
                 ("Birou 09–17, WhatsApp 09–20", "Cine răspunde după ora 17 și sâmbăta, când cei mai mulți oameni caută?"),
                 ("Vizionarea și oferta cer cont", "Câți renunță la pasul «Autentifică-te»? Nimeni nu îi mai vede după aceea."),
                 ("După vizionare", "Ce primește proprietarul? Ce primește cumpărătorul care a spus «mă mai gândesc»?"),
                 ("Dosarul celor 9 servicii", "Cadastru, certificat, credit, acte: cine știe în orice moment unde este fiecare hârtie?")],
    # 5
    vit_k="De ce viteza", vit_t="Primele cinci minute decid cine ia clientul.",
    vit_c="Șansa de a vorbi cu lead-ul, în funcție de timpul de răspuns (studiu Lead Response, InsideSales / MIT)",
    vit_bare=[("5 min", 100), ("10 min", 25), ("30 min", 1)], vit_nota="×100 șansa de contact și ×21 șansa de calificare la 5 min față de 30 min. Măsoară contactul, nu vânzarea.",
    vit_ia=[("30,7 %", "dintre agenții imobiliari din România folosesc IA zilnic (Storia, 2026)"),
            ("descrieri, e-mailuri", "sunt principalele utilizări: IA la vitrină, aproape deloc la răspuns și urmărire"),
            ("7 / 7", "este programul promis clienților; sistemul trebuie să îl țină fără ca agenții să trăiască pe telefon")],
    vit_conc="Avantajul nu este să aveți IA. Este ca niciun client să nu aștepte și niciun proprietar să nu rămână fără vești.",
    # 6
    qw_k="Trei quick wins · primele săptămâni", qw_t="Trei sisteme, fiecare cu un responsabil și o regulă.",
    qw_campos=("Declanșator", "Responsabil", "Regulă", "Predare"),
    qw=[("01", "Niciun lead fără răspuns în 5 minute, 7 zile din 7",
         ["Mesaj pe orice canal: site, aplicație, Alesia, WhatsApp, portal, apel pierdut", "Agentul anunțului; după ora 17 preia sistemul",
          "Răspuns, calificare (buget, finanțare, termen) și propunere de vizionare, imediat", "Agentul primește fișa completă; dimineața are lista zilei"]),
        ("02", "Proprietarul află după fiecare vizionare",
         ["Vizionare încheiată", "Agentul responsabil de proprietate",
          "Feedback către proprietar în 24 h și potrivire cu cumpărătorii din bază", "Raport săptămânal către proprietar: exclusivități păstrate, recomandări câștigate"]),
        ("03", "Dosarul celor 9 servicii, urmărit pas cu pas",
         ["Ofertă acceptată", "Coordonatorul de dosar",
          "Fiecare act are status, termen și persoană; clientul vede oricând unde este", "Semnare fără surprize, apoi cerere de recenzie și recomandare"])],
    # 7
    sca_k="Scalare", sca_t="Trei în prima săptămână. Apoi tot ce curge.",
    sca_a_k="Săptămâna 1", sca_a_n="3", sca_a_t="quick wins construite și pornite",
    sca_a=["Niciun lead fără răspuns în 5 minute, 7 zile din 7", "Proprietarul află după fiecare vizionare", "Dosarul celor 9 servicii, urmărit pas cu pas"],
    sca_b_k="După", sca_b_n="10–20", sca_b_t="scurgeri identificate și rezolvate, una după alta, pe măsură ce auditul le găsește. Candidate deja vizibile:",
    sca_b=["Apel pierdut fără mesaj de revenire", "Lead-uri din portaluri intrate pe e-mail", "Predarea de la Alesia către agent", "Cumpărătorul care a spus «mă mai gândesc»",
           "Evaluare online pentru proprietari", "Raport de piață pe cartier, din blog", "Potrivire automată cumpărător–proprietate", "Exclusivități care expiră fără discuție",
           "Chirii: reînnoiri și întârzieri", "Administrare proprietăți pentru investitori", "Recenzii cerute după fiecare semnare", "Roman, Târgu Neamț și diaspora cu același sistem"],
    sca_conc="Nu o barieră de luni: construim repede, măsurăm, trecem la următoarea. Ordinea o dă acțiunea, nu calendarul.",
    # 8
    cum_k="Cum lucrăm", cum_t="Primul pas este auditul.",
    cum_pasi=["Audit", "Hartă", "Decizie", "Design", "Pilot", "Control"],
    cum_txt=["Observăm fluxurile reale împreună cu echipa: de unde vin cererile, cine răspunde, cât durează, ce se pierde. Fără presupuneri.",
             "Decidem împreună ce construim primul. Fiecare sistem are un responsabil, o regulă și un indicator urmărit săptămânal.",
             "Valoarea auditului se creditează în implementare."],
    cum_livram_k="Ce livrăm", cum_livram="Găsim scurgerea. Proiectăm sistemul. Dovedim impactul.",
    cum_cta_k="Pasul următor", cum_cta="O întâlnire de o oră cu echipa, la birou sau online, ca să stabilim auditul.",
    cum_contact=["Tomás Pacheco · Pacheco Studios", "WhatsApp +40 723 098 556", "ro.pachecost.com"],
)

PT = dict(
    marca="PACHECO STUDIOS · APRESENTAÇÃO PARA A OBIECTIV IMOBILIARE · OUTUBRO 2026",
    capa_k="Obiectiv Imobiliare · Piatra-Neamț",
    capa_t="O que vem depois de uma boa montra.",
    capa_s="O que vimos de fora, como está o mercado de Neamț em 2026, onde se perdem clientes entre a mensagem e a assinatura, e o que construímos para crescer quota num mercado que não cresce.",
    capa_pasi=["O que vimos", "Mercado", "Percurso do cliente", "Velocidade", "3 quick wins", "Escalar", "Como trabalhamos"],
    vaz_k="O que vimos na vossa casa", vaz_t="Na montra estão à frente do mercado.",
    vaz_stats=[("575", "imóveis em carteira"), ("4", "agentes dedicados"), ("9", "serviços sob o mesmo teto"), ("5,0", "no Google · 370 avaliações")],
    vaz_lista=["Site próprio com app móvel e conta de cliente", "Alesia, agente de IA, disponível no site", "Blog com análises mensais dos dados ANCPI", "WhatsApp e e-mail 7 dias por semana, 09–20",
               "Anúncios verificados, tour em vídeo, simulador de prestações", "Crédito, cadastro, escrituras e processo: tudo sob um teto"],
    vaz_conc="A pergunta já não é como se apresentam. A pergunta é o que acontece lá atrás, depois da primeira mensagem de um cliente.",
    pia_k="Mercado · distrito de Neamț", pia_t="O mercado não cresce. A vossa quota pode.",
    pia_c1="Transações no distrito de Neamț, mês de maio", pia_c2="Localidades com mais transações, maio 2026", pia_c3="Tipos de imóvel, maio 2026",
    pia_fapte=[("11.003", "imóveis vendidos em Neamț em 2025, 4.328 com hipoteca (ANCPI)"),
               ("500 mi. lei", "teto de garantias Noua Casă 2026: procura financiada, processos para montar"),
               ("IVA 21 %", "nas casas novas desde agosto de 2025: vantagem para o usado, ou seja, a vossa carteira"),
               ("79.679", "habitantes em Piatra-Neamț no censo (−6,3 % face a 2011, INS)")],
    pia_sursa="Fontes: ANCPI, tratados no blog da Obiectiv Imobiliare (01.07.2026); Governo da Roménia; INS. Números da agência: o vosso site, 22.10.2026.",
    pia_conc="Menos transações por ano, o mesmo número de agências. Ganha quem responde primeiro e quem mantém o proprietário por perto.",
    dru_k="Percurso do cliente", dru_t="Onde se perdem clientes entre a mensagem e a assinatura.",
    dru_pasi=["Pedido", "Resposta", "Visita", "Proposta", "Documentos", "Assinatura", "Recomendação"],
    dru_vede="Vê-se de fora", dru_nuvede="Não se vê de fora (verificamos na auditoria)",
    dru_ipoteze=[("6 canais × 538 anúncios × 4 agentes", "Site, app, Alesia, WhatsApp, telefone, portais. Quem vê todos os fios num só sítio?"),
                 ("Escritório 09–17, WhatsApp 09–20", "Quem responde depois das 17 e ao sábado, quando mais gente procura?"),
                 ("Visita e proposta exigem conta", "Quantos desistem no passo «Autentifica-te»? Depois disso ninguém os volta a ver."),
                 ("Depois da visita", "O que recebe o proprietário? O que recebe o comprador que disse «vou pensar»?"),
                 ("O processo dos 9 serviços", "Cadastro, certificado, crédito, escritura: quem sabe a cada momento onde está cada papel?")],
    vit_k="Porquê a velocidade", vit_t="Os primeiros cinco minutos decidem quem fica com o cliente.",
    vit_c="Probabilidade de falar com o lead, por tempo de resposta (estudo Lead Response, InsideSales / MIT)",
    vit_bare=[("5 min", 100), ("10 min", 25), ("30 min", 1)], vit_nota="×100 a probabilidade de contacto e ×21 a de qualificação aos 5 min face a 30 min. Mede o contacto, não a venda.",
    vit_ia=[("30,7 %", "dos agentes imobiliários na Roménia usam IA todos os dias (Storia, 2026)"),
            ("descrições, e-mails", "são os usos principais: IA na montra, quase nada na resposta e no seguimento"),
            ("7 / 7", "é o horário prometido aos clientes; o sistema tem de o cumprir sem os agentes viverem agarrados ao telemóvel")],
    vit_conc="A vantagem não é ter IA. É nenhum cliente ficar à espera e nenhum proprietário ficar sem notícias.",
    qw_k="Três quick wins · primeiras semanas", qw_t="Três sistemas, cada um com um dono e uma regra.",
    qw_campos=("Gatilho", "Dono", "Regra", "Handoff"),
    qw=[("01", "Nenhum lead sem resposta em 5 minutos, 7 dias por semana",
         ["Mensagem em qualquer canal: site, app, Alesia, WhatsApp, portal, chamada perdida", "O agente do anúncio; depois das 17 assume o sistema",
          "Resposta, qualificação (orçamento, financiamento, prazo) e proposta de visita, de imediato", "O agente recebe a ficha completa; de manhã tem a lista do dia"]),
        ("02", "O proprietário sabe o que aconteceu depois de cada visita",
         ["Visita terminada", "O agente responsável pelo imóvel",
          "Feedback ao proprietário em 24 h e cruzamento com os compradores da base", "Relatório semanal ao proprietário: exclusivos mantidos, recomendações ganhas"]),
        ("03", "O processo dos 9 serviços seguido passo a passo",
         ["Proposta aceite", "O coordenador do processo",
          "Cada documento tem estado, prazo e pessoa; o cliente vê a qualquer momento onde está", "Assinatura sem surpresas, depois pedido de avaliação e recomendação"])],
    sca_k="Escalar", sca_t="Três na primeira semana. Depois tudo o que vaza.",
    sca_a_k="Semana 1", sca_a_n="3", sca_a_t="quick wins construídos e a correr",
    sca_a=["Nenhum lead sem resposta em 5 minutos, 7 dias por semana", "O proprietário sabe o que aconteceu depois de cada visita", "O processo dos 9 serviços seguido passo a passo"],
    sca_b_k="Depois", sca_b_n="10–20", sca_b_t="fugas identificadas e resolvidas, uma a seguir à outra, à medida que a auditoria as encontra. Candidatas já visíveis:",
    sca_b=["Chamada perdida sem mensagem de retorno", "Leads dos portais a cair no e-mail", "Passagem da Alesia para o agente", "O comprador que disse «vou pensar»",
           "Avaliação online para proprietários", "Relatório de mercado por bairro, a partir do blog", "Cruzamento automático comprador–imóvel", "Exclusivos que expiram sem conversa",
           "Arrendamentos: renovações e atrasos", "Gestão de imóveis para investidores", "Avaliações pedidas depois de cada assinatura", "Roman, Târgu Neamț e diáspora com o mesmo sistema"],
    sca_conc="Nenhuma barreira de meses: construímos depressa, medimos, passamos à seguinte. A ordem é dada pela ação, não pelo calendário.",
    cum_k="Como trabalhamos", cum_t="O primeiro passo é a auditoria.",
    cum_pasi=["Auditoria", "Mapa", "Decisão", "Design", "Piloto", "Controlo"],
    cum_txt=["Observamos os fluxos reais com a equipa: de onde vêm os pedidos, quem responde, quanto demora, o que se perde. Sem suposições.",
             "Decidimos juntos o que construir primeiro. Cada sistema tem um dono, uma regra e um indicador seguido semanalmente.",
             "O valor da auditoria é creditado na implementação."],
    cum_livram_k="O que entregamos", cum_livram="Encontramos a fuga. Desenhamos o sistema. Provamos o impacto.",
    cum_cta_k="Próximo passo", cum_cta="Uma reunião de uma hora com a equipa, no escritório ou online, para marcar a auditoria.",
    cum_contact=["Tomás Pacheco · Pacheco Studios", "WhatsApp +40 723 098 556", "ro.pachecost.com"],
)

T = {"ro": RO, "pt": PT}

CSS = """
@page{size:297mm 210mm;margin:0}
:root{--c:#141210;--c2:#1D1A17;--o:#EFEAE3;--o2:#A5A19B;--t2:#4D4A47;--l:#E8622C;--lt:#A64923;--f:#FAF8F4;--b:#CFC8BC;--am:#E3A33B;--vm:#C8432B}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Inter,system-ui,sans-serif;color:var(--c);-webkit-print-color-adjust:exact;print-color-adjust:exact}
.p{width:297mm;height:210mm;position:relative;overflow:hidden;background:var(--f);padding:14mm 18mm 14mm;page-break-after:always;display:flex;flex-direction:column}
.p.esc{background:var(--c);color:var(--o)}
.k{font-family:"Space Mono",monospace;font-size:9.5pt;letter-spacing:.14em;text-transform:uppercase;color:var(--lt);display:flex;align-items:center;gap:3mm}
.esc .k{color:var(--l)}
.k i{display:inline-block;width:9mm;height:2px;background:currentColor}
h1,h2,.num{font-family:"Archivo Black",sans-serif;font-weight:400;letter-spacing:-.01em;line-height:1.02}
h2{font-size:26pt;margin-top:3.5mm;max-width:235mm}
.rod{position:absolute;left:18mm;right:18mm;bottom:7mm;display:flex;justify-content:space-between;font-family:"Space Mono",monospace;font-size:7pt;color:var(--o2);letter-spacing:.06em}
.esc .rod{color:#6f6a63}
.corpo{flex:1;display:flex;margin-top:6mm;min-height:0}
.mono{font-family:"Space Mono",monospace}
svg text{font-family:Inter,sans-serif}
.stat{border-top:2px solid var(--c);padding-top:3mm}
.stat .num{font-size:46pt;color:var(--c)}
.stat .num b{color:var(--l);font-weight:400}
.stat small{display:block;font-size:10.5pt;color:var(--t2);margin-top:1.5mm;line-height:1.3}
.lista li{list-style:none;display:flex;gap:3mm;font-size:12pt;line-height:1.35;padding:4mm 0;border-bottom:1px solid var(--b)}
.lista li:before{content:"";width:4mm;height:4mm;border-radius:50%;background:var(--l);flex:none;margin-top:1.2mm}
.conc{margin-top:auto;background:var(--c);color:var(--o);padding:5mm 7mm;font-size:12.5pt;line-height:1.35;border-left:3mm solid var(--l)}
.esc .conc{background:var(--c2)}
.fapto{display:flex;gap:4mm;align-items:baseline;padding:2.6mm 0;border-bottom:1px solid var(--b)}
.fapto .num{font-size:16pt;min-width:34mm;color:var(--lt)}
.fapto span{font-size:9.3pt;}
.fapto.col{flex-direction:column;gap:1.5mm;border-bottom:0;border-top:2px solid var(--c);padding-top:3mm}
.fapto.col .num{font-size:22pt;min-width:0}
.fapto.col span{font-size:9.6pt;color:var(--t2);line-height:1.3}
.sursa{font-family:"Space Mono",monospace;font-size:6.8pt;color:var(--o2);letter-spacing:.03em;margin-top:3mm}
.ip{display:grid;grid-template-columns:repeat(5,1fr);gap:5mm;margin-top:10mm}
.ip div{border-top:2px solid var(--b);padding-top:2.5mm}
.ip b{display:block;font-size:11pt;line-height:1.25;margin-bottom:1.5mm}
.ip p{font-size:10pt;color:var(--t2);line-height:1.35}
.leg{display:flex;gap:8mm;font-family:"Space Mono",monospace;font-size:7.5pt;letter-spacing:.06em;text-transform:uppercase;color:var(--t2);margin-top:2mm}
.leg i{display:inline-block;width:3.5mm;height:3.5mm;border-radius:50%;margin-right:2mm;vertical-align:-0.5mm}
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:5mm;width:100%}
.card{background:#fff;border:1px solid var(--b);padding:5mm 5.5mm;display:flex;flex-direction:column}
.card .n{font-family:"Space Mono",monospace;font-size:9pt;color:var(--l);letter-spacing:.1em}
.card h3{font-family:"Archivo Black",sans-serif;font-weight:400;font-size:15pt;line-height:1.12;margin:2mm 0 4mm;min-height:17mm}
.card dl{display:grid;grid-template-columns:24mm 1fr;row-gap:4mm;column-gap:2mm;font-size:10.2pt;line-height:1.3}
.card dt{font-family:"Space Mono",monospace;font-size:7.3pt;letter-spacing:.08em;text-transform:uppercase;color:var(--lt);padding-top:.6mm}
.card dd{color:var(--c)}
.trepte{display:grid;grid-template-columns:repeat(4,1fr);gap:4mm;align-items:end;width:100%}
.treapta{background:#fff;border:1px solid var(--b);padding:4.5mm 5mm;border-top:3px solid var(--l)}
.treapta .q{font-family:"Space Mono",monospace;font-size:8pt;letter-spacing:.1em;text-transform:uppercase;color:var(--lt)}
.treapta h3{font-family:"Archivo Black",sans-serif;font-weight:400;font-size:14pt;margin:1.5mm 0 2.5mm}
.treapta p{font-size:10pt;color:var(--t2);line-height:1.38}
.fase{padding:6mm 7mm;display:flex;flex-direction:column}
.fase.a{background:var(--c);color:var(--o);width:92mm;flex:none;border-left:3mm solid var(--l)}
.fase.b{flex:1;border:1px solid var(--b);background:#fff}
.fase .big{font-family:"Archivo Black",sans-serif;font-size:54pt;line-height:1;margin-top:3mm}
.fase .sub{font-size:11pt;line-height:1.35;margin-top:2mm}
.lista.esc{margin-top:5mm}.lista.esc li{border-color:#3a3632;font-size:10.5pt;color:var(--o)}
.chips{display:grid;grid-template-columns:repeat(3,1fr);gap:3mm;margin-top:5mm}
.chip{border:1px solid var(--b);padding:2.5mm 3mm;font-size:8.8pt;line-height:1.3;display:flex;gap:2.5mm;align-items:flex-start}
.chip span{font-family:"Space Mono",monospace;font-size:7.5pt;color:var(--lt);padding-top:.4mm}
.cum p{font-size:11.5pt;line-height:1.45;color:var(--o);max-width:150mm;margin-bottom:4mm}
.cum .lv{font-family:"Archivo Black",sans-serif;font-size:19pt;line-height:1.15;color:var(--o);max-width:150mm}
.ctb{background:var(--l);color:var(--c);padding:5mm 6mm;font-size:11pt;line-height:1.35}
.ct{font-family:"Space Mono",monospace;font-size:9pt;color:var(--o);line-height:1.8;letter-spacing:.04em;margin-top:4mm}
"""


def rod(t, n):
    return f'<div class="rod"><span>{t["marca"]}</span><span>{n:02d}</span></div>'


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def rota_svg(nomes, w=250, ativo=0, claro=True, dash=True):
    xs = [24 + i * (w - 48) / (len(nomes) - 1) for i in range(len(nomes))]
    cor_l = "#EFEAE3" if claro else "#141210"
    nos = ""
    for i, (x, nome) in enumerate(zip(xs, nomes)):
        if i == ativo:
            nos += f'<circle cx="{x}" cy="30" r="7" fill="#E8622C"/>'
        else:
            nos += f'<circle cx="{x}" cy="30" r="5.5" fill="{cor_l}" stroke="{"#141210" if claro else "#EFEAE3"}" stroke-width="1.4"/>'
        cor = "#E8622C" if i == ativo else cor_l
        y = 52 if i % 2 == 0 else 14
        nos += f'<text x="{x}" y="{y}" text-anchor="middle" font-size="5.2" fill="{cor}" style="font-family:Space Mono;letter-spacing:.08em">{esc(nome.upper())}</text>'
    da = 'stroke-dasharray="2 3"' if dash else ''
    return (f'<svg viewBox="0 0 {w} 60" width="100%"><line x1="{xs[0]}" y1="30" x2="{xs[-1]}" y2="30" stroke="{cor_l}" stroke-opacity=".4" stroke-width="1.2" {da}/>'
            f'<line x1="{xs[0]}" y1="30" x2="{xs[min(ativo+1,len(xs)-1)]}" y2="30" stroke="#E8622C" stroke-width="1.6"/>{nos}</svg>')


def capa(t):
    deco = ''.join(f'<circle cx="{40 + (i % 9) * 30}" cy="{30 + (i // 9) * 30}" r="1.1" fill="#EFEAE3" fill-opacity=".12"/>' for i in range(54))
    return f'''<section class="p esc">
<svg style="position:absolute;right:-10mm;top:-6mm;width:150mm" viewBox="0 0 300 200">{deco}</svg>
<div class="k"><i></i>{esc(t["capa_k"])}</div>
<h1 style="font-size:50pt;margin-top:10mm;max-width:220mm">{esc(t["capa_t"])}</h1>
<p style="font-size:14pt;color:var(--o2);margin-top:7mm;max-width:180mm;line-height:1.4">{esc(t["capa_s"])}</p>
<div style="margin-top:auto;margin-bottom:10mm">{rota_svg(t["capa_pasi"])}</div>
{rod(t, 1)}</section>'''


def vazut(t):
    stats = ''.join(f'<div class="stat"><div class="num">{esc(n)}</div><small>{esc(l)}</small></div>' for n, l in t["vaz_stats"])
    lista = ''.join(f'<li>{esc(x)}</li>' for x in t["vaz_lista"])
    return f'''<section class="p">
<div class="k"><i></i>{esc(t["vaz_k"])}</div><h2>{esc(t["vaz_t"])}</h2>
<div class="corpo" style="gap:16mm;align-items:center">
<div style="display:grid;grid-template-columns:1fr 1fr;gap:10mm 12mm;width:128mm;flex:none">{stats}</div>
<ul class="lista" style="flex:1">{lista}</ul>
</div>
<div class="conc">{esc(t["vaz_conc"])}</div>
{rod(t, 2)}</section>'''


def barras(titulo, dados, w=120, h=56, cor_i=None, maxv=None):
    maxv = maxv or max(v for _, v in dados)
    n = len(dados); bw = (w - 10) / n * 0.62; gap = (w - 10) / n
    out = ""
    base = h - 12; alt = base - 10
    for i, (lab, v) in enumerate(dados):
        x = 5 + i * gap + (gap - bw) / 2; bh = alt * v / maxv
        cor = "#E8622C" if (cor_i is not None and i == cor_i) else "#141210"
        out += f'<rect x="{x:.1f}" y="{base - bh:.1f}" width="{bw:.1f}" height="{bh:.1f}" fill="{cor}"/>'
        out += f'<text x="{x + bw / 2:.1f}" y="{base - bh - 2.5:.1f}" text-anchor="middle" font-size="6.2" font-weight="700" fill="#141210">{v}</text>'
        out += f'<text x="{x + bw / 2:.1f}" y="{base + 7:.1f}" text-anchor="middle" font-size="5.4" fill="#4D4A47">{esc(lab)}</text>'
    out += f'<line x1="0" y1="{base}" x2="{w}" y2="{base}" stroke="#CFC8BC" stroke-width=".6"/>'
    return f'<div><div class="k" style="font-size:7.5pt;letter-spacing:.08em;margin-bottom:2mm">{esc(titulo)}</div><svg viewBox="0 0 {w} {h}" width="100%">{out}</svg></div>'


def piata(t):
    g1 = barras(t["pia_c1"], [("2025", 301), ("2026", 279)], cor_i=1)
    g2 = barras(t["pia_c2"], [("Piatra-Neamț", 121), ("Roman", 52), ("Târgu Neamț", 30)], cor_i=0)
    g3 = barras(t["pia_c3"], [("Apart.", 139), ("Case", 102), ("Terenuri", 28), ("Altele", 10)], cor_i=0)
    fapte = ''.join(f'<div class="fapto col"><div class="num">{esc(n)}</div><span>{esc(l)}</span></div>' for n, l in t["pia_fapte"])
    return f'''<section class="p">
<div class="k"><i></i>{esc(t["pia_k"])}</div><h2>{esc(t["pia_t"])}</h2>
<div class="corpo" style="flex-direction:column;align-items:stretch;gap:4mm">
<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10mm">{g1}{g2}{g3}</div>
<div class="sursa">{esc(t["pia_sursa"])}</div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:6mm;margin-top:3mm">{fapte}</div>
</div>
<div class="conc">{esc(t["pia_conc"])}</div>
{rod(t, 3)}</section>'''


def drum(t):
    p = t["dru_pasi"]; w = 270; xs = [26 + i * (w - 52) / (len(p) - 1) for i in range(len(p))]
    vis = [1, 1, 0, 0, 0, 0, 0]  # 0 = invisível de fora
    out = f'<line x1="{xs[0]}" y1="30" x2="{xs[-1]}" y2="30" stroke="#141210" stroke-width="1.2"/>'
    for i, (x, nome) in enumerate(zip(xs, p)):
        if vis[i]:
            out += f'<circle cx="{x}" cy="30" r="6.5" fill="#E8622C"/>'
        else:
            out += f'<circle cx="{x}" cy="30" r="6.5" fill="#FAF8F4" stroke="#A5A19B" stroke-width="1.4" stroke-dasharray="2 2"/>'
        out += f'<text x="{x}" y="50" text-anchor="middle" font-size="5.1" font-weight="700" fill="#141210">{esc(nome)}</text>'
    # chaveta por baixo dos invisíveis
    out += f'<path d="M{xs[2]-8} 58 h{xs[-1]-xs[2]+16}" stroke="#A5A19B" stroke-width=".8" stroke-dasharray="2 2"/>'
    out += f'<text x="{(xs[2]+xs[-1])/2}" y="66" text-anchor="middle" font-size="4.8" fill="#4D4A47" style="font-family:Space Mono;letter-spacing:.08em">{esc(t["dru_nuvede"].upper())}</text>'
    svg = f'<svg viewBox="0 0 {w} 72" width="100%">{out}</svg>'
    ip = ''.join(f'<div><b>{esc(a)}</b><p>{esc(b)}</p></div>' for a, b in t["dru_ipoteze"])
    return f'''<section class="p">
<div class="k"><i></i>{esc(t["dru_k"])}</div><h2>{esc(t["dru_t"])}</h2>
<div style="margin-top:6mm">{svg}</div>
<div class="leg"><span><i style="background:#E8622C"></i>{esc(t["dru_vede"])}</span><span><i style="border:1.5px dashed #A5A19B"></i>{esc(t["dru_nuvede"])}</span></div>
<div class="ip">{ip}</div>
{rod(t, 4)}</section>'''


def viteza(t):
    w, h = 150, 90; base = 70; alt = 50; gap = 44
    out = ""
    for i, (lab, v) in enumerate(t["vit_bare"]):
        x = 14 + i * gap; bw = 26; bh = max(alt * v / 100, 1.2)
        cor = "#E8622C" if i == 0 else "#141210"
        out += f'<rect x="{x}" y="{base - bh:.1f}" width="{bw}" height="{bh:.1f}" fill="{cor}"/>'
        out += f'<text x="{x + bw / 2}" y="{base - bh - 3:.1f}" text-anchor="middle" font-size="7" font-weight="700" fill="#141210">{"×" + str(v) if v > 1 else "×1"}</text>'
        out += f'<text x="{x + bw / 2}" y="{base + 8}" text-anchor="middle" font-size="5.8" fill="#4D4A47">{esc(lab)}</text>'
    out += f'<line x1="8" y1="{base}" x2="{w}" y2="{base}" stroke="#CFC8BC" stroke-width=".6"/>'
    svg = f'<svg viewBox="0 0 {w} {h}" width="100%">{out}</svg>'
    ia = ''.join(f'<div class="fapto"><div class="num" style="min-width:40mm">{esc(n)}</div><span>{esc(l)}</span></div>' for n, l in t["vit_ia"])
    return f'''<section class="p">
<div class="k"><i></i>{esc(t["vit_k"])}</div><h2>{esc(t["vit_t"])}</h2>
<div class="corpo" style="gap:14mm;align-items:flex-start">
<div style="width:130mm;flex:none"><div class="k" style="font-size:7.5pt;margin-bottom:2mm;letter-spacing:.08em">{esc(t["vit_c"])}</div>{svg}<div class="sursa">{esc(t["vit_nota"])}</div></div>
<div style="flex:1">{ia}</div>
</div>
<div class="conc">{esc(t["vit_conc"])}</div>
{rod(t, 5)}</section>'''


def quick(t):
    cs = t["qw_campos"]; cards = ""
    for n, titulo, vals in t["qw"]:
        dl = ''.join(f'<dt>{esc(c)}</dt><dd>{esc(v)}</dd>' for c, v in zip(cs, vals))
        cards += f'<div class="card"><div class="n">SYSTEM PRINT {n}</div><h3>{esc(titulo)}</h3><dl>{dl}</dl></div>'
    return f'''<section class="p">
<div class="k"><i></i>{esc(t["qw_k"])}</div><h2>{esc(t["qw_t"])}</h2>
<div class="corpo" style="align-items:stretch"><div class="cards">{cards}</div></div>
{rod(t, 6)}</section>'''


def scalar(t):
    a = ''.join(f'<li>{esc(x)}</li>' for x in t["sca_a"])
    b = ''.join(f'<div class="chip"><span>{i+1:02d}</span>{esc(x)}</div>' for i, x in enumerate(t["sca_b"]))
    return f'''<section class="p">
<div class="k"><i></i>{esc(t["sca_k"])}</div><h2>{esc(t["sca_t"])}</h2>
<div class="corpo" style="gap:10mm;align-items:stretch">
<div class="fase a"><div class="k" style="color:var(--l)">{esc(t["sca_a_k"])}</div><div class="big">{esc(t["sca_a_n"])}</div><div class="sub">{esc(t["sca_a_t"])}</div><ul class="lista esc">{a}</ul></div>
<div class="fase b"><div class="k">{esc(t["sca_b_k"])}</div><div class="big" style="color:var(--l)">{esc(t["sca_b_n"])}</div><div class="sub" style="color:var(--t2)">{esc(t["sca_b_t"])}</div><div class="chips">{b}</div></div>
</div>
<div class="conc" style="margin-top:6mm">{esc(t["sca_conc"])}</div>
{rod(t, 7)}</section>'''


def cum(t):
    txt = ''.join(f'<p>{esc(x)}</p>' for x in t["cum_txt"])
    ct = '<br>'.join(esc(x) for x in t["cum_contact"])
    return f'''<section class="p esc cum">
<div class="k"><i></i>{esc(t["cum_k"])}</div><h2>{esc(t["cum_t"])}</h2>
<div style="margin-top:5mm;max-width:200mm">{rota_svg(t["cum_pasi"], w=200, ativo=0)}</div>
<div class="corpo" style="gap:16mm;align-items:flex-start;margin-top:4mm">
<div style="flex:1">{txt}<div class="k" style="margin-top:5mm">{esc(t["cum_livram_k"])}</div><div class="lv" style="margin-top:2mm">{esc(t["cum_livram"])}</div></div>
<div style="width:92mm;flex:none"><div class="k" style="margin-bottom:3mm">{esc(t["cum_cta_k"])}</div><div class="ctb">{esc(t["cum_cta"])}</div><div class="ct">{ct}</div></div>
</div>
{rod(t, 8)}</section>'''


if __name__ == "__main__":
    for lang, t in T.items():
        html = (f'<!doctype html><html lang="{ {"ro": "ro", "pt": "pt-PT"}[lang] }"><head><meta charset="utf-8"><title>{esc(t["capa_t"])}</title>'
                f'<style>{FONTES}{CSS}</style></head><body>'
                + capa(t) + vazut(t) + piata(t) + drum(t) + viteza(t) + quick(t) + scalar(t) + cum(t) + '</body></html>')
        h = os.path.join(AQUI, f"obiectiv-imobiliare-{lang}.html")
        open(h, "w").write(html)
        pdf = os.path.join(AQUI, f"obiectiv-imobiliare-{lang}.pdf")
        subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=8000",
                        f"--print-to-pdf={pdf}", "file://" + h], check=True, capture_output=True)
        print(lang, os.path.getsize(pdf) // 1024, "KB")
