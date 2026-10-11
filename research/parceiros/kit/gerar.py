#!/usr/bin/env python3
"""Kit de parceiro em duas peças (regras do Tomás, 11/10/2026 14h38), em RO/EN/PT:

  1) incentivo-{ro,en,pt}.pdf          4 páginas: os 3 quick wins grátis, quanto pode ganhar (cenários), porquê, como apresentar.
  2) proposta-parceria-{ro,en,pt}.pdf  2 páginas: o que cada parte dá, comissões, regras e assinaturas. Vai só depois do incentivo.

  python3 research/parceiros/kit/gerar.py                 # sem nome do parceiro
  python3 research/parceiros/kit/gerar.py "Finova Expert" # com o nome na capa e na proposta (sufixo no ficheiro)

Regras: 3 quick wins sem custo ao parceiro (a triagem levada até ele já mostra pelo menos 1); 15 % do valor de implementação de
cada negócio apresentado; 5 % trimestral (do que esse negócio nos paga no trimestre) enquanto trabalharmos com ele; auditoria
creditada na implementação; sites e mensalidades entram no preço de implementação. Nunca valores fixos: os cenários usam os
exemplos do Tomás (50.000 lei/mês → ~20.000 lei; 1.000.000 lei/mês → ~100.000 lei), em € à razão de 5 lei = 1 € no PT.
Valores por omissão a confirmar pelo Tomás: 180 dias, 12 meses renováveis, 30 dias de aviso.
Playbook: /mnt/project-files/playbook/. Precisa de segno e do Chromium.
"""
import base64, html, os, re, subprocess, sys
import segno

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
CHROMIUM = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
PARCEIRO = sys.argv[1] if len(sys.argv) > 1 else ""

