#!/usr/bin/env python3
"""Doris & Cia Pet Shop (Guarulhos) — checklist de impulso para a reunião. PT-BR.
Reutiliza CSS/fontes de ../be-legend-olhao/build.py.
Render: NODE_PATH=$(npm root -g) node ../be-legend-olhao/render.js  → ver render abaixo."""
import sys, pathlib
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "be-legend-olhao"))
import build as B
from build import esc, NAVY, GOLD, TEAL, LINE, MUTED, INK, PAPER

C = dict(
    cliente="Doris & Cia Pet Shop", bairro="Vila Barros", cidade="Guarulhos · SP",
    morada="R. Alecsander Alves, 162 · Vila Barros · Guarulhos · SP · 07193-240",
    wa="11 97827-7667", ig1="@doriseciapetshop", ig2="@thaispetcare",
    data="Setembro 2026", marca="Pacheco Studios", email="tspacheco26@gmail.com", tel="+351 967 117 357",
)

# ---------- modelo de anúncios (premissas explícitas) ----------
CPC = 8.0        # R$ por conversa iniciada no WhatsApp (faixa 5–12 em serviços locais)
AGENDA = 0.35    # taxa de conversão média final: conversa no WhatsApp → atendimento pago (já desconta quem agenda e não aparece)
TICKET = 80.0     # R$ ticket médio (banho + tosa, misto de portes; tabelas 2026 da Grande SP)
RECOR = 0.40     # clientes novos que voltam todo mês
def cen(budget, eff=1.0):
    conv = budget / CPC * eff
    novos = conv * AGENDA
    m1 = novos * TICKET
    # 6 meses: cada coorte mensal de novos, 40% recorrem mensalmente
    total6 = sum(novos * TICKET * (1 + RECOR * (5 - i)) for i in range(6))
    return dict(conv=conv, novos=novos, m1=m1, m6=total6, custo6=budget * 6, cpa=budget / novos)
S = {400: cen(400), 800: cen(800), 1500: cen(1500, 0.92)}
def r(x): return "R$ " + f"{x:,.0f}".replace(",", ".")

def page(cls, inner, num=None, footer=True):
    ft = f'<footer class="ft"><span>{esc(C["marca"])} · Plano de impulso · {esc(C["cliente"])}</span><span>{num or ""}</span></footer>' if footer else ""
    return f'<section class="page {cls}">{inner}{ft}</section>'
def h(kicker, title, lead=None):
    out = f'<p class="kicker">{kicker}</p><h2>{title}</h2>'
    if lead: out += f'<p class="lead">{lead}</p>'
    return out
def cb(items):
    return '<ul class="ck">' + "".join(f'<li><span class="box"></span><div><b>{esc(a)}</b>{(" " + b) if b else ""}</div></li>' for a, b in items) + "</ul>"

pages = []

# 1 — capa
pages.append(page("cover", f'''
<div class="cover-top"><span class="brand">{esc(C["marca"])}</span><span class="mono">{esc(C["data"])}</span></div>
<div class="cover-mid">
  <p class="cover-kicker">Plano de impulso · checklist para a reunião</p>
  <h1>Mais banhos<br>na agenda.<br>Toda semana.</h1>
  <p class="cover-client">{esc(C["cliente"])} · {esc(C["bairro"])}, {esc(C["cidade"])}</p>
  <p class="cover-sub">Foco em duas coisas: trazer mais clientes e arrumar a infraestrutura digital da loja. O que corrigir primeiro (de graça), o que anunciar depois (de R$ 400 a R$ 1.500 por mês), e como fazer cada cliente novo voltar todo mês.</p>
</div>
<div class="cover-bot">
  <div class="cover-stat"><b>1</b><span>avaliação no Google, hoje</span></div>
  <div class="cover-stat"><b>3</b><span>fases: arrumar · anunciar · fidelizar</span></div>
  <div class="cover-stat"><b>3 km</b><span>o raio que importa em Vila Barros</span></div>
</div>
<div class="cover-rule"></div>
<p class="cover-foot">Documento de trabalho · leitura em 5 minutos</p>
''', footer=False))

