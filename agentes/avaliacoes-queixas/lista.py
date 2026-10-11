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

# Cada dor descreve a fuga operacional (RO, PT), sem ferramenta nem preço: a ferramenta sai da auditoria
# (Playbook de consultoria de IA, 11/10/2026: «primeiro mostrar a fuga, a regra e a ação seguinte»).
SOLUCAO = {
    "telefon": ("Când telefonul sună și toată lumea e ocupată, clientul sună la altcineva și nimeni nu află. "
                "Nu e o problemă de oameni, ci de sistem: cine răspunde, în cât timp și ce se întâmplă cu apelul pierdut.",
                "Quando o telefone toca e estão todos ocupados, o cliente liga a outro e ninguém fica a saber. "
                "Não é um problema de pessoas, é de sistema: quem atende, em quanto tempo e o que acontece à chamada perdida."),
    "mesaje": ("Când mesajele vin pe WhatsApp, Facebook și e-mail fără un responsabil clar, răspunsul întârzie și clientul pleacă. "
               "Nu e o problemă de oameni, ci de sistem: cine răspunde, în cât timp și cine preia ce rămâne în urmă.",
               "Quando as mensagens chegam por WhatsApp, Facebook e e-mail sem um responsável claro, a resposta atrasa e o cliente vai-se. "
               "Não é um problema de pessoas, é de sistema: quem responde, em quanto tempo e quem pega no que fica para trás."),
    "marcacoes": ("Când programările și comenzile trec prin mai multe mâini fără reguli clare, se pierd sau se încurcă. "
                  "Nu e o problemă de oameni, ci de sistem: cine confirmă, cum se verifică și ce se întâmplă când ceva se schimbă.",
                  "Quando as marcações e encomendas passam por várias mãos sem regras claras, perdem-se ou trocam-se. "
                  "Não é um problema de pessoas, é de sistema: quem confirma, como se verifica e o que acontece quando algo muda."),
}

MSG_RO = ("Bună ziua! Sunt Tomás, de la Pacheco Studios, din Iași. Lucrez cu firme de servicii pe sistemele cu IA "
          "care fac ca nicio cerere de client să nu rămână fără răspuns.\n\n"
          "{elogio_ro}Citind recenziile de pe Google pentru {nome}, am dat peste asta ({data}):\n„{citacao}”\n\n"
          "Nu vă scriu ca să vă critic. {solucao_ro}\n\n"
          "Vă propun 20 de minute: vă arăt unde se pierd aceste cereri și care ar fi primul pas cu cel mai mare impact. "
          "Când v-ar fi bine săptămâna aceasta?\n\n"
          "Mai multe despre noi: ro.pachecost.com")
MSG_PT = ("Bom dia! Sou o Tomás, da Pacheco Studios, de Iași. Trabalho com negócios de serviços nos sistemas com IA "
          "que fazem com que nenhum pedido de cliente fique sem resposta.\n\n"
          "{elogio_pt}A ler as avaliações de {nome} no Google, encontrei isto ({data_pt}):\n«{citacao_pt}»\n\n"
          "Não vos escrevo para criticar. {solucao_pt}\n\n"
          "Proponho-vos 20 minutos: mostro-vos onde se perdem estes pedidos e qual seria o primeiro passo com mais impacto. "
          "Quando vos dá jeito esta semana?\n\n"
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
           "Mais fortes primeiro. Cada mensagem cita a frase real do cliente, nomeia a fuga e pede 20 minutos (triagem para a Auditoria de Sistemas com IA; sem preço). "
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
