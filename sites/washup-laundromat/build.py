#!/usr/bin/env python3
"""WashUp Laundromat · site RO + EN (rascunho Pacheco Studios, 31 out 2026).
Gera ../site/index.html (RO) e ../site/en/index.html (EN). Caminhos relativos: funciona em
pachecost.com/p/washup/ ou num Netlify próprio. Para o vídeo vertical do hero, pôr o ficheiro
em site/media/hero-9x16.mp4 (+ hero-9x16.jpg) e mudar HERO_VIDEO para True.
Por confirmar com o dono (marcado <!-- CONFIRMAR -->): hora de abertura, dias, preços, capacidades, pagamento.
"""
import os, html
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = HERE
HERO_VIDEO = False
PHONE = "0766 971 785"; PHONE_INT = "40766971785"
MAPS = "https://www.google.com/maps/search/?api=1&query=WashUp+Laundromat+Bulevardul+Carol+I+26-28+Iasi"

T = {
 "ro": dict(
  lang="ro", path="", other="en/", other_label="EN", self_label="RO",
  title="WashUp Laundromat · Spălătorie self-service în Iași, Bd. Carol I",
  desc="Spălătorie self-service pe Bulevardul Carol I 26-28, Iași. Mașini profesionale, uscătoare rapide, fără programare. 4,9★ pe Google.",
  nav=["Cum funcționează","Pentru cine","Program","Contact"],
  eyebrow="Spălătorie self-service · Iași",
  h1=["Rufe curate","într-o oră.","Fără programare."],
  sub="Pe Bulevardul Carol I, lângă Universitate. Mașini profesionale de spălat și uscătoare rapide, gata când ai tu timp.",
  cta1="Cum ajung", cta2="Scrie-ne pe WhatsApp",
  rating="4,9 din 5 · 78 de recenzii pe Google",
  close="Închidem la 20:00",
  how_label="Cum funcționează", how_h="Trei pași, de la coș la sertar.",
  steps=[("Încarci","Pui rufele în mașină și alegi programul potrivit."),
         ("Pornești","Plătești la mașină și o pornești. Între timp ieși la o cafea pe Carol I."),
         ("Usuci și pleci","Muți rufele în uscător și pleci acasă cu ele calde și uscate.")],
  for_label="Pentru cine", for_h="Pentru toți cei care n-au timp de rufe.",
  segs=[("Studenți","Fără mașină în cămin sau în apartament? Spălarea săptămânii într-o singură oră."),
        ("International students","We speak English. Clear steps on every machine."),
        ("Gazde Airbnb","Lenjerii și prosoape pentru mai multe apartamente, spălate și uscate dintr-o dată."),
        ("Familii","Plăpumi, pilote și pături care nu încap în mașina de acasă.")],
  rev_label="Recenzii", rev_h="4,9 stele din 78 de recenzii.", rev_p="Ne bucurăm de fiecare. Citește-le pe Google sau lasă-ne și tu una după prima vizită.", rev_cta="Vezi recenziile pe Google",
  hrs_label="Program și adresă", hrs_h="Ne găsești pe Carol I.",
  addr="Bulevardul Carol I 26-28, 700505 Iași", plus="Plus Code: 5HGC+P9 Iași",
  hrs=[("Astăzi","Închidem la 20:00")], hrs_note="Programul complet e pe Google Maps.",
  faq_label="Întrebări", faq=[
   ("Am nevoie de programare?","Nu. Vii când vrei în timpul programului și folosești orice mașină liberă."),
   ("Cât durează?","De obicei, o spălare și o uscare se termină în jur de o oră, în funcție de program."),
   ("Pot spăla plăpumi și pilote?","Da, avem mașini de capacitate mare pentru lucrurile voluminoase."),
   ("Cum vă contactez?",f"Sună sau scrie-ne pe WhatsApp la {PHONE}.")],
  contact_h="Ai o întrebare?", contact_p="Scrie-ne pe WhatsApp sau sună-ne. Răspundem repede.",
  call="Sună", wa="WhatsApp", maps="Deschide în Google Maps",
  wa_text="Bună! Am o întrebare despre WashUp Laundromat.",
  foot="Spălătorie self-service în Iași", made="Site realizat de Pacheco Studios",
  drum_label="Mașină de spălat în funcțiune"),
 "en": dict(
  lang="en", path="../", other="../", other_label="RO", self_label="EN",
  title="WashUp Laundromat · Self-service laundry in Iași, Carol I Blvd",
  desc="Self-service laundromat at Bulevardul Carol I 26-28, Iași. Professional washers, fast dryers, no booking needed. Rated 4.9★ on Google.",
  nav=["How it works","Who it's for","Hours","Contact"],
  eyebrow="Self-service laundromat · Iași",
  h1=["Clean laundry","in about an hour.","No booking."],
  sub="On Carol I Boulevard, next to the University. Professional washers and fast dryers, ready whenever you are.",
  cta1="Get directions", cta2="Message us on WhatsApp",
  rating="4.9 out of 5 · 78 Google reviews",
  close="We close at 20:00",
  how_label="How it works", how_h="Three steps, from basket to drawer.",
  steps=[("Load","Put your laundry in the machine and choose the right programme."),
         ("Start","Pay at the machine and start it. Grab a coffee on Carol I while it runs."),
         ("Dry and go","Move everything to a dryer and take it home warm and dry.")],
  for_label="Who it's for", for_h="For everyone with better things to do than laundry.",
  segs=[("Students","No washer in the dorm or the flat? Your weekly wash done in one hour."),
        ("International students","Medical and Erasmus students welcome. Clear steps in English."),
        ("Airbnb hosts","Sheets and towels for several flats, washed and dried in one go."),
        ("Families","Duvets, quilts and blankets that don't fit the machine at home.")],
  rev_label="Reviews", rev_h="4.9 stars from 78 reviews.", rev_p="We're grateful for every one. Read them on Google, or leave yours after your first visit.", rev_cta="See reviews on Google",
  hrs_label="Hours and address", hrs_h="Find us on Carol I.",
  addr="Bulevardul Carol I 26-28, 700505 Iași, Romania", plus="Plus Code: 5HGC+P9 Iași",
  hrs=[("Today","We close at 20:00")], hrs_note="Full opening hours are on Google Maps.",
  faq_label="Questions", faq=[
   ("Do I need to book?","No. Come any time during opening hours and use any free machine."),
   ("How long does it take?","A wash and a dry usually take about an hour, depending on the programme."),
   ("Can I wash duvets?","Yes, we have large-capacity machines for bulky items."),
   ("How do I reach you?",f"Call or WhatsApp us at +40 766 971 785.")],
  contact_h="Got a question?", contact_p="Message us on WhatsApp or give us a call. We reply quickly.",
  call="Call", wa="WhatsApp", maps="Open in Google Maps",
  wa_text="Hi! I have a question about WashUp Laundromat.",
  foot="Self-service laundromat in Iași", made="Website by Pacheco Studios",
  drum_label="Washing machine running"),
}

