#!/usr/bin/env python3
"""Agente 8 — recolhe avaliações Google Maps de negócios de Iași (corre no runner do GitHub, workflow avaliacoes.yml).

  recolher.py --pesquisas pesquisas/AAAA-MM-DD.txt [--por-pesquisa 15] [--max-fichas 80] [--data AAAA-MM-DD]

pesquisas/*.txt: uma pesquisa do Maps por linha (ex.: «salon infrumusetare Tatarasi Iasi»).
Para cada ficha nova (fora de dados/vistos.txt): nome, nota, nº de avaliações, categoria, telefone, morada, site,
prova de WhatsApp, e as avaliações lidas por três vias dentro da ficha: as mais recentes, as piores e a pesquisa
interna das avaliações pelas palavras «telefon», «răspuns», «mesaj», «programare». Grava dados/AAAA-MM-DD.json
(acumula se já existir) e acrescenta as fichas a dados/vistos.txt.
"""
import argparse, datetime, json, os, re, time
from urllib.parse import quote
from playwright.sync_api import sync_playwright

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
AQUI = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(AQUI, "dados")
PALAVRAS = ["telefon", "răspuns", "mesaj", "programare"]
POR_VIA = 25  # avaliações por via (recentes / piores / cada palavra)

JS_AVALIACOES = """() => [...document.querySelectorAll('div[data-review-id][aria-label]')].map(r => {
  const t = r.querySelector('.wiI7pd'); const s = r.querySelector('[role="img"][aria-label*="stea"], .kvMYJc');
  const d = r.querySelector('.rsqaWe, .xRkPPb'); return {id: r.getAttribute('data-review-id'),
  autor: r.getAttribute('aria-label') || '', estrelas: s ? s.getAttribute('aria-label') : '',
  data: d ? d.innerText.split('\\n')[0].trim() : '', texto: t ? t.innerText.trim() : ''}; })"""


def chave(url):
    m = re.search(r"!1s(0x[0-9a-f]+:0x[0-9a-f]+)", url or "")
    return m.group(1) if m else (url or "").split("?")[0]


def clica(pg, sels, espera=4000):
    for s in sels:
        try:
            pg.locator(s).first.click(timeout=espera)
            return s
        except Exception:
            pass
    return None


def desce(pg, vezes=6):
    painel = pg.locator("div.m6QErb.DxyBCb, div[role='main'] div.m6QErb").last
    for _ in range(vezes):
        try:
            painel.evaluate("e => e.scrollBy(0, 4000)")
        except Exception:
            pg.mouse.move(300, 600); pg.mouse.wheel(0, 4000)
        pg.wait_for_timeout(800)


def expande(pg):
    try:
        pg.evaluate("() => document.querySelectorAll('button.w8nwRe, button[aria-label=\"Vezi mai multe\"], button[jsaction*=\"expandReview\"]').forEach(b => b.click())")
        pg.wait_for_timeout(500)
    except Exception:
        pass


def junta(pg, acum, via):
    expande(pg)
    try:
        for a in pg.evaluate(JS_AVALIACOES):
            if a["id"] and a["texto"] and a["id"] not in acum:
                a["via"] = via
                acum[a["id"]] = a
    except Exception:
        pass


def lista_pesquisa(pg, termo, n):
    pg.goto(f"https://www.google.com/maps/search/{quote(termo)}?hl=ro", wait_until="domcontentloaded", timeout=45000)
    pg.wait_for_timeout(4000)
    clica(pg, ['button:has-text("Acceptați tot")', 'button:has-text("Accept all")'], 1500)
    feed = pg.locator("div[role='feed']")
    vistos = []
    for _ in range(10):
        hrefs = pg.evaluate("() => [...document.querySelectorAll('a.hfpxzc')].map(a => [a.href, a.getAttribute('aria-label')])")
        vistos = list(dict.fromkeys(tuple(h) for h in hrefs))
        if len(vistos) >= n:
            break
        try:
            feed.evaluate("e => e.scrollBy(0, 5000)")
        except Exception:
            break
        pg.wait_for_timeout(1200)
    if not vistos and "/maps/place/" in pg.url:  # a pesquisa caiu direto numa ficha
        vistos = [(pg.url, "")]
    return vistos[:n]