T = {
 "ro": dict(
  lang="ro", data="Octombrie 2026", tel="+40 723 098 556", wa="40723098556", site="ro.pachecost.com", funcao="Fondator", pagina="Pagina",
  # 1) incentivo
  i_titulo="Cât puteți câștiga — Pacheco Studios", c_supra="Program de parteneri",
  c_h1="Recomandați<br>afaceri.<br><em>Câștigați din<br>fiecare.</em>",
  c_lead="Pacheco Studios este o consultanță în sisteme cu AI: găsim unde o afacere pierde cereri, timp și bani și construim sistemul "
         "care rezolvă problema. Partenerii noștri sunt oameni care lucrează zilnic cu firme și ne prezintă celor care au nevoie.",
  c_para="Pregătit pentru", c_vazio="numele partenerului",
  c_tres=[("3", "soluții rapide implementate gratuit în afacerea dumneavoastră"), ("15%", "din valoarea implementării, pentru fiecare afacere recomandată"),
          ("5%", "la fiecare 3 luni, cât timp lucrăm cu afacerea recomandată")],
  p2_et="01 · Întâi primiți", p2_h="Înainte să vorbim de comisioane, vă îmbunătățim afacerea.",
  qw_t="3 soluții rapide, gratuit", qw_nota="Le alegem împreună după triaj; triajul pe care vi-l aducem arată deja cel puțin una. Câteva exemple:",
  qw=[("Afiș QR pentru recenzii Google", "Clienții mulțumiți lasă recenzia în 20 de secunde."),
      ("Fișa Google completă", "Program, servicii, poze reale și buton de contact."),
      ("Răspunsuri rapide pe WhatsApp", "Întrebările care se repetă primesc răspuns corect dintr-o atingere."),
      ("Formular de cerere", "Cererea ajunge completă, fără cinci mesaje dus-întors."),
      ("Mesaj automat după serviciu", "Cere recenzia la momentul potrivit."),
      ("Tabel comun de cereri", "Fiecare cerere are un responsabil și un stadiu.")],
  fluxo_t="Apoi, pentru fiecare afacere pe care ne-o prezentați",
  pasos=[("Ne prezentați", "Unei afaceri care pierde cereri, timp sau bani, cu acordul proprietarului.", "Dumneavoastră"),
         ("Triaj și audit", "Găsim pierderea cea mai valoroasă. Auditul nu se plătește separat: se scade din implementare.", "Fără cost separat"),
         ("Începe implementarea", "Afacerea decide să lucreze cu noi. Primiți 15% din valoarea implementării.", "15%"),
         ("Rămânem cu clientul", "Cât timp lucrăm cu afacerea, primiți 5% din ce ne plătește, la fiecare 3 luni.", "5% / trimestru")],
  p3_et="02 · Cât puteți câștiga", p3_h="Fiecare afacere e diferită. De aceea comisionul e un procent, nu o sumă fixă.",
  cen_nota="Valoarea implementării depinde de mărimea afacerii și de impactul pe care îl dovedim. Două exemple:",
  cen=[("Afacere de 50.000 lei / lună", "≈ 20.000 lei", "3.000 lei"), ("Afacere de 1.000.000 lei / lună", "≈ 100.000 lei", "15.000 lei")],
  cen_rot=("Implementare estimată", "Primiți 15%", "Apoi, la fiecare 3 luni", "5% din ce ne plătește"),
  tri_t="Partea trimestrială",
  tri=[("La fiecare 10.000 lei", "500 lei", "plătiți de client într-un trimestru"), ("Cât timp lucrăm", "5%", "cu afacerea recomandată, fără termen"),
       ("La fiecare 3 luni", "Raport", "cu ce a plătit clientul și comisionul")],
  ano="<b>Un an posibil:</b> o afacere mică și una mare recomandate = <b>18.000 lei</b> doar din implementare, plus partea trimestrială.",
  calc_n="Exemple de calcul cu valori aproximative, nu promisiuni și nici prețuri.",
  p4_et="03 · De ce merită", p4_h="Câștigați fără să executați. Clienții dumneavoastră primesc un sistem care funcționează.",
  porque_t="Ce câștigați",
  porque=["Comision real din fiecare implementare, nu o sumă simbolică", "Venit la fiecare 3 luni, cât timp clientul rămâne cu noi",
          "Clienții dumneavoastră vă mulțumesc pentru recomandare", "Noi ne ocupăm de tot: triaj, audit, implementare, suport",
          "Nu costă nimic și nu există exclusivitate"],
  quem_t="Pe cine să ne prezentați",
  quem=["Afaceri care primesc cereri pe WhatsApp, telefon și e-mail", "Proprietari care răspund zilnic la aceleași întrebări",
        "Afaceri care cresc și nu mai țin pasul", "Echipe care copiază date între tabele și programe"],
  como_t="Cum ne prezentați (alegeți una)",
  como=[("Grup pe WhatsApp", "Un grup cu proprietarul și cu noi, și ne prezentați în două rânduri."),
        ("Contactul, cu acord", "Ne trimiteți numele și telefonul, după ce i-ați spus că vă sunăm."),
        ("Numele dumneavoastră", "Îi dați numărul nostru; ne spune că vine de la dumneavoastră.")],
  fwd_t="Mesaj gata de trimis proprietarului",
  fwd="Bună! Îți recomand Pacheco Studios, firma lui Tomás. Se uită la cum intră cererile în afacerea ta și îți arată, pe o pagină, "
      "unde s-ar putea pierde și ce merită verificat. Fă un triaj cu ei: +40 723 098 556.",
  ex_t="Cereți triajul", ex="Scanați: se deschide WhatsApp cu «AUDIT».",
  prox_t="Pasul următor", prox="Dacă are sens pentru dumneavoastră, vă trimitem propunerea de parteneriat, cu regulile și comisioanele în scris, pentru semnat.",
  # 2) proposta
  p_titulo="Propunere de parteneriat — Pacheco Studios", p_et="Propunere de parteneriat",
  p_h="Parteneriat între {p} și Pacheco Studios", p_vazio="……………………",
  da_t="Ce oferă Pacheco Studios",
  da=["3 soluții rapide în afacerea partenerului, gratuit, alese după triaj",
      "15% din valoarea implementării pentru fiecare afacere recomandată",
      "5% din ce plătește afacerea recomandată, la fiecare 3 luni, cât timp lucrăm cu ea",
      "Raport la fiecare 3 luni cu recomandările, plățile și comisioanele",
      "Plata comisionului în 7 zile de la plata clientului"],
  faz_t="Ce face partenerul",
  faz=["<b>1.</b> Când aplicăm cele 3 soluții rapide: prima recomandare online, ca mulțumire",
       "<b>2.</b> Apoi: ne recomandă din gură în gură celor care au nevoie",
       "<b>3.</b> Lunar: ne arată în conținutul său o dată pe lună, cu @pachecostudiospt",
       "Ne prezintă afaceri doar cu acordul proprietarului",
       "Spune că este un parteneriat când vorbește public despre noi"],
  troca="<b>În schimb, în această ordine:</b> 1) când aplicăm cele 3 soluții, prima recomandare online, ca mulțumire; 2) apoi recomandarea din gură în gură; 3) o dată pe lună, ne arătați în conținutul dumneavoastră.",
  tab_cab=("Etapa", "Partenerul primește", "Când"),
  tab=[("Soluții rapide", "3, gratuit", "La început"), ("Audit", "—", "Se scade din implementare"),
       ("Implementare", "15%", "În 7 zile de la plata clientului"), ("Însoțire", "5%", "La fiecare 3 luni, în 7 zile de la închidere")],
  regras_t="Regulile",
  regras=[("Ce înseamnă o recomandare", "Ne prezentați direct proprietarului sau celui care decide; afacerea știe și e de acord; nu era deja în discuție cu noi; implementarea începe în cel mult 180 de zile."),
          ("Baza de calcul", "Comisionul se calculează din ce plătește efectiv clientul. Site-ul, asistentul, automatizările și abonamentele fac parte din prețul implementării, nu se plătesc separat."),
          ("Fără sume fixe", "Fiecare implementare are propria valoare, stabilită după mărimea afacerii și impactul dovedit."),
          ("Durată", "12 luni, cu reînnoire automată. Oricare parte poate încheia parteneriatul în scris, cu 30 de zile înainte; comisioanele pentru afacerile deja recomandate se plătesc în continuare."),
          ("Date și încredere", "Nu cerem liste de contacte și nu contactăm pe nimeni fără acord. Conturile și datele clienților rămân pe numele lor."),
          ("Ce nu promitem", "Nu promitem rezultate înainte de a le măsura. Fiecare audit pornește de la o cifră de bază.")],
  plata="Plata: prin transfer bancar, pe factură (firmă) sau contract de colaborare (persoană fizică).",
  ass_t="Semnături", ass=("Partener", "Pacheco Studios"), ass_campos=("Nume", "Data", "Semnătura"),
 ),
 "en": dict(
  lang="en", data="October 2026", tel="+40 723 098 556", wa="40723098556", site="ro.pachecost.com", funcao="Founder", pagina="Page",
  i_titulo="What you can earn — Pacheco Studios", c_supra="Partner programme",
  c_h1="Introduce<br>businesses.<br><em>Earn from<br>each one.</em>",
  c_lead="Pacheco Studios is an AI systems consultancy: we find where a business loses requests, time and money, and build the system "
         "that fixes it. Our partners are people who work with companies every day and introduce us to the ones who need it.",
  c_para="Prepared for", c_vazio="partner name",
  c_tres=[("3", "quick wins implemented in your business, at no cost"), ("15%", "of the implementation value, for every business you introduce"),
          ("5%", "every 3 months, for as long as we work with that business")],
  p2_et="01 · You receive first", p2_h="Before we talk about commissions, we improve your business.",
  qw_t="3 quick wins, at no cost", qw_nota="We choose them together after the triage; the triage we bring you already shows at least one. Some examples:",
  qw=[("QR poster for Google reviews", "Happy clients leave a review in 20 seconds."),
      ("Complete Google Business Profile", "Hours, services, real photos and a contact button."),
      ("Quick replies on WhatsApp", "Repeated questions get the right answer in one tap."),
      ("Request form", "Requests arrive complete, without five back-and-forth messages."),
      ("Automatic message after the service", "Asks for the review at the right moment."),
      ("Shared request tracker", "Every request has an owner and a status.")],
  fluxo_t="Then, for every business you introduce",
  pasos=[("You introduce us", "To a business losing requests, time or money, with the owner's consent.", "You"),
         ("Triage and audit", "We find the most valuable leak. The audit is not charged separately: it is credited to the implementation.", "No separate cost"),
         ("Implementation starts", "The business decides to work with us. You receive 15% of the implementation value.", "15%"),
         ("We stay with the client", "For as long as we work with the business, you receive 5% of what it pays us, every 3 months.", "5% / quarter")],
  p3_et="02 · What you can earn", p3_h="Every business is different. That is why the commission is a percentage, not a fixed amount.",
  cen_nota="The implementation value depends on the size of the business and the impact we prove. Two examples (in Romanian lei):",
  cen=[("A business turning over 50,000 lei / month", "≈ 20,000 lei", "3,000 lei"), ("A business turning over 1,000,000 lei / month", "≈ 100,000 lei", "15,000 lei")],
  cen_rot=("Estimated implementation", "You receive 15%", "Then, every 3 months", "5% of what it pays us"),
  tri_t="The quarterly share",
  tri=[("For every 10,000 lei", "500 lei", "paid by the client in a quarter"), ("While we work", "5%", "with the business you introduced, no end date"),
       ("Every 3 months", "Report", "with what the client paid and your commission")],
  ano="<b>One possible year:</b> one small and one large business introduced = <b>18,000 lei</b> from implementation alone, plus the quarterly share.",
  calc_n="Worked examples with approximate values, not promises or prices.",
  p4_et="03 · Why it is worth it", p4_h="You earn without delivering. Your clients get a system that works.",
  porque_t="What you gain",
  porque=["A real commission on every implementation, not a token amount", "Income every 3 months, while the client stays with us",
          "Your clients thank you for the introduction", "We handle everything: triage, audit, implementation, support",
          "It costs nothing and there is no exclusivity"],
  quem_t="Who to introduce",
  quem=["Businesses receiving requests by WhatsApp, phone and e-mail", "Owners answering the same questions every day",
        "Businesses growing faster than their operations", "Teams copying data between spreadsheets and tools"],
  como_t="How to introduce us (pick one)",
  como=[("WhatsApp group", "A group with the owner and us, and you introduce us in two lines."),
        ("The contact, with consent", "Send us the name and phone after telling the owner we will call."),
        ("Your name", "Give them our number; they tell us you sent them.")],
  fwd_t="Message ready to forward to the owner",
  fwd="Hi! I recommend Pacheco Studios (Tomás). They look at how requests come into your business and show you, on one page, "
      "where they might get lost and what is worth checking. Do a triage with them: +40 723 098 556.",
  ex_t="Request the triage", ex="Scan: WhatsApp opens with «AUDIT».",
  prox_t="Next step", prox="If it makes sense to you, we send the partnership proposal, with the rules and commissions in writing, to sign.",
  p_titulo="Partnership proposal — Pacheco Studios", p_et="Partnership proposal",
  p_h="Partnership between {p} and Pacheco Studios", p_vazio="……………………",
  da_t="What Pacheco Studios gives",
  da=["3 quick wins in the partner's business, at no cost, chosen after the triage",
      "15% of the implementation value for every business introduced",
      "5% of what the introduced business pays, every 3 months, while we work with it",
      "A report every 3 months with introductions, payments and commissions",
      "Commission paid within 7 days of the client's payment"],
  faz_t="What the partner does",
  faz=["<b>1.</b> When we apply the 3 quick wins: a first online testimonial and recommendation, as a thank-you",
       "<b>2.</b> Then: recommends us by word of mouth to those who need it",
       "<b>3.</b> Monthly: features us in their content once a month, tagging @pachecostudiospt",
       "Introduces businesses only with the owner's consent",
       "Says it is a partnership when talking about us publicly"],
  troca="<b>In return, in this order:</b> 1) when we apply the 3 quick wins, a first online testimonial and recommendation, as a thank-you; 2) then word-of-mouth recommendations; 3) once a month, you feature us in your content.",
  tab_cab=("Stage", "The partner receives", "When"),
  tab=[("Quick wins", "3, at no cost", "At the start"), ("Audit", "—", "Credited to the implementation"),
       ("Implementation", "15%", "Within 7 days of the client's payment"), ("Ongoing support", "5%", "Every 3 months, within 7 days of the close")],
  regras_t="The rules",
  regras=[("What counts as an introduction", "You introduce us directly to the owner or decision-maker; the business knows and agrees; it was not already talking to us; implementation starts within 180 days."),
          ("Basis of calculation", "The commission is calculated on what the client actually pays. Website, assistant, automations and monthly fees are part of the implementation price, not charged separately."),
          ("No fixed amounts", "Each implementation has its own value, set by the size of the business and the proven impact."),
          ("Duration", "12 months, renewing automatically. Either party can end the partnership in writing with 30 days' notice; commissions on businesses already introduced keep being paid."),
          ("Data and trust", "We never ask for contact lists and never contact anyone without consent. Client accounts and data stay in their name."),
          ("What we do not promise", "We do not promise results before measuring them. Every audit starts from a baseline.")],
  plata="Payment: by bank transfer, against an invoice (company) or a collaboration agreement (individual).",
  ass_t="Signatures", ass=("Partner", "Pacheco Studios"), ass_campos=("Name", "Date", "Signature"),
 ),
 "pt": dict(
  lang="pt-PT", data="Outubro 2026", tel="+351 967 117 357", wa="351967117357", site="pachecost.com", funcao="Fundador", pagina="Página",
  i_titulo="Quanto pode ganhar — Pacheco Studios", c_supra="Programa de parceiros",
  c_h1="Apresente<br>negócios.<br><em>Ganhe com<br>cada um.</em>",
  c_lead="A Pacheco Studios é uma consultora de sistemas com IA: encontramos onde um negócio perde pedidos, tempo e dinheiro e construímos "
         "o sistema que resolve. Os nossos parceiros são pessoas que trabalham todos os dias com empresas e nos apresentam às que precisam.",
  c_para="Preparado para", c_vazio="nome do parceiro",
  c_tres=[("3", "soluções rápidas implementadas no seu negócio, sem custo"), ("15 %", "do valor de implementação, por cada negócio que apresentar"),
          ("5 %", "a cada 3 meses, enquanto trabalharmos com esse negócio")],
  p2_et="01 · Primeiro recebe", p2_h="Antes de falarmos de comissões, melhoramos o seu negócio.",
  qw_t="3 soluções rápidas, sem custo", qw_nota="Escolhemo-las consigo depois da triagem; a triagem que lhe trazemos já mostra pelo menos uma. Alguns exemplos:",
  qw=[("Cartaz QR para avaliações Google", "Os clientes satisfeitos deixam a avaliação em 20 segundos."),
      ("Ficha Google completa", "Horário, serviços, fotos reais e botão de contacto."),
      ("Respostas rápidas no WhatsApp", "As perguntas repetidas têm a resposta certa num toque."),
      ("Formulário de pedido", "O pedido chega completo, sem cinco mensagens de ida e volta."),
      ("Mensagem automática depois do serviço", "Pede a avaliação no momento certo."),
      ("Folha partilhada de pedidos", "Cada pedido tem um responsável e um estado.")],
  fluxo_t="Depois, por cada negócio que nos apresentar",
  pasos=[("Apresenta-nos", "A um negócio que perde pedidos, tempo ou dinheiro, com o acordo do dono.", "Você"),
         ("Triagem e auditoria", "Encontramos a fuga de maior valor. A auditoria não se paga à parte: fica creditada na implementação.", "Sem custo à parte"),
         ("Começa a implementação", "O negócio decide trabalhar connosco. Recebe 15 % do valor de implementação.", "15 %"),
         ("Ficamos com o cliente", "Enquanto trabalharmos com o negócio, recebe 5 % do que ele nos paga, a cada 3 meses.", "5 % / trimestre")],
  p3_et="02 · Quanto pode ganhar", p3_h="Cada negócio é diferente. Por isso a comissão é uma percentagem, não um valor fixo.",
  cen_nota="O valor de implementação depende da dimensão do negócio e do impacto que provamos. Dois exemplos:",
  cen=[("Negócio que fatura 10.000 € / mês", "≈ 4.000 €", "600 €"), ("Negócio que fatura 200.000 € / mês", "≈ 20.000 €", "3.000 €")],
  cen_rot=("Implementação estimada", "Recebe 15 %", "Depois, a cada 3 meses", "5 % do que nos paga"),
  tri_t="A parte trimestral",
  tri=[("Por cada 2.000 €", "100 €", "pagos pelo cliente num trimestre"), ("Enquanto trabalharmos", "5 %", "com o negócio que apresentou, sem prazo"),
       ("A cada 3 meses", "Relatório", "com o que o cliente pagou e a sua comissão")],
  ano="<b>Um ano possível:</b> um negócio pequeno e um grande apresentados = <b>3.600 €</b> só em implementação, mais a parte trimestral.",
  calc_n="Exemplos de cálculo com valores aproximados, não promessas nem preços.",
  p4_et="03 · Porque vale a pena", p4_h="Ganha sem executar. Os seus clientes ficam com um sistema que funciona.",
  porque_t="O que ganha",
  porque=["Uma comissão real em cada implementação, não um valor simbólico", "Rendimento a cada 3 meses, enquanto o cliente ficar connosco",
          "Os seus clientes agradecem-lhe a apresentação", "Tratamos de tudo: triagem, auditoria, implementação, suporte",
          "Não custa nada e não há exclusividade"],
  quem_t="Quem nos apresentar",
  quem=["Negócios que recebem pedidos por WhatsApp, telefone e e-mail", "Donos que respondem às mesmas perguntas todos os dias",
        "Negócios a crescer mais depressa do que a operação", "Equipas que copiam dados entre folhas e programas"],
  como_t="Como nos apresentar (escolha uma)",
  como=[("Grupo no WhatsApp", "Um grupo com o dono e connosco, e apresenta-nos em duas linhas."),
        ("O contacto, com autorização", "Envia-nos o nome e o telefone, depois de avisar o dono que vamos ligar."),
        ("O seu nome", "Dá-lhe o nosso número; ele diz-nos que vem da sua parte.")],
  fwd_t="Mensagem pronta a enviar ao dono",
  fwd="Olá! Recomendo-te a Pacheco Studios, do Tomás. Olham para a forma como os pedidos entram no teu negócio e mostram-te, numa página, "
      "onde se podem perder e o que vale a pena validar. Faz uma triagem com eles: +351 967 117 357.",
  ex_t="Pedir a triagem", ex="Aponte a câmara: abre o WhatsApp com «AUDIT».",
  prox_t="Próximo passo", prox="Se fizer sentido para si, enviamos a proposta de parceria, com as regras e as comissões por escrito, para assinar.",
  p_titulo="Proposta de parceria — Pacheco Studios", p_et="Proposta de parceria",
  p_h="Parceria entre {p} e a Pacheco Studios", p_vazio="……………………",
  da_t="O que a Pacheco Studios dá",
  da=["3 soluções rápidas no negócio do parceiro, sem custo, escolhidas depois da triagem",
      "15 % do valor de implementação por cada negócio apresentado",
      "5 % do que o negócio apresentado pagar, a cada 3 meses, enquanto trabalharmos com ele",
      "Relatório a cada 3 meses com apresentações, pagamentos e comissões",
      "Pagamento da comissão até 7 dias depois de o cliente pagar"],
  faz_t="O que o parceiro faz",
  faz=["<b>1.</b> Quando aplicamos as 3 soluções rápidas: o primeiro testemunho online e a recomendação, como agradecimento",
       "<b>2.</b> Depois: recomenda-nos boca a boca a quem precisar",
       "<b>3.</b> Todos os meses: mostra-nos nos seus conteúdos 1 vez por mês, com @pachecostudiospt",
       "Apresenta negócios só com o acordo do dono",
       "Diz que é uma parceria quando fala de nós em público"],
  troca="<b>Em troca, por esta ordem:</b> 1) quando aplicamos as 3 soluções, o primeiro testemunho online e a recomendação, como agradecimento; 2) depois, a recomendação boca a boca; 3) uma vez por mês, mostra-nos nos seus conteúdos.",
  tab_cab=("Fase", "O parceiro recebe", "Quando"),
  tab=[("Soluções rápidas", "3, sem custo", "No início"), ("Auditoria", "—", "Creditada na implementação"),
       ("Implementação", "15 %", "Até 7 dias depois de o cliente pagar"), ("Acompanhamento", "5 %", "A cada 3 meses, até 7 dias depois do fecho")],
  regras_t="As regras",
  regras=[("O que conta como apresentação", "Apresenta-nos diretamente ao dono ou a quem decide; o negócio sabe e concorda; não estava já a falar connosco; a implementação começa até 180 dias depois."),
          ("Base de cálculo", "A comissão calcula-se sobre o que o cliente paga de facto. Site, assistente, automações e mensalidades fazem parte do preço de implementação, não se pagam à parte."),
          ("Sem valores fixos", "Cada implementação tem um valor próprio, definido pela dimensão do negócio e pelo impacto provado."),
          ("Duração", "12 meses, renováveis automaticamente. Qualquer parte pode terminar a parceria por escrito com 30 dias de aviso; as comissões dos negócios já apresentados continuam a ser pagas."),
          ("Dados e confiança", "Nunca pedimos listas de contactos nem contactamos ninguém sem autorização. As contas e os dados dos clientes ficam em nome deles."),
          ("O que não prometemos", "Não prometemos resultados antes de os medir. Cada auditoria parte de um número de base.")],
  plata="Pagamento: por transferência, contra fatura (empresa) ou contrato de colaboração (particular).",
  ass_t="Assinaturas", ass=("Parceiro", "Pacheco Studios"), ass_campos=("Nome", "Data", "Assinatura"),
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


CSS += """
.pasos{grid-template-columns:1fr 1fr;margin-bottom:0}
.pasos li{padding:4.5mm}.pasos b{margin:3.5mm 0 1.5mm}
.troca{margin:-4mm 0 8mm;font-size:9.6pt;line-height:1.5;padding:4mm 5mm;border-left:3px solid var(--l);background:var(--o2)}
.troca b{font-weight:600}
.qw{list-style:none;margin:0 0 8mm;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:3mm 5mm}
.qw li{display:flex;gap:3mm;align-items:flex-start;padding:3.6mm 4mm;border-radius:8px;background:var(--o2);box-shadow:inset 0 0 0 1px var(--li)}
.qw .ok{flex:none;width:4.6mm;height:4.6mm;border-radius:50%;background:var(--l);margin-top:.3mm;position:relative}
.qw .ok::after{content:'';position:absolute;left:1.5mm;top:.9mm;width:1.2mm;height:2.2mm;border:solid var(--c);border-width:0 1.6px 1.6px 0;transform:rotate(45deg)}
.qw b{display:block;font-weight:600;font-size:10pt;margin-bottom:.6mm}
.qw span{font-size:9pt;color:var(--so);line-height:1.4}
.cen{display:grid;grid-template-columns:1fr 1fr;gap:5mm;margin:0 0 8mm}
.cen > div{border-radius:12px;background:var(--o2);box-shadow:inset 0 0 0 1px var(--li);padding:6mm}
.cen > div:last-child{background:var(--c);color:var(--o);box-shadow:inset 0 0 0 1.5px var(--l)}
.cen .mono{color:var(--lt);display:block;margin-bottom:4mm;line-height:1.4}
.cen > div:last-child .mono{color:var(--l)}
.cen dl{margin:0;display:grid;gap:3.2mm}
.cen dt{font-size:8.6pt;color:var(--so)}.cen > div:last-child dt{color:var(--sc)}
.cen dd{margin:.6mm 0 0;font:400 13pt/1.1 'Archivo Black'}
.cen dd.big{font-size:27pt;color:var(--lt)}.cen > div:last-child dd.big{color:var(--l)}
.cen dd.sm{font:600 10pt/1.3 'Inter'}
.tri{display:grid;grid-template-columns:repeat(3,1fr);gap:5mm;margin-bottom:6mm}
.tri div{border-top:2px solid var(--c);padding-top:3mm}
.tri .mono{color:var(--so)}
.tri b{display:block;font:400 17pt/1 'Archivo Black';color:var(--lt);margin:2.5mm 0 1.5mm;white-space:nowrap}
.tri span{font-size:9pt;color:var(--so)}
.ano{background:var(--c);color:var(--o);border-radius:10px;padding:5mm 6mm;font-size:11pt;line-height:1.45}
.ano b{color:var(--l);font-weight:600}
.pequena{font-size:8.4pt;color:var(--so);margin:3mm 0 0}
.prox{margin-top:auto;margin-bottom:8mm;display:grid;grid-template-columns:1fr auto;gap:6mm;align-items:center;background:var(--l);color:var(--c);border-radius:10px;padding:5.5mm 6.5mm}
.prox .mono{display:block;margin-bottom:2mm}
.prox p{margin:0;font:600 11pt/1.4 'Inter'}
.prox b{font:400 22pt/1 'Archivo Black'}
.duas2{display:grid;grid-template-columns:1fr 1fr;gap:6mm;margin-bottom:7mm}
.p4 h2{margin-bottom:7mm}.p4 .como{margin-bottom:6mm}
/* proposta */
.ptop{background:var(--c);color:var(--o);padding:11mm 16mm 9mm}
.ptop .topo{display:flex;justify-content:space-between;align-items:center}.ptop .topo .mono{color:var(--sc)}
.ptop .mono.l{color:var(--l);margin:9mm 0 3mm;display:block}
.ptop h1{font:400 21pt/1.15 'Archivo Black';text-transform:uppercase;margin:0}
.ptop h1 em{font-style:normal;color:var(--l)}
.ptop p{margin:3mm 0 0;font-size:9pt;color:var(--sc)}
.compromissos{display:grid;grid-template-columns:1fr 1fr;gap:6mm;margin-bottom:7mm}
.compromissos .lista li{font-size:9.4pt}.compromissos .lista b{color:var(--l)}.compromissos > div:last-child .lista b{color:var(--lt)}
.regras li{grid-template-columns:42mm 1fr}
.pp .acordo{margin-top:8mm;margin-bottom:auto}.pp .compromissos{margin-bottom:5mm}.ptop{padding:10mm 16mm 7mm}.ptop .mono.l{margin:6mm 0 3mm}.pp .corpo{padding-top:7mm}.pp td{padding:2.4mm 0}.pp .corpo{padding-bottom:6mm}
.local{display:flex;gap:6mm;margin-bottom:5mm}.local .campo{flex:1;margin:0}
"""


def esc(s):
    return html.escape(s, quote=False)


def comum(t):
    wa = f"https://wa.me/{t['wa']}?text=AUDIT"
    qr = segno.make(wa, error="m").svg_inline(scale=3, dark="#141210", light="#EFEAE3", border=2)
    rod = lambda n, total: (f'<footer class="rod"><span class="marca">Pacheco Studios<i></i></span>'
                            f'<span>Tomás Pacheco · {t["tel"]} · {t["site"]}</span>'
                            f'<span class="mono">{t["pagina"]} {n}/{total}</span></footer>')
    cab = lambda sub: f'<header class="cab"><span class="marca">Pacheco Studios<i></i></span><span class="mono">{sub} · {t["data"]}</span></header>'
    return wa, qr, rod, cab


def incentivo_html(t):
    wa, qr, rod, cab = comum(t)
    para = (f'<strong>{esc(PARCEIRO)}</strong>' if PARCEIRO else f'<strong class="vazio">{t["c_vazio"]}</strong>')
    tres = "".join(f"<div><b>{a}</b><span>{b}</span></div>" for a, b in t["c_tres"])
    qw = "".join(f'<li><i class="ok"></i><div><b>{a}</b><span>{b}</span></div></li>' for a, b in t["qw"])
    pasos = "".join(f'<li class="{"forte" if i >= 2 else ""}"><span class="n">0{i+1}</span><span class="tag">{c}</span><b>{a}</b><span>{b}</span></li>'
                    for i, (a, b, c) in enumerate(t["pasos"]))
    r = t["cen_rot"]
    cen = "".join(f'<div><span class="mono">{nome}</span><dl><div><dt>{r[0]}</dt><dd>{impl}</dd></div>'
                  f'<div><dt>{r[1]}</dt><dd class="big">{com}</dd></div><div><dt>{r[2]}</dt><dd class="sm">{r[3]}</dd></div></dl></div>'
                  for nome, impl, com in t["cen"])
    tri = "".join(f'<div><span class="mono">{a}</span><b>{b}</b><span>{c}</span></div>' for a, b, c in t["tri"])
    porque = "".join(f"<li>{x}</li>" for x in t["porque"])
    quem = "".join(f"<li>{x}</li>" for x in t["quem"])
    como = "".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in t["como"])
    sub = t["c_supra"]
    return f"""<!doctype html>
<html lang="{t['lang']}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(t['i_titulo'])}</title><style>{FONTES}{CSS}</style></head><body>
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
<section class="pag">{cab(sub)}<div class="corpo">
  <p class="mono et">{t['p2_et']}</p><h2>{t['p2_h']}</h2>
  <h3>{t['qw_t']}</h3><p class="nota">{t['qw_nota']}</p>
  <ul class="qw">{qw}</ul>
  <p class="troca">{t['troca']}</p>
  <h3>{t['fluxo_t']}</h3>
  <ol class="pasos">{pasos}</ol>
</div>{rod(2, 4)}</section>
<section class="pag">{cab(sub)}<div class="corpo">
  <p class="mono et">{t['p3_et']}</p><h2>{t['p3_h']}</h2>
  <p class="nota">{t['cen_nota']}</p>
  <div class="cen">{cen}</div>
  <h3>{t['tri_t']}</h3><div class="tri">{tri}</div>
  <div class="ano">{t['ano']}</div>
  <p class="pequena">{t['calc_n']}</p>
</div>{rod(3, 4)}</section>
<section class="pag p4">{cab(sub)}<div class="corpo">
  <p class="mono et">{t['p4_et']}</p><h2>{t['p4_h']}</h2>
  <div class="duas2"><div><h3>{t['porque_t']}</h3><ul class="lista">{porque}</ul></div>
    <div class="escuro"><h3>{t['quem_t']}</h3><ul class="lista">{quem}</ul></div></div>
  <h3>{t['como_t']}</h3><ul class="como">{como}</ul>
  <h3>{t['fwd_t']}</h3>
  <div class="fwd"><div class="bolha">{t['fwd']}</div>
    <div class="ex">{qr}<b>{t['ex_t']}</b><br>{t['ex']}<a href="{wa}">wa.me/{t['wa']}</a></div></div>
  <div class="prox"><div><span class="mono">{t['prox_t']}</span><p>{t['prox']}</p></div><b>→</b></div>
</div>{rod(4, 4)}</section>
</body></html>"""


def proposta_html(t):
    wa, qr, rod, cab = comum(t)
    nome = f"<em>{esc(PARCEIRO)}</em>" if PARCEIRO else t["p_vazio"]
    da = "".join(f"<li>{x}</li>" for x in t["da"])
    faz = "".join(f"<li>{x}</li>" for x in t["faz"])
    linhas = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in t["tab"])
    regras1 = "".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in t["regras"][:3])
    regras2 = "".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in t["regras"][3:])
    campos = "".join(f'<div class="campo">{c}<i></i></div>' for c in t["ass_campos"])
    ass = "".join(f'<div><span class="mono">{p}</span>{campos}</div>' for p in t["ass"])
    return f"""<!doctype html>
<html lang="{t['lang']}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(t['p_titulo'])}</title><style>{FONTES}{CSS}</style></head><body>
<section class="pag pp">
  <div class="ptop"><div class="topo"><span class="marca">Pacheco Studios<i></i></span><span class="mono">{t['data']}</span></div>
    <span class="mono l">{t['p_et']}</span><h1>{t['p_h'].format(p=nome)}</h1></div>
  <div class="corpo">
  <div class="compromissos"><div class="escuro"><h3>{t['da_t']}</h3><ul class="lista">{da}</ul></div>
    <div><h3>{t['faz_t']}</h3><ul class="lista">{faz}</ul></div></div>
  <table class="tp"><thead><tr><th>{t['tab_cab'][0]}</th><th>{t['tab_cab'][1]}</th><th>{t['tab_cab'][2]}</th></tr></thead><tbody>{linhas}</tbody></table>
  <p class="nota">{t['plata']}</p>
  <h3>{t['regras_t']}</h3><ul class="regras">{regras1}</ul>
  </div>{rod(1, 2)}</section>
<section class="pag pp">{cab(t['p_et'])}<div class="corpo">
  <ul class="regras">{regras2}</ul>
  <div class="acordo"><h3>{t['ass_t']}</h3><div class="ass">{ass}</div></div>
</div>{rod(2, 2)}</section>
</body></html>"""


CSS += """
.tp td:nth-child(2),.tp th:nth-child(2){text-align:left;padding-right:4mm}
.tp td:last-child{font:400 9.4pt/1.35 'Inter';color:var(--so);white-space:normal}
.tp td:nth-child(2){font:400 12pt/1.2 'Archivo Black';color:var(--lt)}
"""


def pdf(nome, conteudo):
    h = os.path.join(AQUI, nome + ".html")
    open(h, "w", encoding="utf-8").write(conteudo)
    p = h[:-5] + ".pdf"
    subprocess.run([CHROMIUM, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={p}", "file://" + h], check=True, capture_output=True)
    print("ok", os.path.relpath(p, RAIZ), os.path.getsize(p) // 1024, "KB")


sufixo = ("-" + re.sub(r"[^a-z0-9]+", "-", PARCEIRO.lower()).strip("-")) if PARCEIRO else ""
for lingua, t in T.items():
    pdf(f"incentivo-{lingua}{sufixo}", incentivo_html(t))
    pdf(f"proposta-parceria-{lingua}{sufixo}", proposta_html(t))
