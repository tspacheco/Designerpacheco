"""Lista de negócios do tracker das demos, tirada do ramo das demos.

  python3 tracker/sincronizar.py  ->  tracker/negocios.json

Lê a lista DEMOS do gerar.py (cada demo = um negócio), e o nome e o telefone dos
ficheiros de mensagens (CONTACTOS.md, LOTE*-IASI.md) e das tabelas de pesquisa
(research/*lote*-out26.md). O estado de cada negócio (enviado, respondeu...) não
vive aqui: vive na base de dados do Artifact «Tracker das demos», onde o Tomás o marca.
"""
import json, os, re, subprocess

RAMO = "origin/claude/dez-negocios-dez-websites-7gevwu"
AQUI = os.path.dirname(os.path.abspath(__file__))
ALGARVE = {"tasquinha-do-bruno", "tasca-do-to", "o-antonio", "colibri", "barbers-touch",
           "sr-bonifacio", "flor-mimosa", "faisca-henriques", "sos-car", "mb-cakes"}


def ler(caminho):
    try:
        return subprocess.run(["git", "show", f"{RAMO}:{caminho}"], capture_output=True,
                              text=True, check=True).stdout
    except subprocess.CalledProcessError:
        return ""


def ficheiros(pasta):
    out = subprocess.run(["git", "ls-tree", "--name-only", f"{RAMO}", pasta + "/"],
                         capture_output=True, text=True).stdout
    return out.split()


def demos():
    lote, lista = "Iași 1", []
    bloco = ler("sites/demos-pachecost/gerar.py").split("DEMOS = [", 1)[1].split("\n]", 1)[0]
    for i, linha in enumerate(bloco.splitlines()):
        m = re.search(r"#\s*lote\s*(\d+)", linha, re.I)
        if m:
            lote = f"Iași {m.group(1)}"
        m = re.search(r'\("([^"]+)",\s*"([^"]+)"\)', linha)
        if m:
            curto, pasta = m.groups()
            lista.append((curto, pasta, "Algarve" if curto in ALGARVE else lote))
    # os lotes 1 e 2 não têm comentário no gerar.py: 10 + 10 por ordem
    n = 0
    for k, (c, p, l) in enumerate(lista):
        if l == "Iași 1" and c not in ALGARVE:
            lista[k] = (c, p, "Iași 1" if n < 10 else "Iași 2"); n += 1
    return lista


def contactos():
    """curto -> (nome, telefone) a partir dos ficheiros de mensagens."""
    r = {}
    for f in ficheiros("sites/demos-pachecost"):
        if not f.endswith(".md"):
            continue
        txt = ler(f)
        # formato «### Nome» / «Demo: …/demo/x/» / «Tel.: …»
        for bl in re.split(r"\n(?=### )", txt):
            m = re.match(r"### (.+)", bl)
            d = re.search(r"/demo/([a-z0-9-]+)/", bl)
            t = re.search(r"Tel\.?:\s*([^·\n]+)", bl)
            if m and d and d.group(1) not in r:
                r[d.group(1)] = (m.group(1).strip(), t.group(1).strip() if t else "")
        # formato «1. **Nome**» / «Demo: …» / «Telemóvel: …» (CONTACTOS.md)
        for m in re.finditer(r"\*\*(.+?)\*\*\s*\n\s*Demo: \S*/demo/([a-z0-9-]+)/\s*\n\s*Telemóvel: ([^·\n]+)", txt):
            nome, curto, tel = m.groups()
            r.setdefault(curto, (nome.strip(), tel.strip()))
    return r


def pesquisa():
    """pasta -> (nome, telefone) das tabelas research/*lote*.md (lotes sem ficheiro de mensagens)."""
    r = {}
    for f in ficheiros("research"):
        if re.search(r"lote\d+-out26\.md$", f):
            for linha in ler(f).splitlines():
                c = [x.strip() for x in linha.strip("|").split("|")]
                if len(c) > 4 and c[1].startswith("`"):
                    r.setdefault(c[1].strip("`"), (c[0], c[4]))
    return r


def titulo(pasta):
    m = re.search(r"<title>([^<]+)</title>", ler(f"sites/{pasta}/index.html"))
    return re.split(r"\s+[—|·–-]\s+", m.group(1))[0].strip() if m else pasta


def main():
    subprocess.run(["git", "fetch", "-q", "origin", RAMO.split("/", 1)[1]], check=False)
    cont, pesq = contactos(), pesquisa()
    out = []
    for curto, pasta, lote in demos():
        nome, tel = cont.get(curto) or pesq.get(pasta) or (titulo(pasta), "")
        out.append({"id": curto, "nome": nome, "tel": tel, "lote": lote,
                    "demo": f"https://pachecost.com/demo/{curto}/"})
    with open(os.path.join(AQUI, "negocios.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"{len(out)} negócios -> tracker/negocios.json")


if __name__ == "__main__":
    main()