# 2 — diagnóstico
diag = [
    ("Categoria errada no Google", "A ficha aparece como “Loja de répteis”. Quem busca “banho e tosa Guarulhos” não encontra a loja. Prova: uma análise automática concluiu que o negócio devia atrair “entusiastas de répteis”.", "Trocar a categoria principal para Pet shop e adicionar “Banho e tosa”. Cinco minutos, efeito imediato.", "grave"),
    ("Sem descrição do negócio no Google", "O campo está vazio. É onde o Google lê o que a loja faz e para quem.", "Descrição de 750 caracteres com serviços, bairro, portes atendidos e o WhatsApp. Escrevemos e publicamos.", "grave"),
    ("Uma única avaliação", "5,0 estrelas com 1 avaliação. Para quem compara, é como não ter nota.", "Pedir avaliação por WhatsApp a cada cliente que sai do banho, com link direto. Meta: 30 em 60 dias.", "grave"),
    ("A foto principal não mostra o serviço", "A capa é a fachada com sacos de ração. Banho e tosa, o que dá margem, não aparece.", "20 fotos reais: pet saindo do banho, tosa, bancada, equipe. Vídeo de 15 s de antes e depois.", "alto"),
    ("Dois perfis de Instagram", "@doriseciapetshop e @thaispetcare dividem a mesma clientela.", "Um perfil principal para o negócio; o outro redireciona. Bio com oferta e botão de WhatsApp.", "alto"),
    ("Serviços sem preço público", "O flyer diz “consulte pacotes”. Cada pergunta de preço é uma conversa que pode não acontecer.", "Tabela “a partir de” por porte, no Google, no Instagram e no site. Pacotes com nome.", "médio"),
    ("Sem agendamento online", "Tudo passa por mensagem manual. Quem escreve fora do horário fica sem resposta e vai a outro lugar.", "Link de agendamento ligado ao WhatsApp e ao calendário, com confirmação e lembrete automáticos. Loja: catálogo no WhatsApp.", "alto"),
    ("Sem site", "Os anúncios precisam de um lugar que explique, mostre e leve ao WhatsApp em um toque.", "Site de uma página, rápido no celular. Já pronto, entra como extra.", "médio"),
]
rows = "".join(f'<tr><td><span class="sev {s}">{s}</span></td><td><b>{esc(a)}</b><br><span class="small">{esc(b)}</span></td><td>{esc(c)}</td></tr>' for a, b, c, s in diag)
pages.append(page("", h("01 · Situação atual", "O que vimos na ficha do Google e no Instagram.", "Levantamento feito antes da reunião, só com o que está público. A boa notícia: os problemas mais graves são os mais baratos de resolver.") + f'''
<table class="tbl diag">
  <thead><tr><th>Peso</th><th>O que encontramos</th><th>O que fazer</th></tr></thead>
  <tbody>{rows}</tbody>
</table>
<div class="grid3 facts" style="margin-top:8px">
  <div class="tile sm"><b>Ficha Google</b><span>{esc(C["morada"])}<br>09:00 às 19:00 (a confirmar por dia) · WhatsApp {esc(C["wa"])}</span></div>
  <div class="tile sm"><b>Serviços no flyer</b><span>Banho · Tosa geral · Tosa higiênica · Corte de unhas · Limpeza de ouvidos · pacotes promocionais · loja com ração</span></div>
  <div class="tile sm"><b>Identidade</b><span>Casinha com coração, papel kraft, folhas desenhadas. Tem personalidade: dá para construir marca em cima disto.</span></div>
</div>
''', 2))

