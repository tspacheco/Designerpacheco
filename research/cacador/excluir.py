#!/usr/bin/env python3
"""Imprime as chaves normalizadas de todos os negócios já tratados (DEMOS, research/iasi-*.md, fichas da ponte, vistos.tsv)."""
import glob, os, re, unicodedata
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def chave(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"\b(iasi|salon|srl|the|de|si|and)\b", " ", s)
    return re.sub(r"[^a-z0-9]+", "", s)[:18]


def todas():
    k = set()
    g = open(f"{R}/sites/demos-pachecost/gerar.py", encoding="utf-8").read()
    for a, b in re.findall(r'\("([^"]+)", "([^"]+)"\)', g):
        k |= {chave(a.replace("-", " ")), chave(b.replace("-", " "))}
    for f in glob.glob(f"{R}/research/iasi-*.md"):
        for l in open(f, encoding="utf-8"):
            if l.startswith("|") and not l.startswith("|---"):
                c = [x.strip(" *`") for x in l.split("|")[1:3]]
                k |= {chave(x) for x in c if x}
    for f in glob.glob(f"{R}/ponte/r[0-9]-*.txt") + glob.glob(f"{R}/ponte/cc-*-f-*.txt"):
        n = os.path.basename(f)[:-4].split("-", 1)[1]
        if n.startswith("f-"):
            n = n.split("-", 3)[-1]
        k.add(chave(n.replace("-", " ")))
    v = f"{R}/research/cacador/vistos.tsv"
    for l in open(v, encoding="utf-8").read().splitlines()[1:]:
        c = l.split("\t")
        if len(c) > 2:
            k |= {chave(c[1].replace("-", " ")), chave(c[2])}
    k.discard("")
    return k


def digitos(t):
    return re.sub(r"\D", "", t or "")[-9:]


def telefones(hoje=""):
    """Telefones (9 últimos dígitos) de tudo o que já tem demo: CONTACTOS/MENSAGENS/VISITAS das demos, DADOS-PARA-O-DONO de cada site,
    research/iasi-*.md e as listas dos dias anteriores do caçador (menos as do dia `hoje`, AAAA-MM-DD, e os sites desse dia)."""
    import csv
    meus = set()
    if hoje and os.path.exists(f"{R}/research/cacador/{hoje}.tsv"):
        meus = {r["slug"] for r in csv.DictReader(open(f"{R}/research/cacador/{hoje}.tsv", encoding="utf-8"), delimiter="\t")}
    fs = glob.glob(f"{R}/sites/demos-pachecost/*.md") + glob.glob(f"{R}/research/iasi-*.md")
    fs += [f for f in glob.glob(f"{R}/sites/*/DADOS-PARA-O-DONO.md") if f.split("/")[-2] not in meus]
    fs += [f for f in glob.glob(f"{R}/research/cacador/20*.tsv") if hoje not in f]
    t = set()
    for f in fs:
        for m in re.findall(r"(?:\+?40[ .-]?|\b0)(\d{3})[ .-]?(\d{3})[ .-]?(\d{3})\b", open(f, encoding="utf-8", errors="ignore").read()):
            t.add("".join(m))
    return t


def ja_feito(nome, tel, chaves, tels):
    """True se o negócio já foi tratado: telefone igual ou nome que começa pela chave de outro (≥ 10 letras)."""
    if tel and digitos(tel) in tels:
        return True
    k = chave(nome)
    return any(len(x) >= 10 and (k.startswith(x) or x.startswith(k)) for x in chaves if x != k)


if __name__ == "__main__":
    print(len(todas()))
