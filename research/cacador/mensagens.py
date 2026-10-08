#!/usr/bin/env python3
"""Gera a lista do dia do caçador (mensagens prontas, links WhatsApp e SMS, moradas) a partir de um TSV.

  python3 research/cacador/mensagens.py research/cacador/AAAA-MM-DD.tsv > research/cacador/AAAA-MM-DD.md

Colunas do TSV (com cabeçalho): corrida slug nome descricao tel whatsapp morada zona estado
  corrida   A (8h00) ou B (11h30)
  descricao como o negócio aparece na frase, com o artigo: «frizeria Noir Barbershop», «magazinul Arca Pet Iași»
  whatsapp  sim / ? / não (sim só com prova pública: PLAYBOOK §11 ponto 8)
  estado    publicada / por fazer / tirada (motivo)
Só as linhas «publicada» levam mensagem; as outras aparecem numa tabela no fim.
"""
import csv, sys, urllib.parse

MSG = ("Bună ziua! Sunt Tomás, de la Pacheco Studios.\n\n"
       "În acest moment sunt firme care își reduc costurile/își măresc eficiența cu 40% cu IA.\n\n"
       "Am început prin a vă crea un site profesional, pentru că am văzut că {descricao} nu are încă unul. "
       "Îl puteți vedea aici:\n{demo}\n\n"
       "Aș vrea să stabilim o oră să ne întâlnim și să vorbim despre implementarea acestei structuri, "
       "dacă sunteți interesați să faceți un nou pas în ceea ce privește actualitatea.\n\n"
       "Puteți vedea mai multe pe ro.pachecost.com")


def numero(tel):
    d = "".join(c for c in tel if c.isdigit())
    return "40" + d[1:] if d.startswith("0") else d


def fixo(tel):
    d = "".join(c for c in tel if c.isdigit())
    return d.startswith("02") or d.startswith("03")


def main(caminho):
    linhas = list(csv.DictReader(open(caminho, encoding="utf-8"), delimiter="\t"))
    data = caminho.rsplit("/", 1)[-1].split(".")[0]
    pub = [l for l in linhas if l["estado"].strip() == "publicada"]
    print(f"# Caçador de Iași — {data}\n")
    print(f"{len(pub)} demos prontas. Nenhum número com «WhatsApp: ?» está confirmado: toca em **Abrir no WhatsApp**; "
          "se o WhatsApp disser que o número não está registado, usa **Enviar por SMS** (mesmo texto) ou passa lá "
          "com a demo aberta. Depois diz-me quais falharam.\n")
    for corrida in ("A", "B"):
        grupo = [l for l in pub if l["corrida"] == corrida]
        if not grupo:
            continue
        print(f"## Corrida {corrida} ({'8h00' if corrida == 'A' else '11h30'})\n")
        for zona in dict.fromkeys(l["zona"] for l in grupo):
            print(f"### {zona}\n")
            for l in (x for x in grupo if x["zona"] == zona):
                demo = f"https://pachecost.com/demo/{l['slug']}/"
                texto = MSG.format(descricao=l["descricao"], demo=demo)
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
    main(sys.argv[1])
