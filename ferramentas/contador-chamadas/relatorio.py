#!/usr/bin/env python3
"""Relatório do Contador de Chamadas: lê os comentários do registo no GitHub e resume o dia.

Uso:  python3 relatorio.py [--data AAAA-MM-DD] [--desde HH:MM] [--tz Europe/Lisbon] [--issue 3]
Sem --data usa hoje. --desde conta à parte as chamadas começadas a partir dessa hora.
Lê a API pública do GitHub (repositório público); usa GITHUB_TOKEN se existir.
"""
import argparse
import json
import os
import re
import urllib.request
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

REPO = "tspacheco/Designerpacheco"
LINHA = re.compile(r"^chamada v1\s*\|")


def comentarios(issue, desde_utc):
    url = (f"https://api.github.com/repos/{REPO}/issues/{issue}/comments"
           f"?per_page=100&since={desde_utc.strftime('%Y-%m-%dT%H:%M:%SZ')}")
    cab = {"Accept": "application/vnd.github+json", "User-Agent": "contador-relatorio"}
    if os.environ.get("GITHUB_TOKEN"):
        cab["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
    while url:
        r = urllib.request.urlopen(urllib.request.Request(url, headers=cab), timeout=30)
        yield from json.load(r)
        prox = re.search(r'<([^>]+)>;\s*rel="next"', r.headers.get("Link", ""))
        url = prox.group(1) if prox else None


def campos(texto):
    d = {}
    for parte in texto.strip().split("|")[1:]:
        if "=" in parte:
            k, v = parte.split("=", 1)
            d[k.strip()] = v.strip()
    return d


def mmss(seg):
    h, r = divmod(int(seg), 3600)
    m, s = divmod(r, 60)
    return f"{h} h {m:02d} min" if h else f"{m} min {s:02d} s"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data")
    ap.add_argument("--desde")
    ap.add_argument("--tz", default="Europe/Lisbon")
    ap.add_argument("--issue", default="3")
    a = ap.parse_args()
    tz = ZoneInfo(a.tz)
    dia = datetime.strptime(a.data, "%Y-%m-%d").date() if a.data else datetime.now(tz).date()
    ini_dia = datetime.combine(dia, datetime.min.time(), tz)

    vistas, chamadas = set(), []
    # Um comentário pode chegar atrasado (telemóvel sem rede): lê desde a véspera e filtra pela hora de início.
    for c in comentarios(a.issue, (ini_dia - timedelta(days=1)).astimezone(ZoneInfo("UTC"))):
        corpo = (c.get("body") or "").strip()
        if not LINHA.match(corpo):
            continue
        f = campos(corpo)
        chave = (f.get("ap"), f.get("id"))
        if chave in vistas:
            continue
        vistas.add(chave)
        try:
            inicio = datetime.fromisoformat(f["inicio"]).astimezone(tz)
            fim = datetime.fromisoformat(f["fim"]).astimezone(tz)
            dur = int(f.get("dur", 0))
        except (KeyError, ValueError):
            continue
        if inicio.date() != dia:
            continue
        conv = int(f["conv"]) if f.get("conv", "").isdigit() else None
        chamadas.append({"ap": f.get("ap", "?"), "inicio": inicio, "fim": fim, "dur": dur, "conv": conv})

    chamadas.sort(key=lambda x: x["inicio"])
    n = len(chamadas)
    print(f"📞 Chamadas de WhatsApp · {dia.strftime('%d/%m/%Y')} (hora de {a.tz.split('/')[-1]})")
    if not n:
        print("Ainda nenhuma chamada registada hoje.")
        return
    total = sum(x["dur"] for x in chamadas)
    longas = sum(1 for x in chamadas if x["dur"] >= 30)
    atendidas = [x for x in chamadas if x["conv"] is not None]
    print(f"Total: {n} chamadas · {mmss(total)} ao telefone · média {mmss(total / n)}")
    print(f"Com 30 s ou mais: {longas}" + (f" · atendidas: {len(atendidas)}" if atendidas else ""))
    print(f"Primeira às {chamadas[0]['inicio']:%H:%M}, última às {chamadas[-1]['inicio']:%H:%M}")
    if a.desde:
        h, m = map(int, a.desde.split(":"))
        corte = datetime.combine(dia, datetime.min.time(), tz).replace(hour=h, minute=m)
        recentes = [x for x in chamadas if x["inicio"] >= corte]
        print(f"Desde as {a.desde}: {len(recentes)} chamadas · {mmss(sum(x['dur'] for x in recentes))}")
    por_hora = {}
    for x in chamadas:
        por_hora[x["inicio"].hour] = por_hora.get(x["inicio"].hour, 0) + 1
    print("Por hora: " + " · ".join(f"{h}h {q}" for h, q in sorted(por_hora.items())))
    aps = sorted({x["ap"] for x in chamadas})
    if len(aps) > 1:
        print("Por telemóvel: " + " · ".join(f"{p} {sum(1 for x in chamadas if x['ap'] == p)}" for p in aps))


if __name__ == "__main__":
    main()
