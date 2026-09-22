#!/usr/bin/env python3
"""Doris & Cia — apresentação para a cliente: o que encontramos + 3 pacotes. PT-BR."""
import sys, pathlib
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "be-legend-olhao"))
import build as B
from build import esc, NAVY, GOLD, TEAL, LINE, MUTED, INK, PAPER
from build_checklist import diag, C, page as _page, cb, S, r, CPC, AGENDA, TICKET, RECOR
import funil as FN

def page(cls, inner, num=None, footer=True):
    ft = f'<footer class="ft"><span>{esc(C["marca"])} · Proposta · {esc(C["cliente"])}</span><span>{num or ""}</span></footer>' if footer else ""
    return f'<section class="page {cls}">{inner}{ft}</section>'
def h(kicker, title, lead=None):
    out = f'<p class="kicker">{kicker}</p><h2>{title}</h2>'
    if lead: out += f'<p class="lead">{lead}</p>'
    return out

PK = [
 dict(nome="Base", setup="R$ 3.000", mensal="R$ 200", cor=NAVY, tag="arrumar a casa",
      frase="Para ser encontrada, responder bem e não esquecer nenhum cliente. O essencial, com o fluxo automático já ligado.",
      inc=["Ficha do Google corrigida: categoria, descrição, horário, serviços, 20 fotos e vídeo",
           "Pedido de avaliação com mensagem pronta e link direto (meta: 30 em 60 dias)",
           "Um Instagram principal: bio nova, destaques, botão de WhatsApp",
           "WhatsApp Business montado: catálogo de serviços, boas-vindas, fora do horário, etiquetas",
           "Oferta de entrada definida com a Doris",
           "Fluxo automático no WhatsApp: pedido de avaliação 2 h depois do banho e lembrete de banho aos 15 dias",
           "Site de uma página com botão de WhatsApp (extra, já pronto)"],
      mes=["Fluxo automático a funcionar e vigiado", "Site no ar, domínio e hospedagem", "Ficha do Google e Instagram mantidos", "Suporte pelo WhatsApp e relatório mensal"]),
 dict(nome="Crescimento", setup="R$ 5.000", mensal="R$ 400", cor=TEAL, tag="trazer clientes", destaque=True,
      frase="Tudo do Base, mais anúncios geridos e o agendamento que funciona sozinho.",
      inc=["Tudo do pacote Base",
           "Agendamento online ligado ao WhatsApp e ao calendário, com confirmação e lembrete automáticos",
           "Ficha de cliente (tutor, pet, porte, serviço, data) pronta a usar",
           "Anúncios no Instagram e Facebook: campanhas montadas, 3 vídeos editados, segmentação a 3 km",
           "Fluxo automático ampliado: recuperação de quem sumiu (30 dias sem vir → 3 mensagens com o nome do pet e uma oferta)"],
      mes=["Tudo do Base", "Gestão dos anúncios com relatório toda segunda-feira", "Ajustes de oferta e criativos", "Automações a funcionar e vigiadas"]),
 dict(nome="Completo", setup="R$ 8.000", mensal="R$ 900", cor=GOLD, tag="crescer e fidelizar",
      frase="Tudo do Crescimento, mais recuperação de clientes, conteúdo e números na mão.",
      inc=["Tudo do pacote Crescimento",
           "Fluxo automático completo: lembretes de saúde (vermífugo, antipulgas) e aniversário do pet, com produto da loja",
           "Plano mensal de banho e pacote pré-pago montados, com cobrança e agenda fixa",
           "Catálogo da loja no WhatsApp: ração e acessórios para pedir e buscar",
           "Painel de números: conversas, agendados, compareceram, voltaram"],
      mes=["Tudo do Crescimento", "4 vídeos por mês roteirizados e editados", "Ofertas trocadas a cada trimestre", "Assistência prioritária"]),
]

