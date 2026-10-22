#!/usr/bin/env python3
"""Folha de 2 páginas para a Obiectiv Imobiliare: faixa de investimento da implementação (7.500–25.000 €)
e os casos apresentados em pachecost.com. RO para o dono, PT para o Tomás.

Uso: python3 investitie.py  →  obiectiv-investitie-ro.pdf, obiectiv-investimento-pt.pdf
"""
import os, subprocess
from gerar import AQUI, FONTES, CSS, CHROME, esc, rod

RO = dict(
    marca="PACHECO STUDIOS · IMPLEMENTARE · OBIECTIV IMOBILIARE · OCTOMBRIE 2026",
    k="După pilot · implementarea", t="Dacă vedeți rezultate în pilot, la asta vă puteți aștepta.",
    s="Intervalul de investiție pentru implementarea finală la Obiectiv Imobiliare, stabilit de la început ca să nu existe surprize. Valoarea exactă iese din diagnostic.",
    min="7.500 €", max="25.000 €", band_k="Intervalul implementării",
    band_lo="Mai puține blocaje · un singur flux", band_hi="Mai multe blocaje · toate canalele și echipa",
    pay_n="1–3 luni", pay_t="În cazurile de pe pachecost.com, investiția s-a recuperat în 1–3 luni din profitul generat pentru firmă.",
    fac_k="Ce mișcă valoarea în interval",
    fac=[("Câte blocaje atacăm", "Diagnosticul le listează pe toate, cu prioritate. Implementăm întâi ce aduce cel mai mult."),
         ("Câte canale și câți oameni intră în sistem", "Un flux cu doi agenți costă mai puțin decât toate cele 6 canale, 4 agenți și 9 servicii."),
         ("Ce se leagă de ce aveți deja", "Site, aplicație, Alesia, portaluri, bancă de credite: fiecare integrare se face o singură dată.")],
    cond="Pilotul de 30 de zile (1.000 €) se face înainte. Prețul implementării se fixează pe baza diagnosticului, în interval. Abonamentul lunar începe după prima lună de implementare.",
    c_k="Cazuri · rezultate prezentate pe pachecost.com", c_t="Ce au obținut afaceri de servicii cu același fel de sistem.",
    c_nota="Rezultate reale, așa cum sunt prezentate pe pachecost.com, din afaceri de servicii care au pus un sistem cu IA la recepție, la răspuns și la urmărire. Punctul vostru de plecare îl măsurăm în pilot; rezultatele voastre le raportăm față de el.",
    cases=[("Centru medical · programări și recepție", "„Astăzi reușim să automatizăm până la 87 % din recepție și să creștem programările, fără să creștem costul.”",
            [("80–87 %", "din recepție automatizată"), ("+15–20", "programări în plus pe zi"), ("20 min → ~0", "așteptare per client la recepție")]),
           ("Clinică de imagistică · răspuns la cereri și site", "„Generează multe date, ai mai multă predictibilitate și poți măsura cine performează bine și de ce.”",
            [("R$ 40 mii", "în 3,5 luni, doar de la cei care nu programaseră"), ("+10 %", "venit lunar, cu urmărirea automată"), ("+7,5 %", "programări, cu site-ul nou")]),
           ("Magazin de haine · recepție pe WhatsApp", "„Astăzi IA răspunde 24 de ore pe zi și reușește să servească mult mai repede.”",
            [("24 h", "răspuns, în fiecare zi"), ("300+", "contacte pe zi pe WhatsApp"), ("7 zile", "până la primele câștiguri")]),
           ("Băuturi pentru evenimente · răspuns la cereri de ofertă", "„Ceva imposibil de servit manual. Automatizarea a fost factorul-cheie al noii etape de expansiune.”",
            [("50 → 500", "oferte răspunse pe zi"), ("10×", "capacitate în sezonul de vârf"), ("100 %", "din oferte fără așteptare după o persoană")]),
           ("Frizerii · programări", "„Când ajunge mesajul, vine deja lucrat: doar finalizezi programarea. Standardizează servirea.”",
            [("30 %", "servire mai eficientă"), ("3 → 1", "frizerii, o singură recepție"), ("În curs", "implementare, după spusele firmei")])],
    c_imob="La Obiectiv, echivalentul: fiecare cerere răspunsă și calificată în 5 minute, 7 zile din 7; proprietarul informat după fiecare vizionare; dosarul urmărit până la semnare. Obiectivul implementării: cel puțin dublarea caselor vândute în același interval.",
    contact=["Tomás Pacheco · Pacheco Studios", "WhatsApp +40 723 098 556", "ro.pachecost.com"],
)

