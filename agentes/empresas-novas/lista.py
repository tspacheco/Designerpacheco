#!/usr/bin/env python3
"""Agente 7: lista do dia para o Tomás a partir de dados/iasi-*.json (gerados pelo recolher.py no GitHub).

  python3 lista.py [--dias 14] [--saida listas/AAAA-MM-DD.md]

Fica com as empresas do distrito de Iași registadas nos últimos <dias>, ativas, com CAEN de negócio local
(clientes à porta ou serviços ao domicílio) e ainda não listadas (listas/listadas.txt). Para cada uma: mensagem
em romeno com uma demo do mesmo ramo como exemplo, links WhatsApp e SMS e a morada do registo.
"""
import argparse, datetime, glob, json, os, re, urllib.parse

AQUI = os.path.dirname(os.path.abspath(__file__))
LISTAS = os.path.join(AQUI, "listas")
LISTADAS = os.path.join(LISTAS, "listadas.txt")
DEMO = "https://pachecost.com/demo/{}/"

# (prefixos CAEN — Rev. 2 e Rev. 3, ramo em romeno, ramo em PT, demo de exemplo, prioridade 1 = clientes à porta)
RAMOS = [
    (("5610", "5611", "5612", "5621", "5622", "5629"), "restaurant", "restaurante", "bistro-felix", 1),
    (("5630", "5631", "5640"), "cafenea", "café/bar", "fika", 1),
    (("1071", "1072", "1073", "1081", "1082", "1089"), "brutărie / cofetărie", "padaria/pastelaria", "brutaria-rustica", 1),
    (("9602", "9621"), "frizerie / salon", "cabeleireiro/barbearia", "gemino-barbershop", 1),
    (("9622",), "salon de înfrumusețare", "estética", "peony-beauty", 1),
    (("9604", "9623"), "salon de masaj / spa", "massagem/spa", "kineos-massage", 1),
    (("9313",), "sală de fitness", "ginásio", "acm-masaj", 1),
    (("4520", "4532", "4540", "9531"), "service auto", "oficina", "service-la-pici", 1),
    (("7500",), "cabinet veterinar", "veterinário", "pumbavet", 1),
    (("9609", "9699", "9690"), "salon / servicii pentru animale", "serviços (animais, tatuagem…)", "fevila-pet-spa", 1),
    (("4776", "4778"), "florărie / magazin", "florista/loja", "elenor", 1),
    (("4722",), "măcelărie", "talho", "carmangerie-spinu", 1),
    (("4725",), "vinotecă", "garrafeira", "bonvino", 1),
    (("4771", "4772", "4777", "4779", "4775"), "magazin", "loja", "petit-bijou", 1),
    (("9529", "9523", "9525", "9524", "9521", "9522", "9539", "9599"), "atelier de reparații", "oficina de reparações", "ceasornicarie-nicolina", 1),
    (("1413", "1414", "1419"), "atelier de croitorie", "costura", "croitoria-dan", 1),
    (("9601", "9610"), "spălătorie", "lavandaria", "exclusive-laundry", 1),
    (("8621", "8622", "8623", "8690", "8691", "8692", "8693", "8694", "8695", "8696", "8699"), "cabinet medical", "clínica", "estetica-new-shape", 1),
    (("8551", "8552", "8553", "8559", "8891"), "școală / centru", "escola/centro", "fika", 2),
    (("7420", "7421", "7422"), "studio foto", "estúdio de fotografia", "frame-art", 2),
    (("5510", "5520"), "pensiune", "alojamento", "bistro-felix", 2),
    (("4321", "4322", "4329", "4331", "4332", "4333", "4334", "4339", "4341", "4342"), "firmă de instalații / finisaje", "instalações/acabamentos", "interventii-rapide", 2),
    (("8121", "8122", "8129", "8130"), "firmă de curățenie", "limpezas", "exclusive-laundry", 2),
    (("8020", "8010"), "firmă de securitate / lăcătușerie", "segurança/serralharia", "magic-key", 2),
]


