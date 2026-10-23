#!/usr/bin/env python3
"""Gera a lista do dia do caçador (mensagens prontas, links WhatsApp e SMS, moradas) a partir de um TSV.

  python3 research/cacador/mensagens.py research/cacador/AAAA-MM-DD.tsv > research/cacador/AAAA-MM-DD.md

Colunas do TSV (com cabeçalho): corrida slug nome descricao tel whatsapp morada zona estado
  corrida   A (8h00) ou B (11h30)
  descricao (já não entra na mensagem desde 08/10; pode ficar vazia)
  whatsapp  sim / ? / não (sim só com prova pública: PLAYBOOK §11 ponto 8)
  estado    publicada / por fazer / tirada (motivo)
Só as linhas «publicada» levam mensagem; as outras aparecem numa tabela no fim.
"""
import csv, os, sys, urllib.parse

# Mensagem nova do Tomás (08/10, a partir da Star Service Auto do lote 4); texto igual ao de sites/demos-pachecost/LOTE4-IASI.md
# Só a saudação roda (09/10: o WhatsApp bloqueou o Tomás por spam com textos iguais de 10 em 10 s); o resto é fixo.
SAUDACOES = ("Bună ziua! Sunt Tomás, de la Pacheco Studios.",
             "Bună ziua, {nome}! Sunt Tomás, de la Pacheco Studios.",
             "Bună! Mă numesc Tomás și lucrez la Pacheco Studios.",
             "Bună ziua! Aici Tomás, de la Pacheco Studios.")
MSG = ("{saudacao}\n\n"
       "Căutați să creșteți cu 10% până la 30% numărul de clienți, luna aceasta și în continuare? "
       "Iată soluția pe care am creat-o după ce m-am uitat la afacerea dumneavoastră:\n{demo}\n\n"
       "Poate nu înțelegeți încă, dar credeți-mă, așa va fi. Haideți să stabilim o oră ca să implementăm această soluție.\n\nVoi fi pregătit.")

# Corrida B (texto do Tomás, 10/10, igual a sites/demos-pachecost/DESCRICAO-CORRIDA-B.md do ramo das demos). Sem preço.
# [nume] = coluna «dono» do TSV quando se sabe; senão a saudação fica sem nome. [Compania] = nome do negócio.
def tip(cat):
    c = (cat or "").lower()
    if any(k in c for k in ("stomatolog", "clinic", "medic", "fizioterap", "cabinet", "kineto", "masaj", "terap")):
        return "clinici"
    if any(k in c for k in ("salon", "coafor", "cosmetic", "estetic", "frizer", "manichi", "epilare", "tatuaj")):
        return "saloane"
    return "afaceri"


# 23/10 (Tomás): curta (30–50 palavras), Pacheco Studios como consultora de IA, a demo é o gatilho de uma potencial parceria.
MSG_B = ("Bună ziua! Sunt Thomas, de la Pacheco Studios, consultanță în sisteme cu IA.\n\n"
         "Am pregătit o demonstrație pentru {nome}: {demo}\n\n"
         "Dacă vă place, ne vedem în Iași și discutăm un potențial parteneriat: cum reducem la jumătate "
         "timpul pierdut cu programări și follow-up.\n\n"
         "Mai multe: ro.pachecost.com\n"
         "Voi fi pregătit.")


def numero(tel):
    d = "".join(c for c in tel if c.isdigit())
    return "40" + d[1:] if d.startswith("0") else d


def fixo(tel):
    d = "".join(c for c in tel if c.isdigit())
    return d.startswith("02") or d.startswith("03")


NOVO = False  # «novo» como 2.º argumento: texto da corrida B também na A (pedido de 11/10)


def main(caminho):
    linhas = list(csv.DictReader(open(caminho, encoding="utf-8"), delimiter="\t"))
    data = caminho.rsplit("/", 1)[-1].split(".")[0]
    pub = [l for l in linhas if l["estado"].strip() == "publicada"]
    desde = os.environ.get("DESDE")  # slug a partir do qual se imprime (os anteriores já foram enviados)
    if desde:
        ordem_pub = [l["slug"] for c in ("A", "B") for z in dict.fromkeys(l["zona"] for l in pub if l["corrida"] == c)
                     for l in pub if l["corrida"] == c and l["zona"] == z]
        pub = [l for l in pub if ordem_pub.index(l["slug"]) >= ordem_pub.index(desde)]
    print(f"# Caçador de Iași — {data}\n")
    print(f"{len(pub)} demos prontas. Nenhum número com «WhatsApp: ?» está confirmado: toca em **Abrir no WhatsApp**; "
          "se o WhatsApp disser que o número não está registado, usa **Enviar por SMS** (mesmo texto) ou passa lá "
          "com a demo aberta. Depois diz-me quais falharam.\n")
    print("**Envio:** no mínimo **1 minuto** entre mensagens (a 09/10 o WhatsApp bloqueou um dia por envios de 10 em 10 s). "
          "Cada mensagem leva o nome e a demo do negócio; mesmo assim, não as envies coladas.\n")
    if os.environ.get("NO_AR"):
        print("**As demos já estão no ar.**\n")
    else:
        print("**Atenção:** as demos só ficam no ar depois de mandares publicar (diz «publica» no thread do caçador). "
              "Envia as mensagens depois disso.\n")
    ordem = 0
    for corrida in ("A", "B"):
        grupo = [l for l in pub if l["corrida"] == corrida]
        if not grupo:
            continue
        print(f"## Corrida {corrida} ({'8h00' if corrida == 'A' else '11h30'})\n")
        for zona in dict.fromkeys(l["zona"] for l in grupo):
            print(f"### {zona}\n")
            for l in (x for x in grupo if x["zona"] == zona):
                demo = f"https://pachecost.com/demo/{l['slug']}/"
                if True:  # desde 11/10 as duas corridas usam MSG_B («Audit Hook by Demo»: a demo é o trabalho inicial, a triagem é a isca)
                    dono = (l.get("dono") or "").strip()
                    texto = MSG_B.format(tip=tip(l.get("categoria")), nome=l["nome"], demo=demo)
                else:
                    texto = MSG.format(saudacao=SAUDACOES[ordem % len(SAUDACOES)].format(nome=l["nome"]), demo=demo)
                ordem += 1
                q = urllib.parse.quote
                mapa = "https://www.google.com/maps/search/?api=1&query=" + q(f"{l['nome']}, {l['morada']}, Iași")
                print(f"#### {l['nome']}\nDemo: {demo}  \nTel.: {l['tel']} · WhatsApp: {l['whatsapp']}  \n"
                      f"Morada: [{l['morada']}]({mapa})  ")
                if fixo(l["tel"]):
                    print(f"Só telefone fixo: [Ligar](tel:+{numero(l['tel'])}) ou visita.\n")
                else:
                    n = numero(l["tel"])
                    print(f"[Abrir no WhatsApp](https://wa.me/{n}?text={q(texto, safe='/')}) · "
                          f"[Enviar por SMS](sms:+{n}?&body={q(texto, safe='/')})\n")
                print("> " + texto.replace("\n", "\n> ").replace("> \n", ">\n") + "\n")
    resto = [l for l in linhas if l["estado"].strip() != "publicada"]
    if resto:
        print("## Ainda sem demo\n\n| Corrida | Negócio | Tel. | Estado |\n|---|---|---|---|")
        for l in resto:
            print(f"| {l['corrida']} | {l['nome']} | {l['tel']} | {l['estado']} |")


if __name__ == "__main__":
    NOVO = sys.argv[2:3] == ["novo"]
    main(sys.argv[1])
