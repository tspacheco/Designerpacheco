# Pacheco Studios — destaques do Instagram em EN (1080x1920), 31 out 2026.
# python3 build.py  -> gera 0X-*.html ; render.js -> PNG
import pathlib

HERE = pathlib.Path(__file__).parent

CSS = r"""
@font-face{font-family:"Archivo Black";src:url("archivo-black.woff2") format("woff2")}
@font-face{font-family:"Space Mono";font-weight:400;src:url("space-mono-400.woff2") format("woff2")}
@font-face{font-family:"Space Mono";font-weight:700;src:url("space-mono-700.woff2") format("woff2")}
@font-face{font-family:"InterV";font-weight:100 900;src:url("inter-var.woff2") format("woff2")}
:root{--bg:#141210;--ink:#EFEAE3;--o:#E8622C;--dim:rgba(239,234,227,.55);--line:rgba(239,234,227,.16)}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1920px;background:var(--bg);color:var(--ink);font-family:"InterV",sans-serif;position:relative;overflow:hidden}
.glow{position:absolute;right:-220px;top:40px;width:780px;height:780px;background:radial-gradient(circle,rgba(232,98,44,.17),transparent 62%)}
.glow2{position:absolute;left:-260px;bottom:-180px;width:660px;height:660px;background:radial-gradient(circle,rgba(232,98,44,.08),transparent 62%)}
.frame{position:relative;z-index:2;height:100%;display:flex;flex-direction:column;padding:120px 96px 110px}
.top{display:flex;justify-content:space-between;align-items:baseline;font-family:"Space Mono",monospace}
.top .tag{color:var(--o);font-size:30px;font-weight:700;letter-spacing:.42em}
.top .num{color:var(--dim);font-size:30px;letter-spacing:.2em}
h1{font-family:"Archivo Black",sans-serif;font-size:92px;line-height:1.04;margin-top:96px;text-transform:uppercase}
h1 .o,.o{color:var(--o)}
.lead{margin-top:34px;font-size:38px;line-height:1.45;color:rgba(239,234,227,.82);max-width:860px}
.mono{font-family:"Space Mono",monospace;text-transform:uppercase;letter-spacing:.16em}
.foot{margin-top:auto;border-top:2px solid var(--line);padding-top:44px;display:flex;justify-content:space-between;align-items:center;font-family:"Space Mono",monospace;font-size:30px;letter-spacing:.24em}
.foot .brand{display:flex;align-items:center;gap:18px}
.dot{display:inline-block;width:16px;height:16px;border-radius:50%;background:var(--o)}
.foot .ig{color:var(--dim)}
.btn{display:inline-flex;align-items:center;gap:18px;background:var(--o);color:#141210;font-family:"Space Mono",monospace;font-weight:700;font-size:34px;letter-spacing:.14em;text-transform:uppercase;border-radius:999px;padding:30px 56px}
"""

def page(tag, num, body, foot_right="@PACHECOSTUDIOSPT", extra_css=""):
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=1080"><title>Pacheco Studios — {tag}</title>
<style>{CSS}{extra_css}</style></head><body>
<div class="glow"></div><div class="glow2"></div>
<div class="frame">
<div class="top"><span class="tag">{tag}</span><span class="num">{num}&nbsp;/&nbsp;05</span></div>
{body}
<div class="foot"><span class="brand"><span class="dot"></span>PACHECO STUDIOS</span><span class="ig">{foot_right}</span></div>
</div></body></html>"""

# ---------- 01 THE STUDIO ----------
s1_css = """
.center{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;margin-top:-40px}
.logo{width:340px;height:340px}
.name{font-family:"Archivo Black";font-size:118px;line-height:.98;margin-top:48px;text-transform:uppercase}
.sub{margin-top:36px;font-size:42px;color:rgba(239,234,227,.8)}
.motto{margin-top:70px;display:flex;flex-direction:column;gap:14px;font-family:"Archivo Black";font-size:54px;line-height:1.12;text-transform:uppercase}
.motto span:nth-child(2){color:var(--o)}
.founder{margin-top:64px;font-family:"Space Mono";font-size:27px;letter-spacing:.14em;color:var(--dim)}
.focus{margin-top:56px;display:inline-flex;align-items:center;gap:16px;border:2.5px solid var(--o);color:var(--o);border-radius:999px;padding:20px 38px;font-family:"Space Mono";font-weight:700;font-size:27px;letter-spacing:.16em;text-transform:uppercase}
"""
s1 = page("THE STUDIO", "01", """
<div class="center">
  <img class="logo" src="logo.svg" alt="">
  <div class="name">Pacheco<br>Studios</div>
  <div class="sub">AI systems for businesses that want to grow.</div>
  <div class="motto"><span>We find the problem.</span><span>We design the system.</span><span>We prove the impact.</span></div>
  <div class="focus"><span class="dot"></span>Now: AI for dental clinics</div>
  <div class="founder">AI CONSULTANCY · FOUNDED BY TOMÁS PACHECO</div>
