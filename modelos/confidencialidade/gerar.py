#!/usr/bin/env python3
"""Gera o acordo de confidencialidade mútuo (RO, PT, EN) em HTML e PDF A4.

Uso: python3 gerar.py            -> HTML + PDF em saida/
     python3 gerar.py --png      -> também PNG por página (pré-visualização)

Os campos a preencher à mão estão marcados no texto como [[rótulo|largura]].
"""
import html
import re
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
SAIDA = AQUI / "saida"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

TEXTOS = {
    "ro": {
        "ficheiro": "acord-confidentialitate-ro",
        "titulo": "Acord de confidențialitate",
        "sub": "reciproc",
        "partes_intro": "Încheiat între:",
        "parte_a": (
            "<b>Pacheco Studios</b>, reprezentată de <b>Tomás Pacheco</b>, "
            "CUI / NIF [[CUI / NIF|11em]], cu sediul în [[adresă|20em]] "
            "(„<b>Pacheco Studios</b>”);"
        ),
        "parte_b": (
            "[[denumirea firmei|22em]], CUI [[CUI|9em]], nr. Registrul Comerțului "
            "[[J__/____/____|9em]], cu sediul în [[adresă|20em]], reprezentată de "
            "[[nume|14em]], în calitate de [[funcție|9em]] („<b>Clientul</b>”),"
        ),
        "partes_fim": "denumite împreună „Părțile” și separat „Partea”.",
        "clausulas": [
            ("Scopul", [
                "Părțile vor face schimb de informații în cadrul unui interviu "
                "complet și al unui audit al afacerii Clientului (discuții cu "
                "proprietarul și cu echipa, analiza proceselor, a cifrelor și a "
                "instrumentelor folosite), pentru a identifica oportunități de "
                "îmbunătățire și de automatizare (<b>„Scopul”</b>).",
                "Detalii: [[ex.: audit al proceselor și al vânzărilor|30em]]",
            ]),
            ("Informații confidențiale", [
                "Sunt confidențiale toate informațiile nepublice pe care o Parte "
                "le transmite celeilalte în legătură cu Scopul, în orice formă "
                "(verbal, scris, digital sau prin observare la fața locului), în "
                "special: cifre financiare, vânzări, prețuri și marje, clienți și "
                "furnizori, date despre angajați, procese interne, parole și "
                "accesuri, planuri și strategii, precum și metodele, ofertele, "
                "documentele și instrumentele Pacheco Studios. Sunt incluse și "
                "notițele și analizele care conțin astfel de informații.",
            ]),
            ("Excepții", [
                "Nu sunt confidențiale informațiile care: (a) sunt sau devin "
                "publice fără vina Părții care le-a primit; (b) erau deja "
                "cunoscute de aceasta, în mod dovedit; (c) au fost primite legal "
                "de la un terț fără obligație de confidențialitate; (d) au fost "
                "dezvoltate independent; (e) trebuie dezvăluite prin lege sau la "
                "cererea unei autorități, caz în care Partea o anunță pe cealaltă "
                "când legea permite și dezvăluie doar strictul necesar.",
            ]),
            ("Obligații", [
                "Partea care primește informațiile: (a) le folosește numai pentru "
                "Scop; (b) nu le dezvăluie terților fără acordul scris al celeilalte "
                "Părți; (c) le împărtășește doar colaboratorilor care au nevoie de "
                "ele pentru Scop și care au o obligație de confidențialitate "
                "echivalentă, răspunzând pentru aceștia; (d) le protejează cu cel "
                "puțin aceeași grijă ca pe propriile informații; (e) anunță imediat "
                "orice acces sau dezvăluire neautorizată.",
            ]),
            ("Date personale și instrumente digitale", [
                "Datele personale (ale clienților sau angajaților) sunt tratate "
                "conform Regulamentului (UE) 2016/679 (GDPR), numai pentru Scop. "
                "Dacă va fi nevoie de o prelucrare continuă în numele Clientului, "
                "Părțile vor semna un acord de prelucrare separat. Pacheco Studios "
                "nu introduce informațiile confidențiale ale Clientului în servicii "
                "ale terților, inclusiv instrumente de inteligență artificială, care "
                "le-ar folosi pentru antrenarea modelelor sau le-ar face accesibile "
                "altora, și anonimizează datele ori de câte ori este posibil.",
            ]),
            ("Returnare și ștergere", [
                "La cerere sau la finalul colaborării, Partea care a primit "
                "informațiile le returnează sau le șterge în 15 zile. Copiile "
                "păstrate prin lege sau în copii de siguranță automate rămân "
                "confidențiale.",
            ]),
            ("Proprietate și publicitate", [
                "Acest acord nu transferă niciun drept asupra informațiilor: cele "
                "ale Clientului rămân ale Clientului, iar metodele, modelele și "
                "materialele Pacheco Studios rămân ale Pacheco Studios. Acordul nu "
                "obligă nicio Parte să încheie alt contract. Pacheco Studios nu "
                "prezintă Clientul ca studiu de caz și nu publică cifrele acestuia "
                "fără acordul său scris.",
            ]),
            ("Durată", [
                "Acordul intră în vigoare la data semnării. Obligațiile de "
                "confidențialitate durează 3 (trei) ani de la ultimul "
                "schimb de informații; pentru secretele comerciale, cât timp "
                "acestea rămân secrete.",
            ]),
            ("Încălcare", [
                "Partea care încalcă acordul răspunde pentru prejudiciul cauzat, "
                "potrivit legii. Cealaltă Parte poate cere și măsuri urgente "
                "pentru oprirea încălcării.",
            ]),
            ("Legea aplicabilă", [
                "Acordul este guvernat de legea română. Litigiile se soluționează "
                "pe cale amiabilă, iar în caz contrar de instanțele competente din "
                "Iași.",
            ]),
            ("Dispoziții finale", [
                "Acordul reprezintă înțelegerea completă a Părților privind "
                "confidențialitatea. Modificările se fac numai în scris. Dacă o "
                "clauză este nulă, celelalte rămân valabile. Semnat în două "
                "exemplare originale, câte unul pentru fiecare Parte; semnătura "
                "electronică este acceptată.",
            ]),
        ],
        "local_data": "Încheiat la [[localitate|10em]], la data de [[__ / __ / ____|8em]].",
        "assin_a": "Pentru Pacheco Studios",
        "assin_b": "Pentru Client",
        "nome": "Nume",
        "assinatura": "Semnătură",
        "pagina": "Pagina",
        "de": "din",
    },
    "pt": {
        "ficheiro": "acordo-confidencialidade-pt",
        "titulo": "Acordo de confidencialidade",
        "sub": "mútuo",
        "partes_intro": "Celebrado entre:",
        "parte_a": (
            "<b>Pacheco Studios</b>, representada por <b>Tomás Pacheco</b>, "
            "NIF [[NIF|9em]], com morada em [[morada|22em]] "
            "(«<b>Pacheco Studios</b>»);"
        ),
        "parte_b": (
            "[[denominação|22em]], NIPC / NIF [[NIPC|9em]], com sede em "
            "[[morada|20em]], representada por [[nome|14em]], na qualidade de "
            "[[cargo|9em]] («<b>Cliente</b>»),"
        ),
        "partes_fim": "em conjunto «Partes» e cada uma «Parte».",
        "clausulas": [
            ("Objeto", [
                "As Partes vão trocar informação no âmbito de uma entrevista "
                "completa e de uma auditoria ao negócio do Cliente (conversas com "
                "o dono e com a equipa, análise de processos, números e "
                "ferramentas), para identificar oportunidades de melhoria e de "
                "automatização (<b>«Finalidade»</b>).",
                "Detalhe: [[ex.: auditoria a processos e vendas|30em]]",
            ]),
            ("Informação confidencial", [
                "É confidencial toda a informação não pública que uma Parte "
                "transmita à outra no âmbito da Finalidade, por qualquer meio "
                "(oral, escrito, digital ou observação no local), em especial: "
                "números financeiros, faturação, preços e margens, clientes e "
                "fornecedores, dados de colaboradores, processos internos, senhas "
                "e acessos, planos e estratégias, bem como os métodos, propostas, "
                "documentos e ferramentas da Pacheco Studios. Incluem-se as notas "
                "e análises que contenham essa informação.",
            ]),
            ("Exceções", [
                "Não é confidencial a informação que: (a) seja ou se torne pública "
                "sem culpa da Parte que a recebeu; (b) esta já conhecesse, de forma "
                "comprovada; (c) tenha recebido licitamente de terceiro sem dever "
                "de confidencialidade; (d) tenha desenvolvido de forma "
                "independente; (e) deva divulgar por lei ou ordem de autoridade, "
                "caso em que avisa a outra Parte quando a lei o permita e divulga "
                "apenas o estritamente necessário.",
            ]),
            ("Obrigações", [
                "A Parte que recebe a informação: (a) usa-a só para a Finalidade; "
                "(b) não a divulga a terceiros sem autorização escrita da outra "
                "Parte; (c) partilha-a apenas com colaboradores que dela precisem "
                "para a Finalidade e estejam sujeitos a dever de confidencialidade "
                "equivalente, respondendo por eles; (d) protege-a com pelo menos o "
                "mesmo cuidado que dá à sua própria informação; (e) avisa de "
                "imediato qualquer acesso ou divulgação não autorizados.",
            ]),
            ("Dados pessoais e ferramentas digitais", [
                "Os dados pessoais (de clientes ou colaboradores) são tratados nos "
                "termos do Regulamento (UE) 2016/679 (RGPD), apenas para a "
                "Finalidade. Se vier a ser necessário um tratamento continuado por "
                "conta do Cliente, as Partes assinam um acordo de tratamento de "
                "dados separado. A Pacheco Studios não introduz informação "
                "confidencial do Cliente em serviços de terceiros, incluindo "
                "ferramentas de inteligência artificial, que a usem para treinar "
                "modelos ou a tornem acessível a outros, e anonimiza os dados "
                "sempre que possível.",
            ]),
            ("Devolução e eliminação", [
                "A pedido ou no fim da colaboração, a Parte que recebeu a "
                "informação devolve-a ou elimina-a no prazo de 15 dias. As cópias "
                "que a lei obrigue a guardar ou que fiquem em cópias de segurança "
                "automáticas continuam confidenciais.",
            ]),
            ("Propriedade e publicidade", [
                "Este acordo não transfere direitos sobre a informação: a do "
                "Cliente continua do Cliente e os métodos, modelos e materiais da "
                "Pacheco Studios continuam da Pacheco Studios. Nenhuma Parte fica "
                "obrigada a celebrar outro contrato. A Pacheco Studios não "
                "apresenta o Cliente como caso de estudo nem publica os seus "
                "números sem autorização escrita.",
            ]),
            ("Duração", [
                "O acordo produz efeitos na data da assinatura. Os deveres de "
                "confidencialidade duram 3 (três) anos a contar da última "
                "troca de informação; quanto a segredos comerciais, enquanto se "
                "mantiverem secretos.",
            ]),
            ("Incumprimento", [
                "A Parte que violar o acordo responde pelos danos causados, nos "
                "termos da lei. A outra Parte pode ainda pedir providências "
                "urgentes para fazer cessar a violação.",
            ]),
            ("Lei aplicável", [
                "O acordo rege-se pela lei portuguesa. Os litígios resolvem-se "
                "primeiro por acordo e, não sendo possível, no tribunal da comarca "
                "de Faro.",
            ]),
            ("Disposições finais", [
                "O acordo é o entendimento completo das Partes sobre "
                "confidencialidade. Alterações só por escrito. Se uma cláusula for "
                "inválida, as restantes mantêm-se. Feito em dois exemplares "
                "originais, um para cada Parte; a assinatura eletrónica é aceite.",
            ]),
        ],
        "local_data": "Feito em [[localidade|10em]], a [[__ / __ / ____|8em]].",
        "assin_a": "Pela Pacheco Studios",
        "assin_b": "Pelo Cliente",
        "nome": "Nome",
        "assinatura": "Assinatura",
        "pagina": "Página",
        "de": "de",
    },
    "en": {
        "ficheiro": "confidentiality-agreement-en",
        "titulo": "Confidentiality agreement",
        "sub": "mutual",
        "partes_intro": "Made between:",
        "parte_a": (
            "<b>Pacheco Studios</b>, represented by <b>Tomás Pacheco</b>, "
            "tax no. [[tax no.|9em]], of [[address|22em]] "
            "(“<b>Pacheco Studios</b>”); and"
        ),
        "parte_b": (
            "[[company name|22em]], company / tax no. [[number|9em]], registered "
            "at [[address|20em]], represented by [[name|14em]], as "
            "[[position|9em]] (the “<b>Client</b>”),"
        ),
        "partes_fim": "together the “Parties” and each a “Party”.",
        "clausulas": [
            ("Purpose", [
                "The Parties will exchange information in the course of a full "
                "interview and audit of the Client’s business (conversations with "
                "the owner and the team, review of processes, figures and tools), "
                "to identify opportunities for improvement and automation (the "
                "<b>“Purpose”</b>).",
                "Details: [[e.g. audit of processes and sales|30em]]",
            ]),
            ("Confidential information", [
                "All non-public information that one Party discloses to the other "
                "in connection with the Purpose, in any form (oral, written, "
                "digital or by on-site observation), is confidential, in "
                "particular: financial figures, revenue, prices and margins, "
                "customers and suppliers, staff data, internal processes, "
                "passwords and access, plans and strategies, as well as Pacheco "
                "Studios’ methods, proposals, documents and tools. This includes "
                "notes and analyses containing such information.",
            ]),
            ("Exceptions", [
                "Information is not confidential if it: (a) is or becomes public "
                "through no fault of the receiving Party; (b) was demonstrably "
                "already known to it; (c) was lawfully received from a third party "
                "without a duty of confidence; (d) was independently developed; "
                "(e) must be disclosed by law or by order of an authority, in which "
                "case the Party notifies the other where the law allows and "
                "discloses only what is strictly necessary.",
            ]),
            ("Obligations", [
                "The receiving Party shall: (a) use the information only for the "
                "Purpose; (b) not disclose it to third parties without the other "
                "Party’s written consent; (c) share it only with collaborators who "
                "need it for the Purpose and are bound by an equivalent duty of "
                "confidence, remaining responsible for them; (d) protect it with at "
                "least the same care as its own information; (e) promptly report "
                "any unauthorised access or disclosure.",
            ]),
            ("Personal data and digital tools", [
                "Personal data (of customers or staff) is processed in accordance "
                "with Regulation (EU) 2016/679 (GDPR), only for the Purpose. If "
                "ongoing processing on the Client’s behalf becomes necessary, the "
                "Parties will sign a separate data processing agreement. Pacheco "
                "Studios does not enter the Client’s confidential information into "
                "third-party services, including artificial intelligence tools, "
                "that use it to train models or make it available to others, and "
                "anonymises data wherever possible.",
            ]),
            ("Return and deletion", [
                "On request or at the end of the collaboration, the receiving "
                "Party returns or deletes the information within 15 days. Copies "
                "kept by law or in automatic backups remain confidential.",
            ]),
            ("Ownership and publicity", [
                "This agreement transfers no rights in the information: the "
                "Client’s remains the Client’s, and Pacheco Studios’ methods, "
                "templates and materials remain Pacheco Studios’. Neither Party is "
                "obliged to enter into any further contract. Pacheco Studios will "
                "not present the Client as a case study or publish its figures "
                "without written consent.",
            ]),
            ("Term", [
                "This agreement takes effect on signature. The duties of "
                "confidence last 3 (three) years from the last exchange of "
                "information and, for trade secrets, for as long as they remain "
                "secret.",
            ]),
            ("Breach", [
                "A Party in breach is liable for the damage caused, as provided by "
                "law. The other Party may also seek urgent relief to stop the "
                "breach.",
            ]),
            ("Governing law", [
                "This agreement is governed by the law of [[Romania / Portugal|10em]]. "
                "Disputes are first settled amicably and, failing that, by the "
                "competent courts of [[city|8em]].",
            ]),
            ("Final provisions", [
                "This is the Parties’ entire agreement on confidentiality. "
                "Changes must be in writing. If a clause is invalid, the others "
                "remain in force. Signed in two originals, one for each Party; "
                "electronic signatures are accepted.",
            ]),
        ],
        "local_data": "Signed in [[place|10em]] on [[__ / __ / ____|8em]].",
        "assin_a": "For Pacheco Studios",
        "assin_b": "For the Client",
        "nome": "Name",
        "assinatura": "Signature",
        "pagina": "Page",
        "de": "of",
    },
}

