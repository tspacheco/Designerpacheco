#!/usr/bin/env python3
"""Funil e follow-ups a partir de prospecao/tracker.csv (só biblioteca padrão).

    python3 prospecao/stats.py            # funil total, por semana e por cidade
    python3 prospecao/stats.py --hoje     # próximos passos vencidos ou de hoje
    python3 prospecao/stats.py --cidade Faro

Uma linha por contacto (visita, chamada, WhatsApp, reunião). Colunas (separador ';'):
  data (AAAA-MM-DD) · canal (visita/chamada/whatsapp/reuniao) · cidade · zona · negocio · tipo
  estrelas · avaliacoes · tem_site (S/N) · dono_falado (S/N) · contacto · telefone
  demo (S/N) · cartao (S/N) · qr_pack (N / O=oferecido / V=vendido)
  estado: visita | dono | demo | reuniao | proposta | venda | nao | excluir
  proximo_passo · data_proximo (AAAA-MM-DD) · notas
O estado de cada negócio é o mais avançado que alguma vez atingiu.
"""
import csv
import sys
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path

FICHEIRO = Path(__file__).with_name("tracker.csv")
ORDEM = ["visita", "dono", "demo", "reuniao", "proposta", "venda"]
FINAIS = {"nao", "excluir"}


def ler():
    if not FICHEIRO.exists():
        sys.exit(f"Não encontro {FICHEIRO}")
    with FICHEIRO.open(encoding="utf-8", newline="") as f:
        amostra = f.read(2048)
        f.seek(0)
        sep = ";" if amostra.count(";") >= amostra.count(",") else ","
        linhas = [
            {k.strip(): (v or "").strip() for k, v in r.items() if k}
            for r in csv.DictReader(f, delimiter=sep)
        ]
    return [l for l in linhas if l.get("negocio")]


def semana(d):
    try:
        iso = datetime.strptime(d, "%Y-%m-%d").isocalendar()
        return f"{iso[0]}-S{iso[1]:02d}"
    except ValueError:
        return "sem-data"


def sim(v):
    return v.upper() in {"S", "SIM", "Y", "1", "V", "O"}


def funil(linhas):
    """Devolve contagens por negócio (estado máximo) e por contacto."""
    por_negocio = defaultdict(lambda: {"estado": -1, "final": "", "demo": False, "dono": False,
                                       "cartao": False, "pack_o": False, "pack_v": False, "contactos": 0})
    for l in linhas:
        n = por_negocio[(l.get("cidade", ""), l["negocio"].lower())]
        n["contactos"] += 1
        est = l.get("estado", "").lower()
        if est in ORDEM:
            n["estado"] = max(n["estado"], ORDEM.index(est))
        elif est in FINAIS:
            n["final"] = est
        n["dono"] |= sim(l.get("dono_falado", ""))
        n["demo"] |= sim(l.get("demo", ""))
        n["cartao"] |= sim(l.get("cartao", ""))
        n["pack_o"] |= l.get("qr_pack", "").upper() == "O"
        n["pack_v"] |= l.get("qr_pack", "").upper() == "V"
    c = Counter()
    for n in por_negocio.values():
        if n["final"] == "excluir" and n["estado"] < 0:
            c["excluidos"] += 1
            continue
        c["negocios"] += 1
        c["contactos"] += n["contactos"]
        for i, nome in enumerate(ORDEM):
            # todo o negócio contactado conta como porta aberta, mesmo que tenha acabado em 'nao'
            if i == 0 or n["estado"] >= i or (i == 1 and n["dono"]) or (i == 2 and n["demo"]):
                c[nome] += 1
        c["cartoes"] += n["cartao"]
        c["packs_oferecidos"] += n["pack_o"]
        c["packs_vendidos"] += n["pack_v"]
        c["perdidos"] += n["final"] == "nao"
    return c


def pct(a, b):
    return f"{100 * a / b:5.1f} %" if b else "   —  "


def imprimir_funil(titulo, c):
    print(f"\n== {titulo} ==")
    base = c["negocios"]
    if not base:
        print("  (sem dados)")
        return
    print(f"  negócios contactados : {base}   (contactos: {c['contactos']}, "
          f"{c['contactos'] / base:.1f} por negócio)")
    anterior = base
    for nome, rotulo in zip(ORDEM, ["portas abertas", "dono falado", "demo mostrada",
                                    "reunião marcada", "proposta", "VENDA"]):
        v = c[nome]
        print(f"  {rotulo:<21}: {v:4d}   {pct(v, base)} do total   {pct(v, anterior)} do passo anterior")
        anterior = v or anterior
    print(f"  cartões deixados     : {c['cartoes']:4d}   packs QR oferecidos: {c['packs_oferecidos']}"
          f"   vendidos: {c['packs_vendidos']}")
    print(f"  perdidos (nao)       : {c['perdidos']:4d}   excluídos (já têm site/cadeia): {c['excluidos']}")
    if c["venda"]:
        print(f"  → {base / c['venda']:.0f} negócios e {c['contactos'] / c['venda']:.0f} contactos por venda")


def hoje(linhas):
    h = date.today().isoformat()
    ultimo = {}
    for l in linhas:  # o último registo de cada negócio manda
        ultimo[(l.get("cidade", ""), l["negocio"].lower())] = l
    pend = [l for l in ultimo.values()
            if l.get("data_proximo") and l["data_proximo"] <= h
            and l.get("estado", "").lower() not in {"venda", "nao", "excluir"}]
    pend.sort(key=lambda l: l["data_proximo"])
    print(f"\n== Follow-ups vencidos ou de hoje ({h}): {len(pend)} ==")
    for l in pend:
        atraso = (date.today() - datetime.strptime(l["data_proximo"], "%Y-%m-%d").date()).days
        tag = "HOJE " if atraso == 0 else f"-{atraso}d "
        print(f"  {tag:<5} {l['negocio']} ({l.get('cidade', '')}) · {l.get('contacto', '') or 'dono?'} "
              f"{l.get('telefone', '')} · {l.get('proximo_passo', '') or 'sem próximo passo'} "
              f"[{l.get('estado', '')}]")
    if not pend:
        print("  nada pendente — abre 10 portas novas.")


def main(argv):
    linhas = ler()
    if "--cidade" in argv:
        cid = argv[argv.index("--cidade") + 1].lower()
        linhas = [l for l in linhas if l.get("cidade", "").lower() == cid]
    if "--hoje" in argv:
        hoje(linhas)
        return
    imprimir_funil("TOTAL", funil(linhas))
    por_semana = defaultdict(list)
    for l in linhas:
        por_semana[semana(l.get("data", ""))].append(l)
    for s in sorted(por_semana):
        imprimir_funil(f"semana {s}", funil(por_semana[s]))
    por_cidade = defaultdict(list)
    for l in linhas:
        por_cidade[l.get("cidade", "") or "?"].append(l)
    if len(por_cidade) > 1:
        for cid in sorted(por_cidade):
            imprimir_funil(f"cidade {cid}", funil(por_cidade[cid]))
    hoje(linhas)


if __name__ == "__main__":
    main(sys.argv[1:])
