#!/usr/bin/env python3
"""Gera a lista de parceiros para o Tomás (mensagem pronta por tipo, links WhatsApp/SMS, morada) a partir do TSV.

  python3 research/parceiros/mensagens.py > research/parceiros/PARCEIROS.md

Lê research/parceiros/parceiros.tsv. Colunas: semana cidade tipo nome nota avaliacoes tel whatsapp morada maps estado notas
  cidade    Iași ou Faro (decide a língua)
  tipo      contabil · infiintare · tipografie · reclame · case-marcat · imobiliare · fonduri · horeca
  whatsapp  sim / ? / não (sim só com prova pública: PLAYBOOK §11 ponto 8)
  estado    por contactar / contactado AAAA-MM-DD / reunião marcada / parceiro / recusou / sem resposta
Levam mensagem: «por contactar» (hipótese + pedido de triagem) e «contactado» há 7+ dias (lembrete binário).
Regras do Tomás (11/10/2026 14h38): 3 quick wins sem custo ao parceiro; 15 % do valor de implementação e 5 % trimestral do que o
negócio apresentado nos pagar; sem valores fixos; primeiro o incentivo, depois a proposta com assinaturas.
"""
import csv, datetime, os, sys, urllib.parse

AQUI = os.path.dirname(os.path.abspath(__file__))
KIT = "https://github.com/tspacheco/Designerpacheco/raw/claude/parceiros-indicam-4kcnrc/research/parceiros/kit/"
# Nada se envia a parceiros até o Tomás dizer «envia» (11/10/2026).
ENVIAR = False

# Formato «triagem como isca» (playbook de triagem proativa): hipótese pública, nunca afirmar falhas internas sem dados,
# oferta de mostrar o fluxo numa página, validação com o decisor, fecho «faça uma triagem connosco», sem minutos.
RO = ("Bună ziua! Sunt Tomás Pacheco, de la Pacheco Studios: construim sisteme cu AI pentru afaceri locale din Iași.\n\n"
      "M-am uitat la {nome} din exterior. {hipotese}\n\n"
      "Nu am acces la operațiunile dumneavoastră, deci e doar o ipoteză. Vă pot arăta pe o pagină fluxul pe care l-aș verifica. "
      "Dacă se confirmă, e prima din 3 soluții rapide pe care le implementăm gratuit partenerilor noștri; apoi vă arăt cât puteți "
      "câștiga recomandându-ne.\n\nFaceți un triaj cu noi: stabilim o întâlnire săptămâna aceasta?")
RO_LEMBRETE = ("Bună ziua! Revin la ipoteza de săptămâna trecută. E deja rezolvată de la cap la coadă sau merită o întâlnire ca s-o verificăm? "
               "Mulțumesc!")
PT = ("Bom dia! Sou o Tomás Pacheco, da Pacheco Studios: construímos sistemas com IA para negócios locais.\n\n"
      "Olhei para a {nome} de fora. {hipotese}\n\n"
      "Não tenho acesso à vossa operação, por isso é só uma hipótese. Posso mostrar-lhe numa página o fluxo que eu validaria. "
      "Se se confirmar, é a primeira de 3 soluções rápidas que implementamos sem custo aos nossos parceiros; depois mostro-lhe quanto "
      "pode ganhar a apresentar-nos.\n\nFaça uma triagem connosco: marcamos uma reunião esta semana?")
PT_LEMBRETE = ("Bom dia! Volto à hipótese da semana passada. Isto já está resolvido de ponta a ponta ou vale uma reunião para validarmos? "
               "Obrigado!")