# 3 — checklist fases 0 e 1
pages.append(page("", h("02 · Checklist · Fase 0 e Fase 1", "Antes de gastar um real em anúncio.", "Duas semanas de arrumação. Tudo de graça ou quase. É o que faz o anúncio render depois: sem isto, o dinheiro vai para uma ficha errada e um perfil que não fecha.") + f'''
<h3>Fase 0 · Semana 1 · arrumar a casa (custo zero)</h3>
{cb([
 ("Categoria do Google:", "trocar “Loja de répteis” por Pet shop; adicionar Banho e tosa e Loja de ração."),
 ("Descrição do negócio no Google:", "texto completo com serviços, bairro, portes, horário e WhatsApp. Hoje está vazio."),
 ("Fotos e vídeo na ficha:", "20 fotos reais + 1 vídeo de antes e depois. Capa: pet saindo do banho, não a fachada."),
 ("Horário por dia da semana", "confirmado e publicado, com o dia de folga."),
 ("Serviços com preço “a partir de”", "por porte, na ficha do Google (aba Serviços) e nos destaques do Instagram."),
 ("Pedido de avaliação:", "mensagem pronta no WhatsApp com link direto, enviada a cada cliente que sai. Meta: 30 avaliações em 60 dias."),
 ("Responder à avaliação existente", "e a todas as próximas, em 24 h, assinado pelo nome."),
 ("Um Instagram principal:", "decidir entre @doriseciapetshop e @thaispetcare; o outro aponta para ele."),
 ("Bio nova:", "o que faz, o bairro, a oferta de entrada, botão de WhatsApp. Destaques: Banho e Tosa · Preços · Antes e Depois · Onde estamos · Pacotes."),
 ("WhatsApp Business (a loja já tem):", "não é preciso criar conta nem número novo. Organizar o que já está lá: catálogo com serviços e preços, mensagem de boas-vindas, mensagem fora do horário, etiquetas (novo · agendado · voltou · sumiu)."),
])}
<div class="note alt"><b>A loja já usa WhatsApp Business.</b> Isso poupa uma semana: não há conta a criar nem número a divulgar de novo. <b>Confirmar na reunião:</b> é o aplicativo gratuito ou já a API. Os lembretes e a recuperação automáticos precisam da API (Cloud API da Meta), e migrar o número para lá tira o aplicativo do celular. Se ela quiser manter o aplicativo, os primeiros envios ficam semiautomáticos, com a lista pronta e um toque para enviar.</div>
<h3 class="mt">Fase 1 · Semana 2 · a oferta e o lugar para onde mandar as pessoas</h3>
{cb([
 ("Oferta de entrada com nome:", "por exemplo “Primeiro banho com 20 % off” ou “Pacote 4 banhos, o 5.º é por nossa conta”. Uma só, clara, com validade."),
 ("Agendamento online:", "link de marcação (dia, hora, porte, serviço) ligado ao WhatsApp e ao calendário da loja, com confirmação e lembrete automáticos. Também no botão “Reservar” da ficha do Google."),
 ("Catálogo no WhatsApp", "para a loja: ração, petiscos e acessórios com preço; o cliente pede e busca no banho. Sem loja virtual, sem frete."),
 ("Site de uma página, o extra:", "serviços, preços a partir de, antes e depois, horário, mapa, botão de WhatsApp fixo. Já pronto; é para onde os anúncios apontam."),
 ("Ficha de cliente:", "nome do tutor, nome do pet, raça, porte, serviço, data. Numa planilha simples. Sem isto não há fidelização."),
 ("3 conteúdos gravados no celular:", "antes e depois (15 s), a tosadora explicando o que faz (20 s), um pet saindo feliz. São os anúncios."),
 ("Script de atendimento:", "responder em até 10 minutos no horário; três perguntas (porte, serviço, dia); confirmar com hora e endereço."),
])}
''', 3))

# 4 — anúncios
def col(b):
    s = S[b]
    return f'<td>{r(b)}</td><td>{s["conv"]:.0f}</td><td>{s["novos"]:.0f}</td><td>{r(s["cpa"])}</td><td>{r(s["m1"])}</td><td class="hl">{r(s["m6"])}</td>'