CSS = """
@page { size: A4; margin: 16mm 18mm 18mm; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; font-family: Caladea, "Liberation Serif", serif; font-size: 10.4pt;
  line-height: 1.42; color: #16181d; }
.topo { display: flex; justify-content: space-between; align-items: baseline;
  border-bottom: 1.2pt solid #16181d; padding-bottom: 5pt; margin-bottom: 12pt;
  font-family: Inter, sans-serif; font-size: 7.6pt; letter-spacing: .08em;
  text-transform: uppercase; color: #4a4f59; }
.topo b { color: #16181d; letter-spacing: .16em; font-weight: 700; }
h1 { font-family: Inter, sans-serif; font-weight: 700; font-size: 19pt;
  letter-spacing: -.01em; margin: 0 0 1pt; }
.sub { font-family: Inter, sans-serif; font-size: 8.4pt; text-transform: uppercase;
  letter-spacing: .14em; color: #4a4f59; margin-bottom: 11pt; }
.partes p { margin: 0 0 5pt; }
.partes .lado { font-family: Inter, sans-serif; font-size: 7.4pt; font-weight: 700;
  letter-spacing: .1em; color: #4a4f59; margin-right: 4pt; }
ol.cl { list-style: none; counter-reset: c; padding: 0; margin: 10pt 0 0; }
ol.cl > li { counter-increment: c; margin: 0 0 6.5pt; break-inside: avoid; }
ol.cl h2 { font-family: Inter, sans-serif; font-size: 8.6pt; font-weight: 700;
  margin: 0 0 1pt; letter-spacing: .02em; }
ol.cl h2::before { content: counter(c) ". "; color: #4a4f59; }
ol.cl p + p { margin-top: 5pt; }
ol.cl p { margin: 0; text-align: justify; hyphens: auto; }
.campo { display: inline-block; position: relative; border-bottom: .7pt solid #16181d;
  min-height: 1.1em; vertical-align: baseline; margin: 0 1pt; padding-top: 6.5pt; }
.campo i { position: absolute; left: 0; top: -1.5pt; font-style: normal;
  font-family: Inter, sans-serif; font-size: 5.6pt; letter-spacing: .04em;
  color: #6b717c; white-space: nowrap; }
.final { break-inside: avoid; margin-top: 12pt; }
.assin { display: grid; grid-template-columns: 1fr 1fr; gap: 14mm; margin-top: 14pt; }
.assin .t { font-family: Inter, sans-serif; font-size: 7.6pt; font-weight: 700;
  letter-spacing: .1em; text-transform: uppercase; margin-bottom: 34pt; }
.linha { border-bottom: .7pt solid #16181d; height: 1pt; margin-bottom: 2pt; }
.rot { font-family: Inter, sans-serif; font-size: 6.6pt; color: #6b717c;
  margin-bottom: 16pt; }
"""