pages = []
pages.append(page("cover", f'''
<div class="cover-top"><span class="brand">{esc(C["marca"])}</span><span class="mono">{esc(C["data"])}</span></div>
<div class="cover-mid">
  <p class="cover-kicker">Proposta · {esc(C["cliente"])}</p>
  <h1>O que vimos.<br>O que propomos.</h1>
  <p class="cover-client">{esc(C["bairro"])} · {esc(C["cidade"])}</p>
  <p class="cover-sub">O que R$ 400, R$ 800 ou R$ 1.500 por mês em anúncios podem trazer para a loja, oito coisas que hoje afastam clientes sem ninguém perceber, e três pacotes para resolver.</p>
</div>
<div class="cover-bot">
  <div class="cover-stat"><b>R$ 800</b><span>por mês em anúncios: cerca de 35 clientes novos por mês</span></div>
  <div class="cover-stat"><b>8</b><span>pontos a corrigir no Google e no Instagram</span></div>
  <div class="cover-stat"><b>3</b><span>pacotes com fluxo automático e site incluídos</span></div>
</div>
<div class="cover-rule"></div>
<p class="cover-foot">Documento de apresentação · leitura em 5 minutos</p>
''', footer=False))

pages.append(FN.pagina(page, h, C))

def bars():
    W,H=1000,230; ks=[400,800,1500]; mx=max(S[k]["m6"] for k in ks)
    o=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">']
    gw=W/3
    for i,k in enumerate(ks):
        x0=i*gw+40; s_=S[k]
        hf=(s_["m6"]/mx)*150; hi=(s_["custo6"]/mx)*150
        o.append(f'<rect x="{x0}" y="{170-hi}" width="90" height="{hi}" rx="6" fill="#D6D0C2"/>')
        o.append(f'<text x="{x0+45}" y="{162-hi}" text-anchor="middle" font-family="JetBrains Mono" font-size="11" fill="{MUTED}">{r(s_["custo6"])}</text>')
        o.append(f'<rect x="{x0+110}" y="{170-hf}" width="90" height="{hf}" rx="6" fill="{TEAL}"/>')
        o.append(f'<text x="{x0+155}" y="{162-hf}" text-anchor="middle" font-family="Barlow Condensed" font-weight="700" font-size="16" fill="{TEAL}">{r(s_["m6"])}</text>')
        o.append(f'<text x="{x0+100}" y="196" text-anchor="middle" font-family="Barlow Condensed" font-weight="700" font-size="17" fill="{NAVY}">Nível {i+1} · {r(k)}/mês</text>')
        o.append(f'<text x="{x0+100}" y="216" text-anchor="middle" font-family="Inter" font-size="11" fill="{MUTED}">investimento em 6 meses vs faturamento em 6 meses</text>')
    o.append("</svg>"); return "".join(o)

def trow(i,k):
    s_=S[k]; roi=s_["m6"]/s_["custo6"]
    return f'<tr><td class="lab">Nível {i}</td><td>{r(k)}</td><td>{s_["conv"]:.0f}</td><td>{s_["novos"]:.0f}</td><td>{r(s_["cpa"])}</td><td>{r(s_["m1"])}</td><td class="hl">{r(s_["m6"])}</td><td>{roi:.0f}×</td></tr>'
