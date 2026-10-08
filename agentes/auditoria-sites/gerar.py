#!/usr/bin/env python3
"""Agente 3 · auditoria grátis a sites fracos (Pacheco Studios).

Lê o que a PONTE mediu (auditorias/dados/<slug>.json, operação «auditar») e os dados das fichas Google
(candidatos.csv) e produz:

  python3 gerar.py ranking          auditorias/RANKING.md: todos os sites medidos, do mais fraco ao mais forte
  python3 gerar.py <slug> [<slug>]  auditorias/<slug>/: apresentação ao dono em RO e versão PT para o Tomás
  python3 gerar.py --top 10         as 10 primeiras do ranking (com nota Google ≥ 4,4)

Cada apresentação sai em HTML e em PDF (o PDF é o que se manda pelo WhatsApp). Tudo o que aparece com números foi
medido no próprio dia (Lighthouse móvel + Chromium com ecrã de iPhone). A única estatística de fora é a da Google
sobre velocidade e abandono, com a fonte escrita na página.
"""
import base64, csv, html, io, json, os, re, sys, datetime
from urllib.parse import urlparse

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
DADOS = os.path.join(RAIZ, "auditorias", "dados")
SAIDA = os.path.join(RAIZ, "auditorias")
RAMO = "claude/auditoria-sites-fracos-fpyd0h"
RAW = f"https://github.com/tspacheco/Designerpacheco/raw/{RAMO}/auditorias"
WHATSAPP_RO = "+40 723 098 556"
WA_LINK = "https://wa.me/40723098556"
ANO = datetime.date.today().year

# Demo nossa medida com a mesma ferramenta, por tipo de negócio («o que podia ser»).
DEMO_POR_TIPO = [
    (r"barber|frizer|saloon|tuns", "trend-barbershop", "Trend Barbershop"),
    (r"flor|fleur|flower|floral|bujor|rosalia", "elenor", "Florăria Elenor"),
    (r"cofetar|patiser|tort|cake|creme|gelat|brut[aă]r|p[aâ]ine|paini|desert", "laurinda", "Cofetăria Laurinda"),
    (r"vet|pet|animal", "pumbavet", "PumbaVet"),
    (r"sp[aă]l[aă]tor|wash|detailing", "auto-spa", "Auto Spa & Detailing"),
    (r"auto|motors|service|vulcan|termo|geam|tâmpl|tampl|ferestre", "la-punct", "Service Auto La Punct"),
    (r"cafe|coffee|cafenea|roast", "fika", "Fika"),
    (r"shaorm|shaworm|tacos|fast|kebab", "dubai-shaworma", "Dubai Shaworma"),
    (r"pizz|restaurant|bistro|conac|c[aâ]rcium|berăr|berar|trai|rustic|cheffa|vindum|vin", "la-gioia", "La Gioia di Giovanni"),
    (r"salon|beauty|nail|unghii|lash|gene|estetic|skin|body|clinic|masaj|tatu|tattoo|ink|epil|fit|kinetic", "beauty-zone", "Beauty Zone"),
]
DEMO_PADRAO = ("fika", "Fika")
# Fora do --top: lojas de cadeia (a decisão não é local, PLAYBOOK §11).
EXCLUIR = {"magazin-aurora-iasi-calea-gala"}

# Think with Google (2017), «Find out how you stack up to new industry benchmarks for mobile page speed»:
# quando o carregamento passa de 1 s para X s, a probabilidade de o visitante sair (bounce) aumenta Y %.
GOOGLE_ABANDONO = [(10, 123), (6, 106), (5, 90), (3, 32)]
FONTE_GOOGLE = "Think with Google, 2017 — «Find out how you stack up to new industry benchmarks for mobile page speed»"

