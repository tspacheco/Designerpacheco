"""Gera as escritas para o Artifact a partir de tracker/aberturas.json e do estado atual.

  python3 tracker/atualizar.py <pasta-com-os-docs-lidos>  ->  tracker/_escritas.json

<pasta> é o out_dir de um ArtifactData list da coleção «negocios» (um .json por doc,
com «version»). Para cada demo: cria o negócio se falta (estado «por-enviar») e
atualiza a ficha (nome, tel, lote, ordem) e visitas/primeira/ultima se mudaram. Nunca toca no estado nem na nota.
"""
import glob, json, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
lidos = {}
for p in glob.glob(os.path.join(sys.argv[1], "**", "*.json"), recursive=True):
    d = json.load(open(p, encoding="utf-8"))
    lidos[d.get("id") or os.path.basename(p)[:-5]] = d
neg = json.load(open(os.path.join(AQUI, "negocios.json"), encoding="utf-8"))
ab = json.load(open(os.path.join(AQUI, "aberturas.json"), encoding="utf-8")) if os.path.exists(
    os.path.join(AQUI, "aberturas.json")) else {"demos": {}, "lido_em": "", "erro": "sem leitura"}
# o out_dir não guarda a versão: o resultado do list mostra-a; passar {id: versão} em tracker/_versoes.json
VP = os.path.join(AQUI, "_versoes.json")
versoes = json.load(open(VP)) if os.path.exists(VP) else {}
w = []
for i, n in enumerate(neg):
    a = ab["demos"].get(n["id"], {})
    novo = {"visitas": a.get("visitas", 0), "primeira": a.get("primeira", ""), "ultima": a.get("ultima", "")}
    if n["id"] not in lidos:
        doc = {"nome": n["nome"], "tel": n["tel"], "lote": n["lote"], "demo": n["demo"], "ordem": i,
               "estado": "por-enviar", "nota": "", **novo}
        w.append({"op": "set", "collection": "negocios", "doc_id": n["id"], "data": doc})
        continue
    d = lidos[n["id"]]
    atual = d.get("data", d)
    ficha = {"nome": n["nome"], "tel": n["tel"], "lote": n["lote"], "demo": n["demo"], "ordem": i}
    if not ab.get("lido_em") or ab.get("erro"):
        novo = {}
    muda = {k: v for k, v in {**ficha, **novo}.items() if atual.get(k) != v}
    if muda:
        w.append({"op": "update", "collection": "negocios", "doc_id": n["id"], "data": muda,
                  "if_version": d.get("version") or versoes.get(n["id"])})
json.dump(w, open(os.path.join(AQUI, "_escritas.json"), "w"), ensure_ascii=False, indent=1)
print(f"{len(w)} escritas; lido_em={ab.get('lido_em')!r} erro={ab.get('erro')!r}")