pages.append(page("", h("02 · O potencial", "O que cada nível de anúncio pode trazer para a loja.", "Anúncios no Instagram e no Facebook, num raio de 3 km em volta da loja, para tutores de cães e gatos. Cada conversa chega no WhatsApp da Doris & Cia. Os números abaixo são uma projeção com premissas à vista; o piloto de 45 dias troca-os por números reais.") + f'''
<table class="tbl num2">
  <thead><tr><th></th><th>Investimento por mês</th><th>Conversas</th><th>Clientes novos</th><th>Custo por cliente</th><th>Faturamento 1.º mês</th><th class="hl">Faturamento em 6 meses</th><th>Retorno</th></tr></thead>
  <tbody>{trow(1,400)}{trow(2,800)}{trow(3,1500)}</tbody>
</table>
<div class="bars">{bars()}</div>
<div class="grid3 prem">
  <div class="tile sm"><b>{AGENDA*100:.0f} %</b><span>taxa de conversão média final<br><em>de cada 100 conversas no WhatsApp, {AGENDA*100:.0f} viram atendimento pago; já desconta quem agenda e não aparece</em></span></div>
  <div class="tile sm"><b>R$ {TICKET:.0f}</b><span>faturamento médio por atendimento<br><em>banho e tosa, misto de portes; tabelas de 2026 da Grande São Paulo</em></span></div>
  <div class="tile sm"><b>{RECOR*100:.0f} %</b><span>dos clientes novos voltam todo mês<br><em>com o lembrete automático de banho, incluído em todos os pacotes</em></span></div>
</div>
<p class="fine">Custo por conversa iniciada de R$ {CPC:.0f} (faixa de R$ 5 a R$ 12 em serviços locais). “Faturamento em 6 meses” soma cada mês de clientes novos com os que continuam voltando. “Retorno” é faturamento dividido pelo investimento em anúncios no período. Não inclui venda de ração e acessórios, que costuma vir junto com o banho.</p>
<div class="callout"><b>O que isto quer dizer:</b> com R$ 800 por mês em anúncios, a loja pode ganhar cerca de {S[800]["novos"]:.0f} clientes novos por mês e faturar perto de {r(S[800]["m6"])} em seis meses, gastando {r(S[800]["custo6"])}. Isso só acontece se a ficha do Google, o Instagram e o WhatsApp estiverem prontos para receber essa gente. É o que a página seguinte mostra.</div>
''', 3))

rows = "".join(f'<tr><td><span class="sev {s}">{s}</span></td><td><b>{esc(a)}</b><br><span class="small">{esc(b)}</span></td><td>{esc(c)}</td></tr>' for a, b, c, s in diag)
pages.append(page("", h("03 · O que encontramos", "Oito pontos que afastam clientes hoje.", "Levantamento feito só com o que está público: a ficha do Google e o Instagram. A boa notícia: os mais graves são os mais rápidos de resolver.") + f'''
<table class="tbl diag">
  <thead><tr><th>Peso</th><th>O que encontramos</th><th>O que fazer</th></tr></thead>
  <tbody>{rows}</tbody>
</table>
<div class="callout"><b>Em uma frase:</b> a Doris &amp; Cia faz um bom trabalho, mas quem procura “banho e tosa em Vila Barros” não a encontra, e quem encontra não tem como agendar sozinho. Os pacotes a seguir resolvem exatamente isso.</div>
''', 4))

def pcard(p):
    d = ' destaque' if p.get("destaque") else ''
    inc = "".join(f'<li>{esc(x)}</li>' for x in p["inc"])
    mes = "".join(f'<li>{esc(x)}</li>' for x in p["mes"])
    return f'''<div class="pk{d}" style="--c:{p["cor"]}">
  <span class="mono ptag">{esc(p["tag"])}</span>
  <h3>{esc(p["nome"])}</h3>
  <div class="price"><b>{esc(p["setup"])}</b><span>montagem, pagamento único</span></div>
  <div class="price m"><b>{esc(p["mensal"])}</b><span>por mês</span></div>
  <p class="pf">{esc(p["frase"])}</p>
  <h4>Montagem inclui</h4><ul class="ul tight">{inc}</ul>
  <h4>A mensalidade cobre</h4><ul class="ul tight">{mes}</ul>
</div>'''
pages.append(page("", h("04 · Três pacotes", "Do essencial ao completo. A Doris escolhe.", "Todos incluem o fluxo automático no WhatsApp e o site de uma página. Cada pacote contém o anterior. O que muda é até onde o fluxo vai e se há anúncios geridos.") + f'''
<div class="pks">{"".join(pcard(p) for p in PK)}</div>
<p class="fine">A verba dos anúncios (de R$ 400 a R$ 1.500 por mês, paga diretamente à Meta) não está incluída em nenhum pacote: é da loja e fica na conta da loja. As mensagens automáticas pelo WhatsApp têm um custo por conversa cobrado pela Meta, de centavos, também à parte.</p>
''', 5))

