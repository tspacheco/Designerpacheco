"""Lê sites de negócios (página inicial + páginas de contacto) e extrai só o que serve à prospeção:
e-mails e telefones publicados, título, descrição, sinais de canais (WhatsApp, formulário, marcação, chat).

Entrada: .github/emails.txt, uma linha por site: «<id> <url>». Linha «# lote: <nome>» dá o nome do ficheiro.
Saída: ponte/emails-<lote>.enc, cifrado com .github/ponte-cert.pem (a chave privada nunca está no repositório),
para não pôr e-mails de negócios legíveis num repositório público.
"""
import concurrent.futures as cf
import html as H
import json
import re
import ssl
import subprocess
import sys
import urllib.request
from urllib.parse import urljoin, urlparse

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
CTX = ssl.create_default_context()
CTX_LAX = ssl._create_unverified_context()
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")
LIXO = re.compile(r"\.(png|jpe?g|webp|svg|gif|css|js)$|sentry|example|wixpress|@2x|domeniu|exemplu|yourdomain|email@|name@|nume@|user@|your@", re.I)
CF = re.compile(r'data-cfemail="([0-9a-f]+)"|email-protection#([0-9a-f]+)', re.I)
CONTACT = re.compile(r'href=["\']([^"\']*(?:contact|kontakt|despre|about|rezerv|programar)[^"\']*)["\']', re.I)


def baixa(url):
    for ctx in (CTX, CTX_LAX):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "ro,en;q=0.8"})
            with urllib.request.urlopen(req, timeout=20, context=ctx) as r:
                dados = r.read(1500000)
                return r.geturl(), dados.decode(r.headers.get_content_charset() or "utf-8", "ignore")
        except ssl.SSLError:
            continue
        except Exception as ex:
            if ctx is CTX_LAX:
                return None, "ERRO " + str(ex)[:80]
            if "CERTIFICATE" in str(ex).upper():
                continue
            return None, "ERRO " + str(ex)[:80]
    return None, "ERRO ssl"


def cfdecode(hexa):
    try:
        b = bytes.fromhex(hexa)
        return "".join(chr(c ^ b[0]) for c in b[1:])
    except Exception:
        return ""


def extrai(txt, vistos):
    t = H.unescape(txt).replace("(@)", "@").replace("[at]", "@")
    for m in CF.finditer(t):
        e = cfdecode(m.group(1) or m.group(2))
        if "@" in e:
            vistos.add(e.lower())
    for m in re.finditer(r"mailto:([^\"'?>\s]+)", t, re.I):
        vistos.add(m.group(1).lower())
    for m in EMAIL.findall(t):
        vistos.add(m.lower().strip("."))


def um(item):
    id_, url = item
    out = {"id": id_, "url": url, "emails": [], "telefones": [], "titulo": "", "descricao": "", "h1": "", "estado": "ok", "paginas": []}
    vistos, tels, texto = set(), set(), ""
    final, h = baixa(url)
    if not final:
        out["estado"] = h
        return out
    base = final
    paginas = [(base, h)]
    cand = []
    for m in CONTACT.finditer(h):
        u = urljoin(base, H.unescape(m.group(1)))
        if urlparse(u).netloc.replace("www.", "") == urlparse(base).netloc.replace("www.", "") and u not in cand and "#" not in u:
            cand.append(u)
    cand = cand[:2] or [urljoin(base, "/contact")]
    for u in cand:
        f2, h2 = baixa(u)
        if f2:
            paginas.append((f2, h2))
    for u, h_ in paginas:
        out["paginas"].append(u)
        extrai(h_, vistos)
        for m in re.finditer(r"tel:([+\d][\d\s.()-]{6,})", h_):
            tels.add(re.sub(r"[^\d+]", "", m.group(1)))
        for m in re.finditer(r"(?<!\d)(?:\+?40|0)[\s.-]?7\d{2}[\s.-]?\d{3}[\s.-]?\d{3}(?!\d)", h_):
            tels.add(re.sub(r"[^\d+]", "", m.group(0)))
        texto += " " + h_
    dom = urlparse(base).netloc.replace("www.", "").lower()
    out["emails"] = sorted((e for e in vistos if not LIXO.search(e)), key=lambda e: (not e.endswith(dom), e))[:8]
    out["telefones"] = sorted(tels)[:4]
    t = re.search(r"<title[^>]*>(.*?)</title>", h, re.S | re.I)
    d = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']*)', h, re.I) or re.search(r'<meta[^>]+content=["\']([^"\']*)["\'][^>]+name=["\']description', h, re.I)
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", h, re.S | re.I)
    lim = lambda s, n: re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()[:n]
    out["titulo"], out["descricao"], out["h1"] = lim(t.group(1) if t else "", 120), lim(d.group(1) if d else "", 220), lim(h1.group(1) if h1 else "", 120)
    low = texto.lower()
    out["sinais"] = {
        "whatsapp": bool(re.search(r"wa\.me|api\.whatsapp|whatsapp", low)),
        "formular": "<form" in low,
        "marcacao": bool(re.search(r"programar|rezerv|booking|calendly|appointment", low)),
        "oferta": bool(re.search(r"cerere (de )?ofert|solicit[ăa] ofert|ofert[ăa] gratuit|deviz", low)),
        "chat": bool(re.search(r"tawk\.to|crisp\.chat|tidio|livechat|intercom|drift\.com|messenger", low)),
        "facebook": bool(re.search(r"facebook\.com/", low)),
        "instagram": bool(re.search(r"instagram\.com/", low)),
        "comenzi_online": bool(re.search(r"co[sș]ul meu|add to cart|adaug[ăa] [iî]n co[sș]|comand[ăa] online", low)),
    }
    return out


def main():
    lote, itens = "lote", []
    for linha in open(".github/emails.txt", encoding="utf-8"):
        linha = linha.strip()
        m = re.match(r"#\s*lote:\s*(\S+)", linha)
        if m:
            lote = m.group(1)
        if not linha or linha.startswith("#"):
            continue
        p = linha.split(None, 1)
        if len(p) == 2:
            itens.append((p[0], p[1].strip()))
    with cf.ThreadPoolExecutor(max_workers=12) as ex:
        res = list(ex.map(um, itens))
    json.dump(res, open("/tmp/emails.json", "w", encoding="utf-8"), ensure_ascii=False)
    import os
    os.makedirs("ponte", exist_ok=True)
    subprocess.run(["openssl", "smime", "-encrypt", "-aes256", "-binary", "-outform", "DER", "-in", "/tmp/emails.json",
                    "-out", "ponte/emails-%s.enc" % lote, ".github/ponte-cert.pem"], check=True)
    ok = sum(1 for r in res if r["emails"])
    print("%d sites, %d com e-mail, %d com erro" % (len(res), ok, sum(1 for r in res if r["estado"] != "ok")))


if __name__ == "__main__":
    main()