HIPOTESE_RO = {
    "contabil": "Într-un birou de contabilitate, documentele clienților vin de obicei pe e-mail, WhatsApp și pe hârtie. Întrebarea pe care aș verifica-o: când sosește un document, cine răspunde de el până e înregistrat?",
    "infiintare": "Cererile de înființare vin pe telefon, formular și WhatsApp, și fiecare are nevoie de aceleași acte. Întrebarea: cine urmărește fiecare dosar până la final și cum află clientul unde a rămas?",
    "tipografie": "Comenzile vin cu fișiere, dimensiuni și termene pe canale diferite. Întrebarea: când intră o comandă, cine confirmă că fișierul e corect înainte de tipar?",
    "reclame": "O firmă luminoasă trece prin ofertă, măsurători, aviz și montaj. Întrebarea: între ofertă și montaj, cine e responsabil de fiecare pas și cum află clientul unde a rămas?",
    "case-marcat": "Fiecare client nou are nevoie de casă de marcat, fiscalizare și instruire, și întreabă aceleași lucruri. Întrebarea: cine preia fiecare cerere și unde se vede stadiul ei?",
    "imobiliare": "Cererile pentru spații comerciale vin de pe portaluri, telefon și WhatsApp. Întrebarea: când intră o cerere, cine o preia și în cât timp primește clientul un răspuns?",
    "fonduri": "Un dosar de finanțare are multe acte și termene. Întrebarea: cine urmărește ce lipsește din fiecare dosar și cum află clientul fără să sune?",
    "horeca": "Comenzile de echipamente vin cu oferte, livrări și service pe canale diferite. Întrebarea: când intră o cerere de service, cine e responsabil până e rezolvată?",
}
HIPOTESE_PT = {
    "contabil": "Num escritório de contabilidade, os documentos dos clientes costumam chegar por e-mail, WhatsApp e em papel. A pergunta que eu validaria: quando chega um documento, quem fica dono dele até estar lançado?",
    "infiintare": "Os pedidos para abrir empresa chegam por telefone, formulário e WhatsApp, e todos precisam dos mesmos documentos. A pergunta: quem acompanha cada processo até ao fim e como sabe o cliente onde está?",
    "tipografie": "As encomendas chegam com ficheiros, medidas e prazos por canais diferentes. A pergunta: quando entra uma encomenda, quem confirma que o ficheiro está certo antes de imprimir?",
    "reclame": "Um reclamo passa por orçamento, medições, licença e montagem. A pergunta: entre o orçamento e a montagem, quem é dono de cada passo e como sabe o cliente onde está?",
    "case-marcat": "Cada cliente novo precisa de software de faturação, configuração e formação, e pergunta as mesmas coisas. A pergunta: quem fica com cada pedido e onde se vê em que ponto está?",
    "imobiliare": "Os pedidos de espaços comerciais chegam pelos portais, telefone e WhatsApp. A pergunta: quando entra um pedido, quem fica com ele e em quanto tempo o cliente tem resposta?",
    "fonduri": "Uma candidatura tem muitos documentos e prazos. A pergunta: quem acompanha o que falta em cada processo e como sabe o cliente sem ter de ligar?",
    "horeca": "Os pedidos de equipamento chegam com orçamentos, entregas e assistência por canais diferentes. A pergunta: quando entra um pedido de assistência, quem é dono dele até estar resolvido?",
}


def numero(tel, cidade):
    d = "".join(c for c in tel if c.isdigit())
    if cidade == "Iași":
        return "40" + d[1:] if d.startswith("0") else d
    return d if d.startswith("351") else "351" + d


def fixo(tel, cidade):
    d = numero(tel, cidade)
    return d[2] in "23" if cidade == "Iași" else d[3] == "2"


def dias_desde(estado):
    try:
        return (datetime.date.today() - datetime.date.fromisoformat(estado.split()[-1])).days
    except ValueError:
        return None


def ativo(l):
    return l["estado"] == "por contactar" or (l["estado"].startswith("contactado") and (dias_desde(l["estado"]) or 0) >= 7)


