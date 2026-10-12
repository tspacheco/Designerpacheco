# Versão para o dono da Magic Key: romeno em primeiro, inglês por baixo, sem notas internas.
# Gera intrebari-ro-en.html e Magic-Key-intrebari-RO-EN.pdf. Uso: python3 gerar_ro.py
import html, pathlib
import dados_ro as R, dados as E

AQUI = pathlib.Path(__file__).parent
FONTES = (AQUI / "../../../marca/fontes").resolve()
e = html.escape

TIT = {"A1": ("Obiectivul", "The goal"), "A2": ("Ziua de ieri", "Yesterday"), "A3": ("Clienți noi", "New customers"),
       "A4": ("Lucrarea", "The work"), "A5": ("După lucrare", "After the job"),
       "B1": ("Firma și echipa", "The company and the team"), "B2": ("Cererea de cheie auto", "The car key request"),
       "B3": ("Apeluri și mesaje pierdute", "Missed calls and messages"), "B4": ("Prețuri și ce aduce bani", "Prices and what makes money"),
       "B5": ("Deplasări și urgențe", "Call-outs and emergencies"), "B6": ("Recenzii și recomandări", "Reviews and word of mouth"),
       "B7": ("Ateliere, flote și parteneri", "Garages, fleets and partners"), "B8": ("Casă, stoc și furnizori", "Cash, stock and suppliers"),
       "FIM": ("Pentru final", "To finish")}
# ajustes ao texto para o dono ler (sem cenários nossos)
FIX = {"Într-o lună obișnuită, cât facturezi? Scenariul de 20.000 lei pe lună (aproximativ 800 lei pe zi, 25 de zile) e aproape de realitate sau departe?":
         ("Într-o lună obișnuită, cât facturezi, aproximativ?", "In a normal month, roughly how much do you invoice?")}

def grupos():
    out = []
    for gr, ge in zip(R.A + R.B, E.A + E.B):
        qs = [(q[2], qe[2]) for q, qe in zip(gr[4], ge[4])]
        out.append([gr[0], qs])
    a6, b9 = out[5], out[-1]
    fim = ["FIM", a6[1][:3] + b9[1]]
    return out[:5] + out[6:-1] + [fim]

def bloco(i, cod, qs, c):
    ro, en = TIT[cod]
    li = ""
    for r, en_q in qs:
        r, en_q = FIX.get(r, (r, en_q))
        c[0] += 1
        li += f"""<li class="q"><span class="n">{c[0]:02d}</span><div class="corpo"><p class="pt" lang="ro">{e(r)}</p>
<p class="ro" lang="en">{e(en_q)}</p><div class="linhas" aria-hidden="true"><i></i><i></i></div></div></li>"""
    brk = ' style="break-before:page"' if cod == "FIM" else ""
    return f"""<section class="bloco"{brk}><header class="bloco-cab"><span class="bn">{i}</span><div><h2 lang="ro">{e(ro)}</h2>
<p class="quem" lang="en">{e(en)}</p></div></header><ol class="qs">{li}</ol></section>"""

NUM = [("Apeluri pe zi (toate)", "Calls per day (all)"), ("Apeluri pentru chei auto pe zi", "Car key calls per day"),
       ("Apeluri fără răspuns pe săptămână", "Unanswered calls per week"), ("Mesaje WhatsApp / SMS pe zi", "WhatsApp / SMS messages per day"),
       ("Chei auto făcute pe săptămână", "Car keys made per week"), ("Preț mediu al unei chei auto cu cip", "Average price of a chip car key"),
       ("Marja aproximativă pe cheie auto", "Approximate margin per car key"), ("Cereri pierdute pe săptămână", "Lost requests per week"),
       ("Deplasări pe săptămână", "Call-outs per week"), ("Preț mediu al unei deplasări", "Average call-out price"),
       ("Ore pe săptămână la telefon", "Hours per week on the phone"), ("Încasări lunare (estimare)", "Monthly revenue (estimate)"),
       ("Zile lucrate pe lună", "Working days per month"), ("Recenzii Google noi pe lună", "New Google reviews per month")]
