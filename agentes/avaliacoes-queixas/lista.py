#!/usr/bin/env python3
"""Gera a lista do dia do agente 8 a partir do que o recolher.py gravou.

  python3 lista.py dados/AAAA-MM-DD.json            → listas/AAAA-MM-DD.md (e candidatos/AAAA-MM-DD.json)

Fica na lista cada ficha com pelo menos uma avaliação que bate numa dor do queixas.py e que ainda não foi listada
(listas/listadas.txt). A mensagem em romeno cita a frase real da avaliação; a versão PT por baixo é para o Tomás.
As traduções PT das citações vêm de traducoes/AAAA-MM-DD.json ({id_avaliacao: "texto PT"}), escritas pelo Claude
depois de ver candidatos/AAAA-MM-DD.json; sem tradução, aparece «(tradução por fazer)».
"""
import json, os, re, sys, urllib.parse
from queixas import dores, NOME

AQUI = os.path.dirname(os.path.abspath(__file__))
PRIORIDADE = {"telefon": 0, "mesaje": 1, "marcacoes": 2}
MAX_MESES = 24  # queixas mais antigas não se citam

# Cada dor tem a sua frase de solução (RO, PT). Sem números: os números saem da auditoria.
SOLUCAO = {
    "telefon": ("Se întâmplă des la firmele care au mult de lucru: telefonul sună exact când toată lumea e ocupată. "
                "Azi se poate rezolva cu un asistent IA care preia apelurile pierdute, răspunde imediat pe SMS sau "
                "WhatsApp și preia programarea, rezervarea sau comanda în locul dumneavoastră.",
                "Acontece muito em negócios com muito trabalho: o telefone toca precisamente quando estão todos "
                "ocupados. Hoje resolve-se com um assistente de IA que apanha as chamadas perdidas, responde logo por "
                "SMS ou WhatsApp e regista a marcação, a reserva ou a encomenda por vocês."),
    "mesaje": ("Se întâmplă des la firmele care au mult de lucru: mesajele se adună și răspunsul vine prea târziu. "
               "Azi se poate rezolva cu un asistent IA care răspunde în câteva secunde pe WhatsApp, Facebook și "
               "Instagram, cu informațiile dumneavoastră, și vă lasă doar ce are nevoie de un om.",
               "Acontece muito em negócios com muito trabalho: as mensagens acumulam-se e a resposta chega tarde. "
               "Hoje resolve-se com um assistente de IA que responde em segundos no WhatsApp, Facebook e Instagram, "
               "com as vossas informações, e só vos passa o que precisa de uma pessoa."),
    "marcacoes": ("Se întâmplă des la firmele care au mult de lucru: programările și comenzile trec prin prea multe "
                  "mâini. Azi se poate rezolva cu un sistem care primește programarea sau comanda online, o confirmă "
                  "și trimite singur reamintirea, fără nimic scris pe hârtie.",
                  "Acontece muito em negócios com muito trabalho: as marcações e encomendas passam por demasiadas "
                  "mãos. Hoje resolve-se com um sistema que recebe a marcação ou a encomenda online, confirma-a e "
                  "envia sozinho o lembrete, sem nada escrito em papel."),
}

MSG_RO = ("Bună ziua! Sunt Tomás, de la Pacheco Studios, din Iași.\n\n"
          "{elogio_ro}Citind recenziile de pe Google pentru {nome}, am dat peste asta ({data}):\n„{citacao}”\n\n"
          "Nu vă scriu ca să vă critic. {solucao_ro}\n\n"
          "Vă propun o auditare gratuită a firmei: unde se pierd clienți și ce se poate automatiza, cu IA. "
          "Aveți 20 de minute săptămâna aceasta să ne vedem?\n\n"
          "Mai multe despre noi: ro.pachecost.com")