def ficha(pg, url, termo):
    for tentativa in range(3):
        pg.goto(url if "hl=" in url else url + ("&" if "?" in url else "?") + "hl=ro", wait_until="domcontentloaded", timeout=45000)
        pg.wait_for_timeout(3500)
        if pg.locator('button[role="tab"]').count():
            break
        # «secțiune limitată» do Maps (sem separadores): volta a abrir
        pg.goto("https://www.google.com/maps?hl=ro", wait_until="domcontentloaded", timeout=45000)
        pg.wait_for_timeout(2000 + 2000 * tentativa)
    return _ficha(pg, url, termo)


def _ficha(pg, url, termo):
    f = pg.evaluate("""() => { const q = s => document.querySelector(s); const t = s => (q(s) || {}).innerText || '';
      const a = s => { const e = q(s); return e ? e.getAttribute('aria-label') || '' : ''; };
      const nota = (q('div.F7nice span[aria-hidden]') || {}).innerText || '';
      const nAv = (document.querySelector('div.F7nice span[aria-label*="recenzi"]') || {}).getAttribute ?
                  document.querySelector('div.F7nice span[aria-label*="recenzi"]').getAttribute('aria-label') : '';
      const wa = [...document.querySelectorAll('a[href*="wa.me"], a[href*="api.whatsapp.com"]')].map(e => e.href);
      return {nome: t('h1'), nota, n_av: nAv || t('div.F7nice'), categoria: t('button.DkEaL'),
        tel: a('button[data-item-id^="phone:tel:"]').replace(/^[^:]*:\\s*/, ''),
        morada: a('button[data-item-id="address"]').replace(/^[^:]*:\\s*/, ''),
        site: (q('a[data-item-id="authority"]') || {}).href || '', wa }; }""")
    nota = re.search(r"(\d)[,.](\d)", f["nota"] or "")
    nav = re.sub(r"[^\d]", "", re.search(r"[\d.\s]+", f["n_av"] or "0").group(0)) if re.search(r"\d", f["n_av"] or "") else ""
    out = {"chave": chave(url) if "!1s0x" in url else chave(pg.url), "url": url.split("&authuser")[0],
           "nome": f["nome"].strip(), "nota": float(f"{nota.group(1)}.{nota.group(2)}") if nota else None,
           "n_avaliacoes": int(nav) if nav else None, "categoria": f["categoria"].strip(), "tel": f["tel"].strip(),
           "morada": f["morada"].strip(), "site": f["site"], "whatsapp": "sim" if f["wa"] else "", "pesquisa": termo,
           "vias": [], "avaliacoes": []}
    acum = {}
    if not clica(pg, ['button[role="tab"][aria-label^="Recenzii"]', 'button[role="tab"]:has-text("Recenzii")']):
        out["vias"].append("sem separador Recenzii")
        junta(pg, acum, "ficha")
        out["avaliacoes"] = list(acum.values())
        return out
    pg.wait_for_timeout(2500)
    # via 1: mais recentes · via 2: piores
    for via, item in (("recentes", "Cele mai noi"), ("piores", "slabă")):
        if clica(pg, ['button.HQzyZ[aria-haspopup="true"]', 'button[aria-label="Cele mai relevante"]'], 3000):
            pg.wait_for_timeout(1000)
            if clica(pg, [f'div[role="menuitemradio"]:has-text("{item}")'], 3000):
                pg.wait_for_timeout(2500)
                antes = len(acum)
                for _ in range(max(1, POR_VIA // 10)):
                    desce(pg, 2)
                junta(pg, acum, via)
                out["vias"].append(f"{via}:{len(acum) - antes}")
                continue
        out["vias"].append(f"{via}:falhou")
    # via 3: pesquisa interna das avaliações
    for p in PALAVRAS:
        if pg.locator('input.yBHhWb').count() or clica(pg, ['button[aria-label="Caută recenzii"]'], 2500):
            try:
                cx = pg.locator('input.yBHhWb').first
                cx.fill(p, timeout=3000); cx.press("Enter"); pg.wait_for_timeout(2500)
                antes = len(acum)
                desce(pg, 2)
                junta(pg, acum, f"busca:{p}")
                out["vias"].append(f"{p}:{len(acum) - antes}")
                continue
            except Exception:
                pass
        out["vias"].append(f"{p}:falhou")
    if not acum:
        junta(pg, acum, "ficha")
    out["avaliacoes"] = list(acum.values())
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pesquisas", required=True)
    ap.add_argument("--por-pesquisa", type=int, default=15)
    ap.add_argument("--max-fichas", type=int, default=80)
    ap.add_argument("--data", default=datetime.date.today().isoformat())
    ap.add_argument("--min-avaliacoes", type=int, default=15)
    args = ap.parse_args()
    os.makedirs(DADOS, exist_ok=True)
    vistos_p = os.path.join(DADOS, "vistos.txt")
    vistos = set(open(vistos_p, encoding="utf-8").read().split("\n")) if os.path.exists(vistos_p) else set()
    saida = os.path.join(DADOS, f"{args.data}.json")
    fichas = json.load(open(saida, encoding="utf-8")) if os.path.exists(saida) else []
    feitas = {f["chave"] for f in fichas}
    termos = [l.strip() for l in open(os.path.join(AQUI, args.pesquisas), encoding="utf-8") if l.strip() and not l.startswith("#")]
    t0 = time.time()
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        ctx = b.new_context(viewport={"width": 1280, "height": 900}, user_agent=UA, locale="ro-RO")
        pg = ctx.new_page()
        pg.set_default_timeout(15000)
        pg.goto("https://www.google.com/maps?hl=ro", wait_until="domcontentloaded", timeout=45000)
        pg.wait_for_timeout(3000)
        fila = []
        for termo in termos:
            try:
                res = lista_pesquisa(pg, termo, args.por_pesquisa)
            except Exception as ex:
                print(f"ERRO pesquisa «{termo}»: {ex}"); continue
            novos = [(u, n, termo) for u, n in res if chave(u) not in vistos and chave(u) not in feitas
                     and chave(u) not in {chave(x[0]) for x in fila}]
            print(f"pesquisa «{termo}»: {len(res)} fichas, {len(novos)} novas")
            fila += novos
        print(f"fila: {len(fila)} fichas novas (máx. {args.max_fichas})")
        for i, (u, n, termo) in enumerate(fila[:args.max_fichas], 1):
            if time.time() - t0 > 100 * 60:
                print("tempo esgotado, paro aqui"); break
            try:
                f = ficha(pg, u, termo)
            except Exception as ex:
                print(f"ERRO ficha {n}: {ex}"); continue
            vistos.add(f["chave"])
            if (f["n_avaliacoes"] or 0) < args.min_avaliacoes:
                print(f"{i:>3} {f['nome'][:40]:40} {f['n_avaliacoes']} aval. (poucas, sai)"); continue
            fichas.append(f)
            print(f"{i:>3} {f['nome'][:40]:40} {f['nota']} ({f['n_avaliacoes']}) lidas {len(f['avaliacoes'])} · {' '.join(f['vias'])}")
            if i % 10 == 0:
                json.dump(fichas, open(saida, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        b.close()
    json.dump(fichas, open(saida, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    open(vistos_p, "w", encoding="utf-8").write("\n".join(sorted(v for v in vistos if v)) + "\n")
    print(f"total: {len(fichas)} fichas em dados/{args.data}.json, {sum(len(f['avaliacoes']) for f in fichas)} avaliações")


if __name__ == "__main__":
    main()
