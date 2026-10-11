# Fonte única das mensagens, percursos e queries da prospeção no Instagram.
# gerar.py lê este ficheiro e produz o Excel, o MENSAGENS.md e o gerador HTML.
# Marcadores: {saudacao} {nome} {empresa} {gancho} {percurso} {pergunta} {tema} {valor}

CATEGORIAS = [
    {
        "id": "influenciador",
        "nome": "Influenciador / operador",
        "foco": "Parceria de prova e indicações qualificadas.",
        "perfil": "Founder, operador ou criador de negócio com menos de 50 mil seguidores, credível junto de donos de negócio e com operação própria.",
        "primeiro_passo": "DM personalizada a pedir uma conversa curta para mostrar o Partner Systems Opportunity Map.",
        "ativo": "Partner Systems Opportunity Map: 3 a 5 handoffs, uma hipótese de melhoria, um limite humano e uma prioridade de 30 dias.",
        "intuito": "Conversa curta → entregar o mapa → confiança → introduções consentidas a negócios com gargalo operacional.",
        "abordagem": "DM",
        "registo_ro": "tu",
        "excluir": "Criadores de entretenimento; contas sem @ verificável ou sem mercado; perfis cuja única razão é o número de seguidores.",
    },
    {
        "id": "grande",
        "nome": "Grande negócio",
        "foco": "Abrir uma oportunidade com o decisor funcional.",
        "perfil": "Operação multicanal com volume, vários handoffs e transformação ou serviço visível.",
        "primeiro_passo": "DM, e-mail ou LinkedIn a pedir encaminhamento para o dono de operações, CX ou transformação; levar mini-mapa.",
        "ativo": "Mini-mapa de uma página de um percurso público do cliente.",
        "intuito": "Encaminhamento para o dono do processo ou reunião de descoberta que converta numa AI Systems Audit.",
        "abordagem": "DM + LinkedIn do decisor",
        "registo_ro": "dumneavoastră",
        "excluir": "Sem operação de serviço ou percurso multietapa; contacto genérico quando já há decisor identificável; alegações de falha, risco ou ROI sem evidência.",
    },
    {
        "id": "pme_parceiro",
        "nome": "PME / parceiro de indicação",
        "foco": "Co-entrega ou referência mútua.",
        "perfil": "Agência, consultora, software ou serviço complementar com clientes B2B, equipa e processo.",
        "primeiro_passo": "Mensagem de complementaridade: uma operação típica onde a Pacheco protege o resultado que a agência já gera.",
        "ativo": "Mini-mapa de um fluxo conjunto ou de um cliente-tipo da agência.",
        "intuito": "Co-entrega, introdução mútua ou workshop; referrals qualificados e casos partilháveis.",
        "abordagem": "DM ao fundador",
        "registo_ro": "dumneavoastră",
        "excluir": "Concorrentes que vendem auditorias de sistemas de IA; parceiros sem clientes B2B reais; pedidos de parceria vagos.",
    },
    {
        "id": "comunidade",
        "nome": "Página / comunidade B2B",
        "foco": "Ganhar relevância perante uma audiência qualificada.",
        "perfil": "Evento, media, comunidade, aceleradora ou podcast que concentra founders, decisores e profissionais.",
        "primeiro_passo": "Comentário útil no post atual; 2 a 3 interações antes de pedir contacto.",
        "ativo": "Contribuição pública: observação ou pergunta prática ligada ao post.",
        "intuito": "Familiaridade perante a audiência → DM ou introdução → conteúdo, evento ou referência.",
        "abordagem": "Comentários, depois DM",
        "registo_ro": "tu",
        "excluir": "Páginas inativas ou sem audiência de negócio; comentários genéricos ou comerciais; DM antes de qualquer contribuição.",
    },
]

SAUDACOES = {
    "ro": {
        "tu": ["Bună, {nome}!", "Salut, {nome}!", "Bună ziua, {nome}!", "Bună seara, {nome}!"],
        "dumneavoastră": ["Bună ziua, {nome}!", "Bună ziua!", "Bună seara, {nome}!", "Bună dimineața, {nome}!"],
    },
    "pt": {
        "tu": ["Olá, {nome}!", "Boa tarde, {nome}!", "Bom dia, {nome}!", "Olá {nome}, tudo bem?"],
        "dumneavoastră": ["Bom dia, {nome}.", "Boa tarde, {nome}.", "Olá, {nome}.", "Boa tarde."],
    },
    "en": {
        "tu": ["Hi {nome},", "Hey {nome},", "Hello {nome},", "Good afternoon {nome},"],
        "dumneavoastră": ["Hello {nome},", "Good morning {nome},", "Good afternoon {nome},", "Hello,"],
    },
}

