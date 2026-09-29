import asyncio
from playwright.async_api import async_playwright

FONT = "<link href='https://fonts.googleapis.com/css2?family=Manrope:wght@500;700;800&display=swap' rel='stylesheet'>"
BASE = """
*{margin:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;background:transparent;font-family:Manrope,sans-serif;color:#fff;overflow:hidden}
.card{position:absolute;left:84px;right:84px;top:520px}
.l{font-weight:800;font-size:78px;line-height:1.08;letter-spacing:-1.5px;text-shadow:0 4px 30px rgba(0,0,0,.75),0 2px 6px rgba(0,0,0,.6)}
.s{font-weight:600;font-size:46px;line-height:1.2;opacity:.92;margin-bottom:22px;text-shadow:0 3px 18px rgba(0,0,0,.8)}
.hl{color:#6ee7a8}
.box{background:rgba(10,12,14,.78);border-radius:28px;padding:44px 48px;backdrop-filter:blur(6px)}
"""

def page(body, extra=""):
    return f"<!doctype html><html><head><meta charset='utf-8'>{FONT}<style>{BASE}{extra}</style></head><body>{body}</body></html>"

T = {}
# A — cârlig
T["a1"] = page("<div class='card'><div class='l'>Clientul ți-a scris<br>la <span class='hl'>21:40</span>.</div></div>")
T["a2"] = page("<div class='card'><div class='l'>Clientul ți-a scris<br>la <span class='hl'>21:40</span>.</div><div class='l' style='margin-top:26px'>Tu ai văzut<br>la <span style='color:#ff8a7a'>23:10</span>.</div></div>")
# B — recunoaștere
T["b1"] = page("<div class='card' style='top:300px'><div class='l'>Nu pentru că<br>nu-ți pasă.</div></div>")
T["b2"] = page("<div class='card' style='top:300px'><div class='l'>Nu pentru că<br>nu-ți pasă.</div><div class='l' style='margin-top:26px'>Aveai mâinile<br><span class='hl'>pline</span>.</div></div>")
# C — problema
T["c1"] = page("<div class='card' style='top:360px'><div class='s'>Între timp…</div><div class='l'>a rezervat<br>în altă parte.</div></div>")
# E — după
T["e1"] = page("<div class='card' style='top:300px'><div class='l'>Tu te ocupi<br>de oamenii din sală.</div></div>")
T["e2"] = page("<div class='card' style='top:300px'><div class='l'>Tu te ocupi<br>de oamenii din sală.</div><div class='l' style='margin-top:26px'><span class='hl'>Sistemul</span> răspunde<br>la mesaje.</div></div>")
# F — beneficii
ben = ["Răspunde în câteva secunde, <b>zi și noapte</b>", "Face rezervarea <b>direct în WhatsApp</b>", "Trimite reminder → <b>mai puține mese goale</b>"]
def fcard(n):
    li = "".join(f"<div class='it' style='opacity:{1 if i < n else 0}'><span class='ck'>✓</span><span>{t}</span></div>" for i, t in enumerate(ben))
    return page(f"<div class='card' style='top:470px'><div class='box'>{li}</div></div>",
                ".it{display:flex;gap:22px;align-items:flex-start;font-size:48px;line-height:1.22;font-weight:500;margin:18px 0}.it b{font-weight:800}.ck{color:#25d366;font-weight:800}")
for n in (1, 2, 3):
    T[f"f{n}"] = fcard(n)
# G — preț + CTA (fundo opaco escuro por cima de S5 desfocado)
T["g1"] = page("""
<div style='position:absolute;inset:0;background:linear-gradient(180deg,rgba(8,10,12,.55),rgba(8,10,12,.88))'></div>
<div class='card' style='top:380px;text-align:left'>
 <div class='s' style='font-size:44px'>Asistent WhatsApp făcut<br>pe măsura afacerii tale</div>
 <div style='font-size:60px;font-weight:600;margin-top:40px;opacity:.85'>de la</div>
 <div style='font-size:138px;font-weight:800;letter-spacing:-4px;line-height:1'>6.000 lei</div>
 <div style='font-size:62px;font-weight:700;margin-top:12px'>+ 1.000 lei<span style='font-weight:500;opacity:.8'>/lună</span></div>
 <div style='font-size:40px;font-weight:600;margin-top:34px;color:#6ee7a8'>Preț corect. Fără costuri ascunse.</div>
 <div style='margin-top:70px;background:#25d366;color:#06290f;border-radius:999px;padding:30px 44px;font-size:44px;font-weight:800;display:inline-block'>Scrie-ne ce automatizare vrei →</div>
 <div style='margin-top:60px;font-size:36px;font-weight:700;letter-spacing:6px;opacity:.8'>PACHECO STUDIOS</div>
</div>""")