T = {
    "ro": {
        "lang": "ro", "titulo": "Auditul site-ului", "gratis": "Audit gratuit",
        "medido": "Măsurat pe {d}, pe telefon (Lighthouse, motorul Google PageSpeed, + iPhone simulat).",
        "elogio": "{nota}★ pe Google{aval}. Clienții vă apreciază. Site-ul încă nu vă ajută cât ar putea.",
        "aval": " din {n} de recenzii",
        "hoje": "Site-ul tău azi", "podia": "Ce ar putea fi", "podia_sub": "un site făcut de noi ({demo}), măsurat la fel, în aceeași zi",
        "cats": {"performance": "Viteză", "accessibility": "Accesibilitate", "best-practices": "Bune practici", "seo": "Google (SEO)"},
        "de100": "din 100",
        "tempos": "Ce vede clientul pe telefon",
        "fcp": "Apare primul lucru pe ecran", "lcp": "Apare conținutul principal", "peso": "Cât descarcă telefonul",
        "pedidos": "Fișiere încărcate",
        "achados": "Ce am găsit", "sim": "Da", "nao": "Nu",
        "chk": {
            "https": "Conexiune securizată (lacătul din browser)",
            "viewport": "Făcut pentru ecranul de telefon",
            "cabe": "Încape pe ecran, fără să alunece în lateral",
            "tel": "Buton «Sună» care formează numărul",
            "tel1": "Telefonul vizibil din primul ecran",
            "whatsapp": "WhatsApp cu o apăsare",
            "marcacao": "Programare sau rezervare online",
            "mapa": "Hartă / «Cum ajungi»",
            "jsonld": "Fișa pentru Google (program, adresă, tip de afacere)",
            "descricao": "Textul care apare sub numele tău în Google",
            "ano": "Anul din subsol e la zi",
        },
        "ganhos": "3 câștiguri rapide", "ganhos_sub": "Primele lucruri pe care le-am face. Fiecare se vede din prima zi.",
        "g_hoje": "Azi", "g_muda": "Ce schimbăm", "g_ganha": "Ce câștigi",
        "clientes": "Ce înseamnă în clienți",
        "abandono": "Google a măsurat că, atunci când o pagină se încarcă în {x} s în loc de 1 s, șansa ca omul să plece înainte să vadă ceva crește cu {p} %.",
        "abandono_ok": "Viteza nu e problema principală: conținutul apare în {x} s. Câștigul e în ce găsește clientul când ajunge.",
        "teu_lcp": "Site-ul tău: conținutul principal apare după {x} s.", "nosso_lcp": "Site-ul nostru: după {y} s.",
        "passos": "Ca să te sune azi: {a}. Cu site-ul nou: o apăsare pe «Sună» sau «WhatsApp», din primul ecran.",
        "passos_sem": "găsește numărul, ține apăsat, copiază, deschide telefonul, lipește",
        "passos_long": "derulează până la număr, apasă pe el",
        "fonte": "Sursa", "cta_t": "Vrei să vezi cum ar arăta site-ul tău?",
        "cta": "Îți arătăm în 20 de minute, la tine sau la telefon. Fără costuri și fără obligații.",
        "cta_wa": "Scrie-ne pe WhatsApp", "assin": "Tomás Pacheco · Pacheco Studios · ro.pachecost.com",
        "nota_honesta": "Toate cifrele de mai sus au fost măsurate pe site-ul tău, în ziua auditului. Nu am inventat nimic.",
        "nota_demo": "Site-ul nostru de exemplu e ascuns de Google intenționat; nota lui SEO e măsurată fără acea verificare.",
        "pag": "Pagina",
    },
    "pt": {
        "lang": "pt-PT", "titulo": "Auditoria do site", "gratis": "Auditoria grátis",
        "medido": "Medido a {d}, no telemóvel (Lighthouse, o motor do Google PageSpeed, + iPhone simulado).",
        "elogio": "{nota}★ no Google{aval}. Os clientes gostam. O site ainda não ajuda o que podia.",
        "aval": " em {n} avaliações",
        "hoje": "O teu site hoje", "podia": "O que podia ser", "podia_sub": "um site feito por nós ({demo}), medido da mesma forma, no mesmo dia",
        "cats": {"performance": "Velocidade", "accessibility": "Acessibilidade", "best-practices": "Boas práticas", "seo": "Google (SEO)"},
        "de100": "em 100",
        "tempos": "O que o cliente vê no telemóvel",
        "fcp": "Aparece a primeira coisa no ecrã", "lcp": "Aparece o conteúdo principal", "peso": "Quanto o telemóvel descarrega",
        "pedidos": "Ficheiros carregados",
        "achados": "O que encontrámos", "sim": "Sim", "nao": "Não",
        "chk": {
            "https": "Ligação segura (o cadeado do browser)",
            "viewport": "Feito para ecrã de telemóvel",
            "cabe": "Cabe no ecrã, sem deslizar para o lado",
            "tel": "Botão «Ligar» que marca o número",
            "tel1": "Telefone visível no primeiro ecrã",
            "whatsapp": "WhatsApp com um toque",
            "marcacao": "Marcação ou reserva online",
            "mapa": "Mapa / «Como chegar»",
            "jsonld": "Ficha para o Google (horário, morada, tipo de negócio)",
            "descricao": "O texto que aparece debaixo do nome no Google",
            "ano": "O ano do rodapé está atualizado",
        },
        "ganhos": "3 vitórias rápidas", "ganhos_sub": "As primeiras coisas que faríamos. Cada uma vê-se no primeiro dia.",
        "g_hoje": "Hoje", "g_muda": "O que mudamos", "g_ganha": "O que ganhas",
        "clientes": "O que isto quer dizer em clientes",
        "abandono": "A Google mediu que, quando uma página carrega em {x} s em vez de 1 s, a probabilidade de a pessoa sair antes de ver alguma coisa aumenta {p} %.",
        "abandono_ok": "A velocidade não é o problema principal: o conteúdo aparece em {x} s. O ganho está no que o cliente encontra quando chega.",
        "teu_lcp": "O teu site: o conteúdo principal aparece ao fim de {x} s.", "nosso_lcp": "O nosso: ao fim de {y} s.",
        "passos": "Para te ligar hoje: {a}. Com o site novo: um toque em «Ligar» ou «WhatsApp», logo no primeiro ecrã.",
        "passos_sem": "encontra o número, carrega sem largar, copia, abre o telefone, cola",
        "passos_long": "desce até ao número e carrega nele",
        "fonte": "Fonte", "cta_t": "Queres ver como ficaria o teu site?",
        "cta": "Mostramos-te em 20 minutos, aí ou ao telefone. Sem custo e sem compromisso.",
        "cta_wa": "Fala connosco no WhatsApp", "assin": "Tomás Pacheco · Pacheco Studios · pachecost.com",
        "nota_honesta": "Todos os números acima foram medidos no teu site, no dia da auditoria. Nada foi inventado.",
        "nota_demo": "O nosso site de exemplo está escondido do Google de propósito; a nota SEO dele é medida sem essa verificação.",
        "pag": "Página",
    },
}


def ler_candidatos():
    return {r["slug"]: r for r in csv.DictReader(open(os.path.join(AQUI, "candidatos.csv"), encoding="utf-8"))}


