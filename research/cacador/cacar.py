#!/usr/bin/env python3
"""Modo economia do caçador (pedido do Tomás, 09/10): a pesquisa corre em scripts e só imprime contagens curtas.
Nunca abrir à mão os .html/.txt da ponte nem o vistos.tsv inteiro: estes comandos fazem o trabalho.

  python3 research/cacador/cacar.py pesquisas AAAAMMDD [n]   próximas n pesquisas da fila (pesquisas.txt) → .github/ponte.txt (listamaps)
  python3 research/cacador/cacar.py lista AAAAMMDD           lê as listas da ponte → candidatos-AAAAMMDD.tsv (sem site próprio, nota ≥ 4,3, ≥ 15 avaliações, fora da exclusão)
  python3 research/cacador/cacar.py fichas AAAAMMDD [n]      próximos n candidatos (≤ 25) → .github/ponte.txt (fichamaps: ficha + fotos num só pedido)
  python3 research/cacador/cacar.py dia AAAAMMDD             lê as fichas → vistos.tsv; escreve/completa AAAA-MM-DD.tsv (25 A + 25 B) e fotos-AAAAMMDD.txt
  python3 research/cacador/cacar.py fotos AAAAMMDD A|B       pedidos «imagem» das fotos da corrida → .github/ponte.txt

Depois de cada «→ .github/ponte.txt»: commit + push e `bash research/cacador/esperar.sh` (uma só chamada que espera pelo commit da ponte).
"""
import csv, glob, html, os, re, sys, unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
R = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, AQUI)
from excluir import chave, todas  # noqa: E402
from fichas import REDES, ficha  # noqa: E402

CADEIAS = ("dr. max", "catena", "sensiblu", "help net", "mega image", "kaufland", "lidl", "profi", "penny", "carrefour",
           "auchan", "starbucks", "mcdonald", "kfc", "vodafone", "orange", "telekom", "digi", "petrom", "omv", "lukoil",
           "rompetrol", "socar", "5 to go", "ted's", "salad box", "spartan", "fornetti", "luca", "pepco", "flanco",
           "altex", "emag", "fan courier", "sameday", "cargus", "pizza hut", "subway", "vianor", "euromaster", "dodo pizza",
           "paul", "la doi pași", "artima", "annabella", "jysk", "dedeman", "brico", "leroy", "hornbach", "decathlon")
FORA_CAT = ("hotel", "centru comercial", "farmacie", "medicamente", "supermarket", "hipermarket", "benzin", "bancă",
            "spital", "universitate", "parc", "biseric", "mănăstire", "primărie", "școală", "grădiniță", "muzeu", "atm")
CAB_DIA = "corrida slug nome descricao tel whatsapp morada zona estado ficha categoria nota avaliacoes horario presenca".split()


def slug(s, n=3):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    p = [w for w in re.split(r"[^a-z0-9]+", s) if w and w not in ("iasi", "srl", "the")]
    return "-".join(p[:n]) or "negocio"


def ponte(linhas, titulo):
    open(f"{R}/.github/ponte.txt", "w", encoding="utf-8").write(f"# caçador — {titulo}\n" + "\n".join(linhas) + "\n")
    print(f"{len(linhas)} pedidos em .github/ponte.txt ({titulo})")


def pesquisas(data, n=12):
    fila = [l.strip() for l in open(f"{AQUI}/pesquisas.txt", encoding="utf-8") if l.strip() and not l.startswith("#")]
    feitas = {os.path.basename(f).split("-l-", 1)[1][:-5] for f in glob.glob(f"{R}/ponte/cc-*-l-*.html")}
    out = []
    for l in fila:
        termo, _, zona = l.partition("|")
        nome = slug(f"{termo} {zona}", 6)
        if nome in feitas:
            continue
        q = "+".join(f"{termo} {zona} Iași".split())
        out.append(f"listamaps cc-{data}-l-{nome} https://www.google.com/maps/search/{q}?hl=ro")
        if len(out) == n:
            break
    ponte(out, f"pesquisas {data}")
    if len(out) < n:
        print(f"AVISO: a fila de pesquisas.txt só tinha {len(out)} por fazer; acrescentar termos novos")