# D — chat WhatsApp (estados)
CHAT_CSS = """
.ph{position:absolute;left:110px;right:110px;top:300px;min-height:760px;border-radius:56px;background:#0b141a;overflow:hidden;box-shadow:0 30px 90px rgba(0,0,0,.6);border:10px solid #1b1f22}
.hd{background:#1f2c34;height:150px;display:flex;align-items:center;gap:26px;padding:30px 34px 0}
.av{width:78px;height:78px;border-radius:50%;background:linear-gradient(135deg,#c7773a,#7a3b1d);display:flex;align-items:center;justify-content:center;font-weight:800;font-size:36px}
.nm{font-weight:700;font-size:38px}.st{font-size:27px;color:#8ea0aa;margin-top:4px}
.bd{padding:34px 28px;display:flex;flex-direction:column;gap:20px;background:#0b141a}
.m{max-width:80%;padding:20px 26px 14px;border-radius:24px;font-size:36px;line-height:1.3;font-weight:500;position:relative}
.in{align-self:flex-start;background:#202c33;border-top-left-radius:6px}
.out{align-self:flex-end;background:#005c4b;border-top-right-radius:6px}
.tm{display:block;text-align:right;font-size:23px;color:#a8bcc4;margin-top:6px}
.tk{color:#53bdeb}
.ty{align-self:flex-start;background:#202c33;border-radius:24px;padding:24px 30px;display:flex;gap:10px}
.ty i{width:16px;height:16px;border-radius:50%;background:#8ea0aa;display:block}
.lab{position:absolute;left:84px;right:84px;top:1400px;text-align:center}
"""
msgs = [
    ("in", "Bună seara! Aveți masă pentru 4, vineri la 20:00?", "21:40"),
    ("out", "Bună seara! 😊 Da, avem. V-am rezervat masa pentru 4 persoane, vineri la 20:00. Pe ce nume?", "21:40"),
    ("in", "Andrei", "21:41"),
    ("out", "Gata, Andrei! Primiți confirmarea cu o zi înainte. 🍷", "21:41"),
]
def chat(n, typing=False, label=True):
    b = ""
    for k, (w, t, h) in enumerate(msgs[:n]):
        tick = " <span class='tk'>✓✓</span>" if w == "out" else ""
        b += f"<div class='m {w}'>{t}<span class='tm'>{h}{tick}</span></div>"
    if typing:
        b += "<div class='ty'><i></i><i style='opacity:.7'></i><i style='opacity:.45'></i></div>"
    lab = "<div class='lab'><div class='l' style='font-size:62px'>Răspuns în <span class='hl'>câteva secunde</span>.<br>Chiar și la 21:40.</div></div>" if label else ""
    return page(f"<div class='ph'><div class='hd'><div class='av'>B</div><div><div class='nm'>Bistro · Rezervări</div><div class='st'>{'scrie…' if typing else 'online'}</div></div></div><div class='bd'>{b}</div></div>{lab}", CHAT_CSS)
T["d1"] = chat(1, label=False)
T["d2"] = chat(1, typing=True, label=False)
T["d3"] = chat(2)
T["d4"] = chat(3)
T["d5"] = chat(4)

async def main():
    async with async_playwright() as p:
        br = await p.chromium.launch()
        pg = await br.new_page(viewport={"width": 1080, "height": 1920})
        for k, html in T.items():
            await pg.set_content(html, wait_until="networkidle")
            await pg.evaluate("document.fonts.ready")
            await pg.screenshot(path=f"ov/{k}.png", omit_background=True)
        await br.close()
asyncio.run(main())
print("ok", len(T))