MSG_PT = ("Bom dia! Sou o Tomás, da Pacheco Studios, de Iași.\n\n"
          "{elogio_pt}A ler as avaliações de {nome} no Google, encontrei isto ({data_pt}):\n«{citacao_pt}»\n\n"
          "Não vos escrevo para criticar. {solucao_pt}\n\n"
          "Proponho-vos uma auditoria grátis ao negócio: onde se perdem clientes e o que se pode automatizar, com IA. "
          "Têm 20 minutos esta semana para nos vermos?\n\n"
          "Mais sobre nós: ro.pachecost.com")

DATA_PT = [("acum o zi", "há um dia"), ("acum o săptămână", "há uma semana"), ("acum o lună", "há um mês"),
           ("acum un an", "há um ano"), ("de zile", "dias"), ("zile", "dias"), ("de săptămâni", "semanas"),
           ("săptămâni", "semanas"), ("de luni", "meses"), ("luni", "meses"), ("de ani", "anos"), ("ani", "anos"),
           ("acum", "há")]


def data_pt(d):
    d = d.replace("Modificat pe ", "")
    for a, b in DATA_PT:
        d = d.replace(a, b)
    return d


def idade_meses(d):
    """«acum 3 luni» → 3; desconhecida → 99. Para ordenar por recência."""
    d = (d or "").lower()
    m = re.search(r"(\d+)", d)
    n = int(m.group(1)) if m else 1
    if "zi" in d or "or" in d or "minut" in d:
        return 0
    if "săpt" in d or "sapt" in d:
        return 0
    if "lun" in d:
        return n
    if "an" in d:
        return 12 * n
    return 99


def numero(tel):
    d = "".join(c for c in tel or "" if c.isdigit())
    if d.startswith("40"):
        return d
    return "40" + d[1:] if d.startswith("0") else d


def fixo(tel):
    d = numero(tel)
    return d.startswith("402") or d.startswith("403")