# Fecho obrigatório em romeno; PT e EN com equivalente.
FECHO = {"ro": "Voi fi pregătit.", "pt": "Vou estar preparado.", "en": "I'll come prepared."}

MENSAGENS = {
    "influenciador": {
        "ro": {
            "dm1": "{saudacao} Sunt Tomás, de la Pacheco Studios, din Iași. Am văzut {gancho} și m-am gândit la partea din spate a operațiunii tale: {percurso}. Am pregătit ceva util pentru tine, fără cost: o hartă scurtă cu 3–5 predări între oameni și sisteme, o ipoteză de îmbunătățire, punctul unde decide un om și prioritatea pentru următoarele 30 de zile. Întrebarea de la care pornesc: {pergunta} Ai fi deschis la o scurtă întâlnire ca să ți-o arăt? {fecho}",
            "fu": "{saudacao} Revin pe scurt, cu un lucru concret: {valor} Harta rămâne pregătită pentru tine, fără nicio obligație. Dacă acum nu e momentul, înțeleg perfect. {fecho}",
        },
        "pt": {
            "dm1": "{saudacao} Sou o Tomás, da Pacheco Studios. Vi {gancho} e fiquei a pensar na parte de trás da tua operação: {percurso}. Preparei uma coisa útil para ti, sem custo: um mapa curto com 3 a 5 passagens entre pessoas e sistemas, uma hipótese de melhoria, o ponto onde decide uma pessoa e a prioridade para os próximos 30 dias. A pergunta de onde parto: {pergunta} Estarias aberto a uma conversa curta para te mostrar? {fecho}",
            "fu": "{saudacao} Volto só com uma coisa concreta: {valor} O mapa continua preparado para ti, sem compromisso. Se agora não é o momento, percebo perfeitamente. {fecho}",
        },
        "en": {
            "dm1": "{saudacao} I'm Tomás from Pacheco Studios. I saw {gancho} and started thinking about the back end of your operation: {percurso}. I put together something useful for you, at no cost: a short map with 3 to 5 handoffs between people and systems, one improvement hypothesis, the point where a human decides, and a 30-day priority. The question I start from: {pergunta} Would you be open to a short call so I can walk you through it? {fecho}",
            "fu": "{saudacao} A quick follow-up with one concrete thing: {valor} The map is still ready for you, no strings attached. If now isn't the right time, completely understood. {fecho}",
        },
    },
    "grande": {
        "ro": {
            "dm1": "{saudacao} Sunt Tomás, de la Pacheco Studios, din Iași. Am parcurs traseul public al unui client {empresa}: {percurso}. Pe baza a ceea ce este public, am o ipoteză de diagnostic, nu o concluzie: {pergunta} Am pus-o pe o mini-hartă de o pagină. Cu cine din echipă ar fi potrivit să o validez: operațiuni, experiența clienților sau transformare digitală? O întâlnire scurtă de explorare ar fi suficientă. {fecho}",
            "fu": "{saudacao} Revin cu mini-harta despre traseul clientului {empresa}. Am adăugat un singur punct: {valor} Dacă îmi puteți indica persoana potrivită, îi trimit direct harta. {fecho}",
        },
        "pt": {
            "dm1": "{saudacao} Sou o Tomás, da Pacheco Studios. Percorri o percurso público de um cliente {empresa}: {percurso}. Com base no que é público, tenho uma hipótese de diagnóstico, não uma conclusão: {pergunta} Pus isto num mini-mapa de uma página. Quem na equipa seria a pessoa certa para o validar: operações, experiência do cliente ou transformação digital? Uma conversa exploratória curta chega. {fecho}",
            "fu": "{saudacao} Volto ao mini-mapa sobre o percurso do cliente {empresa}. Acrescentei um único ponto: {valor} Se me puderem indicar a pessoa certa, envio-lhe o mapa diretamente. {fecho}",
        },
        "en": {
            "dm1": "{saudacao} I'm Tomás from Pacheco Studios. I walked through the public journey of a {empresa} customer: {percurso}. Based only on what's public, I have a diagnostic hypothesis, not a conclusion: {pergunta} I've put it on a one-page mini-map. Who on the team would be the right person to validate it: operations, customer experience or digital transformation? A short exploratory call would be enough. {fecho}",
            "fu": "{saudacao} Following up on the mini-map of the {empresa} customer journey. I added one point: {valor} If you can point me to the right person, I'll send the map to them directly. {fecho}",
        },
    },
    "pme_parceiro": {
        "ro": {
            "dm1": "{saudacao} Sunt Tomás, de la Pacheco Studios, din Iași. Am văzut {gancho}. Voi aduceți cererea; noi lucrăm în stratul de după lead: cum ajunge cererea la echipă, ce context o însoțește, cine decide și cum se livrează. Nu înlocuim marketingul sau brandingul, protejăm rezultatul pe care îl generați deja. Am schițat o mini-hartă pentru un client tipic de-al vostru: {percurso}. Ați fi deschis la o întâlnire ca să vedem dacă are sens să lucrăm împreună? {fecho}",
            "fu": "{saudacao} Revin cu un exemplu concret de colaborare: {valor} Voi păstrați relația și serviciul, noi intrăm doar pe partea operațională. {fecho}",
        },
        "pt": {
            "dm1": "{saudacao} Sou o Tomás, da Pacheco Studios. Vi {gancho}. Vocês trazem a procura; nós trabalhamos na camada depois do lead: como o pedido chega à equipa, que contexto leva, quem decide e como se entrega. Não substituímos o marketing nem a marca, protegemos o resultado que vocês já geram. Esbocei um mini-mapa para um cliente típico vosso: {percurso}. Estariam abertos a uma reunião para ver se faz sentido trabalharmos juntos? {fecho}",
            "fu": "{saudacao} Volto com um exemplo concreto de colaboração: {valor} Vocês mantêm a relação e o serviço, nós entramos só na parte operacional. {fecho}",
        },
        "en": {
            "dm1": "{saudacao} I'm Tomás from Pacheco Studios. I saw {gancho}. You bring in the demand; we work on the layer after the lead: how the request reaches the team, what context travels with it, who decides and how it gets delivered. We don't replace marketing or branding, we protect the result you already generate. I sketched a mini-map for one of your typical clients: {percurso}. Would you be open to a meeting to see whether it makes sense to work together? {fecho}",
            "fu": "{saudacao} Following up with one concrete collaboration example: {valor} You keep the relationship and the service; we only step into the operational side. {fecho}",
        },
    },
    "comunidade": {
        "ro": {
            "c1": "Punctul despre {tema} mi se pare esențial. În operațiunile pe care le analizez, întrebarea care schimbă cel mai mult este: {pergunta}",
            "c2": "Bună observație. Aș adăuga un detaliu din practică: {valor}",
            "c3": "O întrebare sinceră pentru cei care au trecut prin asta: {pergunta}",
            "dm1": "{saudacao} Sunt Tomás, de la Pacheco Studios, din Iași. Am comentat în ultimele săptămâni la postările voastre despre {tema}. Lucrez pe sisteme cu AI pentru operațiuni: unde stă contextul, cine răspunde de pasul următor și unde decide un om. Cred că publicul vostru ar găsi util un subiect ca acesta: {gancho}, ca articol, workshop scurt sau discuție la un eveniment. Ați fi deschis la o întâlnire scurtă? {fecho}",
            "fu": "{saudacao} Revin cu propunerea de subiect, acum mai concretă: {valor} Mă adaptez formatului care vă ajută cel mai mult. {fecho}",
        },
        "pt": {
            "c1": "O ponto sobre {tema} parece-me essencial. Nas operações que analiso, a pergunta que mais muda o resultado é: {pergunta}",
            "c2": "Boa observação. Acrescentava um detalhe da prática: {valor}",
            "c3": "Uma pergunta sincera para quem já passou por isto: {pergunta}",
            "dm1": "{saudacao} Sou o Tomás, da Pacheco Studios. Tenho comentado nas vossas publicações sobre {tema}. Trabalho em sistemas com IA para operações: onde fica o contexto, quem é dono do próximo passo e onde decide uma pessoa. Acho que a vossa audiência ia achar útil um tema como este: {gancho}, em artigo, workshop curto ou conversa num evento. Estariam abertos a uma reunião curta? {fecho}",
            "fu": "{saudacao} Volto à proposta de tema, agora mais concreta: {valor} Adapto-me ao formato que mais vos ajudar. {fecho}",
        },
        "en": {
            "c1": "The point about {tema} is key. In the operations I map, the question that changes the most is: {pergunta}",
            "c2": "Good point. One detail from practice I'd add: {valor}",
            "c3": "An honest question for anyone who's been through this: {pergunta}",
            "dm1": "{saudacao} I'm Tomás from Pacheco Studios. I've been commenting on your posts about {tema}. I work on AI systems for operations: where context lives, who owns the next step and where a human decides. I think your audience would find a topic like this useful: {gancho}, as an article, a short workshop or a talk at an event. Would you be open to a short meeting? {fecho}",
            "fu": "{saudacao} Following up on the topic idea, now more concrete: {valor} Happy to fit whatever format helps you most. {fecho}",
        },
    },
}

