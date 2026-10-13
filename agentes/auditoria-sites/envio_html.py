#!/usr/bin/env python3
"""Página de envio para o telemóvel (artifact): um cartão por negócio com WhatsApp (mensagem + link do PDF já escritos),
abrir o PDF, copiar a mensagem e marcar como enviado.

  python3 envio_html.py ENVIAR-lote-2.md saida.html ["Raio-X · Lote 2"] ["20 negócios de Iași."] [chave]

Lê as secções «## n. Nome · categoria» do ENVIAR-lote-N.md gerado por raiox.py.
"""
import html, json, re, sys
from urllib.parse import quote

md = open(sys.argv[1], encoding="utf-8").read()
itens = []
for bloco in re.split(r"\n(?=## \d+\. )", md)[1:]:
    nome, _, cat = re.match(r"## \d+\. (.*)", bloco).group(1).partition(" · ")
    cat = re.sub(r"[^\w\s&,.\-]", "", cat).strip()
    g = lambda rx: (re.search(rx, bloco) or [None, ""])[1].strip()
    tel = g(r"Telefone (\+?\d+)")
    wa = g(r"WhatsApp: ([^·\n]+?) ·")
    pdf = g(r"PDF (?:RO )?\(dono\): (\S+)")
    msg = re.search(r"```\n(.*?)\n```", bloco, re.S).group(1).strip()
    google = g(r"Google ([\d,]+)")
    aval = g(r"Google [\d,]+ · ([\d.]+) avalia")
    fixo = "fixo" in wa
    itens.append(dict(nome=nome, cat=cat, tel=tel, fixo=fixo, google=google, aval=aval, morada=g(r"Morada: (.*?) · site"),
                      pdf=pdf, ficheiro=pdf.rsplit("/", 1)[-1], msg=msg, texto=msg,
                      wa=None if fixo else "https://wa.me/" + tel.lstrip("+") + "?text=" + quote(msg)))

PAGINA = open(__file__.replace("envio_html.py", "envio_modelo.html"), encoding="utf-8").read()
titulo, sub, chave = (sys.argv[3:] + ["Raio-X · Lote 2", "20 negócios de Iași.", "raiox-lote2-enviados"][len(sys.argv[3:]):])[:3]
out = (PAGINA.replace("/*DADOS*/[]", json.dumps(itens, ensure_ascii=False)).replace("Raio-X · Lote 2", html.escape(titulo))
       .replace("20 negócios de Iași.", html.escape(sub)).replace("raiox-lote2-enviados", chave).replace("<title>Envio Raio-X</title>", f"<title>{html.escape(titulo)}</title>").replace("0/20", f"0/{len(itens)}"))
open(sys.argv[2], "w", encoding="utf-8").write(out)
print(len(itens), "negócios,", sum(1 for i in itens if i["fixo"]), "fixos")