CAMPO = re.compile(r"\[\[([^|\]]+)\|([^\]]+)\]\]")


def campos(txt):
    """Troca [[rótulo|largura]] por uma linha de preencher com rótulo pequeno."""
    def sub(m):
        rot, larg = m.group(1), m.group(2)
        return f'<span class="campo" style="min-width:{larg}"><i>{html.escape(rot)}</i></span>'
    return CAMPO.sub(sub, txt)


def montar(lang, t):
    cls = "\n".join(
        f"<li><h2>{html.escape(tit)}</h2>"
        + "".join(f"<p>{campos(p)}</p>" for p in pars)
        + "</li>"
        for tit, pars in t["clausulas"]
    )
    def bloco(titulo):
        return (
            f'<div><div class="t">{titulo}</div>'
            f'<div class="linha"></div><div class="rot">{t["assinatura"]}</div>'
            f'<div class="linha"></div><div class="rot">{t["nome"]}</div></div>'
        )
    return f"""<!doctype html>
<html lang="{'pt-PT' if lang == 'pt' else lang}"><head><meta charset="utf-8">
<title>{t['titulo']} · Pacheco Studios</title><style>{CSS}</style></head><body>
<div class="topo"><b>Pacheco Studios</b><span>pachecost.com</span></div>
<h1>{t['titulo']}</h1>
<div class="sub">{t['sub']}</div>
<div class="partes">
<p>{t['partes_intro']}</p>
<p><span class="lado">1</span>{campos(t['parte_a'])}</p>
<p><span class="lado">2</span>{campos(t['parte_b'])}</p>
<p>{t['partes_fim']}</p>
</div>
<ol class="cl">{cls}</ol>
<div class="final">
<p>{campos(t['local_data'])}</p>
<div class="assin">{bloco(t['assin_a'])}{bloco(t['assin_b'])}</div>
</div>
</body></html>"""


def main():
    SAIDA.mkdir(exist_ok=True)
    png = "--png" in sys.argv
    for lang, t in TEXTOS.items():
        h = SAIDA / f"{t['ficheiro']}.html"
        h.write_text(montar(lang, t), encoding="utf-8")
        pdf = SAIDA / f"{t['ficheiro']}.pdf"
        subprocess.run(
            [CHROME, "--headless", "--no-sandbox", "--disable-gpu",
             "--no-pdf-header-footer", f"--print-to-pdf={pdf}", h.as_uri()],
            check=True, capture_output=True,
        )
        if png:
            subprocess.run(["pdftoppm", "-png", "-r", "110", str(pdf),
                            str(SAIDA / t["ficheiro"])], check=True)
        print(pdf.name)


if __name__ == "__main__":
    main()