def cartoes(f):
    h = open(f, encoding="utf-8").read()
    zona = os.path.basename(f).split("-l-", 1)[1][:-5]
    pos = [m.start() for m in re.finditer(r'<a class="hfpxzc"', h)] + [len(h)]
    for a, b in zip(pos, pos[1:]):
        s = h[a:b]
        nome = html.unescape((re.search(r'aria-label="([^"]+)"', s) or [0, ""])[1])
        link = html.unescape((re.search(r'href="(https://www\.google\.com/maps/place/[^"]+)"', s) or [0, ""])[1])
        nota = (re.search(r'aria-label="(\d,\d) stele', s) or [0, ""])[1]
        m = re.search(r'aria-label="\d,\d stele ([\d.]+) (?:de )?recenzii"', s)
        aval = int(m.group(1).replace(".", "")) if m else 0
        site = html.unescape((re.search(r'href="([^"]+)"[^>]*data-value="Site"', s) or
                              re.search(r'data-value="Site"[^>]*href="([^"]+)"', s) or [0, ""])[1])
        t = re.sub(r"<style.*?</style>|<script.*?</script>", "", s, flags=re.S)
        t = [x.strip() for x in re.split(r"(?:<[^>]+>)+", html.unescape(t)) if x.strip() and x.strip() != "·"]
        cat, depois = "", False
        for x in t[1:]:
            if x == nota:
                depois = True
            elif re.fullmatch(r"\(([\d.]+)\)", x):
                aval = aval or int(x.strip("()").replace(".", ""))
            elif depois and not re.search(r"lei|^[\d\s,.+–-]+$|^[\ue000-\uf8ff·]", x):
                cat = x
                break
        tel = next((x for x in t if re.fullmatch(r"(?:\+40 |0)\d{2,3}[ \d]{6,9}", x)), "")
        yield dict(nome=nome, nota=nota, aval=aval, site=site, cat=cat, tel=tel, link=link, zona=zona)


def lista(data):
    excl, saida, contas = todas(), {}, dict(cartoes=0, site=0, nota=0, cadeia=0, visto=0)
    for f in sorted(glob.glob(f"{R}/ponte/cc-{data}-l-*.html")):
        for c in cartoes(f):
            contas["cartoes"] += 1
            k = chave(c["nome"])
            if not c["nome"] or k in saida:
                continue
            if c["site"] and not any(r in c["site"] for r in REDES):
                contas["site"] += 1
                continue
            if not c["nota"] or float(c["nota"].replace(",", ".")) < 4.3 or 0 < c["aval"] < 15:
                contas["nota"] += 1
                continue
            if any(x in c["nome"].lower() for x in CADEIAS) or any(x in c["cat"].lower() for x in FORA_CAT):
                contas["cadeia"] += 1
                continue
            if k in excl:
                contas["visto"] += 1
                continue
            c["forca"] = round(float(c["nota"].replace(",", ".")) * min(c["aval"] or 40, 400))  # sem contagem na lista: a ficha confirma
            saida[k] = c
    cand = sorted(saida.values(), key=lambda c: -c["forca"])
    with open(f"{AQUI}/candidatos-{data}.tsv", "w", encoding="utf-8", newline="") as o:
        w = csv.writer(o, delimiter="\t")
        w.writerow("slug nome categoria nota avaliacoes tel presenca zona forca ficha".split())
        for c in cand:
            w.writerow([slug(c["nome"]), c["nome"], c["cat"], c["nota"], c["aval"], c["tel"], c["site"], c["zona"], c["forca"], c["link"]])
    print(f"{len(cand)} candidatos em candidatos-{data}.tsv | cartões {contas['cartoes']}, com site próprio {contas['site']}, "
          f"nota/avaliações baixas {contas['nota']}, cadeias {contas['cadeia']}, já vistos {contas['visto']}")
    cats = {}
    for c in cand:
        cats[c["cat"]] = cats.get(c["cat"], 0) + 1
    print("categorias: " + ", ".join(f"{k} {v}" for k, v in sorted(cats.items(), key=lambda x: -x[1])[:12]))


def fichas(data, n=25):
    cand = list(csv.DictReader(open(f"{AQUI}/candidatos-{data}.tsv", encoding="utf-8"), delimiter="\t"))
    abertas = {os.path.basename(f).split("-x-", 1)[1][:-5] for f in glob.glob(f"{R}/ponte/cc-*-x-*.html")}
    out = [f"fichamaps cc-{data}-x-{c['slug']} {c['ficha']}" for c in cand if c["slug"] not in abertas][:min(n, 25)]
    ponte(out, f"fichas {data}")