CSS = r"""
/* WashUp · laundromat signage: steel-grey ground, ink navy type, rinse-aqua accent, signal-yellow action. Dela Gothic One display + Manrope body. */
:root{--steel:#E6ECEF;--paper:#F7F9FA;--ink:#0F1E2E;--ink-2:#40566A;--line:#CBD6DC;--aqua:#0098A6;--aqua-deep:#006F7A;--signal:#FFC83A;--drum:#1A2A38;
--f-d:"Dela Gothic One","Arial Black",system-ui,sans-serif;--f-b:"Manrope","Segoe UI",system-ui,sans-serif;--hh:68px;color-scheme:light}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--paper);color:var(--ink);font:17px/1.55 var(--f-b)}
img,video{max-width:100%;display:block}a{color:inherit}
h1,h2,h3{font-family:var(--f-d);font-weight:400;letter-spacing:-.01em;margin:0;text-wrap:balance;line-height:1.05}
.c{max-width:1180px;margin:0 auto;padding-left:max(18px,env(safe-area-inset-left,0px));padding-right:max(18px,env(safe-area-inset-right,0px))}
.label{font:600 .74rem/1 var(--f-b);letter-spacing:.14em;text-transform:uppercase;color:var(--aqua-deep)}
a:focus-visible,button:focus-visible{outline:3px solid var(--aqua);outline-offset:3px}
.btn{display:inline-flex;align-items:center;gap:10px;padding:14px 22px;border-radius:999px;font-weight:700;text-decoration:none;border:2px solid transparent;transition:transform .2s}
.btn:hover{transform:translateY(-2px)}
.btn--cta{background:var(--signal);color:var(--ink)}
.btn--ghost{border-color:var(--ink);color:var(--ink)}
.btn svg{width:20px;height:20px}
/* header */
.demo{background:var(--ink);color:var(--signal);font:700 .7rem/1 var(--f-b);letter-spacing:.16em;text-align:center;padding:8px 12px}
.hd{position:sticky;top:0;z-index:20;background:color-mix(in srgb,var(--paper) 88%,transparent);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.hd .c{display:flex;align-items:center;gap:20px;height:var(--hh)}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;font-family:var(--f-d);font-weight:700;font-size:1.05rem}
.brand small{display:block;font:600 .62rem/1 var(--f-b);letter-spacing:.16em;color:var(--ink-2)}
.nav{display:none;gap:22px;margin-left:auto;font-weight:600;font-size:.95rem}
.nav a{text-decoration:none}.nav a:hover{color:var(--aqua-deep)}
.lang{margin-left:auto;display:flex;border:1.5px solid var(--ink);border-radius:999px;overflow:hidden;font:700 .78rem/1 var(--f-b)}
.lang a,.lang span{padding:7px 11px;text-decoration:none}.lang span{background:var(--ink);color:var(--paper)}
@media(min-width:900px){.nav{display:flex}.lang{margin-left:0}}
/* hero */
.hero{background:var(--steel);overflow:hidden;position:relative}
.hero .c{display:grid;gap:32px;padding-block:40px 48px;align-items:center}
@media(min-width:900px){.hero .c{grid-template-columns:1.15fr .85fr;padding-block:56px 64px;min-height:calc(100svh - var(--hh));max-height:900px}}
.hero h1{font-size:clamp(2.3rem,6.4vw,4.6rem);margin-top:16px}
.hero h1 span{display:block}.hero h1 span:nth-child(2){color:var(--aqua-deep)}
.hero .sub{font-size:1.15rem;color:var(--ink-2);max-width:36ch;margin:20px 0 0}
.ctas{display:flex;flex-wrap:wrap;gap:12px;margin-top:28px}
.chips{display:flex;flex-wrap:wrap;gap:10px;margin-top:26px;font-weight:600;font-size:.9rem}
.chip{display:inline-flex;align-items:center;gap:8px;background:var(--paper);border:1px solid var(--line);border-radius:999px;padding:7px 14px}
.chip .st{color:#E7A600;letter-spacing:1px}
/* vertical hero panel 9:16 */
.tall{position:relative;justify-self:center;width:min(100%,400px);aspect-ratio:9/16;max-height:78svh;border-radius:28px;overflow:hidden;background:linear-gradient(180deg,#D5DEE3,#B9C6CE);box-shadow:0 30px 60px -30px rgba(15,30,46,.45)}
.tall video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.machine{position:absolute;inset:6% 9%;background:linear-gradient(160deg,#F4F7F8,#C9D3D9 60%,#AEBBC3);border-radius:18px;box-shadow:inset 0 2px 0 #fff,inset 0 -3px 0 rgba(0,0,0,.12)}
.panel-top{position:absolute;left:8%;right:8%;top:4%;height:12%;border-radius:10px;background:#DCE3E7;display:flex;align-items:center;gap:8%;padding:0 8%}
.panel-top i{width:16%;aspect-ratio:1;border-radius:50%;background:#9FB0BA}
.panel-top b{flex:1;height:44%;border-radius:6px;background:var(--drum);color:#7FF3D0;font:600 clamp(.6rem,2.4vw,.9rem)/1 ui-monospace,monospace;display:flex;align-items:center;justify-content:center;letter-spacing:.1em}
.door{position:absolute;left:50%;top:56%;width:78%;aspect-ratio:1;transform:translate(-50%,-50%);border-radius:50%;background:radial-gradient(circle,#9DAAB2 0 60%,#7C8C96 61% 70%,#E8EDF0 71% 100%);box-shadow:0 8px 20px rgba(0,0,0,.18)}
.glass{position:absolute;inset:17%;border-radius:50%;overflow:hidden;background:radial-gradient(circle at 35% 30%,#5FC7D0,#13606B 70%);box-shadow:inset 0 0 0 4px rgba(255,255,255,.25)}
.load{position:absolute;inset:0;animation:spin 2.6s linear infinite}
.load span{position:absolute;border-radius:45% 55% 50% 50%;opacity:.95}
.load span:nth-child(1){width:46%;height:30%;left:10%;top:52%;background:#FFC83A}
.load span:nth-child(2){width:40%;height:34%;left:48%;top:44%;background:#F4F4F4}
.load span:nth-child(3){width:34%;height:26%;left:30%;top:62%;background:#E8574A}
.load span:nth-child(4){width:30%;height:22%;left:56%;top:64%;background:#2E4B8F}
.foam{position:absolute;left:0;right:0;top:0;height:46%;background:radial-gradient(circle at 20% 90%,#fff 0 9%,transparent 10%),radial-gradient(circle at 45% 95%,#fff 0 11%,transparent 12%),radial-gradient(circle at 72% 92%,#fff 0 8%,transparent 9%);opacity:.7;animation:slosh 2.6s ease-in-out infinite}
.shine{position:absolute;inset:0;border-radius:50%;background:linear-gradient(130deg,rgba(255,255,255,.45),transparent 40%)}
.tag{position:absolute;left:50%;bottom:4%;transform:translateX(-50%);background:var(--ink);color:var(--paper);font:700 .72rem/1 var(--f-b);letter-spacing:.12em;text-transform:uppercase;padding:9px 14px;border-radius:999px;white-space:nowrap}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes slosh{50%{transform:translateY(8%) rotate(4deg)}}
@media(max-width:899px){.tall{width:min(100%,340px)}}
@media(prefers-reduced-motion:reduce){.load,.foam{animation:none}.btn{transition:none}}
/* sections */
section{scroll-margin-top:var(--hh)}
.sec{padding-block:72px}
.sec h2{font-size:clamp(1.7rem,4vw,2.6rem);margin-top:12px;max-width:20ch}
.steps{display:grid;gap:18px;margin-top:36px;counter-reset:s;list-style:none;padding:0}
@media(min-width:800px){.steps{grid-template-columns:repeat(3,1fr)}}
.steps li{background:var(--steel);border-radius:22px;padding:26px;display:grid;gap:10px;align-content:start}
.steps li::before{counter-increment:s;content:counter(s);font:700 2.6rem/1 var(--f-d);color:var(--aqua)}
.steps h3{font-size:1.25rem}.steps p{margin:0;color:var(--ink-2)}
.segs{display:grid;gap:14px;margin-top:36px}
@media(min-width:700px){.segs{grid-template-columns:1fr 1fr}}
@media(min-width:1050px){.segs{grid-template-columns:repeat(4,1fr)}}
.seg{border-top:3px solid var(--ink);padding-top:16px;display:grid;gap:8px;align-content:start}
.seg h3{font-size:1.1rem}.seg p{margin:0;color:var(--ink-2)}
.band{background:var(--ink);color:var(--paper)}
.band .label{color:var(--signal)}
.rev{display:grid;gap:28px;align-items:center}
@media(min-width:900px){.rev{grid-template-columns:auto 1fr auto}}
.score{font:700 clamp(4rem,12vw,7rem)/1 var(--f-d);color:var(--signal)}
.rev p{color:#C5D2DC;max-width:46ch;margin:12px 0 0}
.band .btn--ghost{border-color:var(--paper);color:var(--paper)}
.visit{display:grid;gap:24px;margin-top:32px}
@media(min-width:900px){.visit{grid-template-columns:1fr 1fr}}
.card{background:var(--steel);border-radius:22px;padding:26px;display:grid;gap:12px;align-content:start}
.card h3{font-size:1.15rem}
.card p{margin:0}.muted{color:var(--ink-2)}
.big{font:700 1.6rem/1.15 var(--f-d)}
.faq{margin-top:28px;border-top:1px solid var(--line)}
.faq details{border-bottom:1px solid var(--line);padding:18px 0}
.faq summary{cursor:pointer;font-weight:700;font-size:1.05rem;list-style:none;display:flex;justify-content:space-between;gap:16px}
.faq summary::after{content:"+";font:700 1.4rem/1 var(--f-d);color:var(--aqua-deep)}
.faq details[open] summary::after{content:"–"}
.faq p{margin:10px 0 0;color:var(--ink-2);max-width:60ch}
.contact{background:var(--aqua-deep);color:#fff;border-radius:28px;padding:40px 28px;display:grid;gap:18px}
.contact h2{color:#fff}.contact p{margin:0;color:#D6F2F4;font-size:1.1rem}
.contact .btn--ghost{border-color:#fff;color:#fff}
.ft{padding-block:36px;color:var(--ink-2);font-size:.9rem;display:flex;flex-wrap:wrap;gap:12px 24px;justify-content:space-between}
.ft a{text-decoration:none;font-weight:600}
"""