pages.append(page("", h("03 · Checklist · Fase 2 · Anúncios", "De R$ 400 a R$ 1.500 por mês. O que cada nível compra.", "Meta Ads (Instagram e Facebook), objetivo “mensagens no WhatsApp”, raio de 3 km em volta da loja, tutores de cães e gatos. Google Ads só depois de a ficha estar arrumada e com avaliações.") + f'''
<table class="tbl num2">
  <thead><tr><th>Por mês</th><th>Conversas no WhatsApp</th><th>Clientes novos</th><th>Custo do anúncio por cliente</th><th>Receita no 1.º mês</th><th class="hl">Receita em 6 meses</th></tr></thead>
  <tbody>
    <tr><td class="lab">Nível 1</td>{col(400)}</tr>
    <tr><td class="lab">Nível 2</td>{col(800)}</tr>
    <tr><td class="lab">Nível 3</td>{col(1500)}</tr>
  </tbody>
</table>
<p class="fine">Premissas, todas a confirmar nas duas primeiras semanas: R$ {CPC:.0f} por conversa iniciada (faixa de R$ 5 a R$ 12 em serviços locais), taxa de conversão média final de {AGENDA*100:.0f} % (conversa no WhatsApp → atendimento pago, já descontando quem agenda e não aparece), ticket médio de R$ {TICKET:.0f} por atendimento (banho e tosa, misto de portes, tabelas de 2026 da Grande São Paulo), {RECOR*100:.0f} % dos clientes novos voltam todo mês. “Receita em 6 meses” soma cada mês de clientes novos com os que continuam voltando; não desconta o custo dos anúncios ({r(400*6)}, {r(800*6)} e {r(1500*6)} no período). Não inclui venda de ração e acessórios, que costuma vir junto.</p>
<div class="cols2">
  <div>
    <h3>O que montar</h3>
    {cb([
      ("Nível 1 (R$ 400):", "uma campanha, a oferta de entrada, dois vídeos. Serve para descobrir o custo real por conversa."),
      ("Nível 2 (R$ 800):", "duas campanhas: oferta de entrada + banho e tosa recorrente (“todo mês, sem pensar”)."),
      ("Nível 3 (R$ 1.500):", "as duas anteriores + remarketing para quem falou e não agendou + impulsionar as melhores avaliações."),
      ("Segmentação:", "raio 3 km, 25 a 60 anos, interesses em cães, gatos, ração, pet shop. Horário de veiculação: 8h às 21h."),
      ("Destino:", "sempre o WhatsApp, com mensagem pré-preenchida: “Oi! Vi o anúncio e quero agendar um banho.”"),
    ])}
  </div>
  <div>
    <h3>Regras para não queimar dinheiro</h3>
    {cb([
      ("Nada de arte genérica.", "Vídeo cru do celular, pet real, gente real. Antes e depois vence tudo neste setor."),
      ("Uma oferta por vez.", "Trocar só depois de 14 dias com dados."),
      ("Responder em 10 minutos.", "Anúncio que gera conversa sem resposta é dinheiro jogado fora."),
      ("Medir toda semana:", "conversas, agendados, compareceram, voltaram. Custo do anúncio por cliente novo."),
      ("Começar no nível 1 ou 2.", "Subir para o 3 só quando o custo por cliente estiver confirmado."),
    ])}
  </div>
</div>
''', 4))

# 5 — fase 3 recorrência + follow-up
pages.append(page("", h("04 · Checklist · Fase 3 · Fidelização", "Cliente que volta todo mês vale mais do que cliente novo.", "Um pet toma banho a cada 15 ou 30 dias. O negócio cresce quando isso vira rotina automática, e não quando o tutor lembra por acaso.") + f'''
{cb([
 ("Plano mensal de banho", "com desconto e dia fixo (“toda 2.ª sexta, 10h”). Receita previsível para a loja, um pet sempre limpo para o tutor."),
 ("Pacote pré-pago", "4 banhos, o 5.º grátis. Vende hoje, entrega ao longo de dois meses."),
 ("Lembrete automático pelo WhatsApp:", "15 dias depois do último banho: “A Mel está pronta para o próximo banho? Tenho vaga sábado.”"),
 ("Recuperação de quem sumiu:", "30 dias sem vir → mensagem com o nome do pet e uma oferta; 3 semanas depois, mais uma. Quem não responde fica em pausa e volta a receber depois."),
 ("Lembretes de saúde", "que vendem produto: vermífugo e antipulgas de 3 em 3 meses, com o item da loja."),
 ("Aniversário do pet:", "mensagem com um mimo (banho com brinde). Custa centavos, gera foto e avaliação."),
 ("Pedido de avaliação", "sempre 2 h depois do banho, enquanto o pet ainda está cheiroso."),
 ("Indicação:", "“traga um amigo peludo, os dois ganham desconto”. É o anúncio mais barato que existe."),
])}
<div class="callout"><b>Como isto funciona sem ninguém lembrar.</b> Os lembretes, a recuperação de quem sumiu e o pedido de avaliação saem sozinhos de um sistema ligado ao WhatsApp da loja, a partir da ficha de cliente. A equipe só fala com quem responde. É o mesmo motor que a Pacheco Studios monta para outros negócios; para a Doris & Cia começa pequeno: um fluxo, o de recuperação.</div>
<h3 class="mt">Ordem de prioridade, se só der para fazer três coisas</h3>
<ol class="ol">
  <li><b>Categoria + fotos + avaliações no Google.</b> Grátis, e é onde a maioria dos clientes de bairro procura.</li>
  <li><b>Um Instagram, uma oferta, agendamento online e o sistema ligado ao WhatsApp da loja.</b> É o que transforma visita em agendamento, mesmo fora do horário.</li>
  <li><b>Anúncio de R$ 400 a R$ 800 com vídeo de antes e depois</b>, medido por semana, e o lembrete de 15 dias para quem já veio.</li>
</ol>
''', 5))