cmp_rows = [
 ("Ficha do Google corrigida e com avaliações", 1,1,1),
 ("Um Instagram, bio e destaques", 1,1,1),
 ("WhatsApp Business montado", 1,1,1),
 ("Site de uma página (extra)", 1,1,1),
 ("Fluxo automático: avaliação 2 h depois + lembrete aos 15 dias", 1,1,1),
 ("Agendamento online com confirmação e lembrete", 0,1,1),
 ("Ficha de cliente", 0,1,1),
 ("Anúncios geridos com relatório semanal", 0,1,1),
 ("Fluxo automático: recuperação de quem sumiu (3 mensagens)", 0,1,1),
 ("Fluxo automático: saúde e aniversário do pet", 0,0,1),
 ("Plano mensal e pacote pré-pago montados", 0,0,1),
 ("Catálogo da loja no WhatsApp", 0,0,1),
 ("4 vídeos por mês", 0,0,1),
 ("Painel de números", 0,0,1),
 ("Assistência prioritária", 0,0,1),
]
def mk(v): return '<td class="y">✓</td>' if v else '<td class="n">—</td>'
crows = "".join(f'<tr><td class="lab">{esc(a)}</td>{mk(b)}{mk(c)}{mk(d)}</tr>' for a,b,c,d in cmp_rows)
pages.append(page("", h("05 · Lado a lado", "O que entra em cada pacote.") + f'''
<table class="tbl cmp2">
  <thead><tr><th></th><th>Base<br><span class="mono">R$ 3.000 · R$ 200/mês</span></th><th class="hl">Crescimento<br><span class="mono">R$ 5.000 · R$ 400/mês</span></th><th>Completo<br><span class="mono">R$ 8.000 · R$ 900/mês</span></th></tr></thead>
  <tbody>{crows}</tbody>
</table>
<h3 class="mt">Como começamos</h3>
<ol class="ol tight">
  <li><b>Escolha do pacote</b> e do nível de anúncios (R$ 400, R$ 800 ou R$ 1.500 por mês).</li>
  <li><b>Semana 1:</b> Google corrigido, um Instagram, WhatsApp Business montado. Já dá para sentir a diferença.</li>
  <li><b>Semana 2:</b> oferta definida, site no ar, agendamento e automações ligados, vídeos gravados.</li>
  <li><b>Semana 3:</b> anúncios no ar. Relatório toda segunda-feira.</li>
  <li><b>Dia 45:</b> revisão com números reais e ajustes.</li>
</ol>
<div class="note"><b>Em qualquer pacote:</b> nada sai sem a Doris aprovar. Mensagens, fotos, ofertas e anúncios passam por ela antes. E se alguma parte tiver de funcionar de outro jeito, ajustamos.</div>
<div class="callout final">
  <div><b>{esc(C["marca"])}</b><br><span>Web design e sistemas para negócios locais</span></div>
  <div class="r"><span class="mono">{esc(C["tel"])}</span><br><span class="mono">{esc(C["email"])}</span></div>
</div>
''', 6))