def ramo(caen):
    c = re.sub(r"\D", "", str(caen or ""))[:4]
    for prefixos, ro, pt, demo, prio in RAMOS:
        if c in prefixos:
            return ro, pt, demo, prio
    return None


def data(s):
    try:
        return datetime.date.fromisoformat(str(s)[:10])
    except ValueError:
        return None


def telefone(t):
    d = re.sub(r"\D", "", t or "")
    if d.startswith("40"):
        d = "0" + d[2:]
    if d.startswith("0040"):
        d = "0" + d[4:]
    if len(d) != 10 or not d.startswith("0"):
        return None, None
    return d, ("móvel" if d.startswith("07") else "fixo")


PESSOA = r"(PERSOAN[AĂ] FIZIC[AĂ] AUTORIZAT[AĂ]|[IÎ]NTREPRINDERE (INDIVIDUAL|FAMILIAL)[AĂ]|P\.?F\.?A\.?|I\.?I\.?|I\.?F\.?)"


def nome_curto(den):
    """(nome para mostrar, é pessoa singular?) — PFA/II/IF têm o nome do dono, não uma marca."""
    n = re.sub(r"\s*-?\s*SEDIU SECUNDAR\s*$", "", den.strip(), flags=re.I)
    pessoa = bool(re.search(r"\s" + PESSOA + r"\s*$", n, flags=re.I))
    n = re.sub(r"\s+" + PESSOA + r"\s*$", "", n, flags=re.I)
    n = re.sub(r"\s*\b(S\.?R\.?L\.?(-D)?|SRL-D|S\.?A\.?)\s*$", "", n, flags=re.I)
    return n.strip(" .-").title(), pessoa


def mensagem(nome, ramo_ro, demo, pessoa=False, filial=False):
    quem = "firma dumneavoastră" if pessoa else nome
    abre = (f"Am văzut că {quem} deschide un nou punct de lucru în Iași. Felicitări și mult succes!" if filial else
            f"Am văzut că {quem} s-a înregistrat de curând. Felicitări și mult succes la început de drum!")
    return (f"Bună ziua! Sunt Tomás, de la Pacheco Studios.\n\n{abre}\n\n"
            f"În acest moment sunt firme care își reduc costurile/își măresc eficiența cu 40% cu IA. "
            f"Noi începem cu un site profesional. Uitați un exemplu făcut pentru o afacere din Iași:\n{DEMO.format(demo)}\n\n"
            f"Vă pot pregăti unul la fel pentru {quem}, ca să vă găsească clienții pe Google din prima zi. "
            f"Aș vrea să stabilim o oră să ne întâlnim, dacă vă interesează.\n\n"
            f"Puteți vedea mais multe pe ro.pachecost.com").replace("mais multe", "mai multe")


