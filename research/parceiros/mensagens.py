#!/usr/bin/env python3
"""Gera a lista de parceiros para o Tomás (mensagem pronta por tipo, links WhatsApp/SMS, morada) a partir do TSV.

  python3 research/parceiros/mensagens.py > research/parceiros/PARCEIROS.md

Lê research/parceiros/parceiros.tsv. Colunas: semana cidade tipo nome nota avaliacoes tel whatsapp morada maps estado notas
  cidade    Iași ou Faro (decide a língua e o valor da comissão)
  tipo      contabil · infiintare · tipografie · reclame · case-marcat · imobiliare · fonduri · horeca
  whatsapp  sim / ? / não (sim só com prova pública: PLAYBOOK §11 ponto 8)
  estado    por contactar / contactado AAAA-MM-DD / aceitou / recusou / sem resposta
Só os «por contactar» e os «contactado» há 7+ dias levam mensagem; o resto vai para a tabela do fim.
"""
import csv, datetime, os, sys, urllib.parse

AQUI = os.path.dirname(os.path.abspath(__file__))
RAW = "https://github.com/tspacheco/Designerpacheco/raw/claude/parceiros-indicam-4kcnrc/research/parceiros/proposta/"

RO = ("Bună ziua! Sunt Tomás Pacheco, de la Pacheco Studios. Facem site-uri pentru afaceri locale din Iași "
      "(un exemplu: https://pachecost.com/demo/la-gioia/).\n\n{gancho}\n\n"
      "Vă propun un parteneriat simplu: pentru fiecare client pe care ni-l recomandați și care își face site-ul cu noi, "
      "primiți 500 de lei. Clientul primește prima lună de întreținere gratuită. Vă trimit și o pagină cu detaliile.\n\n"
      "Pot trece pe la dumneavoastră 10 minute săptămâna aceasta?")
RO_LEMBRETE = ("Bună ziua! Revin la propunerea de parteneriat de săptămâna trecută (500 de lei pentru fiecare client recomandat). "
               "Dacă vă interesează, trec pe la dumneavoastră când vă convine. Mulțumesc!")
PT = ("Bom dia! Sou o Tomás Pacheco, da Pacheco Studios. Fazemos sites para negócios locais do Algarve "
      "(um exemplo: https://pachecost.com/demo/sos-car/).\n\n{gancho}\n\n"
      "Proponho-lhe uma parceria simples: por cada cliente que nos indicar e que faça o site connosco, recebe 100 €. "
      "O cliente fica com o primeiro mês de manutenção grátis. Envio-lhe também uma página com os detalhes.\n\n"
      "Posso passar aí 10 minutos esta semana?")
PT_LEMBRETE = ("Bom dia! Volto à proposta de parceria da semana passada (100 € por cada cliente indicado). "
               "Se lhe interessar, passo aí quando lhe der jeito. Obrigado!")

GANCHO_RO = {
    "contabil": "Știu că vedeți în fiecare lună firme noi care abia pornesc. Multe nu au încă site, iar unele vă întreabă cine le poate face unul.",
    "infiintare": "Ajutați în fiecare lună oameni să-și deschidă firma. Imediat după, au nevoie de site și de o fișă Google, și de cineva de încredere care să le facă.",
    "tipografie": "Cine își comandă cărți de vizită, flyere sau meniuri de multe ori abia a deschis și nu are încă un site la care să ducă codul QR.",
    "reclame": "Cine își comandă firma sau reclama luminoasă tocmai deschide un local. E exact momentul în care are nevoie și de site și de Google.",
    "case-marcat": "Orice afacere nouă trece pe la dumneavoastră pentru casa de marcat, de obicei în prima săptămână. E și momentul în care are nevoie de site.",
    "imobiliare": "Cine închiriază un spațiu comercial prin dumneavoastră deschide o afacere în câteva săptămâni și are nevoie de site și de Google.",
    "fonduri": "Pentru clienții dumneavoastră din Start-Up Nation, site-ul de prezentare și magazinul online sunt cheltuieli eligibile. Le facem cu factură, iar dumneavoastră aveți un furnizor de încredere pentru partea digitală.",
    "horeca": "Cine își cumpără echipamente pentru un local nou deschide în curând și are nevoie de site, meniu online și Google.",
}
GANCHO_PT = {
    "contabil": "Sei que vê todos os meses empresas novas a começar. Muitas ainda não têm site, e algumas perguntam-lhe quem lhes pode fazer um.",
    "infiintare": "Ajuda todos os meses pessoas a abrir empresa. Logo a seguir precisam de site e de ficha no Google, e de alguém de confiança que lhes faça.",
    "tipografie": "Quem encomenda cartões de visita, flyers ou ementas muitas vezes acabou de abrir e ainda não tem um site para onde levar o QR.",
    "reclame": "Quem encomenda o reclamo luminoso está a abrir um espaço. É exatamente quando precisa também de site e de Google.",
    "case-marcat": "Todos os negócios novos passam por si para a máquina registadora ou o software de faturação, normalmente na primeira semana. É também quando precisam de site.",
    "imobiliare": "Quem arrenda ou trespassa um espaço comercial convosco abre um negócio em poucas semanas e precisa de site e de Google.",
    "fonduri": "Para os seus clientes com candidaturas aprovadas, o site e a loja online costumam ser despesa elegível. Fazemo-los com fatura, e o senhor tem um fornecedor de confiança para a parte digital.",
    "horeca": "Quem compra equipamento para um restaurante novo abre em breve e precisa de site, menu online e Google.",
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
    print("Proposta para mandar a seguir à mensagem (PDF, 1 página): "
          f"[romeno]({RAW}parceria-ro.pdf) · [PT Algarve]({RAW}parceria-pt-faro.pdf) · [PT de Iași, para ti]({RAW}parceria-pt-iasi.pdf).  ")
    print("Os escritórios convertem melhor ao vivo: em Iași, passa com a proposta impressa e a demo aberta no telemóvel. "
          "Diz-me quem aceitou, quem recusou e quem não respondeu.\n")
    print("<details><summary>O que diz a mensagem romena (PT)</summary>\n")
    print("> " + PT.replace("do Algarve", "de Iași").replace("sos-car", "la-gioia").replace("100 €", "500 lei")
          .format(gancho="[uma frase sobre o que esse parceiro vê todos os dias: as mesmas frases da versão PT, por tipo]")
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
                    texto = (RO if ro else PT).format(gancho=(GANCHO_RO if ro else GANCHO_PT)[tipo])
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
