#!/usr/bin/env python3
"""Monta o site da Pacheco Studios (destino do QR do cartão) a partir de index.src.html + ../../marca/dados.json.

    python3 gerar.py

Escreve: index.html · 404.html · _redirects · netlify.toml · media/og.png · pacheco-studios-netlify.zip
e corre os testes (HTML, acessibilidade, formulário, sem scroll horizontal) com verificar.cjs.
Os contactos (telefone, email, domínio) vivem em marca/dados.json — os mesmos do cartão.
"""
import base64
import html
import json
import os
import re
import subprocess
import sys
import zipfile
from html.parser import HTMLParser
from urllib.parse import quote

AQUI = os.path.dirname(os.path.abspath(__file__))
MARCA = os.path.join(AQUI, "..", "..", "marca")
NODE_ENV = dict(os.environ, NODE_PATH="/opt/node22/lib/node_modules")

ICONES = {
    "chat": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>',
    "telefone": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>',
    "email": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><path d="M22 6l-10 7L2 6"/></svg>',
    "instagram": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="2" y="2" width="20" height="20" rx="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><path d="M17.5 6.5h.01"/></svg>',
}
MSG_GERAL = "Olá Tomás! Vi o cartão da Pacheco Studios e gostava de saber mais."
MSG_NEGOCIO = "Olá Tomás! Gostava de ver como ficaria o site do meu negócio: "


def fontes_css():
    def ff(fam, peso, fich):
        b64 = base64.b64encode(open(os.path.join(MARCA, "fontes", fich), "rb").read()).decode()
        return (f'@font-face{{font-family:"{fam}";font-weight:{peso};font-style:normal;font-display:swap;'
                f'src:url(data:font/woff2;base64,{b64}) format("woff2")}}')
    return "\n".join([ff("Archivo Black", "400", "archivo-black.woff2"), ff("Space Mono", "400", "space-mono-400.woff2"),
                      ff("Space Mono", "700", "space-mono-700.woff2"), ff("Inter", "100 900", "inter-var.woff2")])


def slogan_html(linhas):
    out = []
    for l in linhas:
        classe = "l o" if l.startswith("*") else "l"
        t = html.escape(l.strip("*"))
        if t.endswith("."):
            t = t[:-1] + '<span class="pf" aria-hidden="true"></span><span class="so-leitor">.</span>'
        out.append(f'<span class="{classe}">{t}</span>')
    return " ".join(out)


class Verificador(HTMLParser):
    VAZIOS = {"meta", "link", "img", "br", "hr", "input", "source", "area", "base", "col", "embed", "track", "wbr"}

    def __init__(self):
        super().__init__()
        self.pilha, self.erros, self.svg = [], [], 0

    def handle_starttag(self, t, a):
        if t == "svg":
            self.svg += 1
        if t not in self.VAZIOS and not self.svg:
            self.pilha.append(t)

    def handle_startendtag(self, t, a):
        pass

    def handle_endtag(self, t):
        if t == "svg":
            self.svg -= 1
            return
        if self.svg:
            return
        if self.pilha and self.pilha[-1] == t:
            self.pilha.pop()
        else:
            self.erros.append(t)


def validar(nome, h):
    p = Verificador()
    p.feed(h)
    ok = not p.pilha and not p.erros
    lang = "ptPT" if 'lang="pt-PT"' in h else "SEM-LANG"
    legal = "legal" if "livroreclamacoes" in h else "SEM-LEGAL"
    estado = "HTML-OK" if ok else "ERRO " + str(p.pilha[-3:]) + str(p.erros[-3:])
    falta = len(re.findall(r"\{\{[A-Z_]+\}\}", h))
    linha = f"  {nome}: {estado} | h1:{h.count('<h1')} | {lang} | {legal} | U+FFFD:{h.count(chr(0xFFFD))} | por preencher:{falta}"
    print(linha)
    return ok and h.count("<h1") == 1 and "livroreclamacoes" in h and chr(0xFFFD) not in h and "{{" not in h


