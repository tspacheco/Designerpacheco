"""Brief de autoridade «AI în operațiuni» (RO e PT), 2 páginas A4.

Uso: python3 gerar.py                      → saida/brief-ro.pdf e saida/brief-pt.pdf
     python3 gerar.py --pentru "MedLife"   → versão com «Pregătit pentru MedLife» na capa
Os números têm todos fonte e data (HONEST-DATA). Mudar texto aqui, nunca no HTML gerado.
"""
import argparse
import html
import os
import re
import subprocess

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, "saida")
FONTES = "../../../../marca/fontes"  # relativo a saida/

TEXTO = {
    "ro": {
        "lang": "ro", "data": "11 octombrie 2026",
        "eyebrow": "Pacheco Studios · Iași · Consultanță de sisteme cu AI",
        "titlu": "AI în operațiuni",
        "sub": "Ce au deja companiile din SUA și China. Ce poate avea compania ta, de azi.",
        "pentru": "Pregătit pentru",
        "s1": "Ce s-a schimbat",
        "fapte": [
            ("78%", "dintre organizații foloseau AI în 2024, față de 55% în 2023.", "Stanford HAI, AI Index 2025"),
            ("109 mld. $", "investiții private în AI în SUA, în 2024. China deține 69,7% din brevetele AI acordate în 2023.", "Stanford HAI, AI Index 2025"),
            ("5,2%", "dintre companiile din România (peste 10 angajați) folosesc AI. Media UE: 20%. Danemarca: 42%.", "Eurostat, 2025"),
            ("2,3 mil.", "de conversații preluate de asistentul AI Klarna în prima lună. Timp de rezolvare: de la 11 minute la sub 2.", "Klarna, cifre proprii, feb. 2024"),
        ],
        "s1_nota": "Diferența nu e tehnologia. Companiile care obțin rezultate au pus AI-ul pe predările dintre oameni, canale și echipe, cu reguli scrise și cu un om la decizie.",
        "s2": "Ce înseamnă un sistem AI în operațiuni",
        "s2_sub": "Nu un chatbot. Un traseu cu reguli, de la prima cerere până la pasul următor.",
        "pasi": ["Trigger", "Context", "Decizie", "Predare", "Livrare", "Pasul următor"],
        "reguli": [
            ("Trigger: ce s-a întâmplat?", "Un eveniment real pornește fluxul: o cerere, o rezervare, un bon, un semnal. Contextul lui călătorește mai departe, clientul nu repetă."),
            ("Responsabil: cine face pasul următor?", "O persoană anume, cu termen. Niciodată un inbox fără nume."),
            ("Regula: ce poate și ce nu poate face sistemul?", "Sursă, limite, timp și aprobare, scrise. AI-ul aplică regula; totul rămâne trasabil."),
            ("Predarea la om: când intră o persoană?", "Excepție, dubiu, reclamație sau decizie importantă. La limită decide un om, nu un model."),
        ],
        "s3": "Drumul: de la 3 soluții rapide la un sistem",
        "etape": [
            ("1", "3 soluții rapide, fără cost", "Alese din situația de azi, implementate în zile, nu în luni. Se văd din afară și se măsoară. Sunt punctul de plecare, nu produsul."),
            ("2", "Triaj scurt", "Trei întrebări: ce rezultat operațional contează în 90 de zile, unde se blochează cererea, cine e responsabil de pasul următor. Dacă o soluție simplă e mai bună, o spunem."),
            ("3", "Audit de Sisteme cu AI", "Harta sistemului actual, blocajele în ordinea valorii, System Print-ul viitor, note de risc și responsabilitate, plan pe 90 de zile."),
            ("4", "Sprint de design și pilot", "Specificație aprobată, apoi un pilot controlat: bază măsurată în ziua 0, rezultat, registru de excepții, predare către echipă."),
        ],
        "s4": "Exemple de soluții rapide",
        "exemple": [
            ("Companie mare", ["Formular de cerere care ajunge structurat la echipa potrivită, cu contextul inclus.", "Triere a mesajelor repetitive după o regulă scrisă, cu predare la om la limită.", "Registru al excepțiilor: responsabil, termen, stare."]),
            ("Agenție / servicii B2B", ["Brief care se păstrează intact de la vânzare la producție și la raportare.", "Răspunsuri rapide pentru cele mai frecvente 5 cereri ale clienților.", "Fișă de predare client → echipă, cu cine decide ce."]),
            ("Fondator / afacere locală", ["Răspunsuri rapide pe WhatsApp și Instagram, cu regulă pentru când preia un om.", "Fișă Google completă, cu programare, și afiș QR pentru recenzii.", "Mesaj de urmărire după serviciu, cu cerere de recenzie."]),
        ],
        "s5": "Ce nu facem",
        "nu": [
            "Nu începem cu „facem site-uri” sau „facem automatizări”. Începem cu blocajul și recomandăm cea mai mică intervenție care poate dovedi valoare.",
            "Nu luăm decizii medicale, de credit sau juridice. Acolo decide mereu un om.",
            "Nu promitem „automatizare totală”. Diferența noastră e metoda: reguli, responsabil, predare umană.",
            "Nu deducem probleme interne din ce e public. Lucrăm cu ipoteze de validat împreună.",
            "Nu folosim date private fără acord scris.",
        ],
        "s6": "Cine suntem",
        "cine": "Pacheco Studios, Iași. Consultanță de sisteme cu AI pentru afaceri de servicii din România, Portugalia și Brazilia. Găsim scurgerea. Desenăm sistemul. Dovedim impactul. Fondator: Tomás Pacheco.",
        "cta": ("Scrie AUDIT", "în DM pe Instagram @pachecostudiospt și primești întrebările de diagnostic. Sau direct pe WhatsApp."),
        "motto": ("Nu promitem.", "Arătăm."),
        "contacte": [("WhatsApp", "+40 723 098 556"), ("Site", "ro.pachecost.com"), ("Instagram", "@pachecostudiospt")],
        "surse_t": "Surse",
        "surse": "Stanford HAI, AI Index Report 2025 · Eurostat, Use of artificial intelligence in enterprises, 2025 · Klarna, comunicat din 27 februarie 2024 (cifre raportate de companie).",
    },
    "pt": {
        "lang": "pt-PT", "data": "11 de outubro de 2026",
        "eyebrow": "Pacheco Studios · Iași · Consultoria de sistemas com IA",
        "titulo": "IA nas operações",
        "sub": "O que as empresas dos EUA e da China já têm. O que a tua empresa pode ter, a partir de hoje.",
        "pentru": "Preparado para",
        "s1": "O que mudou",
        "fapte": [
            ("78%", "das organizações usavam IA em 2024, contra 55% em 2023.", "Stanford HAI, AI Index 2025"),
            ("109 mil M$", "de investimento privado em IA nos EUA, em 2024. A China tem 69,7% das patentes de IA concedidas em 2023.", "Stanford HAI, AI Index 2025"),
            ("5,2%", "das empresas da Roménia (mais de 10 trabalhadores) usam IA. Média da UE: 20%. Dinamarca: 42%.", "Eurostat, 2025"),
            ("2,3 M", "de conversas tratadas pelo assistente de IA da Klarna no primeiro mês. Tempo de resolução: de 11 minutos para menos de 2.", "Klarna, números próprios, fev. 2024"),
        ],
        "s1_nota": "A diferença não é a tecnologia. As empresas com resultados puseram a IA nas passagens entre pessoas, canais e equipas, com regras escritas e uma pessoa na decisão.",
        "s2": "O que é um sistema de IA nas operações",
        "s2_sub": "Não é um chatbot. É um percurso com regras, do primeiro pedido ao passo seguinte.",
        "pasi": ["Trigger", "Contexto", "Decisão", "Handoff", "Entrega", "Próximo passo"],
        "reguli": [
            ("Trigger: o que aconteceu?", "Um evento real inicia o fluxo: um pedido, uma reserva, um recibo, um sinal. O contexto viaja com ele, o cliente não repete."),
            ("Dono: quem faz a próxima ação?", "Uma pessoa concreta, com prazo. Nunca uma caixa de entrada sem nome."),
            ("Regra: o que o sistema pode e não pode fazer?", "Fonte, limites, timing e aprovação, por escrito. A IA aplica a regra; tudo fica rastreável."),
            ("Handoff: quando entra uma pessoa?", "Exceção, dúvida, reclamação ou decisão material. No limite decide uma pessoa, não um modelo."),
        ],
        "s3": "O caminho: de 3 soluções rápidas a um sistema",
        "etape": [
            ("1", "3 soluções rápidas, sem custo", "Escolhidas pela situação de hoje, implementadas em dias, não em meses. Vêem-se de fora e medem-se. São o ponto de partida, não o produto."),
            ("2", "Triagem curta", "Três perguntas: que resultado operacional conta nos próximos 90 dias, onde abranda o pedido, quem é dono do próximo passo. Se uma solução simples for melhor, dizemo-lo."),
            ("3", "Auditoria de Sistemas com IA", "Mapa do sistema atual, fugas por ordem de valor, System Print futuro, notas de risco e propriedade, plano de 90 dias."),
            ("4", "Sprint de desenho e piloto", "Especificação aprovada, depois um piloto controlado: base medida no dia 0, resultado, registo de exceções, handover à equipa."),
        ],
        "s4": "Exemplos de soluções rápidas",
        "exemple": [
            ("Grande empresa", ["Formulário de pedido que chega estruturado à equipa certa, com o contexto incluído.", "Triagem das mensagens repetitivas por uma regra escrita, com passagem a uma pessoa no limite.", "Registo das exceções: responsável, prazo, estado."]),
            ("Agência / serviços B2B", ["Briefing que se mantém intacto da venda à produção e ao relatório.", "Respostas rápidas para os 5 pedidos mais frequentes dos clientes.", "Ficha de passagem cliente → equipa, com quem decide o quê."]),
            ("Fundador / negócio local", ["Respostas rápidas no WhatsApp e no Instagram, com regra para quando entra uma pessoa.", "Ficha Google completa, com marcação, e cartaz QR para avaliações.", "Mensagem de seguimento depois do serviço, com pedido de avaliação."]),
        ],
        "s5": "O que não fazemos",
        "nu": [
            "Não começamos por «fazemos sites» ou «fazemos automações». Começamos pelo gargalo e recomendamos a menor intervenção que prove valor.",
            "Não tomamos decisões médicas, de crédito ou jurídicas. Aí decide sempre uma pessoa.",
            "Não prometemos «automação total». A nossa diferença é o método: regras, responsável, passagem humana.",
            "Não deduzimos problemas internos a partir do que é público. Trabalhamos com hipóteses a validar em conjunto.",
            "Não usamos dados privados sem acordo escrito.",
        ],
        "s6": "Quem somos",
        "cine": "Pacheco Studios, Iași. Consultoria de sistemas com IA para negócios de serviços da Roménia, de Portugal e do Brasil. Encontramos a fuga. Desenhamos o sistema. Provamos o impacto. Fundador: Tomás Pacheco.",
        "cta": ("Escreve AUDIT", "por DM no Instagram @pachecostudiospt e recebes as perguntas de diagnóstico. Ou diretamente pelo WhatsApp."),
        "motto": ("Não prometemos.", "Mostramos."),
        "contacte": [("WhatsApp", "+351 967 117 357"), ("Site", "pachecost.com"), ("Instagram", "@pachecostudiospt")],
        "surse_t": "Fontes",
        "surse": "Stanford HAI, AI Index Report 2025 · Eurostat, Use of artificial intelligence in enterprises, 2025 · Klarna, comunicado de 27 de fevereiro de 2024 (números reportados pela empresa).",
    },
}