def main():
    linhas = list(csv.DictReader(open(os.path.join(AQUI, "parceiros.tsv"), encoding="utf-8"), delimiter="\t"))
    q = lambda s: urllib.parse.quote(s, safe="/:")
    print("# Parceiros que indicam\n")
    if not ENVIAR:
        print("**Rascunho: não enviar nada até o Tomás dizer «envia».**\n")
    print("**Programa (11/10, 14h38):** 3 soluções rápidas sem custo para o parceiro (a triagem já mostra pelo menos 1); por cada "
          "negócio apresentado que comece a trabalhar connosco, 15 % do valor de implementação e 5 % do que nos pagar, a cada 3 meses. "
          "Sem valores fixos. Primeiro o incentivo, depois a proposta para assinar.  ")
    print(f"**1) Incentivo** (4 páginas, o que mostrar primeiro): [romeno]({KIT}incentivo-ro.pdf) · [inglês]({KIT}incentivo-en.pdf) · [PT]({KIT}incentivo-pt.pdf).  ")
    print(f"**2) Proposta para assinar** (2 páginas, só depois): [romeno]({KIT}proposta-parceria-ro.pdf) · [inglês]({KIT}proposta-parceria-en.pdf) · "
          f"[PT]({KIT}proposta-parceria-pt.pdf). Com o nome do parceiro: `python3 research/parceiros/kit/gerar.py \"Nome\"`.  ")
    print("Antes de enviar, confirma a hipótese no percurso público do parceiro (Google, site, WhatsApp) e prepara a página do fluxo. "
          "Diz-me quem marcou reunião e quem aceitou.\n")
    print("<details><summary>O que diz a mensagem romena (PT)</summary>\n")
    print("> " + PT.replace("negócios locais", "negócios locais de Iași")
          .format(nome="[nome]", hipotese="[a hipótese do tipo de negócio: as mesmas frases da versão PT]")
          .replace("\n", "\n> ").replace("> \n", ">\n") + "\n\n</details>\n")
    for cidade in ("Iași", "Faro"):
        grupo = [l for l in linhas if l["cidade"] == cidade]
        ativos = [l for l in grupo if ativo(l)]
        if not ativos:
            continue
        print(f"## {cidade}\n")
        for tipo in dict.fromkeys(l["tipo"] for l in ativos):
            print(f"### {tipo}\n")
            for l in (x for x in ativos if x["tipo"] == tipo):
                ro = cidade == "Iași"
                if l["estado"] == "por contactar":
                    texto = (RO if ro else PT).format(nome=l["nome"], hipotese=(HIPOTESE_RO if ro else HIPOTESE_PT)[tipo])
                else:
                    texto = RO_LEMBRETE if ro else PT_LEMBRETE
                nota = (f" · Google {l['nota']}" + (f" ({l['avaliacoes']} avaliações)" if l["avaliacoes"] else "")) if l["nota"] else ""
                print(f"#### {l['nome']}\nTel.: {l['tel'] or 'a confirmar'} · WhatsApp: {l['whatsapp']}{nota}  ")
                print(f"Morada: [{l['morada'] or 'ver no Maps'}]({l['maps']})  ")
                if l["notas"]:
                    print(f"Nota: {l['notas']}  ")
                if not l["tel"]:
                    print("Sem telefone na ficha: visita.\n")
                elif fixo(l["tel"], cidade):
                    print(f"Telefone fixo: [Ligar](tel:+{numero(l['tel'], cidade)}) ou visita.\n")
                else:
                    n = numero(l["tel"], cidade)
                    print(f"[Abrir no WhatsApp](https://wa.me/{n}?text={q(texto)}) · [Enviar por SMS](sms:+{n}?&body={q(texto)})\n")
                print("> " + texto.replace("\n", "\n> ").replace("> \n", ">\n") + "\n")
    resto = [l for l in linhas if not ativo(l)]
    if resto:
        print("## Já tratados\n\n| Cidade | Parceiro | Tipo | Estado |\n|---|---|---|---|")
        for l in resto:
            print(f"| {l['cidade']} | {l['nome']} | {l['tipo']} | {l['estado']} |")


if __name__ == "__main__":
    main()