def dia(data):
    d = f"{data[:4]}-{data[4:6]}-{data[6:]}"
    cand = {c["slug"]: c for c in csv.DictReader(open(f"{AQUI}/candidatos-{data}.tsv", encoding="utf-8"), delimiter="\t")}
    vpath = f"{AQUI}/vistos.tsv"
    vistos = {l.split("\t")[1] for l in open(vpath, encoding="utf-8").read().splitlines()[1:] if "\t" in l}
    novos, sem = [], []
    for f in sorted(glob.glob(f"{R}/ponte/cc-{data}-x-*.html")):
        r = ficha(f)
        s = os.path.basename(f).split("-x-", 1)[1][:-5]
        c = cand.get(s, {})
        aval = int((r[4] or "0").replace(".", ""))
        nota = float((r[3] or "0").replace(",", "."))
        res = ("site próprio" if r[5] else "sem contacto/fora" if not r[6] else
               "fora (nota/avaliações)" if nota < 4.3 or aval < 15 else "sem site")
        if s not in vistos:
            novos.append([d, s, r[1] or c.get("nome", ""), r[2] or c.get("categoria", ""), r[3], r[4], r[5], res, c.get("ficha", "")])
        if res == "sem site":
            sem.append(dict(slug=s, nome=r[1], tel=r[6], whatsapp=r[10], morada=r[7], zona=c.get("zona", ""),
                            ficha=f"ponte/cc-{data}-x-{s}", categoria=r[2], nota=r[3], avaliacoes=r[4], horario=r[8],
                            presenca=r[9], forca=str(round(nota * min(aval, 400)))))
    with open(vpath, "a", encoding="utf-8") as o:
        for v in novos:
            o.write("\t".join(v) + "\n")
    tpath = f"{AQUI}/{d}.tsv"
    linhas = list(csv.DictReader(open(tpath, encoding="utf-8"), delimiter="\t")) if os.path.exists(tpath) else []
    ja = {l["slug"] for l in linhas}
    sem = sorted((x for x in sem if x["slug"] not in ja), key=lambda x: -int(x["forca"] or 0))
    for x in sem:
        if len(linhas) >= 50:
            break
        x["corrida"] = "A" if sum(l["corrida"] == "A" for l in linhas) < 25 else "B"
        x.update(descricao="", estado="por fazer")
        linhas.append(x)
    with open(tpath, "w", encoding="utf-8", newline="") as o:
        w = csv.DictWriter(o, CAB_DIA, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        w.writerows(linhas)
    a = sum(l["corrida"] == "A" for l in linhas)
    print(f"{len(novos)} fichas novas no vistos.tsv; {len(sem)} sem site novas; {d}.tsv: {a} A + {len(linhas) - a} B "
          f"(faltam {max(0, 50 - len(linhas))})")


def fotos(data, corrida):
    d = f"{data[:4]}-{data[4:6]}-{data[6:]}"
    out = []
    for l in csv.DictReader(open(f"{AQUI}/{d}.tsv", encoding="utf-8"), delimiter="\t"):
        if l["corrida"] != corrida or l["estado"] != "por fazer":
            continue
        f = f"{R}/{l['ficha']}.imagens.txt"
        if not os.path.exists(f):
            continue
        vistos = set()
        for u in open(f, encoding="utf-8").read().split():
            m = re.match(r"(https://lh\d\.googleusercontent\.com/(?:gps-cs-s|p)/[A-Za-z0-9_-]+)", u)
            if not m or m.group(1) in vistos:
                continue
            vistos.add(m.group(1))
            out.append(f'imagem sites/{l["slug"]}/media/g-{len(vistos):02d}.webp "{m.group(1)}=w1600"')
            if len(vistos) == 8:
                break
    ponte(out, f"fotos {d} corrida {corrida}")


if __name__ == "__main__":
    cmd, *a = sys.argv[1:]
    {"pesquisas": lambda: pesquisas(a[0], int(a[1]) if len(a) > 1 else 12), "lista": lambda: lista(a[0]),
     "fichas": lambda: fichas(a[0], int(a[1]) if len(a) > 1 else 25), "dia": lambda: dia(a[0]),
     "fotos": lambda: fotos(a[0], a[1])}[cmd]()