PROC = [("Ce declanșează cererea?", "What triggers the request?"), ("Cine se ocupă de ea?", "Who handles it?"),
        ("Ce reguli folosiți (program, prețuri, documente)?", "What rules do you use (hours, prices, documents)?"),
        ("Când trece la o persoană?", "When does it go to a person?")]

def gerar():
    c = [0]
    bl = "".join(bloco(i + 1, cod, qs, c) for i, (cod, qs) in enumerate(grupos()))
    num = "".join(f"<tr><td><span lang='ro'>{e(r)}</span><br><small class='ro' lang='en'>{e(en)}</small></td><td class='val'></td></tr>" for r, en in NUM)
    proc = "".join(f"<tr><td><span lang='ro'>{e(r)}</span><br><small class='ro' lang='en'>{e(en)}</small></td><td class='em'></td></tr>" for r, en in PROC)
    css = (AQUI / "estilo.css").read_text(encoding="utf-8").replace("FONTES/", FONTES.as_uri() + "/")
    css += ".sp td:first-child{font:400 10pt var(--texto);text-transform:none;color:var(--carvao);width:70mm}.num td small{font-size:8.5pt}.bloco-cab{break-inside:avoid}"
    doc = f"""<!doctype html><html lang="ro"><head><meta charset="utf-8"><title>Magic Key — întrebări pentru audit</title><style>{css}</style></head><body>
<section class="capa"><div class="marca">PACHECO STUDIOS<span class="ponto"></span></div>
<div class="capa-meio"><p class="kicker">Audit · întrebări / audit questions</p><h1>Magic Key<br>chei auto</h1><p class="sub">Iași · Selgros, Șos. Nicolina 57A</p></div>
<dl class="capa-dados"><div><dt>Pentru / For</dt><dd>Magic Key</dd></div><div><dt>Data / Date</dt><dd>octombrie 2026</dd></div>
<div><dt>Întrebări / Questions</dt><dd>{c[0]}</dd></div><div><dt>Limbă / Language</dt><dd>Română · English</dd></div></dl></section>
<section class="pagina intro"><h2 class="titulo">Cum folosim aceste întrebări</h2>
<div class="duas"><div><p lang="ro">Aceste întrebări ne ajută să înțelegem cum funcționează standul zi de zi: cum ajung cererile, unde se pierd și ce merită făcut mai întâi. Puteți răspunde direct pe foaie sau în conversație. Nu există răspunsuri greșite. Dacă nu știți o cifră exactă, o estimare este suficientă.</p>
<p lang="ro" style="margin-top:4mm">Tot ce ne spuneți rămâne confidențial.</p></div>
<div><p class="ro" lang="en">These questions help us understand how the stand works day to day: how requests come in, where they get lost and what is worth doing first. You can answer directly on the sheet or in conversation. There are no wrong answers. If you don't know an exact number, an estimate is enough.</p>
<p class="ro" lang="en" style="margin-top:4mm">Everything you tell us stays confidential.</p></div></div></section>
{bl}
<section class="pagina"><h2 class="titulo">Cum ajunge o cerere la voi</h2><p class="lead">How a request reaches you</p>
<table class="sp"><tbody>{proc}</tbody></table>
<h2 class="titulo" style="margin-top:10mm">Cifre</h2><p class="lead">Numbers · o estimare este suficientă / an estimate is enough</p>
<table class="num"><tbody>{num}</tbody></table></section>
</body></html>"""
    (AQUI / "intrebari-ro-en.html").write_text(doc, encoding="utf-8")
    return c[0]

def pdf():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        pg = b.new_page(); pg.goto((AQUI / "intrebari-ro-en.html").as_uri(), wait_until="networkidle"); pg.evaluate("document.fonts.ready")
        pg.pdf(path=str(AQUI / "Magic-Key-intrebari-RO-EN.pdf"), format="A4", print_background=True,
               margin={"top": "0", "bottom": "0", "left": "0", "right": "0"}, prefer_css_page_size=True)
        b.close()

if __name__ == "__main__":
    print(gerar()); pdf()
