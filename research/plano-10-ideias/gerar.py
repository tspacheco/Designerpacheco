#!/usr/bin/env python3
"""Gera plano-10-ideias.pdf: uma página por ideia + execução diária.

Uso: python3 gerar.py   (precisa de /opt/pw-browsers/chromium)
Os textos estão em IDEIAS e DIARIA abaixo. Só números medidos pelos threads.
"""
import html, pathlib, subprocess

AQUI = pathlib.Path(__file__).resolve().parent
CHROMIUM = "/opt/pw-browsers/chromium"

# estado: "ativo" (a correr), "pronto" (feito, à espera do Tomás), "curso" (em construção)
IDEIAS = [
    {
        "n": 1, "titulo": "Caçador diário de negócios", "estado": "ativo",
        "sub": "50 negócios de Iași sem site e 50 demos por dia útil",
        "exec": [
            "Duas rotinas de segunda a sexta (hora de Iași). <b>7h52, corrida A:</b> pesquisa 50 fichas Google de negócios sem site, constrói as 25 melhores demos com 5 construtores em paralelo e publica-as em pachecost.com/demo/&lt;slug&gt;/. <b>11h22, corrida B:</b> constrói as outras 25.",
            "Zona: bairros e comunas à volta do centro (Tătărași, Nicolina, Valea Lupului, Miroslava, Bucium…) e nichos ainda não pesquisados.",
            "Mensagem nova (desde o Star Services Auto, em romeno): «Procura aumentar entre 10% a 30% o número de clientes deste mês e além? Aqui vai a solução que criei após olhar o seu negócio (link da demo). Pode até não entender, mas acredite, pois será assim mesmo. Vamos marcar uma hora para implementar esta solução.» Cada contacto leva WhatsApp sim / ? / não, link de WhatsApp, link de SMS e morada. O registo das fichas vistas impede repetir negócios.",
            "Se uma corrida não fechar as 25, as que faltam passam para a seguinte, com o motivo.",
        ],
        "kpis": [("50", "negócios por dia"), ("25 + 25", "demos às 7h52 e 11h22"), ("250", "demos por semana")],
        "res": [
            "<b>1.ª corrida: sexta 09/10, às 7h52.</b> Ainda não há resultado próprio desta rotina.",
            "O que a decidiu: no lote 4 (25 demos, feito à mão a 08/10) metade das fichas do centro de Iași já tinha site. Por isso o caçador vai para os bairros e comunas.",
            "Base no ar: 70 demos (Algarve e Iași) no projeto pachecost-demos.",
        ],
        "dia": [
            "7h52 e 11h22: as rotinas deixam a lista do dia em research/cacador/AAAA-MM-DD.md, com os botões de WhatsApp e SMS prontos.",
            "Tu: envias as 25 mensagens da corrida A de manhã e as 25 da corrida B à tarde, pelo WhatsApp Business RO. Os «?» que não entregam passam para SMS ou para a lista de visitas.",
            "Cada demo enviada fica no tracker (ideia 2) como «Enviado».",
        ],
        "tomas": "Enviar as mensagens. Dizer se queres também ao sábado.",
    },
    {
        "n": 2, "titulo": "Tracker das demos", "estado": "pronto",
        "sub": "Quem abriu, quem respondeu, quem não quer, e as contas do funil",
        "exec": [
            "Página no telemóvel: <b>claude.ai/artifact/NDnUhrKktvWHT2tvzMf1wT</b>. No topo o funil (enviados → abriram → responderam → reunião → cliente, mais «sem interesse», com %), depois a lista e uma tabela por lote.",
            "Tocas no negócio e escolhes o estado; a data fica guardada sozinha. Há caixa de notas. O filtro «Abriram e não responderam» diz-te a quem ligar primeiro.",
            "Cada demo tem um contador invisível do GoatCounter, sem cookies, no caminho /demo/&lt;curto&gt;/. As tuas visitas não contam depois de abrires uma vez pachecost.com/demo/fika/#nao-contar em cada aparelho.",
        ],
        "kpis": [("70", "demos no tracker"), ("2", "responderam"), ("19h", "relatório diário")],
        "res": [
            "70 demos carregadas, incluindo as 25 do lote 4 de Iași (estado «por enviar»).",
            "Lote 1 de Iași marcado como enviado. Responderam: <b>Croitoria Dan</b> e <b>Auto Spa</b> (a Auto Spa já tem a oferta escrita de 2.500 RON + 350 RON/mês).",
            "Contador confirmado nas demos no ar (commit a3d8a89). As aberturas anteriores a 08/10 não ficam registadas e as novas só aparecem com o token.",
        ],
        "dia": [
            "19h de Iași: relatório no thread do tracker com o funil, o que mudou desde a véspera e a lista de quem abriu e não respondeu, com telefone. Se nada mudar, não há mensagem.",
            "Tu: marcas os estados ao longo do dia, à medida que respondem.",
            "Na manhã seguinte ligas primeiro a quem abriu e não respondeu.",
        ],
        "tomas": "Criar o token no GoatCounter (Settings → API, «Read statistics») e guardá-lo no GitHub como GOATCOUNTER_TOKEN. Dizer que lotes já enviaste.",
    },
    {
        "n": 3, "titulo": "Auditoria grátis a sites fracos", "estado": "pronto",
        "sub": "Para quem já paga um site: medimos o deles contra uma demo nossa",
        "exec": [
            "Fichas Google de Iași com site próprio. A PONTE mede cada site no telemóvel com o motor do PageSpeed (Lighthouse móvel + iPhone simulado) e verifica o que falta ao cliente: botão de chamada, WhatsApp, marcação, mapa, dados para o Google.",
            "Ranking de fraqueza de 0 a 100. Os 10 mais fracos recebem um PDF de 3 páginas: em RO para o dono e em PT para ti. Compara com uma demo nossa do mesmo tipo, medida no mesmo dia, e dá 3 vitórias rápidas e o dado da Google sobre abandono, com fonte. Não tem preço.",
            "Na reunião pedes as visitas por mês e quanto vale um cliente, e fazes a conta à frente do dono.",
        ],
        "kpis": [("91", "sites medidos"), ("10", "auditorias em PDF"), ("3", "sites que nem abrem")],
        "res": [
            "Exemplo: <b>Trai Restaurant</b> (4,8★, 1.717 avaliações) tem 30/100 de velocidade e o conteúdo aparece aos 30,7 s. A nossa demo La Gioia tem 84/100 e 3,6 s. As nossas 10 demos medidas têm entre 75 e 97 de velocidade e SEO 100.",
            "Os 10: Dr. Bacusca (vet), ERIS VET, Trai, Vetis, Tasha Beauty, Cofetăria de acasă, Centro de imagiologia veterinária, Geamgeria, One Beauty Concept, Gist Coffee. Dois só têm fixo (Bacusca e ERIS): é ligar.",
            "Trimite Flori, La Dolce Vita e Tudor Saloon têm na ficha Google um site que dá erro. São os leads mais quentes.",
        ],
        "dia": [
            "Proposta: segunda às 8h de Iași, lote novo (fichas novas no Maps, medir, 10 PDFs). Fica ativo quando confirmares.",
            "Tu: 2 auditorias por dia útil (10 por semana), com a mensagem e o link do PDF de ENVIAR.md. Nos fixos ligas e pedes um WhatsApp ou e-mail.",
        ],
        "tomas": "Confirmar o lote às segundas. Começar pelos 3 sites que não abrem.",
    },
    {
        "n": 4, "titulo": "Reel de cada demo, com o «sim» do dono", "estado": "pronto",
        "sub": "O 2.º contacto é um presente, não uma insistência",
        "exec": [
            "<b>python3 gerar_reel.py &lt;slug&gt;</b> grava a demo, usa a fonte e as cores dela e junta música própria. Demora cerca de 8 minutos por reel. Abre com a nota Google e fecha com «Ai o afacere? Meriți un site ca acesta.» + ro.pachecost.com.",
            "Mandas o vídeo 2 a 3 dias depois da mensagem da demo, primeiro a quem a abriu. O vídeo é dele, de graça. Pedes autorização para publicar no @pachecostudiospt como Colaboração.",
            "Com «DA» escrito: mensagem 2 e publicação com convite ao @ dele, e o reel aparece nos dois perfis. Sem resposta ou com «não», não se publica. Usá-lo em anúncios pagos pede um 2.º sim.",
        ],
        "kpis": [("1", "reel feito"), ("29 s", "9:16, com som"), ("~8 min", "por reel")],
        "res": [
            "1.º reel: <b>Noir Barbershop</b>. Abre com «4,9★ pe Google · 82 de recenzii. Niciun site. Așa ar arăta.» e o site desce uma secção a cada compasso.",
            "Mensagens de pedido e de resposta ao «sim» em RO e PT, legenda do Instagram e estado de cada reel (gerado → pedido → sim/não → publicado) em reels.json.",
            "Falta o Instagram do Noir para a Colaboração.",
        ],
        "dia": [
            "Cada demo enviada no dia D tem o reel gerado e pronto no dia D+2.",
            "Tu: no D+2 ou D+3 envias os reels, primeiro a quem abriu a demo (filtro do tracker). Quem diz «DA» é lead quente e a resposta já propõe a visita de 20 minutos.",
            "Publicas à noite os reels com «DA» como Colaboração.",
        ],
        "tomas": "Dizer o Instagram do Noir Barbershop.",
    },
    {
        "n": 5, "titulo": "Páginas por nicho e cidade", "estado": "pronto",
        "sub": "Quem pesquisa no Google entra sozinho",
        "exec": [
            "Uma página por nicho e cidade, cada uma com as demos desse nicho e o botão do diagnóstico. As demos aparecem como uma rua de telemóveis, com a morada do negócio numa placa azul (RO) ou em azulejo (PT).",
            "Sem preços nem números inventados: o único número é quantas demos há em cada página. Quem abre uma demo a partir daqui conta à parte, para o tracker continuar a contar só os donos.",
            "Algarve tem poucas demos, por isso as páginas PT mostram também as demos de Iași com versão em PT, com o selo «Feito em Iași».",
        ],
        "kpis": [("12", "páginas RO, Iași"), ("5", "páginas PT, Algarve"), ("3", "demos para nascer página nova")],
        "res": [
            "<b>Iași</b> (ro.pachecost.com/site-uri/): restaurantes, cafés e pastelarias, barbearias, salões de beleza, oficinas e lavagens auto, lojas, animais, tatuagens, massagens, costura e reparações, chaves, serviços ao domicílio.",
            "<b>Algarve</b> (pachecost.com/sites/): restaurantes, pastelarias e cafés, barbearias, oficinas e lojas.",
            "Pré-visualizações: claude.ai/artifact/B3Xnn4im3GtkijK6GvoS2h (barbearias Iași) · claude.ai/artifact/Q8we1oDvdfD3XSk7MhinSe (restaurantes Algarve). Ainda não estão no ar: o thread das demos junta o código.",
        ],
        "dia": [
            "Sozinho: cada demo nova do caçador entra na página do seu nicho no mesmo push. Quando um nicho chega a 3 demos, nasce página nova (o texto para clínicas e ginásios já está escrito).",
            "GoatCounter mostra quem clica no diagnóstico em cada página.",
            "Ao fim de 2 a 4 semanas: ver no Search Console que páginas aparecem e para que palavras, e reforçar o texto dos nichos que pedirem mais.",
        ],
        "tomas": "Subir o zip leve quando o thread das demos o der. No Search Console, criar a propriedade de domínio pachecost.com e enviar o sitemap pachecost.com/sitemap-nichos.xml.",
    },
    {
        "n": 6, "titulo": "Parceiros que indicam clientes", "estado": "pronto",
        "sub": "Quem vê negócios novos todos os dias passa-nos o contacto",
        "exec": [
            "Contabilistas, empresas que abrem firmas, quem vende máquinas registadoras, reclamos luminosos, gráficas, imobiliárias de espaços comerciais, consultores de fundos e fornecedores HoReCa. As agências web ficam de fora.",
            "Mensagem por tipo de parceiro e proposta A4 em PDF (RO, PT de Iași e PT do Algarve), com a demo La Gioia ou SOS Car como exemplo. Aos consultores de fundos diz-se que o site e a loja online são despesa elegível no Start-Up Nation.",
            "Comissão proposta: <b>500 lei (100 €) por site</b> e 250 lei (50 €) por sistema de IA, paga até 7 dias depois de o cliente pagar. O cliente indicado tem o 1.º mês grátis.",
        ],
        "kpis": [("47", "parceiros"), ("37 + 10", "Iași + Faro"), ("6.125 lei", "ficam por cliente, 1.º ano")],
        "res": [
            "Iași: 8 contabilistas, 5 consultores de fundos, 5 gráficas, 4 de abertura de firmas, 4 de máquinas registadoras, 4 de reclamos, 4 imobiliárias e 3 HoReCa. Faro: 5 contabilistas, 4 gráficas e 1 de reclamos.",
            "10 só têm fixo (5 em Iași e 5 em Faro); os outros 37 têm telemóvel com WhatsApp «?».",
            "Conta por cliente indicado em Iași no 1.º ano: 2.500 + 11 × 375 = 6.625 lei; menos 500 de comissão ficam <b>6.125 lei</b>.",
        ],
        "dia": [
            "Segunda às 9h53 de Iași: 10 parceiros novos e lembretes para quem não respondeu em 7 dias, mais o estado das comissões.",
            "Tu: visitas de escritório em Iași com a proposta impressa, juntas às visitas da mesma zona. Os de Faro por telefone.",
        ],
        "tomas": "Decidir a comissão («ok» ou outro valor). Dizer quem aceitou.",
    },
    {
        "n": 7, "titulo": "Empresas acabadas de abrir", "estado": "ativo",
        "sub": "«Felicitări, v-ați înregistrat de curând»: o site antes de alguém lhe vender outro",
        "exec": [
            "Os registos (ONRC, data.gov.ro) não se leem daqui, mas a API pública e grátis da ANAF responde a partir do GitHub. Os números fiscais são dados por ordem, por isso cada empresa nova aparece no próprio dia, com nome, morada, CAEN e, muitas vezes, telefone.",
            "O agente fica só com o distrito de Iași e separa os negócios com clientes à porta (salões, cafés, oficinas, lojas, clínicas). A mensagem leva a frase dos 40 % e uma demo do mesmo ramo como exemplo. O site próprio faz-se só para quem responde.",
            "O telefone é o declarado no registo e às vezes é do contabilista: WhatsApp sempre «?», com SMS ao lado.",
        ],
        "kpis": [("368", "empresas em Iași desde 18/09"), ("25", "na 1.ª lista"), ("2–3", "negócios úteis por dia")],
        "res": [
            "1.ª lista (08/10): 25 empresas registadas nas últimas duas semanas, 19 com telemóvel e mensagem pronta. 19 são de clientes à porta (ex.: Chic Society, Kineto 360, San S Clinique, Aline Concept Store) e 6 de serviços (obras, limpezas, escolas…).",
            "Volume: cerca de 25 registos por dia em Iași, dos quais só 2 ou 3 são negócios locais. Cerca de 60 % declaram telefone.",
            "Portugal (Algarve) fica para depois: o portal de publicações e o Racius abrem pela ponte.",
        ],
        "dia": [
            "8h47 de Iași, de segunda a sexta: lista do dia em agentes/empresas-novas/listas/AAAA-MM-DD.md e aviso no thread.",
            "Tu: 2 ou 3 mensagens por dia, junto com as do caçador. A quem responder, faz-se a demo própria dele.",
        ],
        "tomas": "Nada pendente. Enviar as mensagens.",
    },
    {
        "n": 8, "titulo": "Avaliações Google com queixas", "estado": "ativo",
        "sub": "A dor já está escrita pelos clientes deles",
        "exec": [
            "Pesquisa 10 a 12 ramos de Iași no Maps e lê até 90 fichas: as avaliações mais recentes, as piores e as que falam de «telefon», «răspuns», «mesaj» ou «programare».",
            "Fica com quem tem queixas escritas de telefone ou mensagens sem resposta, ou encomendas esquecidas. Tira cadeias, queixas já resolvidas e queixas com mais de 2 anos.",
            "Cada mensagem cita a frase real da avaliação e oferece a auditoria grátis e os 20 minutos, com botões de WhatsApp e SMS e a versão PT por baixo. É a porta para vender sistemas de IA, não só o site.",
        ],
        "kpis": [("90", "fichas lidas, 12 ramos"), ("717", "avaliações lidas"), ("12", "negócios com queixa citada")],
        "res": [
            "Ramos: dentistas, clínicas, veterinários, pizzarias, salões, service auto, instaladores e mais 5. Saíram 12 leads; 14 foram tirados.",
            "Os mais fortes: <b>Man Pizza</b> (4,9★): «nu mai răspunde nimeni la telefon» (há 2 semanas). <b>Pizzeria Alila</b>: «Am sunat de 5 ori până a răspuns cineva» (há 4 meses). <b>Urgente veterinare non stop</b>: ninguém atende, apesar de ser 24 h (há 3 meses).",
            "Lista: agentes/avaliacoes-queixas/listas/2026-10-08.md, ramo claude/avaliacoes-queixas-m7qdst.",
        ],
        "dia": [
            "Segunda e quinta às 9h37 de Iași: 10 a 12 ramos novos, até 90 fichas, lista nova já revista e traduzida no thread.",
            "Tu: nesses dias envias as cerca de 12 mensagens pelo WhatsApp ou SMS, de manhã, e dizes quem respondeu.",
        ],
        "tomas": "Enviar as 12 mensagens da 1.ª lista e dizer quem respondeu.",
    },
    {
        "n": 9, "titulo": "Ferramenta grátis no site", "estado": "pronto",
        "sub": "Cartaz com QR para pedir avaliações Google, feito em 1 minuto",
        "exec": [
            "O dono cola o link da ficha Google e escreve o nome. Imprime em A4 ou A5, descarrega ou partilha o cartaz. De bónus leva uma mensagem pronta para pedir avaliações aos clientes pelo WhatsApp.",
            "No fim aparece «E agora?», que abre o diagnóstico. Cada cartaz impresso fica no balcão com a linha «Cartaz grátis em pachecost.com/cartaz»: publicidade à frente dos clientes dele.",
            "Escolhido em vez da «nota da ficha Google», que precisava de ler o Google em tempo real (daqui só funciona por lotes).",
        ],
        "kpis": [("3", "línguas: PT, RO e EN"), ("A4 / A5", "imprimir, descarregar, partilhar"), ("1 min", "do link ao cartaz")],
        "res": [
            "Pronta e testada: o QR do cartaz gerado leva ao link exato da ficha.",
            "Pré-visualizações: PT claude.ai/artifact/Rb9i9SEJ5WTosKFvjDERr1 · RO claude.ai/artifact/2HrhkfE3rr1ujbMnBH5GQU (Imprimir e Descarregar só funcionam no site).",
            "Endereços quando entrar no site: pachecost.com/cartaz, ro.pachecost.com/afis e pachecost.com/en/poster. A integração já foi passada ao thread do site.",
        ],
        "dia": [
            "Sozinho: cada uso conta no GoatCounter (colou o link, imprimiu, descarregou, foi ao diagnóstico).",
            "Tu: podes mandar o link aos donos das demos como oferta («fiz-te também o cartaz das avaliações»), por exemplo junto com o reel do D+2.",
        ],
        "tomas": "Subir o zip do pachecost.com quando o thread do site integrar o cartaz.",
    },
    {
        "n": 10, "titulo": "Caso Catarina e pedido de indicações", "estado": "pronto",
        "sub": "Um cliente real mostra o antes e o depois, e indica outros donos",
        "exec": [
            "Página do caso da Pizzaria Catarina: abre com «168 avaliações. Nenhum site. Agora tem.», mostra o antes (a casa só aparecia em sites de outros), o depois (3 ecrãs do site) e os números com «a preencher».",
            "Reel 9:16 de 31 s, com som, que abre com «4,4★ · 168 avaliações. Nenhum site. Agora tem.»",
            "Mensagem à dona, com lembrete ao 4.º dia, a pedir três coisas: autorização, reservas por semana antes e agora, e nome e número de 2 donos da zona.",
        ],
        "kpis": [("1", "caso montado"), ("31 s", "reel 9:16"), ("2", "indicações pedidas")],
        "res": [
            "Pré-visualização: claude.ai/artifact/PYk2ZYwv3oFU5g6MGW38sD. Nenhum número inventado: os resultados ficam «a preencher» até a dona os dar.",
            "O site da Catarina não conta visitas. Com o teu «sim» leva o contador, e daqui a 30 dias o caso já tem esse número.",
            "Ficheiros (mensagem, lembrete, legenda do Instagram) em research/casos/catarina/LEIA-ME.md, ramo claude/caso-catarina-p9rinu.",
        ],
        "dia": [
            "Cada cliente fechado leva o contador no dia da entrega. Ao dia 30, o agente prepara a página, o reel e a mensagem.",
            "Tu: envias a mensagem e ligas aos 2 indicados.",
            "Depois: os números entram no caso, o reel é refeito a abrir com o resultado, a página passa para o site da Pacheco Studios e os indicados entram nos leads como «indicado por…».",
        ],
        "tomas": "Enviar a mensagem à dona no grupo «Sites Catarina», com o reel. Dizer se o site da Catarina leva o contador.",
    },
]

