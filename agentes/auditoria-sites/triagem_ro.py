#!/usr/bin/env python3
"""Agente 3 · Triagens Iași (RO), no formato das triagens PT (triagem_pt.py) e da do Iulian Paraschiv.

Pedido do Tomás (14/10/2026): «Prepara 10 agora negócios romenos para enviar triagem, mesmo estilo, mesma perspicácia».
Mesmas regras do lote PT: só fisioterapia, clínicas e estética, só com WhatsApp provado no próprio site (wa.me / api.whatsapp
com número), lido pela ponte; sinais só do que se vê de fora; nunca propor o que o negócio já tem; a vertente escolhida é a
primeira execução, paga, com valor fechado na reunião; sem preço, sem minutos. Mensagem no molde aprovado dos e-mails RO
(personalização do site, quem somos + o que entregamos, sede em Portugal + Portugal e Brasil + pesquisa sobre a economia
romena, reunião com o dono, «Voi fi pregătit.», ro.pachecost.com, «Sunt în Iași»). Nunca «já trabalhamos na Roménia».

  python3 triagem_ro.py   → raio-x/triagens-ro/<slug>/triagem-<slug>.pdf e raio-x/ENVIAR-RO-triagens-lote-1.md
"""
import datetime, html as H, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gerar import RAIZ, RAMO, ler_candidatos, pdf
from triagem_pt import CSS, FONTES

SAIDA = os.path.join(RAIZ, "raio-x", "triagens-ro")
RAW = f"https://github.com/tspacheco/Designerpacheco/raw/{RAMO}/raio-x/triagens-ro"
OU = "Sau, dacă preferați:"
PROX = ("Pasul următor: alegeți una dintre aceste direcții ca primă execuție. O construim și o măsurăm din prima săptămână; "
        "este o lucrare plătită, cu valoarea stabilită la reuniune. Dacă rezultatul apare, continuăm împreună cu următoarele."
        '<span class="lema">Ce livrăm: scurgerea găsită, sistemul proiectat, impactul dovedit în cifre.</span>')

from triagem_ro_dados import NEG, CURTO, PERSONAL, PT  # noqa: E402

ORDEM = list(NEG)
ASSINA = "Tomás Pacheco · Pacheco Studios · ro.pachecost.com · Sunt în Iași"


def nome(slug, c):
    return NEG[slug].get("nome") or c["nome"]


def pagina(slug, c):
    t = NEG[slug]
    sinais = "".join(f"<li><b>{H.escape(a)}</b>{H.escape(b)}</li>" for a, b in t["sinais"])
    etapas = "".join(f'<div><i>0{i+1}</i><b>{H.escape(a)}</b><span>{H.escape(b)}</span><em><strong>{OU}</strong> {H.escape(x)}</em></div>'
                     for i, (a, b, x) in enumerate(t["etapas"]))
    qw = "".join(f"<div><i>0{i+1}</i><b>{H.escape(a)}</b><span>{H.escape(b)}</span></div>" for i, (a, b) in enumerate(t["qw"]))
    perg = "".join(f"<li>{H.escape(x)}</li>" for x in t["perg"])
    met = "".join(f"<li>{H.escape(x)}</li>" for x in t["met"])
    n = H.escape(nome(slug, c))
    return f"""<!doctype html><html lang="ro"><head><meta charset="utf-8"><title>Triaj · {n}</title>
<style>{FONTES}{CSS}</style></head><body><section class="pag">
<div class="topo"><div class="l1"><span class="marca">Pacheco Studios<i></i></span><span class="mono">Octombrie 2026</span></div>
<span class="mono sup">Triaj · Micro System Print</span><h1>{n}<br><em>{H.escape(t['sub'])}</em></h1>
<p class="aviso">Nu este un diagnostic al afacerii sau al site-ului dumneavoastră: este infrastructura de primire pe care am construi-o noi, Pacheco Studios, eficientă la fiecare pas. Fiecare echipă lucrează în felul ei; alegeți ce vi se potrivește.</p></div>
<div class="corpo">
<div><h3>Ce se vede din afară</h3><ul class="sinais">{sinais}</ul></div>
<div><h3>Drumul Pacheco Studios, pas cu pas</h3><div class="etapas">{etapas}</div></div>
<div><h3>Cele 3 sugestii ale noastre</h3><div class="qw">{qw}</div><p class="alt">{H.escape(t['alt'])}</p></div>
<div class="duas"><div><h3>3 întrebări pentru dumneavoastră</h3><ol>{perg}</ol></div><div><h3>Ce măsurăm</h3><ul>{met}</ul></div></div>
<div class="prox">{PROX}</div>
</div><footer class="rod"><span class="marca">Pacheco Studios<i></i></span><span>Tomás Pacheco · +40 723 098 556 · ro.pachecost.com</span></footer>
</section></body></html>"""


