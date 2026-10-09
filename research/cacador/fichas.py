#!/usr/bin/env python3
"""Lê as fichas do Maps gravadas pela ponte (ponte/<prefixo>*.html) e imprime TSV:
slug nome categoria nota avaliacoes site tel morada horario presenca whatsapp
  python3 research/cacador/fichas.py "ponte/cc-20261009-f-*.html"
site: domínio próprio (→ sai) ou vazio; presenca: facebook/instagram/mero/... quando o «Site» aponta para lá."""
import glob, html, os, re, sys

REDES = ("facebook.", "instagram.", "mero.ro", "diago.ro", "linktr.ee", "tiktok.", "wa.me", "booksy", "fresha", "business.site", "g.page", "google.com", "alteg.io", "linkr", "beacons.ai", "bio.link", "stailer.ro", "ontimeagenda", "fb.com")


def ficha(f):
    h = open(f, encoding="utf-8").read()
    t = open(f[:-5] + ".txt", encoding="utf-8").read() if os.path.exists(f[:-5] + ".txt") else ""
    a = lambda p: (re.search(p, h) or [None, ""])[1]
    site = html.unescape(a(r'aria-label="Site: ([^"]*)"')).strip()
    nome = html.unescape(a(r'<h1[^>]*>(?:<span[^>]*>)?([^<]+)<')).strip()
    nota = a(r'aria-label="(\d,\d) stele')
    aval = a(r'aria-label="([\d.]+) (?:de )?recenzii"')
    cat = html.unescape(a(r'<button[^>]*jsaction="[^"]*category[^"]*"[^>]*>([^<]+)<')).strip()
    if not cat and nome and nome in t:
        m = re.search(re.escape(nome) + r"\n(\d,\d)\n(?:\([\d.]+\)\n)?([^\n]+)", t)
        cat = m.group(2).strip() if m else ""
    tel = a(r'aria-label="Telefon: ([^"]*)"').strip()
    mor = html.unescape(a(r'aria-label="Adresă: ([^"]*)"')).strip().replace(", România", "")
    hor = html.unescape(a(r'aria-label="([^"]*(?:luni|marți|miercuri|joi|vineri)[^"]*ore[^"]*)"') or
                        a(r'aria-label="((?:luni|marți|miercuri|joi|vineri|sâmbătă|duminică),[^"]*)"')).strip()
    wa = "sim" if re.search(r"wa\.me/|api\.whatsapp", h) else ("não (fixo)" if re.sub(r"\D", "", tel)[2:3] in ("2", "3") else "?")
    pres = site if any(r in site for r in REDES) else ""
    proprio = "" if pres or not site else site
    b = os.path.basename(f)[:-5]
    slug = b.split("-f-", 1)[1] if "-f-" in b else b.split("-", 1)[1]
    return [slug, nome, cat, nota, aval, proprio, tel, mor, hor[:200], pres, wa]


if __name__ == "__main__":
    print("\t".join("slug nome categoria nota avaliacoes site tel morada horario presenca whatsapp".split()))
    for f in sorted(glob.glob(sys.argv[1])):
        print("\t".join(ficha(f)))