# Execução diária (hora de Iași). quem: "auto" ou "tu"
DIA = [
    ("7h52", "auto", "Caçador, corrida A", "50 fichas pesquisadas, 25 demos no ar, lista com mensagens"),
    ("8h47", "auto", "Empresas novas", "lista do dia: 2 ou 3 negócios locais registados"),
    ("9h–11h", "tu", "Enviar corrida A + empresas novas", "~27 mensagens pelo WhatsApp Business RO, com a mensagem nova dos 10 a 30 % de clientes"),
    ("11h22", "auto", "Caçador, corrida B", "as outras 25 demos e mensagens"),
    ("11h–13h", "tu", "Reels do D+2/D+3", "primeiro a quem abriu a demo (filtro do tracker)"),
    ("14h–17h", "tu", "Enviar corrida B + 2 auditorias", "~27 mensagens; nos fixos, ligar"),
    ("14h–17h", "tu", "Visitas e chamadas", "quem não tem WhatsApp, agrupados por zona; parceiros em Iași"),
    ("19h", "auto", "Relatório do tracker", "funil, novidades, quem abriu e não respondeu"),
    ("19h–20h", "tu", "Fechar o dia", "marcar estados no tracker, responder a quem respondeu, publicar reels com «DA»"),
]
SEMANAL = [
    ("Segunda 8h00", "Auditorias: lote novo de 10 PDFs (quando confirmares)"),
    ("Segunda 9h53", "Parceiros: 10 novos, lembretes aos 7 dias, comissões"),
    ("Seg e Qui 9h37", "Avaliações com queixas: lista nova com a queixa citada"),
    ("Sempre", "Ideias 5 e 9 (cartaz) trazem contactos sozinhas pelo site e pelo diagnóstico"),
]
AGENDA = [
    ("Sex 09/10", "1.ª corrida do caçador"),
    ("Seg 12/10", "1.ª rotina dos parceiros, 9h53"),
    ("Sex 16/10", "ATIPIC Internațional, Palas Congress Hall, 9h30 (grátis, inscrição antes)"),
    ("Ter 20 e Qua 21/10", "AI4IMPACT Week da DIZ (grátis, lugares limitados, inscrição)"),
    ("Qui 22 e Sex 23/10", "US–Romania Economic Forum: 22 Palatul Culturii, 23 Palas B2B"),
]
CONTAS = [
    ("50", "demos por dia útil"),
    ("~55", "mensagens tuas por dia"),
    ("~305", "contactos novos por semana"),
]
CONTAS_NOTA = ("Semana: 250 demos do caçador + 10 a 15 empresas novas + 10 auditorias "
               "+ 10 parceiros + ~24 queixas citadas ≈ 305 contactos. O limite é o tempo de envio: ~55 mensagens "
               "por dia (mais ~12 à segunda e à quinta), mais os reels e as chamadas.")