# 6 — as sete perguntas
PERG = [
 ("o teto", "Quantos banhos e tosas fazem por semana hoje, e quantos caberiam sem contratar ninguém?",
  "A diferença entre os dois é crescimento que não custa nada. Se cabem mais, os anúncios enchem a loja sem contratar ninguém. Se já está no limite, anunciar só cria fila e clientes chateados."),
 ("o teto", "Qual é o preço de banho e de tosa, por porte?",
  "Multiplica tudo o que está neste plano. A R$ 55 o retorno cai de 7× para 5×. A R$ 110 sobe, e o nível 3 passa a fazer sentido logo no primeiro mês."),
 ("o teto", "Quanto custa uma segunda pessoa no banho e tosa, e em quanto tempo se paga?",
  "Transforma um teto num degrau. Decide se o plano dos próximos seis meses é encher a agenda que já existe ou duplicar a operação."),
 ("o sistema", "Quem responde ao WhatsApp, e em quanto tempo quando a loja está cheia?",
  "É o degrau onde mais se perde. Responder em 10 minutos dobra a conversão. Se a resposta for “eu, quando dá”, o agendamento automático passa a ser a peça central, não um extra."),
 ("o sistema", "Têm guardado nome, telefone e o pet de quem já veio? Quantos?",
  "Com lista, a recuperação de clientes dá dinheiro na primeira semana, sem gastar em anúncio. Sem lista, a ficha de cliente é o primeiro trabalho e o retorno chega um mês mais tarde."),
 ("o sistema", "Usam algum software de gestão, ou é caderno e WhatsApp?",
  "Decide se os lembretes saem sozinhos ou à mão, e se os fluxos de inativos e pagamentos entram já ou ficam para depois."),
 ("a vontade", "Onde é que ela quer estar daqui a um ano?",
  "Mais movimento na mesma loja, mais uma pessoa, ou mais uma loja são três planos diferentes. Se a resposta for “está bom assim”, o pacote certo é o Base e não vale insistir."),
]
qs = "".join(f'<div class="q"><span class="mono">{esc(g)}</span><b>{i}. {esc(t)}</b><p>{esc(p)}</p></div>'
             for i, (g, t, p) in enumerate(PERG, 1))
pages.append(page("", h("05 · Para a reunião", "Sete perguntas que dizem até onde dá para crescer.",
  "O teto deste negócio é uma multiplicação simples. Tudo o resto é o caminho até lá. Estas sete perguntas dão os dois números e dizem se o caminho existe.") + f'''
<div class="teto">
  <div class="tf">
    <span class="mono">o cálculo, à frente dela</span>
    <code>teto mensal = atendimentos que cabem × preço médio</code>
    <code>folga = teto − faturamento de hoje</code>
  </div>
  <p>Se a folga der R$ 8.000 por mês de capacidade parada, está aí o argumento inteiro: os anúncios vão buscar dinheiro que já está pago em renda, luz e salários.</p>
</div>
<div class="qs">{qs}</div>
<div class="callout"><b>A ordem importa.</b> Não comeces pelo orçamento. Se perguntares primeiro quanto ela quer gastar, ela diz um número pequeno por instinto e ficas preso a ele. Pergunta a capacidade, mostra a folga, e só depois fala de verba.</div>
''', 6))

# 7 — próximos passos
pages.append(page("", h("06 · Os próximos passos", "Do sim até ao primeiro relatório.") + f'''
<div class="cols2">
  <div>
    <h3>Calendário</h3>
    <ol class="ol tight">
      <li><b>Hoje:</b> este plano, o site de demonstração (extra) e a escolha do nível de anúncio.</li>
      <li><b>Semana 1:</b> Fase 0 completa: Google arrumado, um Instagram, WhatsApp da loja organizado e ligado ao sistema.</li>
      <li><b>Semana 2:</b> oferta definida, agendamento online e catálogo no WhatsApp, site no ar, 3 vídeos gravados, ficha de cliente criada.</li>
      <li><b>Semana 3:</b> anúncios no ar. Relatório toda segunda-feira: conversas, agendados, custo por cliente.</li>
      <li><b>Dia 45:</b> revisão com números reais. Ajustar oferta e orçamento. Ligar o lembrete de 15 dias e a recuperação de quem sumiu.</li>
    </ol>
  </div>
  <div>
    <h3>O que medir desde o primeiro dia</h3>
    <ul class="ul tight">
      <li>Conversas que chegaram, e de que anúncio</li>
      <li>Quantas viraram agendamento</li>
      <li>Quantas apareceram mesmo</li>
      <li>Quantas voltaram no mês seguinte</li>
      <li>Custo do anúncio por cliente novo</li>
      <li>Atendimentos por semana contra a capacidade</li>
    </ul>
    <div class="note"><b>O que a Pacheco Studios faz:</b> <b>trazer clientes</b> (ficha do Google arrumada e com avaliações, um Instagram que converte, anúncios geridos com relatório semanal) e <b>infraestrutura</b> (o sistema ligado ao WhatsApp Business que a loja já usa, agendamento online, ficha de cliente, lembretes e recuperação automáticos). <b>O site de uma página vai incluído como extra.</b></div>
    <div class="note alt"><b>A parede a vigiar.</b> Com reinvestimento de parte do lucro, a agenda de uma tosadora esgota por volta do sexto mês. A partir do quarto, o problema deixa de ser trazer clientes e passa a ser ter quem os atenda.</div>
  </div>
</div>
<div class="callout final">
  <div><b>{esc(C["marca"])}</b><br><span>Web design e sistemas para negócios locais</span></div>
  <div class="r"><span class="mono">{esc(C["tel"])}</span><br><span class="mono">{esc(C["email"])}</span></div>
</div>
''', 7))