CSS = """
@font-face{font-family:AB;src:url(%(f)s/archivo-black.woff2) format("woff2")}
@font-face{font-family:AB;src:url(%(f)s/archivo-black-latin-ext.woff2) format("woff2");unicode-range:U+0100-024F,U+0259,U+1E00-1EFF,U+2020,U+20A0-20AB,U+20AD-20CF,U+2113,U+2C60-2C7F,U+A720-A7FF}
@font-face{font-family:SM;font-weight:400;src:url(%(f)s/space-mono-400.woff2) format("woff2")}
@font-face{font-family:SM;font-weight:400;src:url(%(f)s/space-mono-400-latin-ext.woff2) format("woff2");unicode-range:U+0100-024F,U+0259,U+1E00-1EFF,U+2020,U+20A0-20AB,U+20AD-20CF,U+2113,U+2C60-2C7F,U+A720-A7FF}
@font-face{font-family:SM;font-weight:700;src:url(%(f)s/space-mono-700.woff2) format("woff2")}
@font-face{font-family:SM;font-weight:700;src:url(%(f)s/space-mono-700-latin-ext.woff2) format("woff2");unicode-range:U+0100-024F,U+0259,U+1E00-1EFF,U+2020,U+20A0-20AB,U+20AD-20CF,U+2113,U+2C60-2C7F,U+A720-A7FF}
@font-face{font-family:IN;font-weight:100 900;src:url(%(f)s/inter-var.woff2) format("woff2")}
@font-face{font-family:IN;font-weight:100 900;src:url(%(f)s/inter-var-latin-ext.woff2) format("woff2");unicode-range:U+0100-024F,U+0259,U+1E00-1EFF,U+2020,U+20A0-20AB,U+20AD-20CF,U+2113,U+2C60-2C7F,U+A720-A7FF}
:root{--c:#141210;--o:#EFEAE3;--l:#E8622C;--lt:#A64923;--sec:#4D4A47;--secc:#A5A19B;--tr:#D35A29}
@page{size:A4;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#fff;color:var(--c);font-family:IN,Inter,Arial,sans-serif;font-size:10.2pt;line-height:1.42}
.pg{width:210mm;height:297mm;padding:14mm 16mm 12mm;position:relative;page-break-after:always;overflow:hidden;background:var(--o)}
.pg:last-child{page-break-after:auto}
.ey{font-family:SM,monospace;font-size:7.6pt;letter-spacing:.14em;text-transform:uppercase;color:var(--sec)}
h1{font-family:AB,Impact,sans-serif;font-size:30pt;line-height:1;text-transform:uppercase;letter-spacing:.005em;margin:5mm 0 2.5mm}
h1 i{font-style:normal;color:var(--l)}
.sub{font-size:13.5pt;line-height:1.3;max-width:172mm;color:var(--c)}
.pentru{margin-top:4mm;font-family:SM,monospace;font-size:8.4pt;letter-spacing:.06em;color:var(--lt)}
h2{font-family:AB,Impact,sans-serif;font-size:12pt;text-transform:uppercase;letter-spacing:.02em;margin:9mm 0 4mm;padding-top:3.5mm;border-top:1.2pt solid var(--c);display:flex;align-items:baseline;gap:3mm}
h2 small{font-family:SM,monospace;font-size:7.4pt;font-weight:400;letter-spacing:.12em;color:var(--lt)}
.fapte{display:grid;grid-template-columns:1fr 1fr;gap:5mm 7mm}
.fapt{border-left:2.2pt solid var(--l);padding:1mm 0 1mm 3.5mm}
.fapt b{display:block;font-family:AB,Impact,sans-serif;font-size:23pt;line-height:1;margin-bottom:1.2mm}
.fapt p{font-size:10.4pt;line-height:1.38}
.fapt small{display:block;font-family:SM,monospace;font-size:7.2pt;color:var(--sec);margin-top:1.2mm;letter-spacing:.04em}
.nota{margin-top:6mm;font-size:11.4pt;line-height:1.42;padding:4mm 5mm;background:var(--c);color:var(--o)}
.nota b{color:var(--l)}
.s2sub{font-size:10pt;color:var(--sec);margin:-1.5mm 0 3.5mm}
.pasi{display:flex;align-items:center;gap:0;margin:0 0 6mm}
.pas{flex:1;text-align:center;font-family:SM,monospace;font-size:8pt;font-weight:700;letter-spacing:.06em;text-transform:uppercase;padding:3.4mm 1mm;border:1pt solid var(--c);background:#fff}
.pas.l{background:var(--l);border-color:var(--l);color:var(--c)}
.arr{width:4mm;text-align:center;font-family:SM,monospace;font-size:9pt;color:var(--tr)}
.reguli{display:grid;grid-template-columns:1fr 1fr;gap:4.5mm 7mm}
.reg{display:grid;grid-template-columns:6mm 1fr;gap:2mm;align-items:start}
.reg i{font-style:normal;font-family:SM,monospace;font-weight:700;font-size:8pt;color:var(--lt);padding-top:.5mm}
.reg b{display:block;font-weight:650;font-size:11pt}
.reg p{font-size:10.2pt;color:var(--sec);line-height:1.38}
.etape{display:grid;grid-template-columns:repeat(4,1fr);gap:3mm}
.cta{margin-top:5mm;display:grid;grid-template-columns:auto 1fr;gap:4mm;align-items:center;background:var(--c);color:var(--o);padding:3.5mm 5mm}
.cta b{font-family:AB,Impact,sans-serif;font-size:14pt;text-transform:uppercase;color:var(--l);white-space:nowrap}
.cta p{font-size:10.4pt;line-height:1.38}
.et{background:#fff;border:1pt solid #D6CFC5;padding:3.5mm 3.5mm 4mm}
.et i{font-style:normal;display:inline-block;font-family:AB,Impact,sans-serif;font-size:20pt;color:var(--l);line-height:1;margin-bottom:1.5mm}
.et b{display:block;font-size:10pt;font-weight:650;margin-bottom:1.4mm;text-wrap:balance}
.et p{font-size:9pt;color:var(--sec);line-height:1.36}
.ex{display:grid;grid-template-columns:1fr 1fr 1fr;gap:4mm}
.ex h3{font-family:SM,monospace;font-size:8pt;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--lt);margin-bottom:1.8mm;padding-bottom:1.2mm;border-bottom:1pt solid var(--tr)}
.ex ul{list-style:none}
.ex li{font-size:9.8pt;line-height:1.36;padding-left:3.4mm;position:relative;margin-bottom:2mm}
.ex li::before{content:"";position:absolute;left:0;top:1.7mm;width:1.6mm;height:1.6mm;background:var(--l)}
.nu{columns:2;column-gap:6mm}
.nu li{list-style:none;font-size:10.2pt;line-height:1.38;padding-left:4.2mm;position:relative;margin-bottom:2.4mm;break-inside:avoid}
.nu li::before{content:"—";position:absolute;left:0;color:var(--tr);font-family:SM,monospace}
.cine{display:grid;grid-template-columns:1fr auto;gap:8mm;align-items:end}
.cine p{font-size:10.6pt;max-width:112mm}
.motto{font-family:AB,Impact,sans-serif;font-size:17pt;text-transform:uppercase;line-height:1.05;margin-top:2mm}
.motto i{font-style:normal;color:var(--l)}
.ct{display:grid;gap:1.2mm;text-align:right}
.ct div{font-family:SM,monospace;font-size:9.4pt}
.ct div span{display:block;font-size:6.6pt;letter-spacing:.12em;text-transform:uppercase;color:var(--sec)}
.p2 h2{margin:5.5mm 0 3mm;padding-top:3mm}
.p2 .ex li{font-size:9.2pt;margin-bottom:1.5mm}
.p2 .nu li{font-size:9.6pt;margin-bottom:1.5mm}
.p2 .cta{margin-top:3.5mm;padding:3mm 4mm}
.p2 .cine p{font-size:10pt;max-width:108mm}
.p2 .motto{font-size:15pt}
.foot{position:absolute;left:16mm;right:16mm;bottom:9mm;display:flex;justify-content:space-between;gap:6mm;font-family:SM,monospace;font-size:6.6pt;color:var(--sec);letter-spacing:.03em;border-top:.6pt solid var(--secc);padding-top:2mm}
.foot .srs{max-width:150mm;line-height:1.35}
.dot{display:inline-block;width:2.2mm;height:2.2mm;background:var(--l);border-radius:50%;vertical-align:baseline;margin-left:.6mm}
"""


