#!/usr/bin/env python3
"""Kit de parceiro (4 páginas A4): o documento a enviar ao parceiro, com as regras de 11/10/2026 (posicionamento de consultoria com IA).

  python3 research/parceiros/kit/gerar.py                 # kit-ro, kit-en, kit-pt (sem nome do parceiro)
  python3 research/parceiros/kit/gerar.py "Finova Expert" # o mesmo, com «Pregătit pentru: Finova Expert» na capa

Regras (Tomás, 11/10 14h17, thread «Playbook de consultoria de IA»): a auditoria não se cobra à parte, fica creditada na
implementação; o parceiro ganha comissão sobre a implementação (quando começamos a trabalhar com o negócio indicado) e,
enquanto o cliente ficar connosco, 10 % a cada 3 meses. Sem comissão sobre a auditoria. Nunca um preço fixo (o ticket vai de
2.000 € a 100.000 € consoante o impacto). Sem quick wins grátis para o parceiro até o Tomás decidir.
Percentagem sobre a implementação: 10 % por omissão (o Tomás só fixou os 10 % trimestrais), a confirmar.
Playbook: /mnt/project-files/playbook/pacheco-studios-playbook-consultoria-ia-pt.md. Precisa de segno e do Chromium.
"""
import base64, html, os, re, subprocess, sys
import segno

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
CHROMIUM = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
PARCEIRO = sys.argv[1] if len(sys.argv) > 1 else ""