PT = dict(
    marca="PACHECO STUDIOS · IMPLEMENTAÇÃO · OBIECTIV IMOBILIARE · OUTUBRO 2026",
    k="Depois do piloto · a implementação", t="Se virem resultados no piloto, é isto que podem esperar.",
    s="Faixa de investimento da implementação final na Obiectiv Imobiliare, fixada desde o início para não haver surpresas. O valor exato sai do diagnóstico.",
    min="7.500 €", max="25.000 €", band_k="Faixa da implementação",
    band_lo="Menos bloqueios · um só fluxo", band_hi="Mais bloqueios · todos os canais e a equipa",
    pay_n="1–3 meses", pay_t="Nos casos de pachecost.com, o investimento pagou-se em 1–3 meses com o lucro gerado para a empresa.",
    fac_k="O que move o valor dentro da faixa",
    fac=[("Quantos bloqueios atacamos", "O diagnóstico lista-os todos, com prioridade. Implementamos primeiro o que rende mais."),
         ("Quantos canais e pessoas entram no sistema", "Um fluxo com dois agentes custa menos do que os 6 canais, 4 agentes e 9 serviços."),
         ("O que se liga ao que já têm", "Site, app, Alesia, portais, banco de crédito: cada integração faz-se uma vez.")],
    cond="O piloto de 30 dias (1.000 €) vem antes. O preço da implementação fixa-se com base no diagnóstico, dentro da faixa. A mensalidade começa depois do primeiro mês de implementação.",
    c_k="Casos · resultados apresentados em pachecost.com", c_t="O que negócios de serviços obtiveram com o mesmo tipo de sistema.",
    c_nota="Resultados reais, tal como apresentados em pachecost.com, de negócios de serviços que puseram um sistema com IA na receção, na resposta e no seguimento. O vosso ponto de partida mede-se no piloto; os vossos resultados reportam-se face a ele.",
    cases=[("Centro médico · marcações e receção", "«Hoje conseguimos automatizar até 87 % do atendimento e ainda aumentar os agendamentos, sem aumentar custo.»",
            [("80–87 %", "da receção automatizada"), ("+15–20", "marcações extra por dia"), ("20 min → ~0", "de espera por cliente na receção")]),
           ("Clínica de exames · resposta a pedidos e site", "«Gera muito dado, tens mais previsibilidade e consegues medir quem está a performar bem e porquê.»",
            [("R$ 40 mil", "em 3,5 meses, só de quem não tinha marcado"), ("+10 %", "na receita mensal, com o seguimento automático"), ("+7,5 %", "nas marcações, com o site novo")]),
           ("Loja de roupa · receção no WhatsApp", "«Hoje a IA responde 24 horas por dia e consegue atender muito mais rápido.»",
            [("24 h", "de atendimento, todos os dias"), ("300+", "contactos por dia no WhatsApp"), ("7 dias", "até aos primeiros ganhos")]),
           ("Bebidas para eventos · resposta a orçamentos", "«Algo humanamente impossível de atender manualmente. A automação foi o fator-chave da nova fase de expansão.»",
            [("50 → 500", "orçamentos respondidos por dia"), ("10×", "capacidade na época alta"), ("100 %", "dos orçamentos sem esperar por uma pessoa")]),
           ("Barbearias · marcações", "«Quando a mensagem chega, já vem trabalhada: é só finalizar o agendamento. Padroniza o atendimento.»",
            [("30 %", "atendimento mais eficiente"), ("3 → 1", "barbearias, uma só receção"), ("Em curso", "implementação, segundo a própria empresa")])],
    c_imob="Na Obiectiv, o equivalente: cada pedido respondido e qualificado em 5 minutos, 7 dias por semana; o proprietário informado depois de cada visita; o processo seguido até à assinatura. Objetivo da implementação: no mínimo duplicar as casas vendidas no mesmo intervalo.",
    contact=["Tomás Pacheco · Pacheco Studios", "WhatsApp +40 723 098 556", "ro.pachecost.com"],
)

T = {"ro": RO, "pt": PT}