def E(s):
    return html.escape(s, quote=False)


def pagina1(t, pentru):
    titulo = t.get("titlu") or t.get("titulo")
    partes = titulo.split(" ")
    h1 = E(" ".join(partes[:-1])) + " <i>" + E(partes[-1]) + "</i>"
    fapte = "".join(
        f'<div class="fapt"><b>{E(n)}</b><p>{E(p)}</p><small>{E(s)}</small></div>' for n, p, s in t["fapte"])
    pasi = []
    for i, p in enumerate(t["pasi"]):
        if i:
            pasi.append('<div class="arr">→</div>')
        pasi.append(f'<div class="pas{" l" if i in (1, 2) else ""}">{E(p)}</div>')
    reguli = "".join(
        f'<div class="reg"><i>0{i + 1}</i><div><b>{E(a)}</b><p>{E(b)}</p></div></div>' for i, (a, b) in enumerate(t["reguli"]))
    pentru_html = f'<div class="pentru">{E(t["pentru"])}: {E(pentru)} · {E(t["data"])}</div>' if pentru else f'<div class="pentru">{E(t["data"])}</div>'
    nota = E(t["s1_nota"]).replace(E("reguli scrise"), "<b>reguli scrise</b>").replace(E("regras escritas"), "<b>regras escritas</b>")
    return f"""<section class="pg">
<div class="ey">{E(t["eyebrow"])}</div>
<h1>{h1}<span class="dot"></span></h1>
<p class="sub">{E(t["sub"])}</p>
{pentru_html}
<h2>{E(t["s1"])}<small>01</small></h2>
<div class="fapte">{fapte}</div>
<div class="nota">{nota}</div>
<h2>{E(t["s2"])}<small>02</small></h2>
<p class="s2sub">{E(t["s2_sub"])}</p>
<div class="pasi">{"".join(pasi)}</div>
<div class="reguli">{reguli}</div>
<div class="foot"><div>Pacheco Studios · {E(t["data"])}</div><div>1 / 2</div></div>
</section>"""


