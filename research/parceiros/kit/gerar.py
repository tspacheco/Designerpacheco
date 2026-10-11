#!/usr/bin/env python3
"""Kit de parceiro (4 páginas A4): o documento profissional a enviar ao parceiro com o acordo de 11/10/2026.

  python3 research/parceiros/kit/gerar.py                 # kit-ro, kit-en, kit-pt (sem nome do parceiro)
  python3 research/parceiros/kit/gerar.py "Finova Expert" # o mesmo, com «Pregătit pentru: Finova Expert» na capa

Adapta o «Playbook de parcerias» (parte 2: estrutura da parceria, indicação válida, kit do parceiro) ao acordo decidido
pelo Tomás: 3 quick wins sem custo → o parceiro mostra o nosso nome → 15 % de cada trabalho recomendado (mensalidades
fora), pago até 7 dias depois de o cliente pagar. Texto mestre: /mnt/project-files/prospecao-instagram/COMISSAO-PARCEIROS.md.
Mostra-se depois de entregues os quick wins (ou na reunião em que se escolhem). Precisa de segno e do Chromium.
"""
import base64, html, os, re, subprocess, sys
import segno

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
CHROMIUM = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
PARCEIRO = sys.argv[1] if len(sys.argv) > 1 else ""

T = {
 "ro": dict(
  lang="ro", data="Octombrie 2026", moeda_ex=[("Site profesional", "2.500 lei", "375 lei"), ("Sistem AI (o automatizare)", "1.250 lei", "187,50 lei"),
                                              ("Proiect de 5.000 lei", "5.000 lei", "750 lei")],
  tel="+40 723 098 556", site="ro.pachecost.com", demo="https://pachecost.com/demo/la-gioia/", funcao="Fondator",
  titulo="Program de parteneri — Pacheco Studios", pagina="Pagina",
  # capa
  c_supra="Program de parteneri", c_h1="Vă ajutăm<br>noi primii.<br><em>Apoi creștem<br>împreună.</em>",
  c_lead="Un parteneriat simplu și transparent pentru oamenii care văd în fiecare zi afaceri locale care pornesc sau cresc: "
         "contabili, tipografii, agenți imobiliari, consultanți, creatori.",
  c_para="Pregătit pentru", c_vazio="numele partenerului",
  c_tres=[("3", "soluții rapide implementate gratuit în afacerea dumneavoastră"), ("1", "mulțumire publică: numele nostru, acolo unde vă văd clienții"),
          ("15%", "din fiecare lucrare care vine din recomandarea dumneavoastră")],
  # p2
  p2_et="01 · Cum funcționează", p2_h="Întâi primiți. Abia apoi vorbim de recomandări.",
  pasos=[("Noi oferim primii", "Alegem împreună 3 soluții rapide, după situația de azi a afacerii dumneavoastră, și le lăsăm funcționale. Nu plătiți nimic și nu semnați nimic.", "Gratuit"),
         ("Ne arătați numele", "Dacă soluțiile v-au ajutat, spuneți cine le-a făcut: o postare sau un story cu @pachecostudiospt și un rând pe site («Sisteme: Pacheco Studios»). Opțional, o recomandare scrisă.", "Recunoaștere"),
         ("Ne recomandați", "Când cunoașteți o afacere care are nevoie de ceva asemănător, ne prezentați. Pentru fiecare lucrare care pornește din recomandarea dumneavoastră primiți 15%.", "15%")],
  menu_et="Alegeți 3 soluții", menu_nota="Bifați-le pe cele 3 care vă ajută cel mai mult acum. Fiecare e mică, funcționează din prima zi și se vede din afară.",
  menu=[("Afiș cu cod QR pentru recenzii Google", "Clienții mulțumiți lasă recenzia în 20 de secunde, fără să le cereți de fiecare dată."),
        ("Fișa Google completă", "Program, servicii, poze reale și buton de programare: cine vă caută vă găsește și vă sună."),
        ("Răspunsuri rapide pe WhatsApp și Instagram", "Cele 5 întrebări care se repetă primesc răspuns corect dintr-o atingere."),
        ("Formular de cerere sau programare", "Cererea ajunge completă și ordonată, fără cinci mesaje dus-întors."),
        ("Pagina pentru link-ul din bio", "Servicii, programare și contact într-un singur link, pe telefon."),
        ("Mesaj automat după serviciu", "Cere recenzia la momentul potrivit, fără să vă amintiți dumneavoastră."),
        ("Tabel comun de cereri", "Fiecare cerere are un responsabil și un stadiu; nimic nu se pierde între colegi.")],
  # p3
  p3_et="02 · Pe cine să ne recomandați", p3_h="Afaceri bune care pierd clienți pe drum.",
  sinais_t="Semnele că o afacere are nevoie de noi",
  sinais=["Are clienți mulțumiți, dar nu are site sau are unul vechi, greu de folosit pe telefon",
          "Răspunde toată ziua pe WhatsApp la aceleași întrebări: preț, program, unde sunteți",
          "Pierde programări sau telefoane când e aglomerat",
          "Are o notă bună pe Google, dar puține recenzii față de câți clienți are",
          "Tocmai a deschis, s-a mutat sau își schimbă imaginea"],
  cliente_t="Ce primește afacerea recomandată",
  cliente=["O demonstrație gratuită a site-ului ei, cu numele ei, înainte de orice plată",
           "Auditul complet al afacerii, inclus: unde se pierd clienți, timp și bani",
           "Implementare cu vizită la locație și suport direct, în română",
           "Nicio presiune: dacă nu e potrivit, rămâne cu demonstrația și cu sfaturile"],
  como_t="Cum faceți o recomandare (alegeți una)",
  como=[("Grup pe WhatsApp", "Faceți un grup cu proprietarul și cu noi și ne prezentați în două rânduri."),
        ("Contactul, cu acordul lui", "Ne trimiteți numele afacerii și telefonul, după ce i-ați spus că vă sunăm."),
        ("Numele dumneavoastră", "Îi dați numărul nostru; ne spune că vine de la dumneavoastră.")],
  fwd_t="Mesaj gata de trimis proprietarului",
  fwd="Bună! Îți recomand pe Tomás de la Pacheco Studios: mi-a făcut [soluția] și chiar a ajutat. Îți face gratuit o demonstrație a site-ului tău înainte să plătești ceva. Îți las numărul lui: +40 723 098 556.",
  calc_t="Cât poate însemna (doar site-uri)", calc=[("1 recomandare", "375 lei", "un site recomandat care pornește"), ("1 pe trimestru", "1.500 lei / an", "4 site-uri pe an"), ("1 pe lună", "4.500 lei / an", "12 site-uri pe an")], calc_n="Exemple de calcul, nu promisiuni. Sistemele AI și proiectele mai mari se adaugă la fel, cu 15%.",
  ex_t="Un exemplu de demonstrație", ex="Făcută pentru o afacere din Iași, înainte ca proprietarul să ne cunoască.",
  # p4
  p4_et="03 · Termenii, pe scurt", p4_h="Clar de la început, plătit la timp.",
  tab_cab=("Lucrarea recomandată", "Valoarea", "Partenerul primește"),
  tab_nota="15% din valoarea implementării. Abonamentul lunar (întreținere, găzduire) nu intră în calcul.",
  regras_t="Regulile", regras=[
   ("Când se plătește", "În 7 zile de la plata clientului, prin transfer bancar. Pe factură (firmă) sau pe contract de colaborare (persoană fizică)."),
   ("Ce înseamnă o recomandare", "Ne prezentați direct proprietarului sau celui care decide; afacerea știe și e de acord; nu era deja în discuție cu noi; începe o lucrare plătită în 180 de zile."),
   ("Fără limită", "Nu există un minim de recomandări și nici o limită. Fiecare lucrare plătită care pornește de la dumneavoastră contează."),
   ("Transparență", "Dacă vorbiți public despre noi după ce parteneriatul e activ, menționați că este un parteneriat. Nu cerem liste de contacte și nu contactăm pe nimeni fără acord."),
   ("Ce nu promitem", "Nu promitem rezultate pe care nu le putem măsura. Arătăm ce am făcut și măsurăm de la ziua 0.")],
  acordo_t="Acord de principiu", acordo_txt="Am citit termenii de mai sus și vrem să începem cu cele 3 soluții alese. Detaliile se trec într-un acord simplu, semnat de ambele părți.",
  ass=("Partener", "Pacheco Studios"), ass_campos=("Nume", "Data", "Semnătura"),
 ),
 "en": dict(
  lang="en", data="October 2026", moeda_ex=[("Professional website", "€500", "€75"), ("AI system (one automation)", "€250", "€37.50"),
                                            ("A €1,000 project", "€1,000", "€150")],
  tel="+40 723 098 556", site="ro.pachecost.com", demo="https://pachecost.com/demo/la-gioia/", funcao="Founder",
  titulo="Partner Programme — Pacheco Studios", pagina="Page",
  c_supra="Partner programme", c_h1="We help you<br>first.<br><em>Then we grow<br>together.</em>",
  c_lead="A simple, transparent partnership for people who see local businesses start and grow every day: "
         "accountants, print shops, estate agents, consultants, creators.",
  c_para="Prepared for", c_vazio="partner name",
  c_tres=[("3", "quick wins implemented in your business, at no cost"), ("1", "public thank-you: our name, where your clients see you"),
          ("15%", "of every job that comes from your recommendation")],
  p2_et="01 · How it works", p2_h="You receive first. Referrals come after.",
  pasos=[("We give first", "Together we choose 3 quick wins based on where your business is today, and we leave them working. You pay nothing and sign nothing.", "No cost"),
         ("You show our name", "If they helped, say who built them: a post or story tagging @pachecostudiospt and a line on your website («Systems: Pacheco Studios»). Optionally, a short testimonial.", "Recognition"),
         ("You recommend us", "When you meet a business that needs something similar, you introduce us. Every job that starts from your recommendation earns you 15%.", "15%")],
  menu_et="Choose 3 quick wins", menu_nota="Tick the 3 that would help you most right now. Each one is small, works from day one and is visible from the outside.",
  menu=[("QR poster for Google reviews", "Happy clients leave a review in 20 seconds, without you asking every time."),
        ("Complete Google Business Profile", "Hours, services, real photos and a booking button: people who search find you and call."),
        ("Quick replies on WhatsApp and Instagram", "The 5 questions you hear every day get the right answer in one tap."),
        ("Request or booking form", "Requests arrive complete and organised, without five back-and-forth messages."),
        ("Link-in-bio page", "Services, booking and contact in a single link, made for the phone."),
        ("Automatic follow-up after the service", "Asks for the review at the right moment, without you having to remember."),
        ("Shared request tracker", "Every request has an owner and a status; nothing gets lost between colleagues.")],
  p3_et="02 · Who to recommend", p3_h="Good businesses that lose clients along the way.",
  sinais_t="Signs a business needs us",
  sinais=["Happy clients, but no website, or an old one that is hard to use on a phone",
          "Answers the same questions on WhatsApp all day: price, hours, where are you",
          "Misses bookings or calls when it gets busy",
          "Good Google rating, but few reviews compared with how many clients it has",
          "Has just opened, moved or is changing its image"],
  cliente_t="What the recommended business gets",
  cliente=["A free demo of its own website, with its name, before any payment",
           "A full business audit included: where clients, time and money are lost",
           "Implementation with an on-site visit and direct support",
           "No pressure: if it is not a fit, it keeps the demo and the advice"],
  como_t="How to make a recommendation (pick one)",
  como=[("WhatsApp group", "Create a group with the owner and us, and introduce us in two lines."),
        ("The contact, with consent", "Send us the business name and phone after telling the owner we will call."),
        ("Your name", "Give them our number; they tell us you sent them.")],
  fwd_t="Message ready to forward to the owner",
  fwd="Hi! I recommend Tomás from Pacheco Studios: he set up [the solution] for me and it really helped. He will build a free demo of your website before you pay anything. Here is his number: +40 723 098 556.",
  calc_t="What it can add up to (websites only)", calc=[("1 recommendation", "€75", "one recommended website that starts"), ("1 per quarter", "€300 / year", "4 websites a year"), ("1 per month", "€900 / year", "12 websites a year")], calc_n="Worked examples, not promises. AI systems and larger projects add up the same way, at 15%.",
  ex_t="A demo example", ex="Built for a business in Iași, before the owner had met us.",
  p4_et="03 · The terms, in short", p4_h="Clear from the start, paid on time.",
  tab_cab=("Recommended job", "Value", "Partner receives"),
  tab_nota="15% of the implementation value. Monthly fees (maintenance, hosting) are not included.",
  regras_t="The rules", regras=[
   ("When it is paid", "Within 7 days of the client's payment, by bank transfer, against an invoice (company) or a simple collaboration agreement (individual)."),
   ("What counts as a recommendation", "You introduce us directly to the owner or decision-maker; the business knows and agrees; it was not already talking to us; it starts paid work within 180 days."),
   ("No limits", "No minimum number of recommendations and no cap. Every paid job that starts from you counts."),
   ("Transparency", "If you talk about us publicly once the partnership is active, mention that it is a partnership. We never ask for contact lists and never contact anyone without consent."),
   ("What we do not promise", "We do not promise results we cannot measure. We show what we did and measure from day 0.")],
  acordo_t="Agreement in principle", acordo_txt="We have read the terms above and want to start with the 3 chosen quick wins. The details go into a simple agreement signed by both parties.",
  ass=("Partner", "Pacheco Studios"), ass_campos=("Name", "Date", "Signature"),
 ),
 "pt": dict(
  lang="pt-PT", data="Outubro 2026", moeda_ex=[("Site profissional", "500 €", "75 €"), ("Sistema de IA (uma automação)", "250 €", "37,50 €"),
                                               ("Projeto de 1.000 €", "1.000 €", "150 €")],
  tel="+351 967 117 357", site="pachecost.com", demo="https://pachecost.com/demo/sos-car/", funcao="Fundador",
  titulo="Programa de parceiros — Pacheco Studios", pagina="Página",
  c_supra="Programa de parceiros", c_h1="Nós ajudamos<br>primeiro.<br><em>Depois crescemos<br>juntos.</em>",
  c_lead="Uma parceria simples e transparente para quem vê todos os dias negócios locais a começar ou a crescer: "
         "contabilistas, gráficas, imobiliárias, consultores, criadores.",
  c_para="Preparado para", c_vazio="nome do parceiro",
  c_tres=[("3", "soluções rápidas implementadas no seu negócio, sem custo"), ("1", "agradecimento público: o nosso nome, onde os seus clientes o veem"),
          ("15 %", "de cada trabalho que vier da sua recomendação")],
  p2_et="01 · Como funciona", p2_h="Primeiro recebe. Só depois falamos de recomendações.",
  pasos=[("Damos primeiro", "Escolhemos consigo 3 soluções rápidas, pela situação de hoje do seu negócio, e deixamo-las a funcionar. Não paga nada e não assina nada.", "Sem custo"),
         ("Mostra o nosso nome", "Se as soluções o ajudaram, diga quem as fez: um post ou story com @pachecostudiospt e uma linha no site («Sistemas: Pacheco Studios»). Opcional: um testemunho.", "Reconhecimento"),
         ("Recomenda-nos", "Quando conhecer um negócio que precise de algo parecido, apresenta-nos. Cada trabalho que começar pela sua recomendação dá-lhe 15 %.", "15 %")],
  menu_et="Escolha 3 soluções", menu_nota="Marque as 3 que mais o ajudam agora. Cada uma é pequena, funciona desde o primeiro dia e vê-se de fora.",
  menu=[("Cartaz com QR para avaliações Google", "Os clientes satisfeitos deixam a avaliação em 20 segundos, sem ter de pedir sempre."),
        ("Ficha Google completa", "Horário, serviços, fotos reais e botão de marcação: quem procura encontra-o e liga."),
        ("Respostas rápidas no WhatsApp e no Instagram", "As 5 perguntas de todos os dias têm a resposta certa num toque."),
        ("Formulário de pedido ou marcação", "O pedido chega completo e arrumado, sem cinco mensagens de ida e volta."),
        ("Página para o link da bio", "Serviços, marcação e contacto num só link, feito para o telemóvel."),
        ("Mensagem automática depois do serviço", "Pede a avaliação no momento certo, sem ter de se lembrar."),
        ("Folha partilhada de pedidos", "Cada pedido tem um responsável e um estado; nada se perde entre colegas.")],
  p3_et="02 · Quem nos recomendar", p3_h="Bons negócios que perdem clientes pelo caminho.",
  sinais_t="Sinais de que um negócio precisa de nós",
  sinais=["Tem clientes satisfeitos, mas não tem site, ou tem um antigo e difícil no telemóvel",
          "Responde o dia todo no WhatsApp às mesmas perguntas: preço, horário, onde fica",
          "Perde marcações ou chamadas quando há muito movimento",
          "Tem boa nota no Google, mas poucas avaliações para os clientes que tem",
          "Acabou de abrir, mudou de sítio ou está a mudar de imagem"],
  cliente_t="O que recebe o negócio recomendado",
  cliente=["Uma demonstração grátis do seu próprio site, com o seu nome, antes de qualquer pagamento",
           "A auditoria completa do negócio, incluída: onde se perdem clientes, tempo e dinheiro",
           "Implementação com visita ao local e suporte direto",
           "Sem pressão: se não fizer sentido, fica com a demonstração e com os conselhos"],
  como_t="Como fazer uma recomendação (escolha uma)",
  como=[("Grupo no WhatsApp", "Cria um grupo com o dono e connosco e apresenta-nos em duas linhas."),
        ("O contacto, com autorização", "Envia-nos o nome do negócio e o telefone, depois de avisar o dono que vamos ligar."),
        ("O seu nome", "Dá-lhe o nosso número; ele diz-nos que vem da sua parte.")],
  fwd_t="Mensagem pronta a enviar ao dono",
  fwd="Olá! Recomendo-te o Tomás, da Pacheco Studios: fez-me [a solução] e ajudou mesmo. Faz-te grátis uma demonstração do teu site antes de pagares o que quer que seja. Fica o número dele: +351 967 117 357.",
  calc_t="Quanto pode representar (só sites)", calc=[("1 recomendação", "75 €", "um site recomendado que avança"), ("1 por trimestre", "300 € / ano", "4 sites por ano"), ("1 por mês", "900 € / ano", "12 sites por ano")], calc_n="Exemplos de cálculo, não promessas. Sistemas de IA e projetos maiores somam da mesma forma, a 15 %.",
  ex_t="Um exemplo de demonstração", ex="Feita para um negócio do Algarve, antes de o dono nos conhecer.",
  p4_et="03 · Os termos, em resumo", p4_h="Claro desde o início, pago a tempo.",
  tab_cab=("Trabalho recomendado", "Valor", "O parceiro recebe"),
  tab_nota="15 % do valor da implementação. As mensalidades (manutenção, alojamento) ficam de fora.",
  regras_t="As regras", regras=[
   ("Quando se paga", "Até 7 dias depois de o cliente pagar, por transferência, contra fatura (empresa) ou contrato de colaboração simples (particular)."),
   ("O que conta como recomendação", "Apresenta-nos diretamente ao dono ou a quem decide; o negócio sabe e concorda; não estava já a falar connosco; começa um trabalho pago em 180 dias."),
   ("Sem limites", "Não há mínimo de recomendações nem teto. Cada trabalho pago que comece por si conta."),
   ("Transparência", "Se falar de nós em público com a parceria ativa, diga que é uma parceria. Nunca pedimos listas de contactos nem contactamos ninguém sem autorização."),
   ("O que não prometemos", "Não prometemos resultados que não conseguimos medir. Mostramos o que fizemos e medimos desde o dia 0.")],
  acordo_t="Acordo de princípio", acordo_txt="Lemos os termos acima e queremos começar pelas 3 soluções escolhidas. Os detalhes passam para um acordo simples, assinado pelas duas partes.",
  ass=("Parceiro", "Pacheco Studios"), ass_campos=("Nome", "Data", "Assinatura"),
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
body{background:#6d6862;font:400 9.6pt/1.5 'Inter',system-ui,sans-serif;color:var(--c);-webkit-print-color-adjust:exact;print-color-adjust:exact}
.pag{width:210mm;height:297mm;margin:0 auto;background:var(--o);position:relative;overflow:hidden;display:flex;flex-direction:column;page-break-after:always;break-after:page}
.pag:last-child{page-break-after:auto;break-after:auto}
@media screen{.pag{margin:24px auto;box-shadow:0 20px 60px rgba(0,0,0,.35)}}
@media print{body{background:none}}
.mono{font:700 7.4pt/1 'Space Mono',monospace;letter-spacing:.14em;text-transform:uppercase}
.marca{font:400 10pt/1 'Archivo Black';letter-spacing:.06em;text-transform:uppercase}
.marca i{display:inline-block;width:.42em;height:.42em;border-radius:50%;background:var(--l);margin-left:.12em}
/* capa */
.capa{background:var(--c);color:var(--o);padding:16mm 16mm 14mm}
.capa .topo{display:flex;justify-content:space-between;align-items:center}
.capa .topo .mono{color:var(--sc)}
.capa .supra{color:var(--l);margin:30mm 0 6mm}
.capa h1{font:400 44pt/1.0 'Archivo Black';text-transform:uppercase;letter-spacing:-.01em;margin:0 0 9mm}
.capa h1 em{font-style:normal;color:var(--l)}
.capa .lead{font-size:11.5pt;line-height:1.55;color:#D9D3CA;max-width:150mm;margin:0}
.fio{margin:14mm 0 0;height:20mm;width:100%}
.tres{display:grid;grid-template-columns:repeat(3,1fr);gap:6mm;margin-top:6mm}
.tres div{border-top:1.5px solid #3A3631;padding-top:4mm}
.tres b{display:block;font:400 30pt/1 'Archivo Black';color:var(--l);margin-bottom:3mm}
.tres span{font-size:9.6pt;color:#D9D3CA;line-height:1.45}
.para{margin-top:auto;display:flex;align-items:flex-end;justify-content:space-between;gap:8mm;padding-top:10mm}
.para .mono{color:var(--sc);display:block;margin-bottom:3mm}
.para strong{display:block;font:400 15pt/1.2 'Archivo Black';text-transform:uppercase;color:#fff;min-width:90mm;border-bottom:1.5px solid var(--l);padding-bottom:2mm}
.para strong.vazio{color:#5E5953;font-family:'Inter';font-weight:400;font-size:10pt;text-transform:none}
.para .quem{text-align:right;font-size:9pt;color:var(--sc)}
.para .quem b{display:block;color:#fff;font-weight:600;font-size:10pt}
/* páginas interiores */
.cab{display:flex;justify-content:space-between;align-items:center;padding:11mm 16mm 0}
.cab .mono{color:var(--so)}
.corpo{flex:1;padding:8mm 16mm 0;display:flex;flex-direction:column}
.et{color:var(--lt);margin:0 0 3mm}
h2{font:400 22pt/1.12 'Archivo Black';text-transform:uppercase;margin:0 0 9mm;letter-spacing:-.005em;max-width:170mm}
h3{font:700 7.6pt/1 'Space Mono';letter-spacing:.14em;text-transform:uppercase;color:var(--lt);margin:0 0 3.5mm;display:flex;align-items:center;gap:3mm}
h3::after{content:'';flex:1;height:1px;background:var(--li)}
.pasos{list-style:none;margin:0 0 11mm;padding:0;display:grid;grid-template-columns:repeat(3,1fr);gap:5mm;counter-reset:p}
.pasos li{counter-increment:p;background:var(--o2);border-radius:10px;box-shadow:inset 0 0 0 1px var(--li);padding:5mm 5mm 5mm;position:relative}
.pasos li.forte{background:var(--c);color:var(--o);box-shadow:inset 0 0 0 1.5px var(--l)}
.pasos .n{font:700 8pt/1 'Space Mono';color:var(--o);background:var(--c);padding:4px 7px;border-radius:3px;display:inline-block}
.pasos li.forte .n{background:var(--l);color:var(--c)}
.pasos .tag{float:right;font:700 7pt/1 'Space Mono';letter-spacing:.12em;text-transform:uppercase;color:var(--lt);padding-top:4px}
.pasos li.forte .tag{color:var(--l)}
.pasos b{display:block;font-weight:600;font-size:11pt;margin:4.5mm 0 2mm}
.pasos span{display:block;font-size:9.3pt;line-height:1.48;color:var(--so)}
.pasos li.forte span{color:#D9D3CA}
.nota{font-size:9pt;color:var(--so);margin:0 0 4mm}
.menu{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:4mm 5mm}
.menu li{display:flex;gap:3.5mm;align-items:flex-start;padding:4.5mm 4.5mm;border-radius:8px;background:var(--o2);box-shadow:inset 0 0 0 1px var(--li)}
.menu li:last-child{grid-column:1/-1}
.cb{flex:none;width:4.6mm;height:4.6mm;border:1.6px solid var(--c);border-radius:2px;margin-top:.4mm;background:#fff}
.menu b{display:block;font-weight:600;font-size:10.2pt;margin-bottom:.8mm}
.menu span{font-size:9.1pt;color:var(--so);line-height:1.42}
.duas{display:grid;grid-template-columns:1fr 1fr;gap:6mm;margin-bottom:8mm}
.lista{list-style:none;margin:0;padding:0;display:grid;gap:3.4mm}
.lista li{position:relative;padding-left:5mm;font-size:10pt;line-height:1.45}
.lista li::before{content:'';position:absolute;left:0;top:.52em;width:5px;height:5px;border-radius:50%;background:var(--l)}
.escuro{background:var(--c);color:var(--o);border-radius:10px;padding:6.5mm;box-shadow:inset 0 0 0 1.5px var(--l)}
.escuro h3{color:var(--l)}.escuro h3::after{background:#3A3631}
.escuro .lista li{color:#D9D3CA}
.como{list-style:none;margin:0 0 8mm;padding:0;display:grid;grid-template-columns:repeat(3,1fr);gap:5mm}
.como li{border-top:2px solid var(--c);padding-top:3mm}
.como b{display:block;font-weight:600;font-size:10.4pt;margin-bottom:1.2mm}
.como span{font-size:9.4pt;color:var(--so)}
.fwd{display:grid;grid-template-columns:1fr 40mm;gap:6mm;align-items:center}
.bolha{background:#DCF8C6;border-radius:12px 12px 12px 3px;padding:6mm 6.5mm;font-size:10.6pt;line-height:1.5;box-shadow:0 1px 0 rgba(0,0,0,.08)}
.ex{text-align:center;font-size:7.8pt;color:var(--so);line-height:1.35}
.ex svg{width:36mm;height:36mm;display:block;margin:0 auto 2mm;border-radius:4px}
.ex a{display:block;font:700 7.2pt/1.3 'Space Mono';color:var(--lt);text-decoration:none;margin-top:1mm;white-space:nowrap;font-size:6.6pt}
table{width:100%;border-collapse:collapse;margin:0 0 2.5mm}
th{font:700 7.2pt/1 'Space Mono';letter-spacing:.12em;text-transform:uppercase;color:var(--so);text-align:left;padding:0 0 2.5mm;border-bottom:1.5px solid var(--c)}
td{padding:3mm 0;border-bottom:1px solid var(--li);font-size:10pt}
td:nth-child(2),th:nth-child(2){text-align:right;padding-right:8mm}
td:last-child,th:last-child{text-align:right}
td:last-child{font:400 13pt/1 'Archivo Black';color:var(--lt)}
.regras{list-style:none;margin:0 0 7mm;padding:0;display:grid;gap:3mm}
.regras li{display:grid;grid-template-columns:44mm 1fr;gap:5mm;font-size:9.6pt;line-height:1.48;padding-bottom:3mm;border-bottom:1px solid var(--li)}
.regras li:last-child{border-bottom:0;padding-bottom:0}
.regras b{font-weight:600}
.regras span{color:var(--so)}
.acordo{margin-top:auto;margin-bottom:8mm;background:var(--o2);border-radius:10px;box-shadow:inset 0 0 0 1px var(--li);padding:5.5mm 6mm}
.acordo p{margin:0 0 5mm;font-size:9.2pt;color:var(--so)}
.ass{display:grid;grid-template-columns:1fr 1fr;gap:10mm}
.ass .mono{color:var(--lt);display:block;margin-bottom:4mm}
.campo{display:flex;align-items:flex-end;gap:3mm;margin-bottom:4mm;font-size:8.4pt;color:var(--so)}
.campo i{flex:1;border-bottom:1px solid var(--c);height:5mm}
/* rodapé */
.rod{background:var(--c);color:var(--o);padding:5.5mm 16mm;display:flex;justify-content:space-between;align-items:center;gap:6mm;font-size:8.4pt}
.rod .mono{color:var(--l)}
.rod span{color:var(--sc);text-align:center}
.rod .marca,.rod .mono{flex:none;white-space:nowrap}
.calc{margin-top:auto;margin-bottom:8mm;padding-top:6mm}
.calc .tiles{display:grid;grid-template-columns:repeat(3,1fr);gap:5mm}
.calc .tiles div{border-radius:10px;background:var(--o2);box-shadow:inset 0 0 0 1px var(--li);padding:5mm}
.calc .tiles div:last-child{background:var(--c);color:var(--o);box-shadow:inset 0 0 0 1.5px var(--l)}
.calc b{display:block;white-space:nowrap;font:400 15.5pt/1 'Archivo Black';color:var(--lt);margin:2mm 0 2mm}
.calc .tiles div:last-child b{color:var(--l)}
.calc span{font-size:8.8pt;color:var(--so)}
.calc .tiles div:last-child span{color:#D9D3CA}
.calc .mono{color:var(--so)}.calc .tiles div:last-child .mono{color:var(--sc)}
.calc p{font-size:8.4pt;color:var(--so);margin:3mm 0 0}
"""

FIO = """<svg class="fio" viewBox="0 0 600 60" preserveAspectRatio="none" aria-hidden="true">
<path d="M4 50 C 120 50, 160 12, 300 12 S 480 48, 596 10" fill="none" stroke="#E8622C" stroke-width="2" stroke-dasharray="6 7" vector-effect="non-scaling-stroke"/></svg>"""


def esc(s):
    return html.escape(s, quote=False)


def pagina_html(t):
    qr = segno.make(t["demo"], error="m").svg_inline(scale=3, dark="#141210", light="#EFEAE3", border=2)
    rod = lambda n: (f'<footer class="rod"><span class="marca">Pacheco Studios<i></i></span>'
                     f'<span>Tomás Pacheco · {t["tel"]} · tomas@pachecost.com · {t["site"]}</span>'
                     f'<span class="mono">{t["pagina"]} {n}/4</span></footer>')
    cab = lambda: f'<header class="cab"><span class="marca">Pacheco Studios<i></i></span><span class="mono">{t["c_supra"]} · {t["data"]}</span></header>'
    para = (f'<strong>{esc(PARCEIRO)}</strong>' if PARCEIRO else f'<strong class="vazio">{t["c_vazio"]}</strong>')
    tres = "".join(f"<div><b>{a}</b><span>{b}</span></div>" for a, b in t["c_tres"])
    pasos = "".join(f'<li class="{"forte" if i == 2 else ""}"><span class="n">0{i+1}</span><span class="tag">{c}</span><b>{a}</b><span>{b}</span></li>'
                    for i, (a, b, c) in enumerate(t["pasos"]))
    menu = "".join(f'<li><i class="cb"></i><div><b>{a}</b><span>{b}</span></div></li>' for a, b in t["menu"])
    sinais = "".join(f"<li>{x}</li>" for x in t["sinais"])
    cliente = "".join(f"<li>{x}</li>" for x in t["cliente"])
    como = "".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in t["como"])
    linhas = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in t["moeda_ex"])
    calc = "".join(f'<div><span class="mono">{a}</span><b>{b}</b><span>{c}</span></div>' for a, b, c in t["calc"])
    regras = "".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in t["regras"])
    campos = "".join(f'<div class="campo">{c}<i></i></div>' for c in t["ass_campos"])
    ass = "".join(f'<div><span class="mono">{p}</span>{campos}</div>' for p in t["ass"])
    return f"""<!doctype html>
<html lang="{t['lang']}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(t['titulo'])}</title><style>{FONTES}{CSS}</style></head><body>
<section class="pag capa">
  <div class="topo"><span class="marca">Pacheco Studios<i></i></span><span class="mono">{t['data']}</span></div>
  <p class="mono supra">{t['c_supra']}</p>
  <h1>{t['c_h1']}</h1>
  <p class="lead">{t['c_lead']}</p>
  {FIO}
  <div class="tres">{tres}</div>
  <div class="para"><div><span class="mono">{t['c_para']}</span>{para}</div>
    <div class="quem"><b>Tomás Pacheco</b>{t['funcao']} · Pacheco Studios<br>{t['tel']}</div></div>
</section>
<section class="pag">{cab()}<div class="corpo">
  <p class="mono et">{t['p2_et']}</p><h2>{t['p2_h']}</h2>
  <ol class="pasos">{pasos}</ol>
  <h3>{t['menu_et']}</h3><p class="nota">{t['menu_nota']}</p>
  <ul class="menu">{menu}</ul>
</div>{rod(2)}</section>
<section class="pag">{cab()}<div class="corpo">
  <p class="mono et">{t['p3_et']}</p><h2>{t['p3_h']}</h2>
  <div class="duas"><div><h3>{t['sinais_t']}</h3><ul class="lista">{sinais}</ul></div>
    <div class="escuro"><h3>{t['cliente_t']}</h3><ul class="lista">{cliente}</ul></div></div>
  <h3>{t['como_t']}</h3><ul class="como">{como}</ul>
  <h3>{t['fwd_t']}</h3>
  <div class="fwd"><div class="bolha">{t['fwd']}</div>
    <div class="ex">{qr}{t['ex_t']}<a href="{t['demo']}">{t['demo'].replace('https://', '')}</a></div></div>
  <div class="calc"><h3>{t['calc_t']}</h3><div class="tiles">{calc}</div><p>{t['calc_n']}</p></div>
</div>{rod(3)}</section>
<section class="pag">{cab()}<div class="corpo">
  <p class="mono et">{t['p4_et']}</p><h2>{t['p4_h']}</h2>
  <table><thead><tr><th>{t['tab_cab'][0]}</th><th>{t['tab_cab'][1]}</th><th>{t['tab_cab'][2]}</th></tr></thead><tbody>{linhas}</tbody></table>
  <p class="nota">{t['tab_nota']}</p>
  <h3>{t['regras_t']}</h3><ul class="regras">{regras}</ul>
  <div class="acordo"><h3>{t['acordo_t']}</h3><p>{t['acordo_txt']}</p><div class="ass">{ass}</div></div>
</div>{rod(4)}</section>
</body></html>"""


sufixo = ("-" + re.sub(r"[^a-z0-9]+", "-", PARCEIRO.lower()).strip("-")) if PARCEIRO else ""
for lingua, t in T.items():
    h = os.path.join(AQUI, f"kit-parceiro-{lingua}{sufixo}.html")
    open(h, "w", encoding="utf-8").write(pagina_html(t))
    pdf = h[:-5] + ".pdf"
    subprocess.run([CHROMIUM, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf}", "file://" + h], check=True, capture_output=True)
    print("ok", os.path.relpath(pdf, RAIZ), os.path.getsize(pdf) // 1024, "KB")
