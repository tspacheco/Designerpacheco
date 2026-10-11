"""Mensagens de abordagem por categoria do guia de prospeção (10/10/2026).

Cada conta traz dois campos escritos à mão na análise, já na língua da conta:
  gancho   — uma frase sobre algo público e concreto da conta (post, app, evento, clientes)
  percurso — o percurso a validar, curto (ex.: "cerere → programare → echipă")
O resto vem dos modelos abaixo. Regra do guia: hipótese a validar, nunca acusação.
Regra do Tomás: em romeno, todas as mensagens fecham com «Voi fi pregătit.»
"""

SAUDACOES = {
    "ro": {"formal": ["Bună ziua"], "informal": ["Salut", "Bună", "Bună ziua"]},
    "pt": {"formal": ["Bom dia", "Olá", "Boa tarde"], "informal": ["Olá", "Boas", "Olá"]},
    "en": {"formal": ["Hello", "Hi", "Good morning"], "informal": ["Hi", "Hey", "Hello"]},
}

FECHO = {"ro": "Voi fi pregătit.", "pt": "", "en": ""}

# Canal da 1.ª acção por categoria (guia, passo 5)
CANAL = {
    "influenciador": "DM",
    "grande": "E-mail",       # sem e-mail público → LinkedIn ou DM a pedir encaminhamento
    "pme_parceiro": "E-mail", # sem e-mail público → DM
    "comunidade": "Comentário",
}

ABORDAGEM = {
    "influenciador": "DM personalizada: 20 min para mostrar o System Print da operação dele (trigger, dono, regra, handoff)",
    "grande": "Pedir encaminhamento para operações/CX/transformação; levar o System Print de um percurso público; convidar para a Auditoria de Sistemas com IA",
    "pme_parceiro": "Complementaridade: eles geram o lead, a Pacheco protege o que acontece depois; System Print de um cliente-tipo",
    "comunidade": "Comentário útil no post atual, 2–3 publicações; só depois DM com proposta editorial",
}

INTUITO = {
    "influenciador": "Chamada de 20 min → entregar System Print → confiança → introduções consentidas",
    "grande": "Chegar ao dono do processo → reunião → Auditoria de Sistemas com IA",
    "pme_parceiro": "Co-entrega, introdução mútua ou workshop → referrals qualificados",
    "comunidade": "Familiaridade com a audiência → DM/introdução → conteúdo, evento ou referência",
}

TOM = {"influenciador": "informal", "grande": "formal", "pme_parceiro": "informal", "comunidade": "informal"}