def pagina2(t):
    etape = "".join(f'<div class="et"><i>{E(n)}</i><b>{E(a)}</b><p>{E(b)}</p></div>' for n, a, b in t["etape"])
    ex = "".join(
        f'<div><h3>{E(h)}</h3><ul>{"".join(f"<li>{E(x)}</li>" for x in li)}</ul></div>' for h, li in t["exemple"])
    nu = "".join(f"<li>{E(x)}</li>" for x in t["nu"])
    ct = "".join(f'<div><span>{E(a)}</span>{E(b)}</div>' for a, b in t["contacte"])
    m1, m2 = t["motto"]
    return f"""<section class="pg p2">
<h2 style="margin-top:0;border-top:0;padding-top:0">{E(t["s3"])}<small>03</small></h2>
<div class="etape">{etape}</div>
<h2>{E(t["s4"])}<small>04</small></h2>
<div class="ex">{ex}</div>
<h2>{E(t["s5"])}<small>05</small></h2>
<ul class="nu">{nu}</ul>
<div class="cta"><b>{E(t["cta"][0])}</b><p>{E(t["cta"][1])}</p></div>
<h2>{E(t["s6"])}<small>06</small></h2>
<div class="cine"><div><p>{E(t["cine"])}</p><div class="motto">{E(m1)} <i>{E(m2)}</i></div></div><div class="ct">{ct}</div></div>
<div class="foot"><div class="srs">{E(t["surse_t"])}: {E(t["surse"])}</div><div>2 / 2</div></div>
</section>"""