def main(caminho):
    fichas = json.load(open(caminho, encoding="utf-8"))
    data = os.path.basename(caminho).split(".")[0]
    listadas_p = os.path.join(AQUI, "listas", "listadas.txt")
    listadas = set(open(listadas_p, encoding="utf-8").read().split("\n")) if os.path.exists(listadas_p) else set()
    trad_p = os.path.join(AQUI, "traducoes", f"{data}.json")
    trad = json.load(open(trad_p, encoding="utf-8")) if os.path.exists(trad_p) else {}
    excluir = trad.pop("_excluir", {})  # {nome: motivo}, decidido pelo Claude ao rever os candidatos

    leads = []
    for f in fichas:
        if f.get("chave") in listadas or f.get("nome") in excluir:
            continue
        achados = []
        for a in f.get("avaliacoes", []):
            if idade_meses(a.get("data")) > MAX_MESES:
                continue
            for dor, frase in dores(a.get("texto", "")):
                achados.append({"dor": dor, "frase": frase, **a})
        if not achados:
            continue
        achados.sort(key=lambda x: (PRIORIDADE[x["dor"]], idade_meses(x.get("data")), len(x["frase"]) > 280))
        escolhida = achados[0]
        leads.append({**f, "achados": achados, "escolhida": escolhida})
    # Mais forte primeiro: dor de telefone/mensagens, várias queixas, queixa recente, ficha com muitas avaliações.
    leads.sort(key=lambda l: (PRIORIDADE[l["escolhida"]["dor"]], -len(l["achados"]),
                              idade_meses(l["escolhida"].get("data")), -(l.get("n_avaliacoes") or 0)))

    os.makedirs(os.path.join(AQUI, "candidatos"), exist_ok=True)
    json.dump([{"id": l["escolhida"]["id"], "nome": l["nome"], "frase": l["escolhida"]["frase"],
                "texto": l["escolhida"]["texto"]} for l in leads],
              open(os.path.join(AQUI, "candidatos", f"{data}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    q = urllib.parse.quote
    out = [f"# Avaliações com queixas — Iași, {data}\n",
           f"{len(leads)} negócios com clientes a queixarem-se de telefone, mensagens ou marcações nas avaliações "
           f"Google ({sum(len(f.get('avaliacoes', [])) for f in fichas)} avaliações lidas em {len(fichas)} fichas). "
           "Mais fortes primeiro. Cada mensagem cita a frase real do cliente e propõe a auditoria grátis e 20 minutos. "
           "WhatsApp «?» = sem prova: toca em **Abrir no WhatsApp**; se não estiver registado, **Enviar por SMS** "
           "ou passa lá. Depois diz-me quais responderam e quais falharam.\n"]
    for i, l in enumerate(leads, 1):
        e = l["escolhida"]
        nota = l.get("nota")
        elogio_ro = elogio_pt = ""
        if nota and nota >= 4.3 and l.get("n_avaliacoes"):
            n_str = f"{nota:.1f}".replace(".", ",")
            n_av = f"{l['n_avaliacoes']:,}".replace(",", ".")
            elogio_ro = f"Am văzut că aveți {n_str} pe Google din {n_av} de recenzii, felicitări. "
            elogio_pt = f"Vi que têm {n_str} no Google em {n_av} avaliações, parabéns. "
        t = trad.get(e["id"], "(tradução por fazer)")
        if isinstance(t, dict):  # {"ro": excerto literal da frase, "pt": tradução}
            e["frase"], cit_pt = t["ro"], t["pt"]
        else:
            cit_pt = t
        ro = MSG_RO.format(elogio_ro=elogio_ro, nome=l["nome"], data=e.get("data", "").replace("Modificat pe ", ""), citacao=e["frase"],
                           solucao_ro=SOLUCAO[e["dor"]][0])
        pt = MSG_PT.format(elogio_pt=elogio_pt, nome=l["nome"], data_pt=data_pt(e.get("data", "")),
                           citacao_pt=cit_pt, solucao_pt=SOLUCAO[e["dor"]][1])
        tel = l.get("tel") or ""
        wa = l.get("whatsapp") or ("?" if tel and not fixo(tel) else "não (fixo)" if tel else "sem número")
        out.append(f"## {i}. {l['nome']}\n")
        nota_txt = f"{nota:.1f}".replace(".", ",") if nota else "?"
        out.append(f"{l.get('categoria') or ''} · Google {nota_txt} ({l.get('n_avaliacoes') or '?'}) · "
                   f"dor: **{NOME[e['dor']]}** ({len(l['achados'])} avaliação(ões)) · "
                   f"site: {l.get('site') or 'não tem'}  ")
        mapa = l.get("url") or ("https://www.google.com/maps/search/?api=1&query=" + q(f"{l['nome']}, Iași"))
        out.append(f"Tel.: {tel or '—'} · WhatsApp: {wa}  \nMorada: [{l.get('morada') or 'ver no Maps'}]({mapa})  ")
        if tel and fixo(tel):
            out.append(f"Só telefone fixo: [Ligar](tel:+{numero(tel)}) ou visita.\n")
        elif tel:
            n = numero(tel)
            out.append(f"[Abrir no WhatsApp](https://wa.me/{n}?text={q(ro, safe='/')}) · "
                       f"[Enviar por SMS](sms:+{n}?&body={q(ro, safe='/')})\n")
        else:
            out.append("Sem telefone na ficha: visita.\n")
        out.append("> " + ro.replace("\n", "\n> ").replace("> \n", ">\n") + "\n")
        out.append("<details><summary>Versão PT</summary>\n\n" + pt.replace("\n", "  \n") + "\n</details>\n")
        if len(l["achados"]) > 1:
            out.append("Outras queixas: " + " · ".join(f"«{a['frase'][:140]}» ({a.get('data', '')})"
                                                     for a in l["achados"][1:4]) + "\n")
    if excluir:
        out.append("## Tirados na revisão\n\n| Negócio | Motivo |\n|---|---|")
        out += [f"| {n} | {m} |" for n, m in excluir.items()]
    os.makedirs(os.path.join(AQUI, "listas"), exist_ok=True)
    open(os.path.join(AQUI, "listas", f"{data}.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    print(f"{len(leads)} leads → listas/{data}.md")


if __name__ == "__main__":
    main(sys.argv[1])