T = {
 "ro": dict(
  lang="ro", data="Octombrie 2026", tel="+40 723 098 556", wa="40723098556", site="ro.pachecost.com", funcao="Fondator",
  titulo="Program de parteneri — Pacheco Studios", pagina="Pagina",
  c_supra="Program de parteneri", c_h1="Recomandați<br>o afacere.<br><em>Noi dovedim<br>valoarea.</em>",
  c_lead="Pacheco Studios este o consultanță în sisteme cu AI. Găsim unde o afacere pierde cereri, timp și bani, proiectăm sistemul "
         "care rezolvă problema și dovedim impactul înainte de a crește. Programul este pentru cei care lucrează zilnic cu firme: "
         "contabili, consultanți, tipografii, agenți imobiliari, furnizori.",
  c_para="Pregătit pentru", c_vazio="numele partenerului",
  c_tres=[("0 lei", "auditul nu se plătește separat: se scade din implementare"),
          ("10%", "din implementare, când începem să lucrăm cu afacerea recomandată"),
          ("10%", "la fiecare 3 luni, cât timp afacerea rămâne cu noi")],
  p2_et="01 · Cum funcționează", p2_h="Clientul vede valoarea înainte să plătească. Partenerul câștigă când începe lucrul.",
  pasos=[("Ne recomandați", "Cunoașteți o afacere care pierde cereri, timp sau bani? Ne prezentați proprietarului sau celui care decide, cu acordul lui.", "Dumneavoastră"),
         ("Facem auditul", "Analizăm operațiunile, găsim pierderea cea mai valoroasă și arătăm sistemul care o rezolvă. Afacerea nu plătește auditul separat.", "Fără cost separat"),
         ("Începe implementarea", "Dacă afacerea decide să continue, auditul devine parte din implementare. În acel moment primiți 10% din valoarea implementării.", "10%"),
         ("Rămânem cu clientul", "Cât timp afacerea continuă să lucreze cu noi, primiți 10% din ce ne plătește, la fiecare 3 luni.", "10% / trimestru")],
  aud_t="Ce primește din audit afacerea recomandată",
  aud_nota="Întâi diagnosticul, apoi instrumentele. Un site, un asistent pe WhatsApp sau o automatizare intră doar dacă sunt răspunsul potrivit.",
  aud=[("Diagnostic pe o pagină", "Simptomul, cauza, cifra de pornire și prima recomandare."),
       ("Harta operațiunilor", "Canale, oameni, instrumente, întârzieri și punctele unde se pierd cererile."),
       ("Priorități", "Impact, fezabilitate, risc și timp până la rezultat, ca să alegem o singură intervenție."),
       ("Plan pe 90 de zile", "Ce măsurăm, ce testăm într-un pilot, cine aprobă și ce decizie iese din pilot."),
       ("System Print", "Sistemul viitor într-o singură imagine: ce îl declanșează, cine răspunde, ce regulă urmează și când intervine un om.")],
  p3_et="02 · Pe cine să ne recomandați", p3_h="Afaceri care vând deja, dar pierd pe drum.",
  sinais_t="Semnele unei pierderi operaționale",
  sinais=["Cereri care vin pe WhatsApp, telefon și e-mail și rămân fără răspuns sau fără responsabil",
          "Proprietarul răspunde zilnic la aceleași întrebări și nu mai are timp să conducă",
          "Programări ratate, clienți care nu revin, oferte pe care nu le urmărește nimeni",
          "Echipa copiază date între tabele, programe și mesaje",
          "Afacerea crește, iar operațiunile nu mai țin pasul"],
  cliente_t="Ce primește afacerea recomandată",
  cliente=["Un audit al operațiunilor, fără cost separat: se scade din implementare dacă merge mai departe",
           "Pierderea cea mai valoroasă, numită și măsurată de la început",
           "Un pilot măsurat, înainte de orice angajament mai mare",
           "Conturile și datele rămân pe numele afacerii; deciziile importante rămân la oameni"],
  como_t="Cum faceți o recomandare (alegeți una)",
  como=[("Grup pe WhatsApp", "Faceți un grup cu proprietarul și cu noi și ne prezentați în două rânduri."),
        ("Contactul, cu acordul lui", "Ne trimiteți numele afacerii și telefonul, după ce i-ați spus că vă sunăm."),
        ("Numele dumneavoastră", "Îi dați numărul nostru; ne spune că vine de la dumneavoastră.")],
  fwd_t="Mesaj gata de trimis proprietarului",
  fwd="Bună! Îți recomand Pacheco Studios, firma lui Tomás. Îți fac un audit al operațiunilor: arată unde se pierd cereri, timp și bani "
      "și ce merită rezolvat primul. Auditul nu se plătește separat. Îți las numărul lui: +40 723 098 556.",
  ex_t="Cereți auditul", ex="Scanați: se deschide WhatsApp cu «AUDIT».",
  princ_t="Cum proiectăm fiecare sistem",
  princ=[("Trigger", "Ce s-a întâmplat: o cerere, o rezervare, o plată."), ("Responsabil", "Cine preia pasul următor. Niciodată o căsuță fără nume."),
         ("Regulă", "Ce poate și ce nu poate face sistemul."), ("Predare", "Când intervine un om: întrebare, reclamație, decizie.")],
  princ_n="Găsim pierderea. Proiectăm sistemul. Dovedim impactul.",
  p4_et="03 · Termenii, pe scurt", p4_h="Clar de la început, plătit la timp.",
  tab_cab=("Etapa clientului", "Clientul plătește", "Partenerul primește"),
  tab=[("Audit", "Se scade din implementare", "—"), ("Implementare", "Valoarea agreată cu clientul", "10%"),
       ("Însoțire", "Cât timp rămâne cu noi", "10% / 3 luni")],
  tab_nota="Fiecare proiect are propria valoare, stabilită după impactul în afacere. Nu există listă de prețuri: comisionul este mereu "
           "un procent din ce plătește efectiv clientul.",
  regras_t="Regulile", regras=[
   ("Când se plătește", "Implementare: în 7 zile de la plata clientului. Însoțire: la fiecare 3 luni, în 7 zile de la închiderea trimestrului. Prin transfer bancar, pe factură (firmă) sau contract de colaborare (persoană fizică)."),
   ("Ce înseamnă o recomandare", "Ne prezentați direct proprietarului sau celui care decide; afacerea știe și e de acord; nu era deja în discuție cu noi; implementarea începe în cel mult 180 de zile."),
   ("Fără limită", "Nu există un minim de recomandări și nici o limită. Fiecare implementare care pornește de la dumneavoastră contează."),
   ("Transparență", "Dacă vorbiți public despre noi după ce parteneriatul e activ, menționați că este un parteneriat. Nu cerem liste de contacte și nu contactăm pe nimeni fără acord."),
   ("Ce nu promitem", "Nu promitem rezultate înainte de a le măsura. Fiecare audit pornește de la o cifră de bază și fiecare pilot arată înainte și după.")],
  acordo_t="Acord de principiu", acordo_txt="Am citit termenii de mai sus și vrem să începem să recomandăm afaceri. Detaliile se trec într-un acord simplu, semnat de ambele părți.",
  ass=("Partener", "Pacheco Studios"), ass_campos=("Nume", "Data", "Semnătura"),
 ),
 "en": dict(
  lang="en", data="October 2026", tel="+40 723 098 556", wa="40723098556", site="ro.pachecost.com", funcao="Founder",
  titulo="Partner Programme — Pacheco Studios", pagina="Page",
  c_supra="Partner programme", c_h1="Introduce<br>a business.<br><em>We prove<br>the value.</em>",
  c_lead="Pacheco Studios is an AI systems consultancy. We find where a business loses requests, time and money, design the system "
         "that fixes it, and prove the impact before scaling. This programme is for people who work with companies every day: "
         "accountants, consultants, print shops, estate agents, suppliers.",
  c_para="Prepared for", c_vazio="partner name",
  c_tres=[("€0", "the audit is not charged separately: it is credited to the implementation"),
          ("10%", "of the implementation, when we start working with the business you introduced"),
          ("10%", "every 3 months, for as long as that business stays with us")],
  p2_et="01 · How it works", p2_h="The client sees value before paying. The partner earns when the work starts.",
  pasos=[("You introduce us", "Know a business losing requests, time or money? Introduce us to the owner or decision-maker, with their consent.", "You"),
         ("We run the audit", "We map the operation, find the most valuable leak and show the system that fixes it. The business does not pay for the audit separately.", "No separate cost"),
         ("Implementation starts", "If the business decides to go ahead, the audit becomes part of the implementation. At that point you earn 10% of the implementation value.", "10%"),
         ("We stay with the client", "For as long as the business keeps working with us, you receive 10% of what it pays us, every 3 months.", "10% / quarter")],
  aud_t="What the audit gives the business you introduce",
  aud_nota="Diagnosis before tools. A website, a WhatsApp assistant or an automation only comes in if it is the right answer.",
  aud=[("One-page diagnosis", "Symptom, root cause, baseline number and first recommendation."),
       ("Operations map", "Channels, people, tools, delays and the points where requests get lost."),
       ("Priorities", "Impact, feasibility, risk and time to value, to choose a single intervention."),
       ("90-day plan", "What to measure, what to pilot, who approves and which decision comes out of the pilot."),
       ("System Print", "The future system in one visual: what triggers it, who owns it, which rule it follows and when a person steps in.")],
  p3_et="02 · Who to introduce", p3_h="Businesses that already sell, but leak along the way.",
  sinais_t="Signs of an operational leak",
  sinais=["Requests arrive by WhatsApp, phone and e-mail and sit unanswered or with no owner",
          "The owner answers the same questions every day and has no time left to manage",
          "Missed bookings, clients who do not return, quotes nobody follows up",
          "The team copies data between spreadsheets, tools and messages",
          "The business is growing and operations can no longer keep up"],
  cliente_t="What the introduced business gets",
  cliente=["An audit of its operations, with no separate cost: credited if it goes ahead",
           "Its most valuable leak named, with a baseline number",
           "A measured pilot before any larger commitment",
           "Accounts and data always in the business's name; important decisions stay with people"],
  como_t="How to introduce us (pick one)",
  como=[("WhatsApp group", "Create a group with the owner and us, and introduce us in two lines."),
        ("The contact, with consent", "Send us the business name and phone after telling the owner we will call."),
        ("Your name", "Give them our number; they tell us you sent them.")],
  fwd_t="Message ready to forward to the owner",
  fwd="Hi! I recommend Pacheco Studios (Tomás). They audit your operations: they show where requests, time and money are lost, "
      "and what to fix first. The audit is not charged separately. Here is his number: +40 723 098 556.",
  ex_t="Request the audit", ex="Scan: WhatsApp opens with «AUDIT».",
  princ_t="How we design every system",
  princ=[("Trigger", "What happened: a request, a booking, a payment."), ("Owner", "Who takes the next action. Never an inbox with no name."),
         ("Rule", "What the system can and cannot do."), ("Handoff", "When a person steps in: a question, a complaint, a decision.")],
  princ_n="We find the leak. We design the system. We prove the impact.",
  p4_et="03 · The terms, in short", p4_h="Clear from the start, paid on time.",
  tab_cab=("Client stage", "The client pays", "The partner receives"),
  tab=[("Audit", "Credited to the implementation", "—"), ("Implementation", "Value agreed with the client", "10%"),
       ("Ongoing support", "For as long as it stays with us", "10% / 3 months")],
  tab_nota="Each project has its own value, set by its impact on the business. There is no price list: the commission is always "
           "a percentage of what the client actually pays.",
  regras_t="The rules", regras=[
   ("When it is paid", "Implementation: within 7 days of the client's payment. Ongoing support: every 3 months, within 7 days of the quarter's close. By bank transfer, against an invoice (company) or a simple collaboration agreement (individual)."),
   ("What counts as an introduction", "You introduce us directly to the owner or decision-maker; the business knows and agrees; it was not already talking to us; implementation starts within 180 days."),
   ("No limits", "No minimum number of introductions and no cap. Every implementation that starts from you counts."),
   ("Transparency", "If you talk about us publicly once the partnership is active, mention that it is a partnership. We never ask for contact lists and never contact anyone without consent."),
   ("What we do not promise", "We do not promise results before measuring them. Every audit starts from a baseline and every pilot shows the before and after.")],
  acordo_t="Agreement in principle", acordo_txt="We have read the terms above and want to start introducing businesses. The details go into a simple agreement signed by both parties.",
  ass=("Partner", "Pacheco Studios"), ass_campos=("Name", "Date", "Signature"),
 ),
 "pt": dict(
  lang="pt-PT", data="Outubro 2026", tel="+351 967 117 357", wa="351967117357", site="pachecost.com", funcao="Fundador",
  titulo="Programa de parceiros — Pacheco Studios", pagina="Página",
  c_supra="Programa de parceiros", c_h1="Apresente<br>um negócio.<br><em>Nós provamos<br>o valor.</em>",
  c_lead="A Pacheco Studios é uma consultora de sistemas com IA. Encontramos onde um negócio perde pedidos, tempo e dinheiro, "
         "desenhamos o sistema que resolve e provamos o impacto antes de crescer. Este programa é para quem trabalha todos os dias "
         "com empresas: contabilistas, consultores, gráficas, imobiliárias, fornecedores.",
  c_para="Preparado para", c_vazio="nome do parceiro",
  c_tres=[("0 €", "a auditoria não se paga à parte: fica creditada na implementação"),
          ("10 %", "da implementação, quando começamos a trabalhar com o negócio que nos apresentou"),
          ("10 %", "a cada 3 meses, enquanto esse negócio continuar connosco")],
  p2_et="01 · Como funciona", p2_h="O cliente vê o valor antes de pagar. O parceiro ganha quando o trabalho começa.",
  pasos=[("Apresenta-nos", "Conhece um negócio que perde pedidos, tempo ou dinheiro? Apresenta-nos ao dono ou a quem decide, com o acordo dele.", "Você"),
         ("Fazemos a auditoria", "Mapeamos a operação, encontramos a fuga de maior valor e mostramos o sistema que a resolve. O negócio não paga a auditoria à parte.", "Sem custo à parte"),
         ("Começa a implementação", "Se o negócio decidir avançar, a auditoria passa a fazer parte da implementação. Nesse momento recebe 10 % do valor da implementação.", "10 %"),
         ("Ficamos com o cliente", "Enquanto o negócio continuar a trabalhar connosco, recebe 10 % do que ele nos paga, a cada 3 meses.", "10 % / trimestre")],
  aud_t="O que a auditoria entrega ao negócio que apresentar",
  aud_nota="Primeiro o diagnóstico, depois as ferramentas. Um site, um assistente no WhatsApp ou uma automação só entram se forem a resposta certa.",
  aud=[("Diagnóstico de uma página", "Sintoma, causa, número de partida e primeira recomendação."),
       ("Mapa da operação", "Canais, pessoas, ferramentas, atrasos e os pontos onde os pedidos se perdem."),
       ("Prioridades", "Impacto, viabilidade, risco e tempo até ao resultado, para escolher uma só intervenção."),
       ("Plano de 90 dias", "O que medir, o que testar num piloto, quem aprova e que decisão sai do piloto."),
       ("System Print", "O sistema futuro num só visual: o que o dispara, quem é dono, que regra segue e quando entra uma pessoa.")],
  p3_et="02 · Quem nos apresentar", p3_h="Negócios que já vendem, mas perdem pelo caminho.",
  sinais_t="Sinais de uma fuga operacional",
  sinais=["Pedidos que chegam por WhatsApp, telefone e e-mail e ficam sem resposta ou sem dono",
          "O dono responde às mesmas perguntas todos os dias e já não tem tempo para gerir",
          "Marcações que falham, clientes que não voltam, orçamentos que ninguém segue",
          "A equipa copia dados entre folhas, programas e mensagens",
          "O negócio está a crescer e a operação já não acompanha"],
  cliente_t="O que recebe o negócio apresentado",
  cliente=["Uma auditoria à operação, sem custo à parte: fica creditada se avançar",
           "A fuga de maior valor nomeada, com um número de partida",
           "Um piloto medido antes de qualquer compromisso maior",
           "Contas e dados sempre em nome do negócio; as decisões importantes ficam com pessoas"],
  como_t="Como nos apresentar (escolha uma)",
  como=[("Grupo no WhatsApp", "Cria um grupo com o dono e connosco e apresenta-nos em duas linhas."),
        ("O contacto, com autorização", "Envia-nos o nome do negócio e o telefone, depois de avisar o dono que vamos ligar."),
        ("O seu nome", "Dá-lhe o nosso número; ele diz-nos que vem da sua parte.")],
  fwd_t="Mensagem pronta a enviar ao dono",
  fwd="Olá! Recomendo-te a Pacheco Studios, do Tomás. Fazem uma auditoria à tua operação: mostram onde se perdem pedidos, tempo e "
      "dinheiro, e o que resolver primeiro. A auditoria não se paga à parte. Fica o contacto dele: +351 967 117 357.",
  ex_t="Pedir a auditoria", ex="Aponte a câmara: abre o WhatsApp com «AUDIT».",
  princ_t="Como desenhamos cada sistema",
  princ=[("Trigger", "O que aconteceu: um pedido, uma reserva, um pagamento."), ("Dono", "Quem fica com a próxima ação. Nunca uma caixa sem nome."),
         ("Regra", "O que o sistema pode e não pode fazer."), ("Handoff", "Quando entra uma pessoa: dúvida, queixa, decisão.")],
  princ_n="Encontramos a fuga. Desenhamos o sistema. Provamos o impacto.",
  p4_et="03 · Os termos, em resumo", p4_h="Claro desde o início, pago a tempo.",
  tab_cab=("Fase do cliente", "O cliente paga", "O parceiro recebe"),
  tab=[("Auditoria", "Creditada na implementação", "—"), ("Implementação", "Valor acordado com o cliente", "10 %"),
       ("Acompanhamento", "Enquanto continuar connosco", "10 % / 3 meses")],
  tab_nota="Cada projeto tem um valor próprio, definido pelo impacto no negócio. Não há tabela de preços: a comissão é sempre "
           "uma percentagem do que o cliente paga de facto.",
  regras_t="As regras", regras=[
   ("Quando se paga", "Implementação: até 7 dias depois de o cliente pagar. Acompanhamento: a cada 3 meses, até 7 dias depois do fecho do trimestre. Por transferência, contra fatura (empresa) ou contrato de colaboração simples (particular)."),
   ("O que conta como apresentação", "Apresenta-nos diretamente ao dono ou a quem decide; o negócio sabe e concorda; não estava já a falar connosco; a implementação começa até 180 dias depois."),
   ("Sem limites", "Não há mínimo de apresentações nem teto. Cada implementação que comece por si conta."),
   ("Transparência", "Se falar de nós em público com a parceria ativa, diga que é uma parceria. Nunca pedimos listas de contactos nem contactamos ninguém sem autorização."),
   ("O que não prometemos", "Não prometemos resultados antes de os medir. Cada auditoria parte de um número de base e cada piloto mostra o antes e o depois.")],
  acordo_t="Acordo de princípio", acordo_txt="Lemos os termos acima e queremos começar a apresentar negócios. Os detalhes passam para um acordo simples, assinado pelas duas partes.",
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


CSS += """
.pasos{grid-template-columns:1fr 1fr;margin-bottom:9mm}
.menu .nr{flex:none;font:700 8pt/1 'Space Mono';color:var(--o);background:var(--c);padding:4px 6px;border-radius:3px;margin-top:.3mm}
.princ{margin-top:auto;margin-bottom:8mm;padding-top:6mm}
.princ .tiles{display:grid;grid-template-columns:repeat(4,1fr);gap:4mm}
.princ .tiles div{border-radius:10px;background:var(--o2);box-shadow:inset 0 0 0 1px var(--li);padding:4.5mm}
.princ .tiles div:last-child{background:var(--c);color:var(--o);box-shadow:inset 0 0 0 1.5px var(--l)}
.princ b{display:block;font:400 12pt/1 'Archivo Black';text-transform:uppercase;color:var(--lt);margin:0 0 2.5mm}
.princ .tiles div:last-child b{color:var(--l)}
.princ span{font-size:8.8pt;line-height:1.42;color:var(--so)}
.princ .tiles div:last-child span{color:#D9D3CA}
.princ p{font:400 10.5pt/1.3 'Archivo Black';text-transform:uppercase;margin:4.5mm 0 0}
td:last-child{white-space:nowrap}
.p3 h2{margin-bottom:6mm}.p3 .duas{margin-bottom:5.5mm}.p3 .como{margin-bottom:5mm}.p3 .lista{gap:2.6mm}
.p3 .princ{padding-top:3mm;margin-bottom:6mm}.p3 .princ p{margin-top:3.5mm}
"""


def esc(s):
    return html.escape(s, quote=False)


def pagina_html(t):
    wa = f"https://wa.me/{t['wa']}?text=AUDIT"
    qr = segno.make(wa, error="m").svg_inline(scale=3, dark="#141210", light="#EFEAE3", border=2)
    rod = lambda n: (f'<footer class="rod"><span class="marca">Pacheco Studios<i></i></span>'
                     f'<span>Tomás Pacheco · {t["tel"]} · {t["site"]}</span>'
                     f'<span class="mono">{t["pagina"]} {n}/4</span></footer>')
    cab = lambda: f'<header class="cab"><span class="marca">Pacheco Studios<i></i></span><span class="mono">{t["c_supra"]} · {t["data"]}</span></header>'
    para = (f'<strong>{esc(PARCEIRO)}</strong>' if PARCEIRO else f'<strong class="vazio">{t["c_vazio"]}</strong>')
    tres = "".join(f"<div><b>{a}</b><span>{b}</span></div>" for a, b in t["c_tres"])
    pasos = "".join(f'<li class="{"forte" if i >= 2 else ""}"><span class="n">0{i+1}</span><span class="tag">{c}</span><b>{a}</b><span>{b}</span></li>'
                    for i, (a, b, c) in enumerate(t["pasos"]))
    aud = "".join(f'<li><i class="nr">0{i+1}</i><div><b>{a}</b><span>{b}</span></div></li>' for i, (a, b) in enumerate(t["aud"]))
    sinais = "".join(f"<li>{x}</li>" for x in t["sinais"])
    cliente = "".join(f"<li>{x}</li>" for x in t["cliente"])
    como = "".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in t["como"])
    linhas = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in t["tab"])
    princ = "".join(f'<div><b>{a}</b><span>{b}</span></div>' for a, b in t["princ"])
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
  <h3>{t['aud_t']}</h3><p class="nota">{t['aud_nota']}</p>
  <ul class="menu">{aud}</ul>
</div>{rod(2)}</section>
<section class="pag p3">{cab()}<div class="corpo">
  <p class="mono et">{t['p3_et']}</p><h2>{t['p3_h']}</h2>
  <div class="duas"><div><h3>{t['sinais_t']}</h3><ul class="lista">{sinais}</ul></div>
    <div class="escuro"><h3>{t['cliente_t']}</h3><ul class="lista">{cliente}</ul></div></div>
  <h3>{t['como_t']}</h3><ul class="como">{como}</ul>
  <h3>{t['fwd_t']}</h3>
  <div class="fwd"><div class="bolha">{t['fwd']}</div>
    <div class="ex">{qr}<b>{t['ex_t']}</b><br>{t['ex']}<a href="{wa}">wa.me/{t['wa']}</a></div></div>
  <div class="princ"><h3>{t['princ_t']}</h3><div class="tiles">{princ}</div><p>{t['princ_n']}</p></div>
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
