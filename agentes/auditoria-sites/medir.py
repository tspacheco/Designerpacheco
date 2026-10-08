# Medição de um site no telemóvel, corrida pela PONTE (operação «auditar <nome> <url>»).
# Duas fontes, ambas reais e repetíveis:
#   1. Lighthouse móvel (o mesmo motor do PageSpeed Insights: 4G lento simulado, telemóvel médio).
#   2. Chromium com ecrã de iPhone: o que o cliente encontra (botão de chamada, WhatsApp, marcação…).
# Grava auditorias/dados/<nome>.json e auditorias/dados/<nome>.jpg (primeiro ecrã no telemóvel).
import json, os, re, subprocess, time

AUD = ["first-contentful-paint", "largest-contentful-paint", "speed-index", "total-blocking-time",
       "cumulative-layout-shift", "interactive", "total-byte-weight", "network-requests", "viewport",
       "is-on-https", "redirects-http", "uses-optimized-images", "modern-image-formats", "uses-responsive-images",
       "offscreen-images", "render-blocking-resources", "unused-javascript", "uses-text-compression",
       "meta-description", "document-title", "font-size", "color-contrast", "image-alt", "link-text",
       "crawlable-anchors", "tap-targets", "errors-in-console", "html-has-lang", "uses-long-cache-ttl"]

CHECAR = r"""() => {
  const q = s => Array.from(document.querySelectorAll(s));
  const hrefs = q('a[href]').map(a => a.getAttribute('href') || '');
  const txt = document.body ? document.body.innerText : '';
  const vis = el => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0 && r.top < innerHeight && r.bottom > 0; };
  const primeiro = q('a[href]').filter(vis).map(a => (a.getAttribute('href') || '').toLowerCase());
  const ld = q('script[type="application/ld+json"]').map(s => { try { const j = JSON.parse(s.textContent); return [].concat(j['@graph'] || j).map(x => x['@type']).flat(); } catch (e) { return ['inválido']; } }).flat();
  const anos = (txt.match(/(?:©|copyright|\(c\))\s*(?:\d{4}\s*[-–]\s*)?(\d{4})/gi) || []).map(m => +m.match(/(\d{4})(?!.*\d{4})/)[1]);
  return {
    titulo: document.title, lang: document.documentElement.lang || '',
    descricao: (document.querySelector('meta[name="description"]') || {}).content || '',
    viewport: (document.querySelector('meta[name="viewport"]') || {}).content || '',
    h1: q('h1').length, imagens: q('img').length, imagens_sem_alt: q('img:not([alt])').length,
    tel: hrefs.filter(h => /^tel:/i.test(h)).length,
    tel_no_1o_ecra: primeiro.some(h => h.startsWith('tel:')),
    whatsapp: hrefs.filter(h => /wa\.me|whatsapp\.com|whatsapp:/i.test(h)).length,
    email: hrefs.filter(h => /^mailto:/i.test(h)).length,
    marcacao: hrefs.filter(h => /mero\.ro|booksy|fresha|calendly|planific|dikidi|setmore|treatwell|simplybook|rezerv|programar|booking/i.test(h)).length,
    mapa: q('iframe[src*="google.com/maps"], iframe[src*="maps.google"], a[href*="maps.app.goo.gl"], a[href*="google.com/maps"], a[href*="goo.gl/maps"]').length,
    facebook: hrefs.filter(h => /facebook\.com/i.test(h)).length, instagram: hrefs.filter(h => /instagram\.com/i.test(h)).length,
    jsonld: ld, formularios: q('form').length,
    telefone_no_texto: /(\+40|0040|\b0)\s?7\d{2}[\s.]?\d{3}[\s.]?\d{3}|\b0\s?2\d{2}[\s.]?\d{3}[\s.]?\d{3}/.test(txt),
    ano_copyright: anos.length ? Math.max(...anos) : null,
    transborda: document.documentElement.scrollWidth > innerWidth + 2,
    palavras: (txt.match(/\S+/g) || []).length,
    gerador: (document.querySelector('meta[name="generator"]') || {}).content || '',
    wordpress: /wp-content|wp-includes/.test(document.documentElement.outerHTML),
  };
}"""


