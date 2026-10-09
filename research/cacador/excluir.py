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


if __name__ == "__main__":
    print(len(todas()))