def gerar_html(lg, pentru=""):
    t = TEXTO[lg]
    titulo = t.get("titlu") or t.get("titulo")
    return f"""<!doctype html><html lang="{t["lang"]}"><head><meta charset="utf-8"><title>{E(titulo)} · Pacheco Studios</title>
<style>{CSS.replace("%(f)s", FONTES)}</style></head><body>{pagina1(t, pentru)}{pagina2(t)}</body></html>"""


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pentru", default="", help="nome da empresa na capa")
    ap.add_argument("--so", choices=["ro", "pt"], help="gerar só uma língua")
    a = ap.parse_args()
    os.makedirs(SAIDA, exist_ok=True)
    pares = []
    for lg in ([a.so] if a.so else ["ro", "pt"]):
        nome = f"brief-{lg}" + (f"-{slug(a.pentru)}" if a.pentru else "")
        h = os.path.join(SAIDA, nome + ".html")
        with open(h, "w", encoding="utf-8") as f:
            f.write(gerar_html(lg, a.pentru))
        pares.append((h, os.path.join(SAIDA, nome + ".pdf")))
    subprocess.run(["node", os.path.join(AQUI, "imprimir.js")] + [x for p in pares for x in p], check=True)
    for _, pdf in pares:
        print(pdf)


if __name__ == "__main__":
    main()
