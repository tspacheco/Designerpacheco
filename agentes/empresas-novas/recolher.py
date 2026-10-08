#!/usr/bin/env python3
"""Agente 7: empresas acabadas de registar (Roménia).

Corre no runner do GitHub (workflow empresas-novas.yml); a rede dos threads não chega à ANAF.
Os CUI são atribuídos por ordem e o último algarismo é de controlo, por isso basta percorrer os números
a seguir ao último visto e perguntar à API pública da ANAF (até 100 CUI por pedido, 1 pedido/s).
Cada empresa encontrada traz nome, morada, telefone (quando declarado), CAEN e data de registo.

  python3 recolher.py                       continua a partir de dados/estado.json
  python3 recolher.py --inicio 5560000      começa nesse número (sem o algarismo de controlo)
  python3 recolher.py --sondar-ckan         também lista os conjuntos de dados ONRC em data.gov.ro
"""
import argparse, datetime, json, os, sys, time, urllib.error, urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(AQUI, "dados")
ESTADO = os.path.join(DADOS, "estado.json")
VISTOS = os.path.join(DADOS, "vistos.txt")  # CUI já lidos (para não repetir)
RECUO = 600  # a ANAF demora a mostrar alguns CUI: cada corrida volta a pedir os últimos 600 números
API = "https://webservicesp.anaf.ro/api/PlatitorTvaRest/v9/tva"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"


def controlo(base):
    s = str(base).zfill(9)
    soma = sum(int(a) * int(b) for a, b in zip(s, "753217532"))
    c = soma * 10 % 11
    return 0 if c == 10 else c


def cui(base):
    return int(f"{base}{controlo(base)}")


def anaf(cuis, data):
    corpo = json.dumps([{"cui": c, "data": data} for c in cuis]).encode()
    for tentativa in range(5):
        try:
            req = urllib.request.Request(API, data=corpo, headers={"Content-Type": "application/json", "User-Agent": UA})
            return json.load(urllib.request.urlopen(req, timeout=60))
        except urllib.error.HTTPError as ex:
            if ex.code == 404:  # a ANAF responde 404 quando nenhum dos CUI existe (passámos a fronteira)
                return {"found": [], "notFound": cuis}
            print(f"  ANAF falhou ({ex}), nova tentativa", file=sys.stderr)
            time.sleep(3 * (tentativa + 1))
        except Exception as ex:
            print(f"  ANAF falhou ({ex}), nova tentativa", file=sys.stderr)
            time.sleep(3 * (tentativa + 1))
    raise RuntimeError("ANAF não respondeu")


def resumo(f):
    g = f.get("date_generale", {})
    s = f.get("adresa_sediu_social", {})
    return {
        "cui": g.get("cui"), "denumire": g.get("denumire"), "nrRegCom": g.get("nrRegCom"),
        "data_inregistrare": g.get("data_inregistrare"), "caen": g.get("cod_CAEN"),
        "telefon": (g.get("telefon") or "").strip(), "adresa": g.get("adresa"),
        "judet": s.get("scod_JudetAuto"), "localitate": s.get("sdenumire_Localitate"),
        "strada": s.get("sdenumire_Strada"), "numar": s.get("snumar_Strada"),
        "forma_juridica": g.get("forma_juridica"), "forma_organizare": g.get("forma_organizare"),
        "stare": g.get("stare_inregistrare"),
    }


def sondar_ckan():
    url = "https://data.gov.ro/api/3/action/package_search?q=onrc&rows=50"
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=90))
        out = [{"nome": p["name"], "titulo": p["title"], "modificado": p.get("metadata_modified"),
                "recursos": [{"nome": x.get("name"), "url": x.get("url"), "modificado": x.get("last_modified") or x.get("created")}
                             for x in p.get("resources", [])]} for p in r["result"]["results"]]
    except Exception as ex:
        out = {"erro": str(ex)}
    json.dump(out, open(os.path.join(DADOS, "ckan-onrc.json"), "w"), ensure_ascii=False, indent=1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inicio", type=int)
    ap.add_argument("--max-lotes", type=int, default=120)
    ap.add_argument("--parar-vazios", type=int, default=6)
    ap.add_argument("--sondar-ckan", action="store_true")
    a = ap.parse_args()
    os.makedirs(DADOS, exist_ok=True)
    if a.sondar_ckan:
        sondar_ckan()
    estado = json.load(open(ESTADO)) if os.path.exists(ESTADO) else {}
    base = a.inicio if a.inicio else estado.get("ultimo_base", 0) - RECUO
    vistos = set(open(VISTOS).read().split()) if os.path.exists(VISTOS) else set()
    if not base or base < 1000000:
        sys.exit("Sem ponto de partida: usar --inicio")
    hoje = datetime.date.today().isoformat()
    achadas, vazios, maior = [], 0, estado.get("ultimo_base", 0)
    for lote in range(a.max_lotes):
        bases = list(range(base, base + 100))
        r = anaf([cui(b) for b in bases], hoje)
        f = r.get("found") or []
        for x in f:
            if str(x["date_generale"]["cui"]) not in vistos:
                achadas.append(resumo(x))
            maior = max(maior, int(str(x["date_generale"]["cui"])[:-1]))
        print(f"lote {lote}: {bases[0]}..{bases[-1]} -> {len(f)} encontradas", file=sys.stderr)
        vazios = 0 if f else vazios + 1
        if achadas and vazios >= a.parar_vazios:
            break
        base += 100
        time.sleep(1.2)
    ficheiro = os.path.join(DADOS, f"iasi-{hoje}.json")
    anteriores = json.load(open(ficheiro)) if os.path.exists(ficheiro) else []
    iasi = [x for x in achadas if x["judet"] == "IS"]  # só se guarda o distrito de Iași; dos outros fica o CUI em vistos
    json.dump(anteriores + iasi, open(ficheiro, "w"), ensure_ascii=False, indent=0)
    with open(VISTOS, "a") as v:
        v.write("".join(f"{x['cui']}\n" for x in achadas))
    estado.update({"ultimo_base": maior, "ultima_corrida": datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z"})
    json.dump(estado, open(ESTADO, "w"), indent=1)
    print(f"{len(achadas)} empresas novas lidas, {len(iasi)} no distrito de Iași, último CUI-base {maior}")


if __name__ == "__main__":
    main()