# Percursos tipo: o ponto de partida da análise. Editar sempre com o que a conta mostra.
PERCURSOS = [
    {"tipo": "Hotel / alojamento", "ro": "cerere de rezervare pe Instagram sau site → verificare disponibilitate → ofertă → plată → check-in → recenzie", "pt": "pedido de reserva no Instagram ou site → ver disponibilidade → proposta → pagamento → check-in → avaliação", "en": "booking request via Instagram or site → availability check → offer → payment → check-in → review",
     "pergunta": {"ro": "Ce context trebuie să ajungă de la mesajul inițial la recepție, ca oaspetele să nu repete totul?", "pt": "Que contexto tem de chegar da primeira mensagem à receção para o hóspede não repetir tudo?", "en": "What context has to travel from the first message to the front desk so the guest doesn't repeat everything?"}},
    {"tipo": "Clínica / várias unidades", "ro": "mesaj sau apel → triere → programare în unitatea potrivită → consultație → plan de tratament → revenire", "pt": "mensagem ou chamada → triagem → marcação na unidade certa → consulta → plano de tratamento → regresso", "en": "message or call → triage → booking at the right location → appointment → treatment plan → return visit",
     "pergunta": {"ro": "Cine decide unitatea și ora potrivită, și ce informație administrativă trebuie să aibă la momentul acela?", "pt": "Quem decide a unidade e a hora certas, e que informação administrativa precisa de ter nesse momento?", "en": "Who decides the right location and slot, and what administrative information do they need at that moment?"}},
    {"tipo": "Ginásio / estúdio", "ro": "întrebare pe DM → ședință de probă → abonament → plan de antrenament → prezență → reînnoire", "pt": "pergunta por DM → aula experimental → inscrição → plano de treino → presença → renovação", "en": "DM inquiry → trial session → membership → training plan → attendance → renewal",
     "pergunta": {"ro": "Cine observă primul că un membru nu mai vine și ce urmează după acel semnal?", "pt": "Quem repara primeiro que um membro deixou de vir e o que acontece depois desse sinal?", "en": "Who notices first that a member has stopped coming, and what happens after that signal?"}},
    {"tipo": "Restaurante / hospitality", "ro": "rezervare sau cerere de eveniment → confirmare → detalii (meniu, alergii, număr) → servire → feedback", "pt": "reserva ou pedido de evento → confirmação → detalhes (menu, alergias, número) → serviço → feedback", "en": "reservation or event request → confirmation → details (menu, allergies, headcount) → service → feedback",
     "pergunta": {"ro": "Unde stă informația despre un eveniment privat între primul mesaj și seara în care are loc?", "pt": "Onde fica a informação de um evento privado entre a primeira mensagem e a noite em que acontece?", "en": "Where does the information about a private event live between the first message and the night it happens?"}},
    {"tipo": "Imobiliária", "ro": "lead din anunț → calificare → vizionare → ofertă → acte → predare", "pt": "lead do anúncio → qualificação → visita → proposta → documentação → entrega", "en": "listing lead → qualification → viewing → offer → paperwork → handover",
     "pergunta": {"ro": "Ce criterii decid ce lead primește prima vizionare și cine le aplică?", "pt": "Que critérios decidem que lead tem a primeira visita e quem os aplica?", "en": "What criteria decide which lead gets the first viewing, and who applies them?"}},
    {"tipo": "E-commerce / retalho com app", "ro": "comandă (site, app, magazin) → confirmare → pregătire → livrare → suport → retur", "pt": "encomenda (site, app, loja) → confirmação → preparação → entrega → apoio → devolução", "en": "order (site, app, store) → confirmation → picking → delivery → support → return",
     "pergunta": {"ro": "Când un client scrie la suport, ce context despre comandă are deja echipa în față?", "pt": "Quando um cliente escreve ao apoio, que contexto da encomenda a equipa já tem à frente?", "en": "When a customer contacts support, what order context does the team already have in front of them?"}},
    {"tipo": "Agência de marketing / web", "ro": "lead generat pentru client → răspuns → calificare → ofertă → livrare → raportare", "pt": "lead gerado para o cliente → resposta → qualificação → proposta → entrega → relatório", "en": "lead generated for the client → response → qualification → proposal → delivery → reporting",
     "pergunta": {"ro": "Ce se întâmplă cu un lead bun în primele ore după ce ajunge la clientul vostru?", "pt": "O que acontece a um bom lead nas primeiras horas depois de chegar ao vosso cliente?", "en": "What happens to a good lead in the first hours after it reaches your client?"}},
    {"tipo": "Consultora / software B2B", "ro": "cerere de demo → calificare → ofertă → onboarding → suport → extindere", "pt": "pedido de demo → qualificação → proposta → onboarding → apoio → expansão", "en": "demo request → qualification → proposal → onboarding → support → expansion",
     "pergunta": {"ro": "Ce informație din vânzare ajunge la echipa de onboarding și ce trebuie cerut din nou clientului?", "pt": "Que informação da venda chega à equipa de onboarding e o que tem de ser pedido de novo ao cliente?", "en": "What information from the sale reaches the onboarding team, and what has to be asked again?"}},
    {"tipo": "Evento / comunidade", "ro": "înscriere → selecție → confirmare → participare → follow-up → următorul eveniment", "pt": "inscrição → seleção → confirmação → participação → follow-up → próximo evento", "en": "registration → selection → confirmation → attendance → follow-up → next event",
     "pergunta": {"ro": "Ce se întâmplă cu contactele făcute la eveniment în săptămâna de după?", "pt": "O que acontece aos contactos feitos no evento na semana seguinte?", "en": "What happens to the connections made at the event in the following week?"}},
    {"tipo": "Criador / founder com operação", "ro": "mesaj de la public → calificare → apel sau ofertă → livrare (curs, consultanță, produs) → comunitate", "pt": "mensagem do público → qualificação → chamada ou proposta → entrega (curso, consultoria, produto) → comunidade", "en": "message from audience → qualification → call or offer → delivery (course, consulting, product) → community",
     "pergunta": {"ro": "Ce mesaje din DM merită un om, care pot primi un răspuns standard, și cine decide diferența?", "pt": "Que mensagens por DM merecem uma pessoa, quais podem ter resposta padrão, e quem decide a diferença?", "en": "Which DMs deserve a human, which can get a standard reply, and who decides the difference?"}},
]