</div>""", extra_css=s1_css)

# ---------- 02 SERVICES ----------
services = [
    ("Dental Clinic Systems", "Zero unanswered patients, day and night.", True),
    ("AI &amp; Automation", "Agents and workflows that work for you, 24/7.", False),
    ("Websites", "Fast, beautiful and built to convert.", False),
    ("Software &amp; Apps", "Tools made for the way your business runs.", False),
    ("Marketing &amp; Growth", "The right clients, not just visits.", False),
    ("Strategy &amp; Diagnosis", "A clear plan of what to do next.", False),
]
rows = "".join(
    f"""<div class="row{' feat' if f else ''}"><span class="n">{i:02d}</span><div><div class="t">{t}{' <span class="badge">Focus</span>' if f else ''}</div><div class="d">{d}</div></div></div>"""
    for i, (t, d, f) in enumerate(services, 1))
s2_css = """
.list{margin-top:64px;border-top:2px solid var(--line)}
.row{display:flex;gap:44px;padding:32px 0;border-bottom:2px solid var(--line)}
.row .n{font-family:"Space Mono";font-size:32px;color:var(--o);padding-top:8px;min-width:60px}
.row .t{font-size:50px;font-weight:600;letter-spacing:-.01em;display:flex;align-items:center;gap:22px}
.row .d{margin-top:12px;font-size:34px;color:rgba(239,234,227,.62)}
.row.feat{background:linear-gradient(90deg,rgba(232,98,44,.14),transparent 85%);margin:0 -30px;padding:32px 30px;border-left:6px solid var(--o)}
.badge{font-family:"Space Mono";font-weight:700;font-size:22px;letter-spacing:.16em;text-transform:uppercase;background:var(--o);color:#141210;border-radius:999px;padding:8px 18px}
"""
s2 = page("SERVICES", "02", f"""
<h1>Systems that work <span class="o">while you don't.</span></h1>
<div class="list">{rows}</div>""", foot_right="PACHECOST.COM", extra_css=s2_css)

# ---------- 03 PARTNERS ----------
# Só clientes/projetos reais (memória do projeto + destaque anterior). Nada inventado.
sectors = [
    ("Restaurants &amp; Hospitality", ["Andalu Gastrobar", "Olá Kathmandu", "Hanam Korean BBQ", "Simona's O Bom Paladar", "Borda d'Água", "Gelataria Muxagata"]),
    ("Retail &amp; E-commerce", ["La Costa", "CarnePura", "Tshirts do Sul", "TopCopias"]),
    ("Health &amp; Care", ["PhysioAlba", "Barbearia do Cão"]),
    ("Local Services", ["Magic Key", "Espresso Service Center"]),
    ("Construction &amp; Industry", ["ProBuilders", "Grupo Naval"]),
]
total = sum(len(n) for _, n in sectors)
blocks = "".join(
    f"""<div class="sec"><div class="sl"><span>{i:02d}</span>{s}</div><div class="pills">{''.join(f'<span class="pill">{n}</span>' for n in names)}</div></div>"""
    for i, (s, names) in enumerate(sectors, 1))
s3_css = """
h1{font-size:96px;margin-top:72px}
.stats{margin-top:36px;font-family:"Space Mono";font-size:28px;letter-spacing:.16em;color:var(--dim);text-transform:uppercase}
.secs{margin-top:48px;display:flex;flex-direction:column;gap:30px}
.sl{font-family:"Space Mono";font-weight:700;font-size:25px;letter-spacing:.2em;text-transform:uppercase;color:var(--o);display:flex;gap:20px;margin-bottom:16px}
.sl span{color:var(--dim);font-weight:400}
.pills{display:flex;flex-wrap:wrap;gap:14px}
.pill{font-family:"Archivo Black";font-size:27px;letter-spacing:.02em;text-transform:uppercase;border:2px solid rgba(239,234,227,.5);border-radius:16px;padding:15px 24px}
.you{margin-top:40px;display:flex;justify-content:space-between;align-items:center;background:var(--o);color:#141210;border-radius:24px;padding:34px 44px}
.you b{font-family:"Archivo Black";font-size:44px;text-transform:uppercase}
.you span{font-family:"Space Mono";font-weight:700;font-size:28px;letter-spacing:.16em;text-transform:uppercase}
"""
s3 = page("PARTNERS", "03", f"""
<h1><span class="o">15+</span> partners.<br><span class="o">5</span> sectors.</h1>
<div class="stats">Real businesses we've built for · Portugal · Romania · Spain</div>
<div class="secs">{blocks}</div>
<div class="you"><b>Your business?</b><span>Talk with us →</span></div>""", extra_css=s3_css)

# ---------- 04 DENTAL ----------
s4_css = """
h1{font-size:94px;margin-top:72px}
.flow{margin-top:52px;display:flex;flex-direction:column;gap:0}
.step{display:flex;gap:36px;align-items:flex-start;position:relative;padding-bottom:34px}
.step:not(:last-child)::after{content:"";position:absolute;left:39px;top:84px;bottom:6px;width:3px;background:linear-gradient(var(--o),rgba(232,98,44,.15))}
.step .c{flex:none;width:82px;height:82px;border-radius:50%;border:3px solid var(--o);display:flex;align-items:center;justify-content:center;font-family:"Space Mono";font-weight:700;font-size:28px;color:var(--o)}
.step:last-child .c{background:var(--o);color:#141210}
.step .t{font-size:44px;font-weight:600;padding-top:8px}
.step .d{margin-top:8px;font-size:32px;color:rgba(239,234,227,.62);line-height:1.4}
.card{margin-top:10px;border:2px solid var(--line);border-radius:28px;padding:40px 44px;background:rgba(239,234,227,.03)}
.card .k{font-family:"Space Mono";font-size:25px;letter-spacing:.18em;text-transform:uppercase;color:var(--dim)}
.card .v{margin-top:16px;font-family:"Archivo Black";font-size:50px;line-height:1.05;text-transform:uppercase}
.card .m{margin-top:14px;font-size:30px;color:rgba(239,234,227,.7);line-height:1.4}
.note{margin-top:14px;font-family:"Space Mono";font-size:20px;letter-spacing:.06em;color:rgba(239,234,227,.4)}
.cta{margin-top:36px}
"""
s4 = page("DENTAL CLINICS", "04", """
<h1>Zero unanswered <span class="o">patients.</span></h1>
<p class="lead">When a patient calls and nobody answers, they don't wait. They call the next clinic.</p>
<div class="flow">
  <div class="step"><span class="c">01</span><div><div class="t">A call is missed</div><div class="d">Busy line, after hours, weekend.</div></div></div>
  <div class="step"><span class="c">02</span><div><div class="t">A message goes out in seconds</div><div class="d">On WhatsApp or SMS, in the clinic's name.</div></div></div>
  <div class="step"><span class="c">03</span><div><div class="t">The appointment is booked</div><div class="d">Your team only confirms. Nobody is lost.</div></div></div>
</div>
<div class="card">
  <div class="k">Just 3 lost patients a month</div>
  <div class="v">3 × 1,500 € = <span class="o">4,500 €/month</span></div>
  <div class="m">Already have a receptionist? We cover after hours, weekends and busy lines.</div>
  <div class="note">Estimate based on market data and sector references.</div>
</div>
<div class="cta"><span class="btn">Talk with us →</span></div>""", extra_css=s4_css)

# ---------- 05 TALK (2 variantes de telefone) ----------
s5_css = """
h1{font-size:112px;margin-top:110px}
.avail{margin-top:40px;font-family:"Space Mono";font-size:28px;letter-spacing:.14em;color:rgba(239,234,227,.7);text-transform:uppercase;display:flex;gap:18px;align-items:center}
.contacts{margin-top:70px;border-top:2px solid var(--line)}
.ct{display:flex;align-items:baseline;padding:40px 0;border-bottom:2px solid var(--line)}
.ct .k{width:250px;font-family:"Space Mono";font-size:26px;letter-spacing:.18em;color:var(--dim);text-transform:uppercase}
.ct .v{font-size:50px;font-weight:500}
.cta{margin-top:72px}
.langs{margin-top:44px;font-family:"Space Mono";font-size:26px;letter-spacing:.14em;color:var(--dim);text-transform:uppercase}
"""
def talk(phone):
    return page("TALK", "05", f"""
<h1>Let's <span class="o">talk.</span></h1>
<div class="avail"><span class="dot"></span>Open for new projects · Same-day reply</div>
<div class="contacts">
  <div class="ct"><span class="k">WhatsApp</span><span class="v">{phone}</span></div>
  <div class="ct"><span class="k">Email</span><span class="v">tomas@pachecost.com</span></div>
  <div class="ct"><span class="k">Site</span><span class="v">pachecost.com</span></div>
</div>
<div class="cta"><span class="btn">Talk with us →</span></div>
<div class="langs">English · Português · Română</div>""", extra_css=s5_css)

files = {
    "01-the-studio": s1, "02-services": s2, "03-partners": s3,
    "04-dental-clinics": s4,
    "05-talk-RO": talk("+40 723 098 556"),
    "05-talk-PT": talk("+351 967 117 357"),
}
for name, html in files.items():
    (HERE / f"{name}.html").write_text(html, encoding="utf-8")
print("ok", total, "parceiros")