def ler(slug):
    p = os.path.join(DADOS, f"{slug}.json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def aud(d, k, campo="valor"):
    return ((d or {}).get("auditorias", {}).get(k) or {}).get(campo)


def seg(ms):
    return None if ms is None else round(ms / 1000, 1)


def demo_para(c):
    txt = f"{c.get('categoria', '')} {c.get('nome', '')} {c.get('site', '')}".lower()
    for rx, slug, nome in DEMO_POR_TIPO:
        if re.search(rx, txt):
            return slug, nome
    return DEMO_PADRAO


def verificacoes(d, c):
    """Cada verificação: (chave, passou?) — None quando não foi possível medir."""
    p = d.get("pagina") or {}
    if not p:
        return []
    url = d.get("url_final_tel") or d.get("url_final") or d.get("url", "")
    tipos = " ".join(map(str, p.get("jsonld") or [])).lower()
    marc = re.search(r"salon|barber|frizer|beauty|nail|unghii|lash|gene|estetic|clinic|masaj|tatu|tattoo|vet|service|restaurant|bistro|pizz|kinetic|fit",
                     f"{c.get('categoria', '')} {c.get('nome', '')}".lower())
    out = [
        ("https", url.startswith("https://")),
        ("viewport", "width=device-width" in (p.get("viewport") or "")),
        ("cabe", not p.get("transborda")),
        ("tel", (p.get("tel") or 0) > 0),
        ("tel1", bool(p.get("tel_no_1o_ecra"))),
        ("whatsapp", (p.get("whatsapp") or 0) > 0),
    ]
    if marc:
        out.append(("marcacao", (p.get("marcacao") or 0) > 0))
    out += [
        ("mapa", (p.get("mapa") or 0) > 0),
        ("jsonld", any(t in tipos for t in ("localbusiness", "restaurant", "store", "salon", "barber", "beauty",
                                                "clinic", "veterinary", "autorepair", "bakery", "florist", "cafe",
                                                "foodestablishment", "health", "automotive", "professionalservice"))),
        ("descricao", len((p.get("descricao") or "").strip()) >= 50),
    ]
    if p.get("ano_copyright"):
        out.append(("ano", p["ano_copyright"] >= ANO - 1))
    return out


def fraqueza(d, c):
    """0–100: quanto mais alto, mais fraco o site (e mais fácil mostrar a diferença)."""
    if not d:
        return None
    if d.get("erro_pagina") and not d.get("notas"):
        return 100
    n = dict(d.get("notas") or {})
    if n.get("performance") == 0 and aud(d, "largest-contentful-paint") is None:
        n["performance"] = 50  # o Lighthouse não apanhou o LCP: nota 0 não é real
    f = (100 - n.get("performance", 50)) * 0.35 + (100 - n.get("seo", 80)) * 0.15 + (100 - n.get("accessibility", 80)) * 0.1
    pesos = {"https": 10, "viewport": 15, "cabe": 8, "tel": 10, "tel1": 5, "whatsapp": 5, "marcacao": 6,
             "jsonld": 4, "descricao": 3, "ano": 6, "mapa": 2}
    for k, ok in verificacoes(d, c):
        if ok is False:
            f += pesos.get(k, 2)
    lcp = seg(aud(d, "largest-contentful-paint"))
    if lcp and lcp > 4:
        f += min(10, (lcp - 4) * 2)
    return round(min(100, f))


def nota_num(c):
    try:
        return float(c.get("nota", "0").replace(",", "."))
    except ValueError:
        return 0


def ranking(cands):
    linhas = []
    for slug, c in cands.items():
        d = ler(slug)
        if not d:
            continue
        fr = fraqueza(d, c)
        n = d.get("notas") or {}
        linhas.append((fr, slug, c, d, n))
    linhas.sort(key=lambda x: (-(x[0] or 0), -nota_num(x[2])))
    return linhas


def escrever_ranking(cands):
    linhas = ranking(cands)
    demos = {s: ler(f"demo-{s}") for _, s, _ in DEMO_POR_TIPO + [(None,) + DEMO_PADRAO]}
    out = ["# Agente 3 · ranking dos sites medidos (Iași)", "",
           "Do mais fraco para o mais forte. Fraqueza 0–100 (velocidade, SEO, acessibilidade e o que falta ao cliente no telemóvel). "
           "Medido pela PONTE (`auditar`): Lighthouse móvel + Chromium com ecrã de iPhone. Regerar: `python3 agentes/auditoria-sites/gerar.py ranking`.", "",
           "## As nossas demos, medidas da mesma forma", "", "| Demo | Velocidade | SEO | Acess. | Conteúdo principal |", "|---|---|---|---|---|"]
    for s, d in demos.items():
        if d and d.get("notas"):
            n = d["notas"]
            out.append(f"| {s} | {n.get('performance')} | {n.get('seo')} | {n.get('accessibility')} | {seg(aud(d, 'largest-contentful-paint'))} s |")
    out += ["", "## Negócios", "", "| # | Fraqueza | Negócio | Google | Velocidade | SEO | Conteúdo principal | Falta | Site |", "|---|---|---|---|---|---|---|---|---|"]
    for i, (fr, slug, c, d, n) in enumerate(linhas, 1):
        falta = [k for k, ok in verificacoes(d, c) if ok is False]
        lcp = seg(aud(d, "largest-contentful-paint"))
        erro = "não abre" if d.get("erro_pagina") and not n else ""
        out.append(f"| {i} | {fr} | {c['nome']} ({slug}) | {c.get('nota')}{' · ' + c['avaliacoes'] if c.get('avaliacoes') else ''} | "
                   f"{n.get('performance', '—')} | {n.get('seo', '—')} | {str(lcp) + ' s' if lcp else '—'} | {erro or ', '.join(falta) or '—'} | {c['site']} |")
    open(os.path.join(SAIDA, "RANKING.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    return linhas


# ---------------------------------------------------------------- vitórias rápidas

def vitorias(d, c, demo, L):
    """Lista ordenada de (titulo, hoje, muda, ganha). As 3 primeiras vão para a apresentação."""
    ro = L["lang"] == "ro"
    p = d.get("pagina") or {}
    chk = dict(verificacoes(d, c))
    lcp, lcp_d = seg(aud(d, "largest-contentful-paint")), seg(aud(demo, "largest-contentful-paint"))
    peso = aud(d, "total-byte-weight")
    img_poupa = sum((aud(d, k, "poupa_bytes") or 0) for k in ("uses-optimized-images", "modern-image-formats", "uses-responsive-images", "offscreen-images"))
    v = []
    if chk.get("viewport") is False or chk.get("cabe") is False:
        v.append(("Site-ul nu e făcut pentru telefon" if ro else "O site não está feito para telemóvel",
                  ("Pe telefon textul iese din ecran și trebuie mărit cu degetele." if ro else "No telemóvel o texto sai do ecrã e é preciso ampliar com os dedos")
                  if chk.get("cabe") is False else ("Pagina se afișează ca pe calculator, micșorată." if ro else "A página aparece como no computador, encolhida."),
                  "Reconstruim pagina pentru ecranul de telefon, unde vin majoritatea clienților din Google Maps." if ro else "Refazemos a página para o ecrã do telemóvel, de onde vem a maioria dos clientes do Google Maps.",
                  "Se citește fără zoom, din prima secundă." if ro else "Lê-se sem zoom, desde o primeiro segundo."))
    if lcp and lcp_d and lcp - lcp_d >= 1.5:
        mb = f"{peso / 1048576:.1f} MB" if peso else ""
        hoje = (f"Conținutul principal apare după {lcp} s; telefonul descarcă {mb}." if ro else f"O conteúdo principal aparece ao fim de {lcp} s; o telemóvel descarrega {mb}.")
        muda = ((f"Pozele comprimate corect ({img_poupa / 1048576:.1f} MB economisiți doar din imagini) și pagina fără scripturi inutile." if ro else
                 f"Fotos comprimadas como deve ser ({img_poupa / 1048576:.1f} MB poupados só nas imagens) e página sem scripts a mais.")
                if img_poupa > 200_000 else ("Pagina rescrisă ușoară: fără scripturi inutile, poze în format modern." if ro else "Página reescrita leve: sem scripts a mais, fotos em formato moderno."))
        v.append(("Pagina se încarcă greu pe telefon" if ro else "A página demora a carregar no telemóvel", hoje, muda,
                  (f"{round(lcp - lcp_d, 1)} s mai repede: {lcp_d} s în loc de {lcp} s, măsurat la fel." if ro else f"{round(lcp - lcp_d, 1)} s mais rápido: {lcp_d} s em vez de {lcp} s, medido da mesma forma.")))
    if chk.get("tel") is False or chk.get("tel1") is False:
        v.append(("Clientul nu te poate suna cu o apăsare" if ro else "O cliente não te consegue ligar com um toque",
                  (("Numărul e scris ca text: trebuie copiat și lipit." if ro else "O número está escrito como texto: tem de ser copiado e colado.") if chk.get("tel") is False
                   else ("Butonul de apel există, dar nu apare în primul ecran." if ro else "O botão de ligar existe, mas não aparece no primeiro ecrã.")),
                  "Buton «Sună» fix, vizibil pe tot site-ul." if ro else "Botão «Ligar» fixo, visível em todo o site.",
                  "O apăsare până la apel, de pe orice pagină." if ro else "Um toque até à chamada, de qualquer página."))
    if chk.get("marcacao") is False:
        v.append(("Nu se poate face programare online" if ro else "Não dá para marcar online",
                  "Clientul trebuie să sune în programul tău ca să-și facă programare." if ro else "O cliente tem de ligar dentro do horário para marcar.",
                  "Buton de programare legat de agenda ta (MERO sau alt sistem), 24 de ore din 24." if ro else "Botão de marcação ligado à tua agenda (MERO ou outro sistema), 24 horas por dia.",
                  "Programări și seara, când ești închis, fără să răspunzi la telefon." if ro else "Marcações também à noite, com a porta fechada, sem atender o telefone."))
    if chk.get("whatsapp") is False:
        v.append(("Lipsește WhatsApp" if ro else "Falta o WhatsApp",
                  "Nu există un buton de WhatsApp pe site." if ro else "Não há botão de WhatsApp no site.",
                  "Buton WhatsApp cu mesajul deja scris («Bună ziua, aș dori…»)." if ro else "Botão de WhatsApp com a mensagem já escrita («Olá, queria…»).",
                  "Cine nu vrea să sune îți scrie în 2 secunde, și ai mesajul în scris." if ro else "Quem não quer ligar escreve-te em 2 segundos, e fica tudo por escrito."))
    if chk.get("https") is False:
        v.append(("Chrome afișează «Nesigur»" if ro else "O Chrome mostra «Não seguro»",
                  "Site-ul se deschide fără lacăt (http)." if ro else "O site abre sem cadeado (http).",
                  "Certificat de securitate inclus." if ro else "Certificado de segurança incluído.",
                  "Fără avertismentul care sperie clientul înainte să citească ceva." if ro else "Sem o aviso que assusta o cliente antes de ler alguma coisa."))
    if chk.get("ano") is False:
        an = p.get("ano_copyright")
        v.append((f"© {an} în subsol" if ro else f"© {an} no rodapé",
                  f"Subsolul spune {an}. Clientul se întreabă dacă mai sunteți deschiși." if ro else f"O rodapé diz {an}. O cliente pergunta-se se ainda estão abertos.",
                  "Site întreținut lunar: anul, programul și prețurile mereu la zi." if ro else "Site mantido todos os meses: ano, horário e preços sempre em dia.",
                  "Arată că afacerea e vie." if ro else "Mostra que o negócio está vivo."))
    if chk.get("jsonld") is False:
        v.append(("Google nu știe exact ce ești" if ro else "O Google não sabe bem o que és",
                  "Site-ul nu are fișa tehnică pentru Google (tip de afacere, program, adresă, telefon)." if ro else "O site não tem a ficha técnica para o Google (tipo de negócio, horário, morada, telefone).",
                  "Adăugăm fișa, legată de profilul tău Google Maps." if ro else "Juntamos a ficha, ligada ao teu perfil do Google Maps.",
                  "Google îți poate arăta programul și adresa direct în rezultate." if ro else "O Google pode mostrar o horário e a morada diretamente nos resultados."))
    if chk.get("descricao") is False:
        v.append(("Textul din Google e ales la întâmplare" if ro else "O texto do Google é escolhido ao acaso",
                  "Nu există descriere pentru Google; el ia o bucată oarecare din pagină." if ro else "Não há descrição para o Google; ele usa um pedaço qualquer da página.",
                  "Scriem 2 rânduri care spun ce faci, unde și cum te contactează." if ro else "Escrevemos 2 linhas que dizem o que fazes, onde e como te contactam.",
                  "Mai mulți oameni apasă pe tine în loc de concurent." if ro else "Mais pessoas carregam em ti em vez de no concorrente."))
    return v


def b64img(path, largura=520):
    from PIL import Image
    im = Image.open(path).convert("RGB")
    if im.width > largura:
        im = im.resize((largura, round(im.height * largura / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=80, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def cor_nota(n):
    return "var(--mau)" if n < 50 else ("var(--medio)" if n < 90 else "var(--bom)")


def anel(n, rot):
    c = 2 * 3.14159 * 26
    return (f'<div class="anel"><svg viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="32" r="26" class="trilho"/>'
            f'<circle cx="32" cy="32" r="26" class="arco" style="stroke:{cor_nota(n)};stroke-dasharray:{c * n / 100:.1f} {c:.1f}"/></svg>'
            f'<b style="color:{cor_nota(n)}">{n}</b><span>{html.escape(rot)}</span></div>')


CSS = """
@page{size:A4;margin:0}
:root{--carvao:#141210;--osso:#EFEAE3;--papel:#FAF8F4;--laranja:#E8622C;--laranja-t:#A64923;--linha:#D9D2C6;--cinza:#6B655C;
--mau:#C4372B;--medio:#B7791F;--bom:#2F7D5B;--display:"Archivo Black",system-ui,sans-serif;--corpo:"Archivo",system-ui,sans-serif;--num:"JetBrains Mono",ui-monospace,monospace}
*{box-sizing:border-box;margin:0;padding:0}
html{background:#E7E1D7}
body{font:400 10.5pt/1.45 var(--corpo);color:var(--carvao);-webkit-print-color-adjust:exact;print-color-adjust:exact}
.folha{width:210mm;height:297mm;margin:0 auto 10mm;background:var(--papel);padding:16mm 15mm 14mm;position:relative;display:flex;flex-direction:column;page-break-after:always;break-after:page;overflow:hidden}
.folha:last-child{page-break-after:auto;break-after:auto}
@media print{html{background:none}.folha{margin:0}}
.topo{display:flex;align-items:center;justify-content:space-between;font:600 8pt/1 var(--corpo);letter-spacing:.14em;text-transform:uppercase;color:var(--cinza);margin-bottom:9mm}
.topo .marca{display:flex;align-items:center;gap:8px;color:var(--carvao)}
.topo svg{width:26px;height:26px}
.etiqueta{align-self:flex-start;display:inline-block;background:var(--laranja);color:#fff;font:700 7.5pt/1 var(--corpo);letter-spacing:.16em;text-transform:uppercase;padding:5px 8px 4px;border-radius:2px}
h1{font:400 30pt/0.98 var(--display);text-transform:uppercase;letter-spacing:-.01em;margin:4mm 0 3mm;max-width:16ch}
h1 em{font-style:normal;color:var(--laranja)}
h2{font:400 17pt/1 var(--display);text-transform:uppercase;margin-bottom:4mm}
.dominio{font:500 10pt/1 var(--num);color:var(--cinza)}
.elogio{font:500 12pt/1.4 var(--corpo);margin-top:4mm;max-width:52ch}
.medido{font-size:8pt;color:var(--cinza);margin-top:2mm}
.duelo{display:grid;grid-template-columns:1fr 1fr;gap:7mm;margin-top:7mm;flex:1}
.lado{border:1px solid var(--linha);border-radius:6px;padding:5mm;background:#fff;display:flex;flex-direction:column;gap:4mm}
.lado.nosso{background:var(--carvao);color:var(--osso);border-color:var(--carvao)}
.lado h3{font:400 11pt/1 var(--display);text-transform:uppercase;letter-spacing:.02em}
.lado .sub{font-size:7pt;line-height:1.3;color:var(--cinza);margin-top:-2.5mm;min-height:4em}
.lado.nosso .sub{color:#A9A196}
.tel{width:43mm;height:88mm;margin:0 auto;border-radius:7mm;border:2.2mm solid #1E1C1A;background:#1E1C1A;overflow:hidden;box-shadow:0 6px 18px rgba(0,0,0,.18)}
.lado.nosso .tel{border-color:#3A3631;background:#3A3631}
.tel img{width:100%;height:100%;object-fit:cover;object-position:top;display:block;border-radius:4.5mm}
.aneis{display:grid;grid-template-columns:repeat(4,1fr);gap:2mm}
.anel{position:relative;text-align:center}
.anel svg{width:100%;max-width:17mm;display:block;margin:0 auto;transform:rotate(-90deg)}
.anel .trilho{fill:none;stroke:rgba(128,120,110,.22);stroke-width:6}
.anel .arco{fill:none;stroke-width:6;stroke-linecap:round}
.anel b{position:absolute;top:0;left:0;right:0;height:17mm;display:flex;align-items:center;justify-content:center;font:700 12pt/1 var(--num)}
.lado.nosso .anel b{filter:brightness(1.35)}
.anel span{display:block;font-size:6.5pt;line-height:1.15;margin-top:1mm;letter-spacing:.02em}
.tempos{display:grid;gap:1.6mm;font-size:8pt}
.tempos div{display:flex;justify-content:space-between;border-top:1px dashed rgba(128,120,110,.35);padding-top:1.4mm}
.tempos b{font:700 9pt/1 var(--num)}
table.chk{width:100%;border-collapse:collapse;font-size:10pt}
table.chk td{padding:2.4mm 0;border-bottom:1px solid var(--linha);vertical-align:middle}
table.chk td.r{text-align:right;width:20mm}
.pill{display:inline-block;min-width:13mm;text-align:center;padding:3px 7px 2px;border-radius:20px;font:700 7.5pt/1.2 var(--corpo);letter-spacing:.06em;text-transform:uppercase}
.pill.s{background:#E3F0E9;color:var(--bom)}.pill.n{background:#F7E1DD;color:var(--mau)}
.numeros{display:grid;grid-template-columns:repeat(4,1fr);gap:3mm;margin:6mm 0 7mm}
.numeros div{border:1px solid var(--linha);border-radius:5px;padding:3.5mm;background:#fff}
.numeros b{display:block;font:700 15pt/1 var(--num);margin-bottom:1.5mm}
.numeros span{font-size:7.5pt;color:var(--cinza);line-height:1.25;display:block}
.numeros i{font-style:normal;font:500 7.5pt/1 var(--num);color:var(--bom);display:block;margin-top:1.5mm}
.vit{display:grid;gap:4mm;margin-bottom:7mm}
.v{display:grid;grid-template-columns:11mm 1fr;gap:3mm;border:1px solid var(--linha);border-radius:6px;background:#fff;padding:4mm}
.v .n{font:400 22pt/1 var(--display);color:var(--laranja)}
.v h3{font:700 11.5pt/1.2 var(--corpo);margin-bottom:2mm}
.v dl{display:grid;grid-template-columns:24mm 1fr;gap:1.2mm 3mm;font-size:9pt}
.v dt{font:700 7pt/1.6 var(--corpo);letter-spacing:.12em;text-transform:uppercase;color:var(--cinza)}
.v dd.g{font-weight:700;color:var(--bom)}
.clientes{background:var(--osso);border-radius:6px;padding:5mm;font-size:10pt;display:grid;gap:2mm}
.clientes .grande{font:700 12pt/1.35 var(--corpo)}
.fonte{font-size:7pt;color:var(--cinza)}
.cta{margin-top:auto;background:var(--carvao);color:var(--osso);border-radius:6px;padding:6mm;display:flex;justify-content:space-between;align-items:center;gap:6mm}
.cta h3{font:400 14pt/1.05 var(--display);text-transform:uppercase;margin-bottom:2mm}
.cta p{font-size:9.5pt;color:#CFC8BC;max-width:46ch}
.cta a{flex:none;background:var(--laranja);color:#fff;text-decoration:none;font:700 10pt/1 var(--corpo);padding:4mm 5mm;border-radius:4px;text-align:center}
.cta a small{display:block;font:500 8pt/1 var(--num);margin-top:1.5mm;opacity:.9}
.rodape{display:flex;justify-content:space-between;font-size:7pt;color:var(--cinza);margin-top:5mm;padding-top:3mm;border-top:1px solid var(--linha)}
.notas{font-size:9.5pt;display:grid;gap:3mm}
.notas pre{white-space:pre-wrap;font:400 9pt/1.45 var(--corpo);background:#fff;border:1px solid var(--linha);border-radius:5px;padding:4mm}
.notas h3{font:700 10pt/1 var(--corpo);margin-top:2mm}
"""


def logo_mini():
    return ('<svg viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="32" r="31" fill="#141210"/>'
            '<circle cx="32" cy="32" r="27" fill="none" stroke="#C9A256" stroke-width="1.6"/>'
            '<text x="32" y="43" text-anchor="middle" font-family="Archivo Black,sans-serif" font-size="30" fill="#E8622C">P</text></svg>')


def whatsapp(c):
    """Regra do PLAYBOOK: «sim» só com prova pública. Fixo (+40 2…/3…) não tem WhatsApp."""
    t = re.sub(r"\D", "", c.get("telefone", ""))
    return "não (fixo: ligar)" if t.startswith(("402", "403")) else "?"


def nome_curto(c):
    n = re.split(r"\s+[-|–]\s+|,|\(", c["nome"])[0].strip()
    return n if len(n) <= 40 else n[:38].rsplit(" ", 1)[0]


def mensagem_ro(c, slug):
    return (f"Bună ziua! Sunt Tomás, de la Pacheco Studios (Iași). Am văzut că {nome_curto(c)} are {c.get('nota')}★ pe Google, "
            f"așa că v-am făcut gratuit un audit al site-ului, măsurat pe telefon: viteza, ce găsește clientul și ce i-ar lipsi ca să vă sune. "
            f"Vi-l trimit aici în PDF (3 pagini). Dacă vreți, vă arăt în 20 de minute cum ar arăta site-ul refăcut. Mulțumesc!")


def apresentacao(slug, c, lang, cand_pt=False):
    L = T[lang]
    d = ler(slug)
    demo_slug, demo_nome = demo_para(c)
    dm = ler(f"demo-{demo_slug}")
    if not d or not dm:
        raise SystemExit(f"Faltam medições: {slug if not d else 'demo-' + demo_slug}")
    n, nd = d.get("notas") or {}, dm.get("notas") or {}
    data = (d.get("medido_em") or "")[:10]
    data_fmt = ".".join(reversed(data.split("-"))) if data else "?"
    aval = L["aval"].format(n=c["avaliacoes"]) if c.get("avaliacoes") else ""
    dom = urlparse(c["site"]).netloc.replace("www.", "")
    shot = os.path.join(DADOS, f"{slug}.jpg")
    shot_d = os.path.join(DADOS, f"demo-{demo_slug}.jpg")
    img = f'<img src="{b64img(shot)}" alt="">' if os.path.exists(shot) else ""
    img_d = f'<img src="{b64img(shot_d)}" alt="">' if os.path.exists(shot_d) else ""

    def lado(dd, nn, cls, titulo, sub, im):
        lcp, fcp, peso = seg(aud(dd, "largest-contentful-paint")), seg(aud(dd, "first-contentful-paint")), aud(dd, "total-byte-weight")
        return (f'<div class="lado {cls}"><div><h3>{titulo}</h3></div><p class="sub">{sub}</p>'
                f'<div class="tel">{im}</div><div class="aneis">' + "".join(anel(nn.get(k, 0), L["cats"][k]) for k in L["cats"]) + "</div>"
                f'<div class="tempos"><div><span>{L["fcp"]}</span><b>{fcp} s</b></div><div><span>{L["lcp"]}</span><b>{lcp} s</b></div>'
                f'<div><span>{L["peso"]}</span><b>{(peso or 0) / 1048576:.1f} MB</b></div></div></div>')

    topo = (f'<div class="topo"><span class="marca">{logo_mini()}Pacheco Studios</span><span>{L["titulo"]} · {html.escape(dom)}</span></div>')
    p1 = (f'<section class="folha">{topo}<span class="etiqueta">{L["gratis"]}</span>'
          f'<h1 style="font-size:{30 if len(nome_curto(c)) <= 18 else 24}pt">{html.escape(nome_curto(c))}</h1><p class="dominio">{html.escape(dom)}</p>'
          f'<p class="elogio">{L["elogio"].format(nota=c.get("nota"), aval=aval)}</p><p class="medido">{L["medido"].format(d=data_fmt)}</p>'
          f'<div class="duelo">{lado(d, n, "teu", L["hoje"], "", img)}{lado(dm, nd, "nosso", L["podia"], L["podia_sub"].format(demo=demo_nome) + ". " + L["nota_demo"], img_d)}</div>'
          f'<div class="rodape"><span>{L["nota_honesta"]}</span><span>{L["pag"]} 1/3</span></div></section>')

    chk = verificacoes(d, c)
    tabela = "".join(f'<tr><td>{L["chk"][k]}</td><td class="r"><span class="pill {"s" if ok else "n"}">{L["sim"] if ok else L["nao"]}</span></td></tr>' for k, ok in chk)
    lcp, lcp_d = seg(aud(d, "largest-contentful-paint")), seg(aud(dm, "largest-contentful-paint"))
    peso, peso_d = aud(d, "total-byte-weight") or 0, aud(dm, "total-byte-weight") or 0
    req, req_d = aud(d, "network-requests") or 0, aud(dm, "network-requests") or 0
    num = [(f"{n.get('performance', 0)}/100", L["cats"]["performance"], f"{nd.get('performance')} {('la noi' if lang == 'ro' else 'no nosso')}"),
           (f"{lcp} s", L["lcp"], f"{lcp_d} s {('la noi' if lang == 'ro' else 'no nosso')}"),
           (f"{peso / 1048576:.1f} MB", L["peso"], f"{peso_d / 1048576:.1f} MB {('la noi' if lang == 'ro' else 'no nosso')}"),
           (f"{req}", L["pedidos"], f"{req_d} {('la noi' if lang == 'ro' else 'no nosso')}")]
    numeros = "".join(f"<div><b>{a}</b><span>{b}</span><i>{c_}</i></div>" for a, b, c_ in num)
    vs = vitorias(d, c, dm, L)[:3]
    vit = "".join(f'<div class="v"><div class="n">{i}</div><div><h3>{html.escape(t)}</h3><dl><dt>{L["g_hoje"]}</dt><dd>{html.escape(h)}</dd>'
                  f'<dt>{L["g_muda"]}</dt><dd>{html.escape(m)}</dd><dt>{L["g_ganha"]}</dt><dd class="g">{html.escape(g)}</dd></dl></div></div>'
                  for i, (t, h, m, g) in enumerate(vs, 1))
    pct = next((p for lim, p in GOOGLE_ABANDONO if lcp and lcp >= lim), None)
    lim = next((lim for lim, p in GOOGLE_ABANDONO if lcp and lcp >= lim), None)
    p_ = (d.get("pagina") or {})
    passos = L["passos_sem"] if not p_.get("tel") else (L["passos_long"] if not p_.get("tel_no_1o_ecra") else None)
    linhas = []
    if pct:
        linhas.append(f'<p class="grande">{L["abandono"].format(x=lim, p=pct)}</p><p>{L["teu_lcp"].format(x=lcp)} {L["nosso_lcp"].format(y=lcp_d)}</p>'
                      f'<p class="fonte">{L["fonte"]}: {FONTE_GOOGLE}.</p>')
    else:
        linhas.append(f'<p class="grande">{L["abandono_ok"].format(x=lcp)}</p>')
    if passos:
        linhas.append(f"<p>{L['passos'].format(a=passos)}</p>")
    p2 = (f'<section class="folha">{topo}<h2>{L["achados"]}</h2><div class="numeros">{numeros}</div>'
          f'<table class="chk">{tabela}</table>'
          f'<h2 style="margin-top:8mm">{L["clientes"]}</h2><div class="clientes">{"".join(linhas)}</div>'
          f'<div class="rodape" style="margin-top:auto"><span>{L["nota_honesta"]}</span><span>{L["pag"]} 2/3</span></div></section>')

    p3 = (f'<section class="folha">{topo}<h2>{L["ganhos"]}</h2><p style="margin:-2mm 0 5mm;color:var(--cinza)">{L["ganhos_sub"]}</p>'
          f'<div class="vit">{vit}</div>'
          f'<div class="cta"><div><h3>{L["cta_t"]}</h3><p>{L["cta"]}</p></div><a href="{WA_LINK}">{L["cta_wa"]}<small>{WHATSAPP_RO}</small></a></div>'
          f'<div class="rodape"><span>{L["assin"]}</span><span>{L["pag"]} 3/3</span></div></section>')

    p4 = ""
    if cand_pt:
        wa = whatsapp(c)
        p4 = (f'<section class="folha">{topo}<h2>Notas para o Tomás</h2><div class="notas">'
              f'<p><b>{html.escape(c["nome"])}</b> · {html.escape(c.get("categoria", ""))} · {html.escape(c.get("morada", "") or "morada a confirmar")}</p>'
              f'<p>Telefone {html.escape(c.get("telefone", ""))} · WhatsApp: {wa}  · Google {c.get("nota")}{" · " + c["avaliacoes"] + " avaliações" if c.get("avaliacoes") else ""}</p>'
              f'<p>Fraqueza {fraqueza(d, c)}/100 · demo de comparação: {demo_nome} (pachecost.com/demo/{demo_slug}/)</p>'
              f'<h3>Mensagem (RO), mandar com o PDF romeno</h3><pre>{html.escape(mensagem_ro(c, slug))}</pre>'
              f'<h3>PDF para o dono</h3><pre>{RAW}/{slug}/auditie-{slug}-ro.pdf</pre>'
              f'<h3>Na reunião (20 min)</h3><pre>1. Abrir o site deles no telemóvel deles e cronometrar.\n2. Mostrar a demo {demo_nome} ao lado.\n'
              f'3. Perguntar: quantas visitas tem o site por mês (Google Business Profile → Desempenho) e quanto vale um cliente novo. '
              f'Com esses dois números faz-se a conta à frente dele.\n4. Proposta só do site, em RON (regra de Iași).</pre></div>'
              f'<div class="rodape"><span>Interno · não enviar</span><span>4/4</span></div></section>')

    titulo = f'{L["titulo"]} · {c["nome"]}'
    return (f'<!doctype html><html lang="{L["lang"]}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<meta name="robots" content="noindex"><title>{html.escape(titulo)}</title>'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Archivo:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">'
            f'<style>{CSS}</style></head><body>{p1}{p2}{p3}{p4}</body></html>')


def pdf(html_path, pdf_path):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("  (sem playwright: só HTML)")
        return False
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=os.environ.get("CHROMIUM") or None)
        pg = b.new_page()
        pg.goto("file://" + html_path, wait_until="networkidle")
        pg.pdf(path=pdf_path, format="A4", print_background=True, margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
        b.close()
    return True


def gerar(slug, cands):
    c = cands[slug]
    pasta = os.path.join(SAIDA, slug)
    os.makedirs(pasta, exist_ok=True)
    for lang, nome, pt in (("ro", f"auditie-{slug}-ro", False), ("pt", f"auditoria-{slug}-pt", True)):
        h = os.path.join(pasta, nome + ".html")
        open(h, "w", encoding="utf-8").write(apresentacao(slug, c, lang, cand_pt=pt))
        pdf(h, os.path.join(pasta, nome + ".pdf"))
    print("ok", slug)


def mensagem_morto(c):
    dom = urlparse(c["site"]).netloc.replace("www.", "")
    return (f"Bună ziua! Sunt Tomás, de la Pacheco Studios (Iași). Am văzut că {c['nome']} are {c.get('nota')}★ pe Google. "
            f"Vă scriu pentru că linkul de site din profilul vostru Google ({dom}) nu se mai deschide: cine apasă pe el ajunge la o eroare. "
            f"Dacă vreți, vă arăt în 20 de minute un site nou pentru voi, gata de pus în loc. Mulțumesc!")


def escrever_envio(escolhidos, cands):
    data = datetime.date.today().strftime("%d/%m/%Y")
    out = [f"# Agente 3 · auditorias para enviar ({data})", "",
           "Mandar pelo WhatsApp Business RO: mensagem + PDF romeno (link raw abaixo, descarrega no telemóvel). "
           "WhatsApp dos donos: «?» nos telemóveis (sem prova pública), «não» nos fixos. Se a mensagem não entregar, ligar ou visitar com a morada; nos fixos, ligar e pedir um WhatsApp ou e-mail para mandar o PDF.", ""]
    for i, s in enumerate(escolhidos, 1):
        c = cands[s]
        out += [f"## {i}. {c['nome']} · {c.get('categoria', '')}", "",
                f"- Telefone {c.get('telefone')} · WhatsApp: {whatsapp(c)} · Google {c.get('nota')}{' · ' + c['avaliacoes'] + ' avaliações' if c.get('avaliacoes') else ''}",
                f"- Morada: {c.get('morada') or 'a confirmar'} · site {c['site']}",
                f"- PDF RO (dono): {RAW}/{s}/auditie-{s}-ro.pdf",
                f"- PDF PT (Tomás): {RAW}/{s}/auditoria-{s}-pt.pdf", "", "```", mensagem_ro(c, s), "```", ""]
    mortos = [(s, c) for s, c in cands.items() if (ler(s) or {}).get("erro_pagina") and not (ler(s) or {}).get("notas")]
    if mortos:
        out += ["## Sites que já não abrem (o Google manda os clientes para um erro)", "",
                "O link do site na ficha Google dá erro (o domínio não existe). É o argumento mais forte: não precisa de PDF.", ""]
        for s, c in mortos:
            out += [f"### {c['nome']} · {c.get('categoria', '')}", "",
                    f"- Telefone {c.get('telefone')} · WhatsApp: {whatsapp(c)} · Google {c.get('nota')} · morada {c.get('morada') or 'a confirmar'}",
                    f"- Erro medido: {(ler(s).get('erro_pagina') or '').splitlines()[0][:120]}", "", "```", mensagem_morto(c), "```", ""]
    open(os.path.join(SAIDA, "ENVIAR.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")


def main():
    cands = ler_candidatos()
    a = sys.argv[1:]
    if not a or a[0] == "ranking":
        for i, (fr, slug, c, d, n) in enumerate(escrever_ranking(cands)[:25], 1):
            print(i, fr, slug, n.get("performance"), c.get("nota"))
        return
    if a[0] == "--top":
        k = int(a[1])
        escolhidos = [s for fr, s, c, d, n in escrever_ranking(cands) if s not in EXCLUIR and nota_num(c) >= 4.4 and d.get("notas") and aud(d, "largest-contentful-paint") is not None][:k]
    else:
        escolhidos = a
    for s in escolhidos:
        gerar(s, cands)
    if a[0] == "--top":
        escrever_envio(escolhidos, cands)


if __name__ == "__main__":
    main()
