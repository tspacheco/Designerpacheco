#!/usr/bin/env python3
"""Gera o plano semanal de prospeção a pé em Iași: mapa HTML (Leaflet embutido, mapa OpenStreetMap ao vivo) + KML para o Google My Maps.
Coordenadas aproximadas (sem acesso a dados de mapa nesta sessão): confirmar no mapa e ajustar ZONAS se preciso, depois correr outra vez."""
import json, math, pathlib, urllib.parse as up
AQUI = pathlib.Path(__file__).parent
LEAFLET = pathlib.Path('/tmp/claude-0/-home-user-Designerpacheco/53c8a074-377d-58ee-b801-b59b59b7af13/scratchpad/lf/package/dist')

BASE = {"nome": "Universitatea Alexandru Ioan Cuza (Bd. Carol I 11)", "lat": 47.1742, "lon": 27.5717}

ZONAS = [
  dict(dia="Segunda", curto="SEG", cor="#E4572E", nome="Copou — à volta da universidade", lat=47.1765, lon=27.5700, r=600,
       hora="15h00–18h00", chegar="A pé (é a tua zona)", km="≈ 3 km",
       ruas=["Bd. Carol I", "Parcul Copou e ruas à volta", "Str. Lascăr Catargi", "Ruas laterais entre a UAIC e o parque"],
       alvos=["Cafés e pastelarias de estudantes", "Copy-centers e papelarias", "Clínicas dentárias e óticas", "Salões e barbearias", "Restaurantes de almoço"],
       nota="Dia de aquecimento: zona que já conheces, donos jovens, inglês funciona. Treina a abertura do guião aqui.",
       pesquisa=["cafenea", "restaurant", "salon"]),
  dict(dia="Terça", curto="TER", cor="#F3A712", nome="Centro — Piața Unirii e Lăpușneanu", lat=47.1662, lon=27.5790, r=500,
       hora="15h00–18h00", chegar="A pé, ~1,2 km a descer o Bd. Carol I", km="≈ 3 km",
       ruas=["Piața Unirii", "Str. Lăpușneanu", "Bd. Ștefan cel Mare și Sfânt", "Str. Cuza Vodă"],
       alvos=["Restaurantes com turistas", "Cafés de especialidade", "Pastelarias e gelatarias", "Lojas independentes (roupa, presentes)"],
       nota="Zona mais disputada: os melhores vão ter site. Procura os de 4,5★ SEM site — são os que valem uma demo.",
       pesquisa=["restaurant", "specialty coffee", "cofetărie"]),
  dict(dia="Quarta", curto="QUA", cor="#2E86AB", nome="Palatul Culturii, Hala Centrală e Anastasie Panu", lat=47.1578, lon=27.5885, r=520,
       hora="15h00–18h00", chegar="A pé, ~2 km, ou elétrico até Palas", km="≈ 3–4 km",
       ruas=["Str. Anastasie Panu", "Hala Centrală e ruas à volta", "Str. Palat", "Fim sul do Bd. Ștefan cel Mare"],
       alvos=["Padarias e talhos independentes (à volta da Hala)", "Restaurantes e bistrôs", "Serviços: explicações, fotografia, reparações"],
       nota="Ignora o Palas Mall: é tudo cadeias. O ouro está nas ruas à volta da Hala Centrală.",
       pesquisa=["brutărie", "restaurant", "bistro"]),
  dict(dia="Quinta", curto="QUI", cor="#6A4C93", nome="Tătărași", lat=47.1640, lon=27.6045, r=650,
       hora="15h00–18h00", chegar="Autocarro/elétrico (~2,5 km da UAIC)", km="≈ 3–4 km",
       ruas=["Str. Vasile Lupu (eixo principal)", "Ruas comerciais paralelas"],
       alvos=["Padarias e cafés de bairro", "Salões e barbearias", "Oficinas e serviços auto", "Clínicas e farmácias independentes"],
       nota="Bairro residencial: negócios de clientela fixa, muitos só com Facebook. Argumento: aparecer no Google a quem se muda para o bairro.",
       pesquisa=["salon", "brutărie", "service auto"]),
  dict(dia="Sexta", curto="SEX", cor="#1B998B", nome="Păcurari e zona da Gara", lat=47.1690, lon=27.5570, r=650,
       hora="15h00–18h00", chegar="A pé, ~1,5 km para oeste, ou autocarro", km="≈ 3–4 km",
       ruas=["Str. Păcurari (eixo principal)", "Zona da Gara Iași"],
       alvos=["Clínicas dentárias e veterinárias", "Oficinas", "Restaurantes de bairro e take-away", "Pequenos hotéis perto da estação"],
       nota="Perto da estação há alojamento pequeno que vive de reservas online — bom alvo para site com botão de reserva.",
       pesquisa=["cabinet stomatologic", "restaurant", "pensiune"]),
  dict(dia="Sábado", curto="SÁB", cor="#C5283D", nome="Podu Roș e Piața Nicolina", lat=47.1470, lon=27.5930, r=650,
       hora="09h30–13h00", chegar="Elétrico até Podu Roș (~3 km)", km="≈ 3–4 km",
       ruas=["Podu Roș", "Bd. Nicolae Iorga", "Piața Nicolina (mercado) e ruas à volta"],
       alvos=["Bancas e lojas do mercado com marca própria (mel, queijo, charcutaria)", "Padarias e pastelarias", "Floristas", "Take-away"],
       nota="Sábado de manhã o mercado está cheio e os donos estão lá. Só cartão e conversa curta — nada de demos longas.",
       pesquisa=["piață", "brutărie", "florărie"]),
]