def lighthouse(url, demo=False):
    t0 = time.time()
    # As demos têm «noindex» de propósito (não aparecem no Google): sem isso a nota SEO cairia ~34 pontos por
    # uma escolha nossa que o site do cliente não teria. Só nas demos se salta essa verificação.
    extra = ["--skip-audits=is-crawlable"] if demo else []
    r = subprocess.run(["lighthouse", url, *extra, "--quiet", "--output=json", "--output-path=/tmp/lh.json",
                        "--only-categories=performance,accessibility,best-practices,seo", "--max-wait-for-load=45000",
                        "--chrome-flags=--headless=new --no-sandbox --disable-gpu"], capture_output=True, text=True, timeout=180)
    if r.returncode or not os.path.exists("/tmp/lh.json"):
        raise RuntimeError("lighthouse: " + (r.stderr.strip().splitlines() or ["?"])[-1][:200])
    j = json.load(open("/tmp/lh.json", encoding="utf-8")); os.remove("/tmp/lh.json")
    if j.get("runtimeError"):
        raise RuntimeError("lighthouse: " + j["runtimeError"].get("message", "")[:200])
    aud = {}
    for k in AUD:
        a = j["audits"].get(k)
        if not a:
            continue
        d = {"nota": a.get("score"), "valor": a.get("numericValue"), "texto": a.get("displayValue", "")}
        det = a.get("details") or {}
        if det.get("overallSavingsMs"):
            d["poupa_ms"] = det["overallSavingsMs"]
        if det.get("overallSavingsBytes"):
            d["poupa_bytes"] = det["overallSavingsBytes"]
        if k == "network-requests":
            d["valor"] = len(det.get("items", []))
        aud[k] = d
    return {"notas": {c: round((v.get("score") or 0) * 100) for c, v in j["categories"].items()},
            "auditorias": aud, "url_final": j.get("finalDisplayedUrl") or j.get("finalUrl"),
            "lighthouse": j.get("lighthouseVersion"), "segundos": round(time.time() - t0)}


def medir_todos(lista):
    from playwright.sync_api import sync_playwright
    os.makedirs("auditorias/dados", exist_ok=True)
    rel = []
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=os.environ.get("CHROMIUM") or None)
        tel = dict(pw.devices["iPhone 13"]); tel.pop("default_browser_type", None)
        for nome, url in lista:
            d = {"nome": nome, "url": url, "medido_em": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())}
            try:
                d.update(lighthouse(url, demo=nome.startswith("demo-")))
            except Exception as ex:
                d["erro_lighthouse"] = str(ex)
            try:
                ctx = b.new_context(**tel, locale="ro-RO")
                pg = ctx.new_page()
                t0 = time.time()
                r = pg.goto(url, wait_until="load", timeout=60000)
                d["carga_real_s"] = round(time.time() - t0, 1)
                d["http"] = r.status if r else None
                pg.wait_for_timeout(2500)
                d["pagina"] = pg.evaluate(CHECAR)
                d["url_final_tel"] = pg.url
                pg.screenshot(path=f"auditorias/dados/{nome}.jpg", type="jpeg", quality=72)
                ctx.close()
            except Exception as ex:
                d["erro_pagina"] = str(ex)[:300]
            json.dump(d, open(f"auditorias/dados/{nome}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            n = d.get("notas", {})
            rel.append(f"{'ok ' if 'notas' in d else 'ERRO'} auditar {nome} desempenho {n.get('performance', '?')} "
                       f"seo {n.get('seo', '?')} acess. {n.get('accessibility', '?')} {d.get('erro_lighthouse', '')} {d.get('erro_pagina', '')}".strip())
        b.close()
    return rel