MODELOS = {
    "ro": {
        "influenciador": (
            "{saud}, {nome}! Sunt Tomás, de la Pacheco Studios. {gancho} "
            "Lucrez pe partea operațională a afacerilor: ce se întâmplă după ce intră o cerere, "
            "cine o preia și ce context ajunge la următorul om. "
            "Aș vrea să vă arăt un System Print al propriei operațiuni ({percurso}): ce declanșează fiecare pas, cine îl deține, "
            "ce regulă decide și unde se face predarea între oameni, plus o prioritate pe 30 de zile. "
            "Ați avea 20 de minute să v-o arăt?"
        ),
        "grande": (
            "{saud}! Sunt Tomás, de la Pacheco Studios. {gancho} "
            "Am pregătit un System Print al unui parcurs public al {nome} ({percurso}), doar din ce se vede din afară: declanșator, responsabil, regulă și predare. "
            "E o ipoteză de validat, nu o concluzie: ce context trebuie să meargă cu fiecare cerere "
            "și cine deține pasul următor. "
            "Cine din echipă se ocupă de operațiuni sau de experiența clienților? "
            "Aș vrea să i-l arăt într-o întâlnire scurtă despre unde se pierd lead-urile, deciziile și livrarea."
        ),
        "pme_parceiro": (
            "{saud}, {nome}! Sunt Tomás, de la Pacheco Studios. {gancho} "
            "Voi aduceți cererile; noi lucrăm pe ce se întâmplă după lead: date, echipă, decizii și livrare, "
            "ca rezultatul muncii voastre să nu se piardă pe drum. Nu concurăm cu ce faceți, completăm. "
            "Vă pot arăta un System Print pentru un client-tip de-al vostru ({percurso}) "
            "și cum am putea lucra împreună sau să ne recomandăm reciproc. "
            "Ați fi deschiși la o discuție scurtă?"
        ),
        "comunidade": (
            "{saud}! Sunt Tomás, de la Pacheco Studios; am urmărit și am comentat la postările {nome}. {gancho} "
            "Lucrez cu firme pe procese și IA cu reguli clare: cine deține pasul următor după un lead "
            "și unde rămâne decizia umană. "
            "Aș putea contribui cu ceva practic pentru comunitate: un studiu de caz sau un mini-atelier de 30 de minute. "
            "V-ar interesa?"
        ),
        "comentario": [
            "Întrebare practică: după {tema}, cine preia pasul următor și ce informație trebuie să ajungă la el?",
            "Interesant. La firmele cu care lucrez, partea grea nu e unealta, ci regula: cine decide și când intervine omul. Cum ați văzut asta la {tema}?",
            "Bun punct. Ce ar trebui măsurat în prima lună ca să știi că {tema} chiar funcționează?",
        ],
        "followup": (
            "{saud}, revin scurt la mesajul de mai sus pentru {nome}. "
            "Dacă nu e momentul potrivit, nicio problemă; System Print-ul rămâne disponibil oricând."
        ),
        "assunto": {
            "influenciador": "System Print pentru operațiunea {nome}",
            "grande": "{nome}: unde se pot pierde lead-urile și deciziile",
            "pme_parceiro": "{nome} × Pacheco Studios: colaborare",
            "comunidade": "Contribuție pentru comunitatea {nome}",
        },
        "rodape": "Tomás Pacheco · Pacheco Studios · ro.pachecost.com · WhatsApp +40 723 098 556\n"
                  "Dacă nu doriți alte mesaje, răspundeți «STOP» și nu vă mai scriu.",
    },
    "pt": {
        "influenciador": (
            "{saud}, {nome}! Sou o Tomás, da Pacheco Studios. {gancho} "
            "Trabalho a parte operacional dos negócios: o que acontece depois de entrar um pedido, "
            "quem o pega e que contexto chega à pessoa seguinte. "
            "Queria mostrar-lhe um System Print da sua própria operação ({percurso}): o que dispara cada passo, quem é o dono, "
            "que regra decide e onde há passagem entre pessoas, mais uma prioridade a 30 dias. "
            "Tem 20 minutos para eu lho mostrar?"
        ),
        "grande": (
            "{saud}! Sou o Tomás, da Pacheco Studios. {gancho} "
            "Preparei um System Print de um percurso público da {nome} ({percurso}), só com o que se vê de fora: gatilho, dono, regra e passagem. "
            "É uma hipótese a validar, não uma conclusão: que contexto tem de viajar com cada pedido "
            "e quem é dono do passo seguinte. "
            "Quem na equipa trata de operações ou experiência de cliente? "
            "Gostava de o mostrar numa reunião curta sobre onde os leads, as decisões e a entrega se partem."
        ),
        "pme_parceiro": (
            "{saud}, {nome}! Sou o Tomás, da Pacheco Studios. {gancho} "
            "Vocês trazem os pedidos; nós trabalhamos o que acontece depois do lead: dados, equipa, decisões e entrega, "
            "para o resultado do vosso trabalho não se perder pelo caminho. Não concorremos, complementamos. "
            "Posso mostrar-vos um System Print de um cliente-tipo vosso ({percurso}) "
            "e como podíamos trabalhar juntos ou indicar-nos mutuamente. "
            "Estão abertos a uma conversa curta?"
        ),
        "comunidade": (
            "{saud}! Sou o Tomás, da Pacheco Studios; tenho acompanhado e comentado as publicações da {nome}. {gancho} "
            "Trabalho com empresas em processos e IA com regras claras: quem é dono do passo seguinte depois de um lead "
            "e onde fica a decisão humana. "
            "Podia contribuir com algo prático para a comunidade: um caso de estudo ou um mini-workshop de 30 minutos. "
            "Interessa-vos?"
        ),
        "comentario": [
            "Pergunta prática: depois de {tema}, quem pega no passo seguinte e que informação tem de lhe chegar?",
            "Interessante. Nas empresas com quem trabalho, o difícil não é a ferramenta, é a regra: quem decide e quando entra a pessoa. Como viram isso em {tema}?",
            "Bom ponto. O que mediriam no primeiro mês para saber que {tema} está mesmo a funcionar?",
        ],
        "followup": (
            "{saud}, volto só à mensagem acima sobre a {nome}. "
            "Se não for o momento, sem problema; o System Print fica disponível quando quiser."
        ),
        "assunto": {
            "influenciador": "System Print para a operação da {nome}",
            "grande": "{nome}: onde os leads e as decisões se podem perder",
            "pme_parceiro": "{nome} × Pacheco Studios: parceria",
            "comunidade": "Contributo para a comunidade {nome}",
        },
        "rodape": "Tomás Pacheco · Pacheco Studios · pachecost.com · WhatsApp +351 967 117 357\n"
                  "Se não quiser receber mais mensagens, responda «STOP» e não volto a escrever.",
    },
    "en": {
        "influenciador": (
            "{saud} {nome}! I'm Tomás from Pacheco Studios. {gancho} "
            "I work on the operational side of businesses: what happens after a request comes in, "
            "who picks it up and what context reaches the next person. "
            "I'd like to show you a System Print of your own operation ({percurso}): what triggers each step, who owns it, "
            "which rule decides and where the handoff happens, plus a 30-day priority. "
            "Would you have 20 minutes for me to walk you through it?"
        ),
        "grande": (
            "{saud}! I'm Tomás from Pacheco Studios. {gancho} "
            "I prepared a System Print of one public journey at {nome} ({percurso}), using only what is visible from outside: trigger, owner, rule and handoff. "
            "It is a hypothesis to validate, not a conclusion: what context has to travel with each request "
            "and who owns the next step. "
            "Who on the team looks after operations or customer experience? "
            "I'd like to walk them through it in a short meeting about where leads, decisions and delivery break."
        ),
        "pme_parceiro": (
            "{saud} {nome}! I'm Tomás from Pacheco Studios. {gancho} "
            "You bring in the demand; we work on what happens after the lead: data, team, decisions and delivery, "
            "so the result of your work isn't lost along the way. We don't compete, we complement. "
            "I can show you a System Print for one of your typical clients ({percurso}) "
            "and how we could co-deliver or refer each other. "
            "Open to a short call?"
        ),
        "comunidade": (
            "{saud}! I'm Tomás from Pacheco Studios; I've been following and commenting on {nome}'s posts. {gancho} "
            "I work with companies on processes and AI with clear rules: who owns the next step after a lead "
            "and where the human decision stays. "
            "I could contribute something practical for the community: a case study or a 30-minute mini-workshop. "
            "Would that be of interest?"
        ),
        "comentario": [
            "Practical question: after {tema}, who picks up the next step and what information has to reach them?",
            "Interesting. In the companies I work with, the hard part isn't the tool, it's the rule: who decides and when a human steps in. How did you see that with {tema}?",
            "Good point. What would you measure in the first month to know {tema} is actually working?",
        ],
        "followup": (
            "{saud}, just following up on the message above about {nome}. "
            "If the timing isn't right, no problem; the System Print stays available whenever you want it."
        ),
        "assunto": {
            "influenciador": "A System Print for {nome}'s operation",
            "grande": "{nome}: where leads and decisions can break",
            "pme_parceiro": "{nome} × Pacheco Studios: partnership",
            "comunidade": "A contribution for the {nome} community",
        },
        "rodape": "Tomás Pacheco · Pacheco Studios · pachecost.com\n"
                  "If you'd rather not hear from me again, reply \"STOP\".",
    },
}


