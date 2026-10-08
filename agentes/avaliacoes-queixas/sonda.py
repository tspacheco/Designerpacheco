#!/usr/bin/env python3
"""Sonda: testa formas de ler as avaliações de uma ficha do Maps a partir do runner. Grava em dados/sonda/."""
import json, os, re, sys
from playwright.sync_api import sync_playwright

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
OUT = "agentes/avaliacoes-queixas/dados/sonda"
os.makedirs(OUT, exist_ok=True)


def grava(pg, nome):
    open(f"{OUT}/{nome}.txt", "w", encoding="utf-8").write(pg.url + "\n\n" + pg.inner_text("body"))
    open(f"{OUT}/{nome}.html", "w", encoding="utf-8").write(pg.content())
    pg.screenshot(path=f"{OUT}/{nome}.jpg", full_page=False, type="jpeg", quality=60)


def tenta(pg, sels, log, rot):
    for s in sels:
        try:
            pg.locator(s).first.click(timeout=4000)
            log.append(f"{rot}: clicou {s}")
            return True
        except Exception:
            pass
    log.append(f"{rot}: nada clicável")
    return False


def main(urls):
    log = []
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        ctx = b.new_context(viewport={"width": 1280, "height": 900}, user_agent=UA, locale="ro-RO")
        for i, url in enumerate(urls):
            pg = ctx.new_page()
            try:
                pg.goto(url, wait_until="domcontentloaded", timeout=45000)
            except Exception as ex:
                log.append(f"{i} goto erro {ex}")
            pg.wait_for_timeout(5000)
            grava(pg, f"{i}-a-ficha")
            tenta(pg, ['button[role="tab"][aria-label*="Recenzii"]', 'button[role="tab"]:has-text("Recenzii")',
                       'button:has-text("Mai multe recenzii")', 'button[aria-label*="recenzii"]'], log, f"{i} separador")
            pg.wait_for_timeout(4000)
            grava(pg, f"{i}-b-recenzii")
            tenta(pg, ['button[aria-label*="Sorta"]', 'button:has-text("Sortați")', 'button:has-text("Cele mai relevante")'], log, f"{i} ordenar")
            pg.wait_for_timeout(1500)
            tenta(pg, ['[role="menuitemradio"]:has-text("mici")', 'div[role="menuitemradio"] >> nth=3'], log, f"{i} piores")
            pg.wait_for_timeout(3000)
            for _ in range(8):
                pg.mouse.move(300, 600); pg.mouse.wheel(0, 3000); pg.wait_for_timeout(900)
            n = pg.locator("div[data-review-id]").count()
            log.append(f"{i} data-review-id: {n}")
            grava(pg, f"{i}-c-piores")
            # C: página antiga de avaliações por place_id
            m = re.search(r"19s(ChIJ[^?&!]+)", url)
            if m:
                pg2 = ctx.new_page()
                try:
                    pg2.goto(f"https://search.google.com/local/reviews?placeid={m.group(1)}&hl=ro", wait_until="domcontentloaded", timeout=45000)
                    pg2.wait_for_timeout(5000)
                    grava(pg2, f"{i}-d-local-reviews")
                    log.append(f"{i} local/reviews: {pg2.url[:120]}")
                except Exception as ex:
                    log.append(f"{i} local/reviews erro {ex}")
                pg2.close()
            pg.close()
        b.close()
    open(f"{OUT}/log.txt", "w", encoding="utf-8").write("\n".join(log) + "\n")
    print("\n".join(log))


if __name__ == "__main__":
    main(sys.argv[1:])