def circulo(lat, lon, r, n=72):
    pts = []
    for k in range(n + 1):
        a = 2 * math.pi * k / n
        dlat = (r * math.cos(a)) / 111320
        dlon = (r * math.sin(a)) / (111320 * math.cos(math.radians(lat)))
        pts.append((lat + dlat, lon + dlon))
    return pts

def dist_km(a, b):
    R = 6371
    p1, p2 = math.radians(a[0]), math.radians(b[0]); dp = p2 - p1; dl = math.radians(b[1] - a[1])
    h = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2 * R * math.asin(math.sqrt(h))

for z in ZONAS:
    z["dist"] = round(dist_km((BASE["lat"], BASE["lon"]), (z["lat"], z["lon"])), 1)
    z["dir"] = "https://www.google.com/maps/dir/?api=1&origin=" + up.quote(f'{BASE["lat"]},{BASE["lon"]}') + "&destination=" + up.quote(f'{z["lat"]},{z["lon"]}') + "&travelmode=" + ("walking" if z["dist"] < 1.8 else "transit")
    z["links"] = [(q, f"https://www.google.com/maps/search/{up.quote(q)}/@{z['lat']},{z['lon']},16z") for q in z["pesquisa"]]

# ---------- KML (Google My Maps) ----------
def kml_cor(hexcor, alpha):
    h = hexcor.lstrip('#'); return f"{alpha}{h[4:6]}{h[2:4]}{h[0:2]}".lower()
pm = []
for i, z in enumerate(ZONAS):
    coords = " ".join(f"{lo:.6f},{la:.6f},0" for la, lo in circulo(z["lat"], z["lon"], z["r"]))
    desc = f"{z['hora']} · {z['km']} a pé dentro da zona · {z['chegar']}\nRuas: {', '.join(z['ruas'])}\nAlvos: {', '.join(z['alvos'])}\n{z['nota']}"
    pm.append(f"""<Style id="s{i}"><LineStyle><color>{kml_cor(z['cor'],'ff')}</color><width>3</width></LineStyle><PolyStyle><color>{kml_cor(z['cor'],'40')}</color></PolyStyle></Style>
<Placemark><name>{z['dia']} — {z['nome']}</name><description><![CDATA[{desc}]]></description><styleUrl>#s{i}</styleUrl><Polygon><outerBoundaryIs><LinearRing><coordinates>{coords}</coordinates></LinearRing></outerBoundaryIs></Polygon></Placemark>""")
pm.append(f'<Placemark><name>Base — UAIC</name><Point><coordinates>{BASE["lon"]},{BASE["lat"]},0</coordinates></Point></Placemark>')
(AQUI / "semana-1.kml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2"><Document><name>Pacheco Studios — Iași, semana 1</name>\n' + "\n".join(pm) + "\n</Document></kml>\n", encoding="utf-8")

# ---------- HTML ----------
dados = [dict(dia=z["dia"], curto=z["curto"], cor=z["cor"], nome=z["nome"], lat=z["lat"], lon=z["lon"], r=z["r"], hora=z["hora"], chegar=z["chegar"], km=z["km"], dist=z["dist"], ruas=z["ruas"], alvos=z["alvos"], nota=z["nota"], dir=z["dir"], links=z["links"]) for z in ZONAS]
css = (LEAFLET / "leaflet.css").read_text(encoding="utf-8")
js = (LEAFLET / "leaflet.js").read_text(encoding="utf-8").replace("</script>", "<\\/script>")
html = (AQUI / "semana-1.src.html").read_text(encoding="utf-8")
html = html.replace("/*LEAFLET_CSS*/", css).replace("/*LEAFLET_JS*/", js).replace("/*DADOS*/", "var ZONAS=" + json.dumps(dados, ensure_ascii=False) + ";var BASE=" + json.dumps(BASE, ensure_ascii=False) + ";")
(AQUI / "semana-1.html").write_text(html, encoding="utf-8")
for z in ZONAS: print(z["curto"], z["nome"], f'{z["dist"]} km da UAIC', f'r={z["r"]} m')