EXTRA = f"""
.ck{{list-style:none;margin-top:4px}}
.ck li{{display:flex;gap:9px;align-items:flex-start;margin-bottom:6px;font-size:10pt;line-height:1.4}}
.ck .box{{flex:0 0 14px;width:14px;height:14px;border:1.6px solid var(--navy);border-radius:3px;margin-top:3px;background:#fff}}
.ck b{{color:var(--navy)}}
.tbl.diag td{{padding:6px 8px;font-size:9.1pt;vertical-align:top;line-height:1.35}}
.tbl.diag td:first-child{{width:16mm}}
.tbl.diag td:nth-child(2){{width:76mm}}
.sev{{display:inline-block;font-family:'JetBrains Mono',monospace;font-size:8pt;padding:2px 7px;border-radius:10px;text-transform:uppercase;letter-spacing:.04em}}
.sev.grave{{background:#F7E0E0;color:#8A2B2B}} .sev.alto{{background:#FBF3E1;color:#7A5A12}} .sev.médio{{background:#EEF0F4;color:var(--navy)}}
.facts{{margin-top:10px}}
.facts .tile.sm b{{font-size:13pt;color:var(--navy)}}
.facts .tile.sm span{{font-size:8.6pt}}
.facts .tile{{padding:10px 12px}}
.tbl.num2 td,.tbl.num2 th{{text-align:right;padding:7px 8px;font-size:9.6pt}}
.tbl.num2 td.lab,.tbl.num2 th:first-child{{text-align:left}}
.tbl.num2 td{{font-family:'JetBrains Mono',monospace}}
.tbl.num2 td.lab{{font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:12pt;color:var(--navy)}}
.tbl.num2 th.hl,.tbl.num2 td.hl{{background:#F2F8F7;color:var(--teal);font-weight:700}}
.cols2 .ck li{{font-size:9.6pt}}
.ol.tight li{{font-size:9.8pt;margin-bottom:6px}}
.teto{{display:grid;grid-template-columns:1.1fr 1fr;gap:16px;align-items:center;background:var(--navy);color:#fff;border-radius:12px;padding:14px 18px;margin:4px 0 12px}}
.teto .mono{{display:block;color:var(--gold);margin-bottom:6px}}
.teto code{{display:block;font-family:'JetBrains Mono',monospace;font-size:10pt;color:#fff;background:rgba(255,255,255,.08);border-radius:6px;padding:6px 10px;margin-bottom:5px}}
.teto p{{font-size:9.8pt;color:#C9CFDA}}
.qs{{display:grid;grid-template-columns:1fr 1fr;gap:9px 18px}}
.q .mono{{display:block;color:var(--gold);font-size:8.2pt;margin-bottom:1px}}
.q b{{display:block;font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:13pt;color:var(--navy);line-height:1.15;margin-bottom:2px}}
.q p{{font-size:9pt;color:#3A3F4B;line-height:1.35}}
.callout.final{{margin-top:14px}}
.callout.final .r{{text-align:right;white-space:nowrap}}
h1{{font-size:60pt}}
"""
if __name__ == "__main__":
  doc = f"""<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="utf-8"><title>Plano de impulso · {esc(C["cliente"])}</title>
<style>{B.CSS}{EXTRA}</style></head><body>{''.join(pages)}</body></html>"""
  (HERE / "checklist.html").write_text(doc, encoding="utf-8")
  print("checklist.html", len(doc)//1024, "KB")