PENDENTES = [
    "Token do GoatCounter no GitHub (GOATCOUNTER_TOKEN) e que lotes já enviaste",
    "Comissão dos parceiros: «ok» aos 500 lei / 100 € ou outro valor",
    "Confirmar o lote de auditorias às segundas",
    "Instagram do Noir Barbershop",
    "Subir o zip leve novo (páginas por nicho e cartaz) e enviar o sitemap no Search Console",
    "Enviar as 12 mensagens das avaliações com queixas",
    "Mensagem à dona da Catarina (caso e 2 indicações)",
    "Inscrição na ATIPIC (16/10) e na AI4IMPACT (20–21/10)",
]

ESTADOS = {"ativo": ("A correr", "ok"), "pronto": ("Pronto, à espera de ti", "wait"),
           "curso": ("Em curso", "run")}

CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
:root { --ink:#16181d; --mut:#5d6370; --line:#e3e1db; --paper:#fbfaf7; --acc:#c8481f; --acc2:#1f4e5f; --soft:#f3efe7; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: 'Inter', sans-serif; color: var(--ink); background: var(--paper); font-size: 9.6pt; line-height: 1.42; }
.pg { width: 210mm; height: 297mm; padding: 15mm 16mm 13mm; position: relative; overflow: hidden; page-break-after: always; background: var(--paper); }
.pg:last-child { page-break-after: auto; }
.top { display:flex; justify-content:space-between; align-items:center; font-size:7.6pt; letter-spacing:.12em; text-transform:uppercase; color:var(--mut); border-bottom:1px solid var(--line); padding-bottom:3.2mm; }
.top b { color: var(--ink); font-weight:600; }
.hero { display:grid; grid-template-columns: 30mm 1fr; gap: 6mm; margin-top: 8mm; align-items:end; }
.num { font-family:'Inter Display', sans-serif; font-weight:800; font-size:64pt; line-height:.8; color: var(--acc); letter-spacing:-.04em; }
h1 { font-family:'Inter Display', sans-serif; font-weight:700; font-size:22pt; line-height:1.05; letter-spacing:-.02em; }
.sub { color: var(--mut); font-size:10.5pt; margin-top:2mm; }
.badge { display:inline-block; margin-top:3mm; font-size:7.4pt; font-weight:600; letter-spacing:.08em; text-transform:uppercase; padding:1.2mm 2.6mm; border-radius:20mm; }
.badge.ok { background:#dcefe3; color:#1d6b3d; } .badge.wait { background:#fbe6d6; color:#9a3d12; } .badge.run { background:#e3e8f2; color:#2c4a7c; }
h2 { font-size:7.8pt; letter-spacing:.14em; text-transform:uppercase; color: var(--acc2); font-weight:700; margin: 0 0 2.4mm; display:flex; align-items:center; gap:2.5mm; }
h2::after { content:''; flex:1; height:1px; background: var(--line); }
section { margin-top: 7mm; }
ul { list-style:none; } li { position:relative; padding-left: 4.2mm; margin-bottom: 1.8mm; }
li::before { content:''; position:absolute; left:0; top:1.9mm; width:1.8mm; height:1.8mm; background: var(--acc); border-radius:50%; }
.dia li::before { background: var(--acc2); border-radius:0; transform: rotate(45deg); }
.kpis { display:grid; grid-template-columns: repeat(3, 1fr); gap: 3mm; margin-bottom: 3.5mm; }
.kpi { background: var(--soft); border-radius: 2.5mm; padding: 3mm 3.5mm; }
.kpi .v { font-family:'Inter Display', sans-serif; font-weight:800; font-size:19pt; line-height:1; letter-spacing:-.02em; }
.kpi .l { font-size:7.8pt; color: var(--mut); margin-top:1.2mm; }
.tomas { position:absolute; left:16mm; right:16mm; bottom: 13mm; border:1.4px solid var(--ink); border-radius:2.5mm; padding: 3mm 4mm; font-size:9.2pt; }
.tomas b { font-size:7.4pt; letter-spacing:.12em; text-transform:uppercase; color: var(--acc); margin-right: 2mm; }
.curso { border:1.4px dashed #9aa6bd; border-radius:2.5mm; padding:4mm; color:#2c4a7c; background:#f2f4f9; }
/* capa da execução diária */
.tl { width:100%; border-collapse:collapse; font-size:8.9pt; }
.tl td { padding: 1.9mm 2mm; border-bottom:1px solid var(--line); vertical-align:top; }
.tl td.h { font-weight:700; white-space:nowrap; width:20mm; font-variant-numeric: tabular-nums; }
.tl td.q { width:13mm; } .tl td.o { color: var(--mut); }
.tag { font-size:6.8pt; font-weight:700; letter-spacing:.08em; text-transform:uppercase; padding:.6mm 1.6mm; border-radius:1mm; }
.tag.auto { background:#e3e8f2; color:#2c4a7c; } .tag.tu { background:#fbe6d6; color:#9a3d12; }
.cols { display:grid; grid-template-columns: 1fr 1fr; gap: 7mm; }
.mini td { padding:1.2mm 1.6mm; }
.pd section { margin-top:5mm; } .pd .tl td { padding:1.4mm 1.8mm; font-size:8.5pt; } .pd .hero { margin-top:5mm; } .pd .kpis { margin-bottom:2mm; } .pd .kpi { padding:2.2mm 3mm; } .pd li { margin-bottom:1.1mm; } .nota { font-size:8.2pt; color: var(--mut); margin-top:1mm; }
"""


def lista(itens, cls=""):
    return f'<ul class="{cls}">' + "".join(f"<li>{t}</li>" for t in itens) + "</ul>"


def pagina_ideia(i):
    est, cls = ESTADOS[i["estado"]]
    kp = ""
    if i["kpis"]:
        kp = '<div class="kpis">' + "".join(
            f'<div class="kpi"><div class="v">{v}</div><div class="l">{l}</div></div>' for v, l in i["kpis"]) + "</div>"
    res = lista(i["res"])
    if i["estado"] == "curso":
        res = f'<div class="curso">{lista(i["res"])}</div>'
    tomas = f'<div class="tomas"><b>De ti</b>{i["tomas"]}</div>' if i["tomas"] else ""
    return f"""
<div class="pg">
  <div class="top"><span><b>Pacheco Studios</b> · 10 ideias para leads</span><span>Ideia {i['n']:02d} / 10 · 08/10/2026</span></div>
  <div class="hero"><div class="num">{i['n']:02d}</div>
    <div><h1>{i['titulo']}</h1><div class="sub">{i['sub']}</div><span class="badge {cls}">{est}</span></div></div>
  <section><h2>Como se executa</h2>{lista(i['exec'])}</section>
  <section><h2>Resultado da 1.ª pesquisa</h2>{kp}{res}</section>
  <section><h2>Execução diária</h2>{lista(i['dia'], 'dia')}</section>
  {tomas}
</div>"""


def pagina_diaria():
    linhas = "".join(
        f'<tr><td class="h">{h}</td><td class="q"><span class="tag {q}">{"auto" if q=="auto" else "tu"}</span></td>'
        f'<td><b>{o}</b></td><td class="o">{d}</td></tr>' for h, q, o, d in DIA)
    sem = "".join(f'<tr><td class="h">{h}</td><td>{d}</td></tr>' for h, d in SEMANAL)
    ag = "".join(f'<tr><td class="h">{h}</td><td>{d}</td></tr>' for h, d in AGENDA)
    kp = '<div class="kpis">' + "".join(
        f'<div class="kpi"><div class="v">{v}</div><div class="l">{l}</div></div>' for v, l in CONTAS) + "</div>"
    pend = lista(PENDENTES)
    return f"""
<div class="pg pd">
  <div class="top"><span><b>Pacheco Studios</b> · 10 ideias para leads</span><span>Execução diária · seg–sex, hora de Iași</span></div>
  <div class="hero" style="grid-template-columns:1fr"><div><h1>O dia inteiro, com as novas abordagens</h1>
    <div class="sub">O que corre sozinho e o que fazes tu no telemóvel</div></div></div>
  <section><h2>Um dia útil</h2><table class="tl">{linhas}</table></section>
  <section><h2>As contas</h2>{kp}<div class="nota">{CONTAS_NOTA}</div></section>
  <div class="cols">
    <section><h2>Todas as semanas</h2><table class="tl mini">{sem}</table></section>
    <section><h2>Próximas duas semanas</h2><table class="tl mini">{ag}</table></section>
  </div>
  <section><h2>Pendente de ti para tudo arrancar</h2>{pend}</section>
</div>"""


def main():
    corpo = "".join(pagina_ideia(i) for i in IDEIAS) + pagina_diaria()
    doc = f'<!doctype html><html lang="pt-PT"><head><meta charset="utf-8"><title>10 ideias para leads</title><style>{CSS}</style></head><body>{corpo}</body></html>'
    src = AQUI / "plano-10-ideias.html"
    src.write_text(doc, encoding="utf-8")
    pdf = AQUI / "plano-10-ideias.pdf"
    subprocess.run([CHROMIUM, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf}", src.as_uri()], check=True, capture_output=True)
    print(pdf)


if __name__ == "__main__":
    main()