def main():
    d = json.load(open(os.path.join(MARCA, "dados.json"), encoding="utf-8"))
    s = d["site"]  # textos da página (em português); contactos no topo de dados.json, partilhados com o cartão
    dominio = d["dominio"].strip().lower()
    url_site = f"https://{dominio}/"
    email, ig = d["email"].strip(), d["instagram"].lstrip("@")
    digitos = re.sub(r"\D", "", d.get("telefone", ""))
    if digitos.startswith("351") and len(digitos) == 12:
        digitos = digitos[3:]
    tel_ok = len(digitos) == 9
    tel_legivel = f"+351 {digitos[:3]} {digitos[3:6]} {digitos[6:]}" if tel_ok else ""  # sempre com o indicativo
    whatsapp = tel_ok and d.get("telefone_tem_whatsapp", True)

    if whatsapp:
        cta_url = f"https://wa.me/351{digitos}?text={quote(MSG_GERAL)}"
        cta_neg = f"https://wa.me/351{digitos}?text={quote(MSG_NEGOCIO)}"
        cta_txt, cta_ico = "Falar no WhatsApp", ICONES["chat"]
        cta_nota = "Diga-nos o nome do seu negócio no WhatsApp. Fazemos o site e mostramos-lho, sem compromisso."
    else:
        cta_url = f"mailto:{email}?subject={quote('Pacheco Studios — pedido de contacto')}&body={quote(MSG_GERAL)}"
        cta_neg = f"mailto:{email}?subject={quote('O site do meu negócio')}&body={quote(MSG_NEGOCIO)}"
        cta_txt, cta_ico = "Enviar email", ICONES["email"]
        cta_nota = "Escreva-nos com o nome do seu negócio. Fazemos o site e mostramos-lho, sem compromisso."

    contactos = []
    if whatsapp:
        contactos.append(("WhatsApp", tel_legivel, cta_url, "chat"))
    if tel_ok:
        contactos.append(("Telefone", tel_legivel, f"tel:+351{digitos}", "telefone"))
    contactos.append(("Email", email, f"mailto:{email}", "email"))
    contactos.append(("Instagram", f"@{ig}", f"https://www.instagram.com/{ig}/", "instagram"))
    contactos_html = "\n".join(
        f'        <li><a href="{html.escape(u)}"{" rel=noopener" if u.startswith("http") else ""}>{ICONES[i]}'
        f'<span class="txt"><span class="qual">{q}</span><span class="valor">{html.escape(v)}</span></span></a></li>'
        for q, v, u, i in contactos)

    jsonld = {"@context": "https://schema.org", "@type": "ProfessionalService", "name": "Pacheco Studios",
              "url": url_site, "image": url_site + "media/og.png",
              "description": "Sites, lojas online e automações para restaurantes, lojas e negócios do Algarve.",
              "areaServed": {"@type": "AdministrativeArea", "name": s["regiao"]},
              "email": email, "sameAs": [f"https://www.instagram.com/{ig}/"],
              "founder": {"@type": "Person", "name": d["nome"]}}
    if tel_ok:
        jsonld["telephone"] = tel_legivel

    valores = {
        "FONTES": fontes_css(), "URL_SITE": url_site, "DOMINIO": html.escape(dominio),
        "JSONLD": json.dumps(jsonld, ensure_ascii=False).replace("</", "<\\/"),
        "SLOGAN": slogan_html(s["slogan"]), "REGIAO": html.escape(s["regiao"].upper()),
        "REGIAO_TEXTO": html.escape(s["regiao"]), "NOME": html.escape(d["nome"]),
        "CTA_URL": html.escape(cta_url), "CTA_URL_NEGOCIO": html.escape(cta_neg), "CTA_TEXTO": cta_txt,
        "CTA_ICONE": cta_ico, "CTA_NOTA": cta_nota, "CONTACTOS": contactos_html,
    }
    src = open(os.path.join(AQUI, "index.src.html"), encoding="utf-8").read()
    pagina = re.sub(r"\{\{([A-Z_]+)\}\}", lambda m: valores[m.group(1)], src)
    open(os.path.join(AQUI, "index.html"), "w", encoding="utf-8").write(pagina)

    # 404: mesma folha de estilos, só o campo do endereço e o contacto
    estilo = re.search(r"<style>.*?</style>", pagina, re.S).group(0)
    p404 = f"""<!DOCTYPE html>
<html lang="pt-PT">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Endereço não encontrado — Pacheco Studios</title>
<meta name="robots" content="noindex">
<meta name="theme-color" content="#141210">
{estilo}
</head>
<body>
<a class="saltar" href="#conteudo">Saltar para o conteúdo</a>
<header class="envolver topo">
  <a class="marca" href="/" aria-label="Pacheco Studios — início"><span class="ponto" aria-hidden="true"></span><span aria-hidden="true">Pacheco Studios</span></a>
  <span class="regiao">{valores['REGIAO']}</span>
</header>
<main id="conteudo" class="envolver heroi">
  <p class="etiqueta">Endereço não encontrado</p>
  <h1 class="afirmacao">Este endereço não existe (ainda).</h1>
  <p class="intro">Confirme o que está escrito no espaço tracejado do cartão e tente outra vez.</p>
  <form class="endereco" id="form-endereco" action="/" method="get" novalidate>
    <label for="endereco">Escreva o que está depois de <b>{valores['DOMINIO']}/</b></label>
    <div class="linha-campo">
      <div class="campo">
        <span class="prefixo" aria-hidden="true">{valores['DOMINIO']}/</span>
        <input id="endereco" name="e" type="text" autocomplete="off" autocapitalize="none" autocorrect="off" spellcheck="false" enterkeyhint="go" placeholder="tasca-ria" aria-describedby="endereco-erro">
      </div>
      <button class="botao primario" type="submit">Abrir</button>
    </div>
    <p id="endereco-erro" class="erro" role="alert"></p>
  </form>
  <div class="accoes">
    <a class="botao primario" href="{valores['CTA_URL']}">{cta_ico}{cta_txt}</a>
    <a class="botao secundario" href="/">Ver a página inicial</a>
  </div>
</main>
<footer class="rodape">
  <div class="envolver">
    <p>Pacheco Studios · {valores['NOME']} · {valores['REGIAO_TEXTO']}</p>
    <p><a href="https://www.livroreclamacoes.pt/inicio" rel="noopener">Livro de Reclamações</a></p>
  </div>
</footer>
<script>
(function () {{
  var form = document.getElementById('form-endereco'), campo = document.getElementById('endereco'),
      erro = document.getElementById('endereco-erro'), dominio = '{valores['DOMINIO']}';
  form.addEventListener('submit', function (ev) {{
    ev.preventDefault();
    var v = campo.value.trim().toLowerCase().replace(/^https?:\\/\\//, '').replace(/^www\\./, '');
    if (v.indexOf(dominio) === 0) v = v.slice(dominio.length);
    v = v.replace(/^\\/+|\\/+$/g, '').normalize('NFD').replace(/[\\u0300-\\u036f]/g, '').replace(/\\s+/g, '-');
    if (!/^[a-z0-9-]{{1,40}}$/.test(v)) {{
      erro.textContent = v ? 'Esse endereço tem caracteres que não existem nos nossos links. Use só letras, números e hífenes, como está no cartão.'
                           : 'Escreva o endereço que está no cartão, por exemplo: tasca-ria';
      campo.setAttribute('aria-invalid', 'true'); campo.focus(); return;
    }}
    window.location.assign('/' + v);
  }});
}})();
</script>
</body>
</html>
"""
    open(os.path.join(AQUI, "404.html"), "w", encoding="utf-8").write(p404)

    # Netlify: o QR aponta para /c — o destino muda aqui, sem reimprimir cartões
    curtos = {k: v for k, v in d.get("enderecos_curtos", {}).items() if not k.startswith("_")}
    caminho = d.get("caminho_qr", "c").strip("/").lower()
    destino_qr = d.get("destino_qr", "/?origem=cartao").strip()
    red = ["# Gerado por gerar.py a partir de marca/dados.json — não editar à mão.",
           "# QR do cartão (https://%s/%s) → marca/dados.json: destino_qr. Muda-se sem reimprimir cartões." % (dominio, caminho.upper()),
           f"/{caminho}    {destino_qr}    302", f"/{caminho.upper()}    {destino_qr}    302",
           "# Campo \"Tem um endereço escrito no cartão?\" quando o JavaScript está desligado",
           "/    e=:e    /:e    302!",
           "# Endereços escritos à mão no cartão (marca/dados.json → enderecos_curtos)"]
    for slug, destino in sorted(curtos.items()):
        s = re.sub(r"[^a-z0-9-]", "", slug.lower())
        red.append(f"/{s}    {destino}    302")
    open(os.path.join(AQUI, "_redirects"), "w", encoding="utf-8").write("\n".join(red) + "\n")
    open(os.path.join(AQUI, "netlify.toml"), "w", encoding="utf-8").write(
        '[build]\npublish = "."\n\n[[headers]]\nfor = "/*"\n[headers.values]\nX-Content-Type-Options = "nosniff"\n'
        'Referrer-Policy = "strict-origin-when-cross-origin"\n\n[[headers]]\nfor = "/media/*"\n[headers.values]\n'
        'Cache-Control = "public, max-age=604800"\n')

    # imagem de partilha (WhatsApp/Facebook) 1200×630, com o slogan
    og = f"""<!DOCTYPE html><html lang="pt-PT"><head><meta charset="utf-8"><style>{valores['FONTES']}
    body{{margin:0;width:1200px;height:630px;background:#141210;color:#EFEAE3;position:relative;overflow:hidden}}
    .m{{position:absolute;left:84px;top:72px;display:flex;align-items:center;gap:18px;font:700 24px/1 "Space Mono";letter-spacing:.24em}}
    .m i{{width:18px;height:18px;border-radius:50%;background:#E8622C}}
    .r{{position:absolute;right:84px;top:72px;font:400 24px/1 "Space Mono";letter-spacing:.24em;color:#A5A19B}}
    h1{{position:absolute;left:80px;top:152px;margin:0;font:400 90px/.93 "Archivo Black";text-transform:uppercase}}
    h1 span{{display:block}} .o{{color:#E8622C}}
    .pf{{display:inline-block;width:.2em;height:.2em;border-radius:50%;background:#E8622C;margin-left:.06em}}
    .so-leitor{{display:none}}
    .s{{position:absolute;left:84px;bottom:60px;font:400 24px/1 "Space Mono";letter-spacing:.12em;color:#A5A19B;text-transform:uppercase}}
    </style></head><body><p class="m"><i></i>PACHECO STUDIOS</p><p class="r">{valores['REGIAO']}</p>
    <h1>{slogan_html(s['slogan'])}</h1><p class="s">{html.escape(s['servicos'])}</p></body></html>"""
    tmp_og = os.path.join(AQUI, ".og.html")
    open(tmp_og, "w", encoding="utf-8").write(og)
    subprocess.run(["node", "-e", """
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
  await p.goto('file://' + process.argv[1]); await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: process.argv[2] }); await b.close(); })();
""", tmp_og, os.path.join(AQUI, "media", "og.png")], check=True, env=NODE_ENV)
    os.remove(tmp_og)

    print("\nVALIDAÇÃO")
    ok = validar("index.html", pagina) & validar("404.html", p404)
    print(f"  index.html: {len(pagina.encode()) / 1024:.0f} KB (fontes embutidas) · media: "
          + ", ".join(f"{f} {os.path.getsize(os.path.join(AQUI, 'media', f)) // 1024} KB"
                      for f in sorted(os.listdir(os.path.join(AQUI, "media")))))

    zipp = os.path.join(AQUI, "pacheco-studios-netlify.zip")
    with zipfile.ZipFile(zipp, "w", zipfile.ZIP_DEFLATED) as z:
        for f in ("index.html", "404.html", "_redirects", "netlify.toml"):
            z.write(os.path.join(AQUI, f), f)
        for f in sorted(os.listdir(os.path.join(AQUI, "media"))):
            z.write(os.path.join(AQUI, "media", f), f"media/{f}")
    print(f"  zip Netlify: {os.path.getsize(zipp) // 1024} KB")

    r = subprocess.run(["node", os.path.join(AQUI, "verificar.cjs"), AQUI], env=NODE_ENV)
    if not tel_ok:
        print("\n⚠ Sem telefone em marca/dados.json: os botões usam o email em vez do WhatsApp.")
    sys.exit(0 if ok and r.returncode == 0 else 1)


if __name__ == "__main__":
    main()
