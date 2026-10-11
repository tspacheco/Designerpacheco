#!/usr/bin/env python3
"""Gera a lista de parceiros para o Tomás (mensagem pronta por tipo, links WhatsApp/SMS, morada) a partir do TSV.

  python3 research/parceiros/mensagens.py > research/parceiros/PARCEIROS.md

Lê research/parceiros/parceiros.tsv. Colunas: semana cidade tipo nome nota avaliacoes tel whatsapp morada maps estado notas
  cidade    Iași ou Faro (decide a língua)
  tipo      contabil · infiintare · tipografie · reclame · case-marcat · imobiliare · fonduri · horeca
  whatsapp  sim / ? / não (sim só com prova pública: PLAYBOOK §11 ponto 8)
  estado    por contactar / contactado AAAA-MM-DD / reunião marcada / parceiro / recusou / sem resposta
Levam mensagem: «por contactar» (convite para o programa e pedido de reunião) e «contactado» há 7+ dias (lembrete).
Regras de 11/10/2026 (posicionamento de consultoria com IA): a auditoria fica creditada na implementação; o parceiro recebe
10 % da implementação e 10 % a cada 3 meses enquanto o cliente ficar connosco; sem preços fixos, sem sites, sem quick wins grátis.
"""
import csv, datetime, os, sys, urllib.parse

AQUI = os.path.dirname(os.path.abspath(__file__))
KIT = "https://github.com/tspacheco/Designerpacheco/raw/claude/parceiros-indicam-4kcnrc/research/parceiros/kit/"
# Nada se envia a parceiros até o Tomás dizer «envia» (11/10/2026).
ENVIAR = False

RO = ("Bună ziua! Sunt Tomás Pacheco, de la Pacheco Studios, o consultanță în sisteme cu AI din Iași: găsim unde o afacere pierde "
      "cereri, timp și bani și proiectăm sistemul care rezolvă problema.\n\n{gancho}\n\n"
      "Avem un program de parteneri: pentru fiecare afacere pe care ne-o prezentați și cu care începem să lucrăm, primiți 10% din "
      "implementare și apoi 10% la fiecare 3 luni, cât timp rămâne cu noi. Afacerea recomandată nu plătește auditul separat.\n\n"
      "Putem stabili o întâlnire săptămâna aceasta?")
RO_LEMBRETE = ("Bună ziua! Revin la mesajul de săptămâna trecută despre programul de parteneri Pacheco Studios. "
               "Dacă vă interesează, stabilim o întâlnire când vă convine. Mulțumesc!")
PT = ("Bom dia! Sou o Tomás Pacheco, da Pacheco Studios, uma consultora de sistemas com IA: encontramos onde um negócio perde "
      "pedidos, tempo e dinheiro e desenhamos o sistema que resolve.\n\n{gancho}\n\n"
      "Temos um programa de parceiros: por cada negócio que nos apresentar e com quem comecemos a trabalhar, recebe 10 % da "
      "implementação e depois 10 % a cada 3 meses, enquanto ficar connosco. O negócio apresentado não paga a auditoria à parte.\n\n"
      "Podemos marcar uma reunião esta semana?")
PT_LEMBRETE = ("Bom dia! Volto à mensagem da semana passada sobre o programa de parceiros da Pacheco Studios. "
               "Se lhe interessar, marcamos uma reunião quando lhe der jeito. Obrigado!")

GANCHO_RO = {
    "contabil": "Vedeți din interior cum lucrează firmele clienților dumneavoastră: unde pierd timp, cereri și bani. De multe ori sunteți primul căruia îi spun.",
    "infiintare": "Ajutați în fiecare lună oameni să-și deschidă firma. Cei care cresc repede ajung curând să piardă cereri și timp și caută pe cineva de încredere.",
    "tipografie": "Lucrați zilnic cu afaceri locale care își fac reclamă. Multe dintre ele pierd apoi cererile care vin din acea reclamă.",
    "reclame": "Cine își comandă firma luminoasă deschide sau extinde un local. Atunci apar și cererile pe care nu le preia nimeni la timp.",
    "case-marcat": "Orice afacere trece pe la dumneavoastră pentru casa de marcat sau facturare. Vedeți primii cum își organizează vânzările și unde se blochează.",
    "imobiliare": "Cine închiriază un spațiu comercial prin dumneavoastră deschide sau se extinde. Exact atunci operațiunile nu mai țin pasul.",
    "fonduri": "Clienții dumneavoastră cu finanțare aprobată au buget pentru digitalizare. Le arătăm întâi unde pierd bani, ca investiția să meargă acolo unde contează.",
    "horeca": "Cine își cumpără echipamente pentru un local nou sau mai mare are curând mai multe rezervări și comenzi decât poate gestiona pe WhatsApp.",
}
GANCHO_PT = {
    "contabil": "Vê por dentro como trabalham as empresas dos seus clientes: onde perdem tempo, pedidos e dinheiro. Muitas vezes é o primeiro a quem o contam.",
    "infiintare": "Ajuda todos os meses pessoas a abrir empresa. As que crescem depressa começam cedo a perder pedidos e tempo, e procuram alguém de confiança.",
    "tipografie": "Trabalha todos os dias com negócios locais que fazem publicidade. Muitos perdem depois os pedidos que essa publicidade traz.",
    "reclame": "Quem encomenda o reclamo luminoso está a abrir ou a crescer. É aí que aparecem os pedidos que ninguém atende a tempo.",
    "case-marcat": "Todos os negócios passam por si para a faturação. Vê antes de todos como organizam as vendas e onde encravam.",
    "imobiliare": "Quem arrenda um espaço comercial convosco está a abrir ou a expandir. É exatamente aí que a operação deixa de acompanhar.",
    "fonduri": "Os seus clientes com candidaturas aprovadas têm orçamento para digitalização. Mostramos-lhes primeiro onde perdem dinheiro, para o investimento ir para onde conta.",
    "horeca": "Quem compra equipamento para um restaurante novo ou maior tem em breve mais reservas e pedidos do que consegue gerir no WhatsApp.",
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
    print("**Programa (11/10):** o parceiro apresenta um negócio; fazemos a auditoria, que não se paga à parte (fica creditada na "
          "implementação); quando começamos a trabalhar com esse negócio, o parceiro recebe 10 % da implementação e, enquanto o cliente "
          "ficar connosco, 10 % a cada 3 meses. Sem preços fixos.  ")
    print("**Kit do parceiro** (4 páginas, para enviar ou levar impresso, com o acordo para assinar): "
          f"[romeno]({KIT}kit-parceiro-ro.pdf) · [inglês]({KIT}kit-parceiro-en.pdf) · [PT]({KIT}kit-parceiro-pt.pdf). "
          "Com o nome do parceiro na capa: `python3 research/parceiros/kit/gerar.py \"Nome\"`.  ")
    print("Os escritórios convertem melhor ao vivo: em Iași, passa lá com o kit. Diz-me quem marcou reunião e quem aceitou.\n")
    print("<details><summary>O que diz a mensagem romena (PT)</summary>\n")
    print("> " + PT.replace("consultora de sistemas com IA", "consultora de sistemas com IA de Iași")
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
