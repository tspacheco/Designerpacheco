"""Carrossel «Start here · AI Systems Audit» em romeno (10 slides, 1080x1350).

Recria o carrossel do Tomás (11/10/2026) com o slide 2 novo que ele enviou.
Uso: python3 gerar.py  →  saida/carrossel-ro.html; depois fotografar.js gera os JPG.
"""
import html
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
E = html.escape


def rich(s):
    """**negrito** e [[destaque]] (cor de acento) dentro de um texto já escapado."""
    s = E(s)
    out, i = "", 0
    while i < len(s):
        if s.startswith("**", i):
            j = s.index("**", i + 2)
            out += "<b>" + s[i + 2:j] + "</b>"
            i = j + 2
        elif s.startswith("[[", i):
            j = s.index("]]", i + 2)
            out += '<span class="ac">' + s[i + 2:j] + "</span>"
            i = j + 2
        else:
            out += s[i]
            i += 1
    return out


SLIDES = [
    {"tema": "esc", "eyebrow": "ÎNCEPE AICI · CE GĂSEȘTE UN AUDIT DE SISTEME CU AI", "marca": "PACHECO STUDIOS",
     "h1": "Ce găsește de fapt un<br>[[Audit de Sisteme cu AI.]]", "h1px": 84,
     "sub": "Problema ta cu AI nu e AI-ul. E locul unde lead-urile, deciziile și livrarea **se rup.**",
     "pill": "GLISEAZĂ CA SĂ VEZI CE GĂSIM →", "extra": "orbita",
     "rodape": "Primul lucru pe care îl diagnosticăm este operațiunea, nu unealta."},
    {"tema": "lar", "eyebrow": "CE DIAGNOSTICHEAZĂ AUDITUL", "marca": "PACHECO STUDIOS",
     "kicker": "ÎNAINTE SĂ DESENĂM SOLUȚIA", "h1": "Nu automatiza un<br>sistem stricat.", "h1px": 100,
     "sub": "Mai întâi găsim **ce se strică.**",
     "cartoes_esc": [("Lead-uri", "Fără pasul următor"), ("Predare", "Fără responsabil clar"),
                     ("Context", "Copiat sau pierdut"), ("Decizii", "Fără regulă aprobată")],
     "nota": "GLISEAZĂ · VEZI CUM ARATĂ FIECARE RUPTURĂ",
     "rodape": "Un audit găsește ruptura înainte să fie desenat sistemul."},
    {"tema": "esc", "eyebrow": "PRIMA SCURGERE PE CARE O CĂUTĂM", "marca": "PACHECO STUDIOS", "topo": True,
     "kicker": "01 / LEAD-URI", "h1": "Lead-urile fără responsabil<br>[[se răcesc.]]", "h1px": 80,
     "sub": "Un client te poate găsi prin mai multe puncte de contact și tot să nu aibă **un pas următor vizibil.**",
     "extra": "diag_leads",
     "rodape": "Așa arată de fapt „scurgerea de lead-uri”."},
    {"tema": "esc", "eyebrow": "A DOUA SCURGERE PE CARE O CĂUTĂM", "marca": "PACHECO STUDIOS", "topo": True,
     "kicker": "02 / CONTEXT", "h1": "Un client nu ar trebui<br>să aibă [[cinci povești.]]", "h1px": 84,
     "sub": "Când contextul e copiat între WhatsApp, e-mail, notițe și CRM, echipa reconstruiește mereu ce știe deja.",
     "extra": "diag_contexto",
     "rodape": "AI-ul are nevoie de context util înainte să poată fi de folos."},
    {"tema": "lar", "eyebrow": "A TREIA SCURGERE PE CARE O CĂUTĂM", "marca": "PACHECO STUDIOS",
     "kicker": "03 / DECIZII", "h1": "Fără regulă nu există<br>[[automatizare sigură.]]", "h1px": 84,
     "sub": "Dacă echipa spune „depinde”, sistemul are nevoie de o regulă de decizie înainte de o automatizare.",
     "cartoes": [("Cerere nouă", "Trebuie luată o decizie."), ("„Depinde”", "Regulile trăiesc doar în mintea oamenilor."),
                 ("Regulă aprobată", "Acum decizia se poate repeta.")],
     "rodape": "Regulile creează consecvență. Consecvența creează sisteme sigure."},
    {"tema": "esc", "eyebrow": "PREDAREA PE CARE O DESENĂM", "marca": "PACHECO STUDIOS",
     "kicker": "04 / JUDECATA UMANĂ", "h1": "Scopul nu e să automatizăm<br>[[totul.]]", "h1px": 82,
     "sub": "Auditul definește momentul în care un om trebuie să preia, înainte ca relația cu clientul să fie pusă în pericol.",
     "cartoes": [("Rutină", "Sistemul poate continua."), ("Incert", "Cazul trebuie escaladat."),
                 ("Uman", "Relația rămâne protejată.")],
     "rodape": "O predare către om funcționează doar când declanșatorul e clar."},
    {"tema": "esc", "eyebrow": "PRIORITATEA PE CARE O ALEGEM", "marca": "PACHECO STUDIOS",
     "kicker": "05 / PRIMA REPARAȚIE", "h1": "Rezolvă mai întâi<br>[[un singur blocaj.]]", "h1px": 88,
     "sub": "Cel mai bun prim proiect nu e cel mai spectaculos. E cel cu impact, urgență, date utilizabile și un responsabil clar.",
     "cartoes": [("Impact", "Schimbă un rezultat care contează?"), ("Fezabilitate", "Îl putem pilota cu datele existente?"),
                 ("Responsabil", "Îl poate conduce cineva după lansare?")],
     "rodape": "Începe cu blocajul cu cea mai mare valoare, nu cu cea mai populară unealtă."},
    {"tema": "esc", "eyebrow": "CU CE RĂMÂI", "marca": "PACHECO STUDIOS",
     "kicker": "REZULTATUL", "h1": "Un plan clar<br>[[pe 90 de zile.]]", "h1px": 92,
     "sub": "Nu o listă generică de unelte AI. Un plan prioritizat, pe baza procesului, a regulilor, a riscurilor și a metricii care contează cel mai mult.",
     "cartoes": [("Harta scurgerilor", "Vezi unde se rupe operațiunea."), ("Prioritate", "Alegi primul sistem potrivit."),
                 ("Plan", "Pilot, măsurare, revizuire, extindere.")],
     "rodape": "Întâi diagnosticul. Apoi implementarea."},
    {"tema": "lar", "eyebrow": "PENTRU CINE ESTE", "marca": "PACHECO STUDIOS",
     "h1": "Pentru afacerile cu un<br>[[blocaj operațional activ.]]", "h1px": 82,
     "sub": "Volum mare de cereri. Comunicare fragmentată. Follow-up manual. Mai multe unelte. Echipe care iau aceeași decizie în moduri diferite.",
     "pill": "NU PENTRU „HAI SĂ PUNEM AI UNDEVA”",
     "rodape": "Cea mai bună muncă începe cu o problemă care merită rezolvată."},
    {"tema": "lar", "eyebrow": "PACHECO STUDIOS / AUDITURI DE SISTEME CU AI", "marca": "VORBEȘTE CU NOI",
     "h1": "Găsește blocajul înainte<br>să automatizezi.", "h1px": 90,
     "sub": "Trimite „AUDIT” în mesaj privat și spune-ne care proces din afacerea ta pierde cel mai mult timp, bani sau follow-up.",
     "botao": "TRIMITE „AUDIT” ÎN PRIVAT",
     "rodape": "Salvează-l pentru următoarea ședință despre operațiuni."},
]

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{background:#000}
.slide{position:relative;width:1080px;height:1350px;overflow:hidden;font-family:"Liberation Sans",Arial,sans-serif;display:flex;flex-direction:column;align-items:center;text-align:center}
.esc{background:radial-gradient(60% 45% at 50% 40%,rgba(255,106,59,.10),transparent 70%),radial-gradient(55% 40% at 0% 100%,rgba(255,106,59,.16),transparent 70%),linear-gradient(160deg,#101115 0%,#111216 55%,#1c1d22 100%);color:#F5EFE6}
.esc::before{content:"";position:absolute;inset:0 0 50% 0;background:repeating-linear-gradient(90deg,rgba(255,255,255,.022) 0 1px,transparent 1px 36px);-webkit-mask:linear-gradient(#000,transparent);pointer-events:none}
.lar{background:radial-gradient(26% 17% at 50% 34%,rgba(110,36,14,.42),transparent 100%),linear-gradient(135deg,#FF956F 0%,#FF7F50 35%,#FF6C3D 65%,#EC5423 100%);color:#141214}
.lar::before{content:"";position:absolute;inset:0;background:repeating-linear-gradient(90deg,rgba(120,40,10,.10) 0 1px,transparent 1px 72px),repeating-linear-gradient(0deg,rgba(120,40,10,.10) 0 1px,transparent 1px 72px);pointer-events:none}
.top{position:absolute;top:66px;left:0;right:0;z-index:2}
.eyebrow{font-weight:700;font-size:19px;letter-spacing:.2em}
.esc .eyebrow{color:#F59A73}.lar .eyebrow{color:#5C2A17}
.marca{margin-top:14px;font-weight:700;font-size:17px;letter-spacing:.14em}
.esc .marca{color:#F3EEE8}.lar .marca{color:#141214}
.regua{width:66px;height:3px;margin:34px auto 0}
.esc .regua{background:#F26F43}.lar .regua{background:#1A1414}
.miolo{position:absolute;left:0;right:0;top:170px;bottom:150px;display:flex;flex-direction:column;align-items:center;justify-content:center;z-index:2;padding:0 60px}
.miolo.topo{justify-content:flex-start;padding-top:44px}
.kicker{font-weight:700;font-size:21px;letter-spacing:.16em;margin-bottom:26px}
.esc .kicker{color:#F59A73}.lar .kicker{color:#5C2A17}
h1{font-family:"Liberation Serif","Times New Roman",serif;font-weight:700;letter-spacing:-.06em;line-height:1}
.esc h1{color:#F5EFE6}.esc h1 .ac{color:#FF6A3B}
.lar h1{color:#141214}.lar h1 .ac{color:#FFF3E8}
.sub{margin-top:30px;font-size:29px;line-height:1.36;max-width:700px}
.esc .sub{color:#C9C4BE}.esc .sub b{color:#fff}
.lar .sub{color:#4A2112}.lar .sub b{color:#141214}
.pill{margin-top:40px;display:inline-block;border-radius:999px;padding:16px 26px;font-weight:700;font-size:19px;letter-spacing:.08em}
.esc .pill{border:1.5px solid rgba(242,111,67,.75);color:#F8A884}
.lar .pill{border:1.5px solid rgba(20,18,20,.7);color:#141214}
.botao{margin-top:44px;background:#121316;color:#fff;font-weight:700;font-size:27px;letter-spacing:.02em;padding:22px 30px}
.cartoes{margin-top:44px;display:grid;grid-template-columns:repeat(3,300px);gap:15px}
.cartao{height:170px;padding:30px 14px 0;text-align:center}
.cartao h3{font-family:"Liberation Serif","Times New Roman",serif;font-weight:700;font-size:34px;letter-spacing:-.045em;line-height:1}
.cartao p{margin-top:12px;font-size:17px;line-height:1.3}
.esc .cartao{background:rgba(255,255,255,.035);border:1px solid rgba(255,255,255,.16)}
.esc .cartao h3{color:#F5EFE6}.esc .cartao p{color:#C9C4BE}
.lar .cartao{border:1px solid rgba(60,20,8,.35)}
.lar .cartao h3{color:#141214}.lar .cartao p{color:#4A2112}
.c4{margin-top:40px;display:grid;grid-template-columns:repeat(2,351px);gap:18px}
.c4 div{background:#101115;height:142px;padding-top:32px;box-shadow:0 9px 0 rgba(150,50,20,.45)}
.c4 h3{font-family:"Liberation Serif","Times New Roman",serif;font-weight:700;font-size:46px;letter-spacing:-.05em;color:#FBF4EC;line-height:1}
.c4 p{margin-top:14px;font-size:17px;color:#FFD3BE}
.nota{margin-top:44px;font-weight:700;font-size:18px;letter-spacing:.16em;color:#4A2112}
.pag{position:absolute;left:76px;bottom:66px;font-weight:700;font-size:17px;letter-spacing:.04em;z-index:2}
.esc .pag{color:#C9C4BE}.esc .pag span{color:#F59A73}
.lar .pag{color:#4A2112}.lar .pag span{color:#FFC2A6}
.rod{position:absolute;right:76px;bottom:66px;max-width:360px;text-align:right;font-size:17px;line-height:1.3;z-index:2}
.esc .rod{color:#BDB8B2}.lar .rod{color:#5A2410}
/* diagramas */
.diag{position:relative;width:960px;margin-top:36px;border-top:1px solid rgba(255,255,255,.14);border-bottom:1px solid rgba(255,255,255,.14)}
.diag .n{position:absolute;display:flex;align-items:center;justify-content:center;border:1.5px solid rgba(255,255,255,.28);background:#121317;color:#F5EFE6;font-weight:700;font-size:20px;border-radius:999px}
.diag .n.o{border-color:rgba(255,106,59,.75);color:#FFA27E}
.diag .n.g{box-shadow:0 0 0 10px rgba(255,106,59,.10),0 0 26px rgba(255,106,59,.25)}
.diag .box{position:absolute;border:1.5px solid rgba(255,255,255,.28);border-radius:18px;background:#121317}
.diag .box b{display:block;margin-top:14px;color:#F59A73;font-size:19px;letter-spacing:.14em}
.diag .mini{position:absolute;top:46px;height:48px;border:1px solid rgba(255,255,255,.22);border-radius:8px;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px;color:#F5EFE6}
.diag .l{position:absolute;background:#F26F43}
.diag .d{position:absolute;width:12px;height:12px;margin:-6px 0 0 -6px;border-radius:50%;background:#FF6A3B;box-shadow:0 0 0 6px rgba(255,106,59,.15)}
.diag .lab{position:absolute;padding:0 12px;background:#121317;color:#F8A884;font-weight:700;font-size:15px;letter-spacing:.16em}
.legenda{margin-top:30px;font-size:22px;color:#C9C4BE}.legenda b{color:#fff}
.orbita{position:absolute;left:310px;top:1045px;width:460px;height:183px;border:1px solid rgba(242,111,67,.45);border-radius:50%;z-index:1}
.orbita i{position:absolute;top:41px;width:100px;height:100px;border-radius:50%;border:1px solid rgba(255,255,255,.22)}
.orbita em{position:absolute;left:216px;top:77px;width:28px;height:28px;border-radius:50%;background:#FF6A3B;box-shadow:0 0 0 16px rgba(255,106,59,.16)}
"""


def diag_leads():
    # Coordenadas relativas à caixa .diag (960 x 410); recriam o diagrama do original
    return """<div class="diag" style="height:408px">
<div class="box" style="left:35px;top:40px;width:255px;height:132px"><b>GOOGLE</b>
<div class="mini" style="left:13px;width:70px">Site</div><div class="mini" style="left:91px;width:70px">LinkedIn</div><div class="mini" style="left:169px;width:70px">Twitter</div></div>
<div class="n" style="left:325px;top:68px;width:160px;height:68px">WhatsApp</div>
<div class="n" style="left:556px;top:68px;width:160px;height:68px">Instagram</div>
<div class="l" style="left:162px;top:172px;width:2px;height:33px"></div>
<div class="l" style="left:404px;top:136px;width:2px;height:69px"></div>
<div class="l" style="left:635px;top:136px;width:2px;height:69px"></div>
<div class="l" style="left:162px;top:204px;width:474px;height:2px"></div>
<div class="lab" style="left:405px;top:176px;transform:translateX(-50%)">COLECTOR DE CANALE</div>
<div class="d" style="left:163px;top:205px"></div><div class="d" style="left:405px;top:205px"></div><div class="d" style="left:636px;top:205px"></div>
<div class="l" style="left:404px;top:205px;width:2px;height:50px"></div>
<div class="d" style="left:405px;top:255px"></div>
<div class="n o" style="left:305px;top:256px;width:200px;height:66px">Inbox comun</div>
<div class="l" style="left:404px;top:322px;width:2px;height:18px"></div>
<div class="d" style="left:405px;top:340px"></div>
<div class="n o g" style="left:235px;top:340px;width:340px;height:68px;transform:translateY(-1px)">Responsabil + pasul următor</div>
</div>
<p class="legenda">Toate sursele se adună înainte ca o persoană să preia <b>pasul următor.</b></p>"""


def diag_contexto():
    return """<div class="diag" style="height:360px;border:0">
<div class="n" style="left:150px;top:10px;width:160px;height:64px">WhatsApp</div>
<div class="n" style="left:650px;top:10px;width:160px;height:64px">E-mail</div>
<div class="l" style="left:229px;top:74px;width:2px;height:30px"></div>
<div class="l" style="left:729px;top:74px;width:2px;height:30px"></div>
<div class="l" style="left:229px;top:104px;width:502px;height:2px"></div>
<div class="d" style="left:230px;top:105px"></div><div class="d" style="left:730px;top:105px"></div><div class="d" style="left:480px;top:105px"></div>
<div class="l" style="left:479px;top:105px;width:2px;height:30px"></div>
<div class="d" style="left:480px;top:135px"></div>
<div class="n o g" style="left:320px;top:135px;width:320px;height:66px">Un singur context util</div>
<div class="d" style="left:480px;top:201px"></div>
<div class="l" style="left:479px;top:201px;width:2px;height:38px"></div>
<div class="l" style="left:289px;top:239px;width:382px;height:2px"></div>
<div class="d" style="left:290px;top:240px"></div><div class="d" style="left:670px;top:240px"></div>
<div class="l" style="left:289px;top:240px;width:2px;height:25px"></div>
<div class="l" style="left:669px;top:240px;width:2px;height:25px"></div>
<div class="n o" style="left:200px;top:265px;width:180px;height:64px">Tabel</div>
<div class="n o" style="left:580px;top:265px;width:180px;height:64px">Notițe CRM</div>
</div>
<p class="legenda" style="margin-top:6px">Patru locuri care țin contextul, <b>un singur client.</b></p>"""


def slide(s, i, total):
    tema = s["tema"]
    partes = []
    if s.get("kicker"):
        partes.append(f'<div class="kicker">{E(s["kicker"])}</div>')
    partes.append(f'<h1 style="font-size:{s["h1px"]}px">{rich(s["h1"]).replace("&lt;br&gt;", "<br>")}</h1>')
    partes.append(f'<p class="sub">{rich(s["sub"])}</p>')
    if s.get("extra") == "diag_leads":
        partes.append(diag_leads())
    if s.get("extra") == "diag_contexto":
        partes.append(diag_contexto())
    if s.get("cartoes"):
        partes.append('<div class="cartoes">' + "".join(
            f'<div class="cartao"><h3>{E(a)}</h3><p>{E(b)}</p></div>' for a, b in s["cartoes"]) + "</div>")
    if s.get("cartoes_esc"):
        partes.append('<div class="c4">' + "".join(
            f'<div><h3>{E(a)}</h3><p>{E(b)}</p></div>' for a, b in s["cartoes_esc"]) + "</div>")
    if s.get("nota"):
        partes.append(f'<p class="nota">{E(s["nota"])}</p>')
    if s.get("pill"):
        partes.append(f'<div class="pill">{E(s["pill"])}</div>')
    if s.get("botao"):
        partes.append(f'<div class="botao">{E(s["botao"])}</div>')
    orb = '<div class="orbita"><i style="left:70px"></i><i style="left:290px"></i><em></em></div>' if s.get("extra") == "orbita" else ""
    n = f"{i:02d}"
    return f"""<section class="slide {tema}">
<div class="top"><div class="eyebrow">{E(s["eyebrow"])}</div><div class="marca">{E(s["marca"])}</div><div class="regua"></div></div>
<div class="miolo{' topo' if s.get('topo') else ''}">{''.join(partes)}</div>{orb}
<div class="pag"><span>{n}</span> / {total}</div>
<div class="rod">{E(s["rodape"])}</div>
</section>"""


# No vídeo não se desliza: os textos «glisează» mudam (video.js lê carrossel-ro-video.html)
VIDEO = {"GLISEAZĂ CA SĂ VEZI CE GĂSIM →": "URMĂREȘTE CE GĂSIM",
         "GLISEAZĂ · VEZI CUM ARATĂ FIECARE RUPTURĂ": "URMEAZĂ: CUM ARATĂ FIECARE RUPTURĂ"}


def main():
    os.makedirs(os.path.join(AQUI, "saida"), exist_ok=True)
    for nome, troca in (("carrossel-ro.html", {}), ("carrossel-ro-video.html", VIDEO)):
        slides = [{k: troca.get(v, v) if isinstance(v, str) else v for k, v in s.items()} for s in SLIDES]
        corpo = "\n".join(slide(s, i, len(slides)) for i, s in enumerate(slides, 1))
        caminho = os.path.join(AQUI, "saida", nome)
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(f'<!doctype html><html lang="ro"><head><meta charset="utf-8"><title>Carusel Audit de Sisteme cu AI</title><style>{CSS}</style></head><body>{corpo}</body></html>')
        print(caminho)


if __name__ == "__main__":
    main()
