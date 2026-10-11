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
    "influenciador": "DM com hipótese + Micro System Print de 1 página + 3 perguntas; fecho: triagem connosco",
    "grande": "Pedir encaminhamento para operações/CX/transformação; Micro System Print de 1 página + 3 perguntas; fecho: triagem connosco",
    "pme_parceiro": "Complementaridade: eles geram o lead, a Pacheco protege o que acontece depois; System Print de um cliente-tipo",
    "comunidade": "Comentário útil no post atual, 2–3 publicações; só depois DM com proposta editorial",
}

INTUITO = {
    "influenciador": "Triagem → entregar System Print → confiança → introduções consentidas",
    "grande": "Chegar ao dono do processo → reunião → Auditoria de Sistemas com IA",
    "pme_parceiro": "Co-entrega, introdução mútua ou workshop → referrals qualificados",
    "comunidade": "Familiaridade com a audiência → DM/introdução → conteúdo, evento ou referência",
}

TOM = {"influenciador": "informal", "grande": "formal", "pme_parceiro": "informal", "comunidade": "informal"}

MODELOS = {
    "ro": {
        "influenciador": (
            '{saud}, {nome}! Sunt Tomás, de la Pacheco Studios. {gancho} '
            'Lucrez pe partea operațională: ce se întâmplă după ce intră o cerere, cine o preia și unde se blochează. '
            'Am pregătit un Micro System Print de o pagină pentru propria operațiune ({percurso}): declanșator, responsabil, regulă și predare. '
            'Trei întrebări rapide: aveți azi o IA care răspunde la întrebările frecvente după regulile voastre? '
            'Sistemul vostru captează, califică și filtrează mesajele și vă cere decizia doar unde contează? '
            'Relația cu clienții vă costă mai puțin de o oră pe zi? '
            'Dacă la vreuna răspunsul e «nu», faceți o triere cu noi.'
        ),
        "grande": (
            '{saud}! Sunt Tomás, de la Pacheco Studios. {gancho} '
            'Am pregătit un Micro System Print de o pagină al unui parcurs public al {nome} ({percurso}), doar din ce se vede din afară: declanșator, responsabil, regulă și predare. '
            'E o ipoteză de validat, nu o concluzie. '
            'Trei întrebări: aveți azi o IA care răspunde la întrebările frecvente după regulile voastre? '
            'Sistemul vostru captează, califică și filtrează e-mailurile și cere decizia echipei doar unde contează? '
            'Relația cu clienții costă mai puțin de o oră pe zi? '
            'Cine din echipă se ocupă de operațiuni sau de experiența clienților? Faceți o triere cu noi.'
        ),
        "pme_parceiro": (
            '{saud}, {nome}! Sunt Tomás, de la Pacheco Studios. {gancho} '
            'Voi aduceți cererile; noi lucrăm pe ce se întâmplă după lead: cine răspunde, cum se califică și unde se ia decizia, '
            'ca rezultatul muncii voastre să nu se piardă pe drum. Nu concurăm cu ce faceți, completăm. '
            'Am pregătit un Micro System Print de o pagină pentru un client-tip de-al vostru ({percurso}). '
            'O întrebare pentru clienții voștri: sistemul lor captează, califică și filtrează mesajele și cere decizia omului doar unde contează? '
            'Dacă nu, faceți o triere cu noi și vedem împreună cum am putea lucra sau să ne recomandăm reciproc.'
        ),
        "comunidade": (
            "{saud}! Sunt Tomás, de la Pacheco Studios; am urmărit și am comentat la postările {nome}. {gancho} "
            "Lucrez cu firme pe procese și IA cu reguli clare: cine deține pasul următor după un lead "
            "și unde rămâne decizia umană. "
            "Aș putea contribui cu ceva practic pentru comunitate: un studiu de caz sau un mini-atelier. "
            "V-ar interesa?"
        ),
        "comentario": [
            "Întrebare practică: după {tema}, cine preia pasul următor și ce informație trebuie să ajungă la el?",
            "Interesant. La firmele cu care lucrez, partea grea nu e unealta, ci regula: cine decide și când intervine omul. Cum ați văzut asta la {tema}?",
            "Bun punct. Ce ar trebui măsurat în prima lună ca să știi că {tema} chiar funcționează?",
        ],
        "followup": (
            '{saud}, revin scurt la mesajul de mai sus. '
            'Micro System Print-ul rămâne pregătit; dacă vreți, faceți o triere cu noi când vă potrivește.'
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
            '{saud}, {nome}! Sou o Tomás, da Pacheco Studios. {gancho} '
            'Trabalho a parte operacional: o que acontece depois de entrar um pedido, quem o pega e onde encrava. '
            'Preparei um Micro System Print de 1 página da sua própria operação ({percurso}): gatilho, dono, regra e passagem. '
            'Três perguntas rápidas: hoje tem uma IA que responde às FAQ da sua diretriz? '
            'O seu sistema capta, qualifica e filtra os e-mails e só pede a sua decisão no que importa? '
            'O atendimento custa-lhe menos de 1 hora por dia? '
            'Se alguma resposta for «não», faça uma triagem connosco.'
        ),
        "grande": (
            '{saud}! Sou o Tomás, da Pacheco Studios. {gancho} '
            'Preparei um Micro System Print de 1 página de um percurso público da {nome} ({percurso}), só com o que se vê de fora: gatilho, dono, regra e passagem. '
            'É uma hipótese a validar, não uma conclusão. '
            'Três perguntas: hoje têm uma IA que responde às FAQ da vossa diretriz? '
            'O vosso sistema capta, qualifica e filtra os e-mails e só pede a decisão da equipa no que importa? '
            'O atendimento custa menos de 1 hora por dia? '
            'Quem na equipa trata de operações ou experiência de cliente? Façam uma triagem connosco.'
        ),
        "pme_parceiro": (
            '{saud}, {nome}! Sou o Tomás, da Pacheco Studios. {gancho} '
            'Vocês trazem os pedidos; nós trabalhamos o que acontece depois do lead: quem responde, como se qualifica e onde se decide, '
            'para o resultado do vosso trabalho não se perder pelo caminho. Não concorremos, complementamos. '
            'Preparei um Micro System Print de 1 página de um cliente-tipo vosso ({percurso}). '
            'Uma pergunta sobre os vossos clientes: o sistema deles capta, qualifica e filtra os e-mails e só pede a decisão no que importa? '
            'Se não, façam uma triagem connosco e vemos como trabalhar juntos ou indicar-nos mutuamente.'
        ),
        "comunidade": (
            "{saud}! Sou o Tomás, da Pacheco Studios; tenho acompanhado e comentado as publicações da {nome}. {gancho} "
            "Trabalho com empresas em processos e IA com regras claras: quem é dono do passo seguinte depois de um lead "
            "e onde fica a decisão humana. "
            "Podia contribuir com algo prático para a comunidade: um caso de estudo ou um mini-workshop. "
            "Interessa-vos?"
        ),
        "comentario": [
            "Pergunta prática: depois de {tema}, quem pega no passo seguinte e que informação tem de lhe chegar?",
            "Interessante. Nas empresas com quem trabalho, o difícil não é a ferramenta, é a regra: quem decide e quando entra a pessoa. Como viram isso em {tema}?",
            "Bom ponto. O que mediriam no primeiro mês para saber que {tema} está mesmo a funcionar?",
        ],
        "followup": (
            '{saud}, volto só à mensagem acima. '
            'O Micro System Print continua preparado; quando fizer sentido, faça uma triagem connosco.'
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
            'I work on the operational side: what happens after a request comes in, who picks it up and where it gets stuck. '
            'I prepared a one-page Micro System Print of your own operation ({percurso}): trigger, owner, rule and handoff. '
            'Three quick questions: do you have an AI today that answers FAQs following your own guidelines? '
            'Does your system capture, qualify and filter emails and only ask for your decision where it matters? '
            'Does customer service cost you less than an hour a day? '
            'If any answer is no, do a triage with us.'
        ),
        "grande": (
            "{saud}! I'm Tomás from Pacheco Studios. {gancho} "
            'I prepared a one-page Micro System Print of one public journey at {nome} ({percurso}), using only what is visible from outside: trigger, owner, rule and handoff. '
            'It is a hypothesis to validate, not a conclusion. '
            'Three questions: do you have an AI today that answers FAQs following your guidelines? '
            'Does your system capture, qualify and filter emails and only ask the team to decide where it matters? '
            'Does customer service cost less than an hour a day? '
            'Who on the team looks after operations or customer experience? Do a triage with us.'
        ),
        "pme_parceiro": (
            "{saud} {nome}! I'm Tomás from Pacheco Studios. {gancho} "
            'You bring in the demand; we work on what happens after the lead: who answers, how it is qualified and where decisions are made, '
            "so the result of your work isn't lost along the way. We don't compete, we complement. "
            'I prepared a one-page Micro System Print for one of your typical clients ({percurso}). '
            'One question about your clients: does their system capture, qualify and filter emails and only ask for a decision where it matters? '
            "If not, do a triage with us and let's see how we could co-deliver or refer each other."
        ),
        "comunidade": (
            "{saud}! I'm Tomás from Pacheco Studios; I've been following and commenting on {nome}'s posts. {gancho} "
            "I work with companies on processes and AI with clear rules: who owns the next step after a lead "
            "and where the human decision stays. "
            "I could contribute something practical for the community: a case study or a short mini-workshop. "
            "Would that be of interest?"
        ),
        "comentario": [
            "Practical question: after {tema}, who picks up the next step and what information has to reach them?",
            "Interesting. In the companies I work with, the hard part isn't the tool, it's the rule: who decides and when a human steps in. How did you see that with {tema}?",
            "Good point. What would you measure in the first month to know {tema} is actually working?",
        ],
        "followup": (
            '{saud}, just following up on the message above. '
            'The Micro System Print is still ready; whenever it makes sense, do a triage with us.'
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