ICON_WA = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 11.9 11.9 0 0 0 4.6 4c1.7.7 2.4.8 3.2.7a2.8 2.8 0 0 0 1.8-1.3 2.3 2.3 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3z"/></svg>'
ICON_PIN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 22s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/></svg>'
ICON_TEL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2z"/></svg>'
LOGO = '<svg width="36" height="36" viewBox="0 0 36 36" aria-hidden="true"><rect width="36" height="36" rx="10" fill="#0F1E2E"/><circle cx="18" cy="20" r="10" fill="none" stroke="#FFC83A" stroke-width="3"/><path d="M11 21.5c2.4-2.6 4.6 1.7 7-.7s4.6 1.9 7-.7" fill="none" stroke="#00B5C4" stroke-width="2.4"/><circle cx="10" cy="6.8" r="1.6" fill="#E6ECEF"/><circle cx="15" cy="6.8" r="1.6" fill="#E6ECEF"/></svg>'

def page(k):
    t = T[k]; e = html.escape
    from urllib.parse import quote
    wa = f"https://wa.me/{PHONE_INT}?text={quote(t['wa_text'])}"
    ids = ["cum","pentru","program","contact"] if k=="ro" else ["how","who","hours","contact"]
    nav = "".join(f'<a href="#{i}">{e(n)}</a>' for i,n in zip(ids,t["nav"]))
    if k=="ro": lang = f'<span>RO</span><a href="{t["other"]}" hreflang="en">EN</a>'
    else: lang = f'<a href="{t["other"]}" hreflang="ro">RO</a><span>EN</span>'
    hero_media = ('<video autoplay muted loop playsinline poster="{p}media/hero-9x16.jpg"><source src="{p}media/hero-9x16.mp4" type="video/mp4"></video>'.format(p=t["path"])
                  if HERO_VIDEO else
                  f'<div class="machine" role="img" aria-label="{e(t["drum_label"])}"><div class="panel-top"><i></i><b>00:38</b><i></i></div><div class="door"><div class="glass"><div class="load"><span></span><span></span><span></span><span></span></div><div class="foam"></div><div class="shine"></div></div></div></div>')
    steps = "".join(f"<li><h3>{e(a)}</h3><p>{e(b)}</p></li>" for a,b in t["steps"])
    segs = "".join(f'<div class="seg"><h3>{e(a)}</h3><p>{e(b)}</p></div>' for a,b in t["segs"])
    faq = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q,a in t["faq"])
    hrs = "".join(f'<p class="big">{e(b)}</p>' for a,b in t["hrs"])
    canon = "https://pachecost.com/p/washup/" + ("" if k=="ro" else "en/")
    ld = ('{"@context":"https://schema.org","@type":"Laundromat","name":"WashUp Laundromat","telephone":"+40766971785",'
          '"address":{"@type":"PostalAddress","streetAddress":"Bulevardul Carol I 26-28","postalCode":"700505","addressLocality":"Iași","addressCountry":"RO"},'
          '"aggregateRating":{"@type":"AggregateRating","ratingValue":"4.9","reviewCount":"78"}}')
    return f"""<!doctype html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(t['title'])}</title>
<meta name="description" content="{e(t['desc'])}">
<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="ro" href="https://pachecost.com/p/washup/"><link rel="alternate" hreflang="en" href="https://pachecost.com/p/washup/en/">
<meta property="og:title" content="{e(t['title'])}"><meta property="og:description" content="{e(t['desc'])}"><meta property="og:type" content="website">
<meta name="theme-color" content="#E6ECEF">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Dela+Gothic+One&family=Manrope:wght@400;600;700&display=swap">
<script type="application/ld+json">{ld}</script>
<style>{CSS}</style>
</head>
<body>
<div class="demo">{"PREZENTARE PACHECO STUDIOS · SCHIȚĂ" if k=="ro" else "PACHECO STUDIOS PRESENTATION · DRAFT"}</div>
<header class="hd"><div class="c">
  <a class="brand" href="#top">{LOGO}<span>WashUp<small>LAUNDROMAT · IAȘI</small></span></a>
  <nav class="nav" aria-label="Menu">{nav}</nav>
  <div class="lang">{lang}</div>
</div></header>
<main id="top">
<section class="hero"><div class="c">
  <div>
    <p class="label">{e(t['eyebrow'])}</p>
    <h1>{''.join(f'<span>{e(x)}</span>' for x in t['h1'])}</h1>
    <p class="sub">{e(t['sub'])}</p>
    <div class="ctas"><a class="btn btn--cta" href="{MAPS}" target="_blank" rel="noopener">{ICON_PIN}<span>{e(t['cta1'])}</span></a><a class="btn btn--ghost" href="{wa}" target="_blank" rel="noopener">{ICON_WA}<span>{e(t['cta2'])}</span></a></div>
    <div class="chips"><span class="chip"><span class="st" aria-hidden="true">★★★★★</span>{e(t['rating'])}</span><span class="chip">{e(t['close'])}</span></div>
  </div>
  <div class="tall">{hero_media}<span class="tag">Bd. Carol I 26-28</span></div>
</div></section>

<section class="sec" id="{ids[0]}"><div class="c">
  <p class="label">{e(t['how_label'])}</p><h2>{e(t['how_h'])}</h2>
  <ol class="steps">{steps}</ol>
</div></section>

<section class="sec" id="{ids[1]}" style="padding-top:0"><div class="c">
  <p class="label">{e(t['for_label'])}</p><h2>{e(t['for_h'])}</h2>
  <div class="segs">{segs}</div>
</div></section>

<section class="sec band"><div class="c rev">
  <div class="score">{"4,9" if k=="ro" else "4.9"}</div>
  <div><p class="label">{e(t['rev_label'])}</p><h2>{e(t['rev_h'])}</h2><p>{e(t['rev_p'])}</p></div>
  <a class="btn btn--ghost" href="{MAPS}" target="_blank" rel="noopener">{e(t['rev_cta'])}</a>
</div></section>

<section class="sec" id="{ids[2]}"><div class="c">
  <p class="label">{e(t['hrs_label'])}</p><h2>{e(t['hrs_h'])}</h2>
  <div class="visit">
    <div class="card"><h3>{e(t['hrs'][0][0])}</h3>{hrs}<p class="muted">{e(t['hrs_note'])}</p><!-- CONFIRMAR: hora de abertura e dias --></div>
    <div class="card"><h3>{e(t['addr'])}</h3><p class="muted">{e(t['plus'])}</p><p><a class="btn btn--cta" href="{MAPS}" target="_blank" rel="noopener">{ICON_PIN}<span>{e(t['maps'])}</span></a></p></div>
  </div>
  <div class="faq" aria-label="{e(t['faq_label'])}">{faq}</div>
</div></section>

<section class="sec" id="{ids[3]}" style="padding-top:0"><div class="c">
  <div class="contact"><h2>{e(t['contact_h'])}</h2><p>{e(t['contact_p'])}</p>
    <div class="ctas" style="margin-top:6px"><a class="btn btn--cta" href="{wa}" target="_blank" rel="noopener">{ICON_WA}<span>{e(t['wa'])}</span></a><a class="btn btn--ghost" href="tel:+{PHONE_INT}">{ICON_TEL}<span>{e(t['call'])} {PHONE}</span></a></div>
  </div>
</div></section>
</main>
<footer class="c ft"><span><b>WashUp Laundromat</b> · {e(t['foot'])} · {e(t['addr'])}</span><a href="https://pachecost.com" target="_blank" rel="noopener">{e(t['made'])}</a></footer>
</body></html>
"""

if __name__ == "__main__":
    os.makedirs(os.path.join(OUT, "en"), exist_ok=True)
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(page("ro"))
    open(os.path.join(OUT, "en", "index.html"), "w", encoding="utf-8").write(page("en"))
    print("ok")