def _saud(lingua, categoria, i, tom=None):
    lista = SAUDACOES[lingua][tom or TOM[categoria]]
    return lista[i % len(lista)]


def _fechar(texto, lingua):
    fecho = FECHO[lingua]
    return (texto + " " + fecho).strip() if fecho else texto


def canal(conta):
    c = CANAL[conta["categoria"]]
    if c == "E-mail" and not conta.get("email"):
        return "DM" if conta.get("instagram") else "LinkedIn"
    return c


def mensagem(conta, i=0):
    """Mensagem principal (DM ou corpo do e-mail) para uma conta."""
    lingua = conta.get("lingua") or "ro"
    cat = conta["categoria"]
    m = MODELOS[lingua]
    texto = m[cat].format(
        saud=_saud(lingua, cat, i, conta.get("tom")),
        nome=conta.get("nome_curto") or conta["nome"],
        gancho=(conta.get("gancho") or "").strip(),
        percurso=conta.get("percurso") or conta.get("foco") or "",
    )
    texto = " ".join(texto.split())
    return _fechar(texto, lingua)


def comentarios(conta):
    """Para comunidades: 3 arranques de comentário; {tema} = tema do post do dia."""
    lingua = conta.get("lingua") or "ro"
    return [c.format(tema=conta.get("tema") or "…") for c in MODELOS[lingua]["comentario"]]


def assunto(conta):
    lingua = conta.get("lingua") or "ro"
    return MODELOS[lingua]["assunto"][conta["categoria"]].format(nome=conta.get("nome_curto") or conta["nome"])


def email(conta, i=0):
    lingua = conta.get("lingua") or "ro"
    return mensagem(conta, i) + "\n\n" + MODELOS[lingua]["rodape"]


def followup(conta, i=1):
    lingua = conta.get("lingua") or "ro"
    cat = conta["categoria"]
    texto = MODELOS[lingua]["followup"].format(
        saud=_saud(lingua, cat, i, conta.get("tom")), nome=conta.get("nome_curto") or conta["nome"])
    return _fechar(texto, lingua)


if __name__ == "__main__":
    exemplo = {"categoria": "pme_parceiro", "nome": "Agenția X", "lingua": "ro",
               "gancho": "Am văzut studiul de caz cu clinica din Iași.", "percurso": "lead → ofertă → programare"}
    print(mensagem(exemplo))
    print(assunto(exemplo))
    print(followup(exemplo))