EXTRA = f"""
.tbl.num2 td,.tbl.num2 th{{text-align:right;padding:6px 7px;font-size:9.2pt}}
.tbl.num2 td.lab,.tbl.num2 th:first-child{{text-align:left}}
.tbl.num2 td{{font-family:'JetBrains Mono',monospace}}
.tbl.num2 td.lab{{font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:12pt;color:var(--navy);white-space:nowrap}}
.tbl.num2 th.hl,.tbl.num2 td.hl{{background:#F2F8F7;color:var(--teal);font-weight:700}}
.bars{{margin:10px 0 4px}} .bars svg{{width:100%;height:auto}}
.prem .tile.sm b{{font-size:20pt;color:var(--navy)}} .prem .tile.sm span{{font-size:9pt}} .prem .tile.sm em{{font-size:7.4pt}}
.prem{{margin-top:6px}}
.tbl.diag td{{padding:6px 8px;font-size:9.1pt;vertical-align:top;line-height:1.35}}
.tbl.diag td:first-child{{width:16mm}} .tbl.diag td:nth-child(2){{width:76mm}}
.sev{{display:inline-block;font-family:'JetBrains Mono',monospace;font-size:8pt;padding:2px 7px;border-radius:10px;text-transform:uppercase;letter-spacing:.04em}}
.sev.grave{{background:#F7E0E0;color:#8A2B2B}} .sev.alto{{background:#FBF3E1;color:#7A5A12}} .sev.médio{{background:#EEF0F4;color:var(--navy)}}
.callout{{margin-top:12px}}
.pks{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:8px}}
.pk{{border:1.5px solid #EAE5DA;border-radius:12px;padding:14px 13px 12px;background:#fff;position:relative}}
.pk.destaque{{border-color:var(--c);box-shadow:0 8px 24px -12px rgba(31,122,109,.35)}}
.pk.destaque::after{{content:"mais escolhido";position:absolute;top:-9px;right:12px;background:var(--c);color:#fff;font-family:'JetBrains Mono',monospace;font-size:7.5pt;padding:2px 8px;border-radius:10px}}
.ptag{{color:var(--c);display:block;margin-bottom:2px}}
.pk h3{{font-size:20pt;margin-bottom:6px;color:var(--navy)}}
.price b{{display:block;font-family:'Barlow Condensed',sans-serif;font-weight:800;font-size:26pt;line-height:1;color:var(--navy)}}
.price span{{font-size:8pt;color:var(--muted)}}
.price.m{{margin-top:6px}} .price.m b{{font-size:19pt;color:var(--c)}}
.pf{{font-size:9pt;color:#3A3F4B;margin:8px 0 6px;line-height:1.35}}
.pk h4{{font-family:'JetBrains Mono',monospace;font-weight:500;font-size:7.5pt;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:8px 0 3px}}
.pk .ul.tight li{{font-size:8.5pt;margin-bottom:3px;line-height:1.3;padding-left:12px}}
.pk .ul.tight li::before{{width:5px;height:5px;top:5px;background:var(--c)}}
.tbl.cmp2 th{{text-align:center;font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:13pt;text-transform:none;letter-spacing:0;color:var(--navy);padding:6px}}
.tbl.cmp2 th:first-child{{text-align:left}}
.tbl.cmp2 th .mono{{display:block;font-size:8pt;margin-top:2px}}
.tbl.cmp2 th.hl{{background:#F2F8F7;color:var(--teal)}}
.tbl.cmp2 td{{padding:5px 8px;font-size:9.4pt;text-align:center}}
.tbl.cmp2 td.lab{{text-align:left}}
.tbl.cmp2 td.y{{color:var(--teal);font-weight:700}} .tbl.cmp2 td.n{{color:#C9C6D0}}
.tbl.cmp2 td:nth-child(3){{background:#F2F8F7}}
.ol.tight li{{font-size:9.6pt;margin-bottom:5px}}
.callout.final{{margin-top:10px;padding:11px 16px}}
.callout.final .r{{text-align:right;white-space:nowrap}}
.note{{margin-top:8px}}
h1{{font-size:64pt}}
"""
EXTRA = EXTRA + FN.EXTRA

doc = f"""<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="utf-8"><title>Proposta · {esc(C["cliente"])}</title>
<style>{B.CSS}{EXTRA}</style></head><body>{''.join(pages)}</body></html>"""
(HERE / "apresentacao.html").write_text(doc, encoding="utf-8")
print("apresentacao.html", len(doc)//1024, "KB")