QUERIES = [
    ("Influenciador / operador", "Romanian entrepreneur · Romanian founder · business podcast Romania · hospitality Bucharest · antreprenor · fondator · afaceri · podcast antreprenori · antreprenor Iași"),
    ("Grande negócio", "Romania customer experience digital transformation · Romania omnichannel retail app delivery · Romania logistics operations AI · clinică Iași · rezervări Iași · lanț magazine Iași"),
    ("PME / parceiro", "Romania performance marketing agency · agenție SEO România · B2B digital agency Bucharest · Romania CRM consultancy · agenție marketing Iași · GEO agency · growth agency"),
    ("Página / comunidade", "AI conference Romania · startup community Romania · tech event Bucharest · antreprenori podcast · business community Romania · evenimente Iași · comunitate antreprenori Iași"),
]

TERMOS = [
    ("Inglês", "booking, inquiry, customer support, delivery, operations, partners, CRM, appointments, member, application, onboarding, marketplace, events"),
    ("Romeno", "programări, rezervări, cereri, clienți, livrare, suport, operațiuni, parteneri, aplicație, înscrieri, antreprenori, servicii"),
    ("Sinais de sistema", "app, portal, loyalty, membership, locations, franchise, academy, team, case study, automation, AI, digital transformation"),
]

ESTADOS = [
    ("Descoberto", "Entrou na lista longa; ainda sem validação suficiente."),
    ("Em validação", "Fontes e decisor/canal a confirmar."),
    ("Validado", "Tem @ correto, mercado, encaixe, evidência e abordagem."),
    ("Mini-mapa em preparação", "Selecionado para receber hipótese visual personalizada."),
    ("Contactado", "Primeira mensagem enviada; follow-up com data."),
    ("Resposta", "Houve interação; registar contexto e próximo passo."),
    ("Reunião marcada", "Conversa com data, objetivo e responsável."),
    ("Não adequado", "Sem mercado, acesso, operação, timing ou interesse; registar motivo."),
    ("Sem resposta", "Depois do follow-up; pausar sem insistir."),
]

EVITAR = [
    ("Há uma questão operacional que vale a pena mapear.", "Vimos que o vosso processo está a falhar."),
    ("Hipótese de diagnóstico baseada no percurso público.", "Sabemos onde estão a perder dinheiro."),
    ("Onde deve ficar o contexto, o dono e a regra de decisão?", "A IA resolve tudo automaticamente."),
    ("Vamos validar antes de sugerir ferramenta.", "Temos uma automação pronta para instalar."),
]