def mensagem_pt(nome, ramo_pt, pessoa=False):
    quem = "a vossa empresa" if pessoa else f"a {nome}"
    return (f"Olá! Sou o Tomás, da Pacheco Studios. Vi que {quem} foi registada há pouco. Parabéns e boa sorte neste início! "
            f"Neste momento há empresas que reduzem custos/aumentam a eficiência em 40% com IA. Nós começamos por um site profissional. "
            f"Aqui está um exemplo feito para um negócio de Iași: [demo]. Posso preparar-vos um igual, para os clientes vos encontrarem "
            f"no Google desde o primeiro dia. Gostava de marcar uma hora para nos encontrarmos, se tiverem interesse. Mais em ro.pachecost.com")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dias", type=int, default=14)
    ap.add_argument("--saida")
    ap.add_argument("--todas", action="store_true", help="não excluir as já listadas")
    a = ap.parse_args()
    hoje = datetime.date.today()
    os.makedirs(LISTAS, exist_ok=True)
    listadas = set(open(LISTADAS).read().split()) if os.path.exists(LISTADAS) and not a.todas else set()
    empresas = {}
    for f in sorted(glob.glob(os.path.join(AQUI, "dados", "iasi-*.json"))):
        for x in json.load(open(f)):
            empresas[str(x["cui"])] = x
    cand = []
    for c, x in empresas.items():
        d = data(x.get("data_inregistrare"))
        r = ramo(x.get("caen"))
        if c in listadas or not d or not r or (hoje - d).days > a.dias:
            continue
        if not x.get("nrRegCom") and "SEDIU SECUNDAR" not in (x.get("denumire") or "").upper():
            continue  # sem número do Registo Comercial = profissão liberal (médico colaborador, assistente…), não é loja
        if "RADIERE" in (x.get("stare") or "").upper() or "INACTIV" in (x.get("stare") or "").upper():
            continue
        tel, tipo = telefone(x.get("telefon"))
        cand.append((r[3], 0 if tipo == "móvel" else 1 if tipo else 2, -d.toordinal(), c, x, r, tel, tipo, d))
    cand.sort()
    saida = a.saida or os.path.join(LISTAS, f"{hoje.isoformat()}.md")
    L = [f"# Empresas acabadas de abrir em Iași — {hoje.strftime('%d/%m/%Y')}", "",
         f"Registadas nos últimos {a.dias} dias, ativas, de negócio local. {len(cand)} novas nesta lista.",
         "O telefone é o que a empresa declarou à ANAF: às vezes é do contabilista. WhatsApp: ? em todas (sem prova pública).",
         "A morada é a sede no registo: pode ser casa do dono, não a loja. Visita só se o Maps mostrar o espaço.", ""]
    secao, ja = None, set()
    for prio, _, _, c, x, (ro, pt, demo, _p), tel, tipo, d in cand:
        s = "Clientes à porta" if prio == 1 else "Serviços (obras, limpezas, escolas…)"
        if s != secao:
            L += [f"## {s}", ""]
            secao = s
        nome, pessoa = nome_curto(x["denumire"])
        if nome in ja:
            continue
        ja.add(nome)
        filial = "SEDIU SECUNDAR" in x["denumire"].upper()
        msg = mensagem(nome, ro, demo, pessoa, filial)
        if filial:
            pt = pt + " (novo espaço de uma empresa que já existe: ver antes se já tem site)"
        morada = x.get("adresa") or ""
        L.append(f"### {nome}" + (" (PFA/II, nome do dono)" if pessoa else ""))
        L.append(f"{pt.capitalize()} · CAEN {x.get('caen')} · registada a {d.strftime('%d/%m')} · CUI {c}  ")
        L.append(f"Firma: {x['denumire']} ({x.get('nrRegCom') or '?'})  ")
        L.append(f"Sede: [{morada.title()}](https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(morada)})  ")
        if tel:
            wa = "40" + tel[1:]
            q = urllib.parse.quote(msg)
            fone = f"{tel[:4]} {tel[4:7]} {tel[7:]}"
            if tipo == "móvel":
                L.append(f"Tel.: {fone} ({tipo}) · WhatsApp: ?  ")
                L.append(f"[Abrir no WhatsApp](https://wa.me/{wa}?text={q}) · [Enviar por SMS](sms:+{wa}?&body={q})")
            else:
                L.append(f"Tel.: {fone} (fixo, só chamada) · WhatsApp: não (fixo)")
        else:
            L.append("Tel.: sem telefone no registo · procurar no Google/Facebook pelo nome antes de enviar")
        L += ["", "> " + msg.replace("\n", "\n> "), "", f"<details><summary>PT</summary>{mensagem_pt(nome, pt, pessoa)}</details>", ""]
    open(saida, "w").write("\n".join(L) + "\n")
    with open(LISTADAS, "a") as f:
        f.write("".join(f"{c[3]}\n" for c in cand))
    print(f"{len(cand)} empresas -> {saida}")


if __name__ == "__main__":
    main()