CSS3 = CSS + """
.band{margin-top:8mm}
.band .ends{display:flex;justify-content:space-between;align-items:flex-end}
.band .v{font-family:"Archivo Black",sans-serif;font-size:40pt;line-height:1;color:var(--o)}
.band .v.hi{color:var(--l)}
.band .lab{font-family:"Space Mono",monospace;font-size:7.5pt;letter-spacing:.08em;text-transform:uppercase;color:var(--o2);margin-top:2mm}
.band .bar{height:9mm;margin-top:4mm;background:linear-gradient(90deg,#4D4A47 0%,#A64923 55%,#E8622C 100%);border-radius:1mm;position:relative}
.band .bar i{position:absolute;top:-2.5mm;bottom:-2.5mm;width:.6mm;background:var(--o)}
.pay{display:flex;gap:7mm;align-items:center;margin-top:7mm;background:var(--c2);padding:4.5mm 6mm;border-left:3mm solid var(--l)}
.pay .n{font-family:"Archivo Black",sans-serif;font-size:26pt;line-height:1;color:var(--l);flex:none}
.pay p{font-size:11.5pt;line-height:1.4;color:var(--o)}
.fac{display:grid;grid-template-columns:repeat(3,1fr);gap:6mm;margin-top:6mm}
.fac div{border-top:1px solid #3a3632;padding-top:3mm}
.fac b{display:block;font-size:11pt;margin-bottom:1.5mm;color:var(--o)}
.fac p{font-size:9.5pt;line-height:1.4;color:var(--o2)}
.cond{margin-top:auto;font-family:"Space Mono",monospace;font-size:8pt;line-height:1.5;color:var(--o2);max-width:230mm}
.cz{display:grid;grid-template-columns:repeat(5,1fr);gap:4mm;margin-top:5mm}
.cz>div{background:#fff;border:1px solid var(--b);padding:4mm 4.5mm;display:flex;flex-direction:column}
.cz .sec{font-family:"Space Mono",monospace;font-size:7pt;letter-spacing:.08em;text-transform:uppercase;color:var(--lt);line-height:1.4;min-height:9mm}
.cz .q{font-size:8.6pt;line-height:1.35;color:var(--t2);margin:3mm 0 4mm;min-height:24mm}
.cz .num{border-top:1px solid var(--b);padding:2.2mm 0}
.cz .num b{display:block;font-family:"Archivo Black",sans-serif;font-weight:400;font-size:13pt;line-height:1.05}
.cz .num span{font-size:7.8pt;color:var(--t2);line-height:1.3}
.nota{font-size:9.5pt;line-height:1.45;color:var(--t2);max-width:240mm;margin-top:3mm}
"""


def pagina1(t):
    fac = ''.join(f'<div><b>{esc(a)}</b><p>{esc(b)}</p></div>' for a, b in t["fac"])
    return f'''<section class="p esc">
<div class="k"><i></i>{esc(t["k"])}</div><h2 style="max-width:250mm">{esc(t["t"])}</h2>
<p style="font-size:11.5pt;color:var(--o2);margin-top:4mm;max-width:190mm;line-height:1.4">{esc(t["s"])}</p>
<div class="band"><div class="k" style="margin-bottom:3mm">{esc(t["band_k"])}</div>
<div class="ends"><div><div class="v">{esc(t["min"])}</div><div class="lab">{esc(t["band_lo"])}</div></div><div style="text-align:right"><div class="v hi">{esc(t["max"])}</div><div class="lab">{esc(t["band_hi"])}</div></div></div>
<div class="bar"><i style="left:0"></i><i style="left:50%"></i><i style="right:0"></i></div></div>
<div class="pay"><div class="n">{esc(t["pay_n"])}</div><p>{esc(t["pay_t"])}</p></div>
<div class="k" style="margin-top:7mm">{esc(t["fac_k"])}</div>
<div class="fac">{fac}</div>
<div class="cond">{esc(t["cond"])}</div>
{rod(t, 1)}</section>'''


def pagina2(t):
    cz = ''
    for sec, q, nums in t["cases"]:
        n = ''.join(f'<div class="num"><b>{esc(a)}</b><span>{esc(b)}</span></div>' for a, b in nums)
        cz += f'<div><div class="sec">{esc(sec)}</div><div class="q">{esc(q)}</div>{n}</div>'
    ct = ' · '.join(esc(x) for x in t["contact"])
    return f'''<section class="p">
<div class="k"><i></i>{esc(t["c_k"])}</div><h2>{esc(t["c_t"])}</h2>
<div class="cz">{cz}</div>
<p class="nota">{esc(t["c_nota"])}</p>
<div class="conc" style="margin-top:4mm;font-size:11pt">{esc(t["c_imob"])}</div>
<div style="font-family:Space Mono,monospace;font-size:8pt;color:var(--t2);letter-spacing:.04em;margin-top:3mm">{ct}</div>
{rod(t, 2)}</section>'''


if __name__ == "__main__":
    for lang, t in T.items():
        html = (f'<!doctype html><html lang="{ {"ro": "ro", "pt": "pt-PT"}[lang] }"><head><meta charset="utf-8"><title>{esc(t["t"])}</title>'
                f'<style>{FONTES}{CSS3}</style></head><body>' + pagina1(t) + pagina2(t) + '</body></html>')
        nome = {"ro": "obiectiv-investitie-ro", "pt": "obiectiv-investimento-pt"}[lang]
        h = os.path.join(AQUI, nome + ".html")
        open(h, "w").write(html)
        pdf = os.path.join(AQUI, nome + ".pdf")
        subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=8000",
                        f"--print-to-pdf={pdf}", "file://" + h], check=True, capture_output=True)
        print(lang, os.path.getsize(pdf) // 1024, "KB")