def mensagem(slug):
    n = CURTO[slug]
    return (f"Bună ziua,\n\n{PERSONAL[slug]}\n\n"
            "Sunt Tomás Pacheco, de la Pacheco Studios. Facem audit de sisteme cu IA pentru afaceri locale. "
            "Ce livrăm: găsim unde afacerea pierde clienți și timp, proiectăm sistemul care oprește această scurgere și dovedim impactul în cifre.\n\n"
            "Avem sediul în Portugalia și lucrăm în Portugalia și Brazilia. Pe baza cercetării noastre despre economia României, "
            "am identificat o oportunitate în oferta locală, pe care vrem s-o abordăm acum din Iași, începând cu clinicile de sănătate "
            "și estetică, unde fiecare cerere de programare contează. Fiecare proiect pornește de la un câștig rapid, măsurabil, "
            "înainte de orice investiție mai mare.\n\n"
            f"Am pregătit pe o pagină drumul unui pacient la {n}, de la primul contact la următoarea vizită, și ce am construi "
            "la fiecare pas. O găsiți atașată.\n\n"
            f"Aș vrea o reuniune cu dumneavoastră, să vă arăt ce am observat la {n} și ce putem face concret. "
            "Spuneți-mi ce zi vă convine.\n\nVoi fi pregătit.\n\n" + ASSINA)


def seguimentos(slug):
    n = CURTO[slug]
    return {
     "d3": f"Bună ziua, revin pe scurt. Ce livrăm: găsim unde se pierd clienți și timp, proiectăm sistemul care rezolvă asta și "
           f"dovedim impactul în cifre. Aș vrea să vă arăt, într-o reuniune, ce am observat la {n}. {ASSINA}",
     "d7": f"Bună ziua, o singură întrebare, da sau nu: v-ar conveni o reuniune cu mine, săptămâna aceasta sau săptămâna viitoare, "
           f"ca să vă arăt ce am observat la {n}? {ASSINA}",
     "d12": f"Bună ziua, închid aici discuția despre {n}, ca să nu vă deranjez. Dacă într-o zi vreți să vedeți ce am observat, "
            f"îmi scrieți. Voi fi pregătit. {ASSINA}",
    }


def main():
    cands = ler_candidatos()
    data = datetime.date.today().strftime("%d/%m/%Y")
    out = [f"# Agente 3 · Triagens Iași para enviar ({data})", "",
           "Mesmo formato das triagens PT (1 página, caminho Pacheco Studios em 6 passos com «Sau, dacă preferați», 3 sugestões, "
           "3 perguntas, o que medimos). Só negócios com WhatsApp provado no próprio site. Não sai grátis: a vertente escolhida é a "
           "primeira execução, paga, com valor fechado na reunião. Mensagem no molde aprovado dos e-mails RO (13/10); o PDF vai "
           "anexado, nunca link. Cada secção tem, em PT, o que a mensagem cita do site.", ""]
    for i, s in enumerate(ORDEM, 1):
        c = cands[s]
        pasta = os.path.join(SAIDA, s)
        os.makedirs(pasta, exist_ok=True)
        h = os.path.join(pasta, f"triagem-{s}.html")
        open(h, "w", encoding="utf-8").write(pagina(s, c))
        pdf(h, h[:-5] + ".pdf")
        out += [f"## {i}. {nome(s, c)} · {c.get('categoria', '')}", "",
                f"- Telefone {c['telefone']} · WhatsApp: sim (no site) · Google {c['nota']} · {c['avaliacoes']} avaliações",
                f"- Morada: {c['morada']} · site {c['site']}",
                f"- Em PT: {PT[s]}",
                f"- PDF RO (dono): {RAW}/{s}/triagem-{s}.pdf", "", "```", mensagem(s), "```", ""]
        out += ["Seguimentos (sem resposta; mesmo WhatsApp, sem novo PDF):", ""] + [f"- {k.upper()}: {v}" for k, v in seguimentos(s).items()] + [""]
        print("ok", s)
    open(os.path.join(RAIZ, "raio-x", "ENVIAR-RO-triagens-lote-1.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
