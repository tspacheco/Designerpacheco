#!/usr/bin/env python3
"""Agente 3 · Triagem Portugal (Micro System Print de 1 página), no formato da triagem do Iulian Paraschiv.

Pedido do Tomás (13/10/2026): só negócios com WhatsApp provado (fixo = há quem atenda; a mensagem vai por WhatsApp),
fisioterapia, clínicas e estética (nada de restaurantes); não é sobre o site mas sobre a infraestrutura de atendimento.
A mensagem leva o lema e pachecost.com. Não sai grátis: a vertente escolhida é a primeira execução, paga, com valor
fechado na reunião, e abre o acompanhamento / Auditoria de Sistemas com IA. Sem preços nem números inventados.

  python3 triagem_pt.py     → raio-x/triagens-pt/<slug>/triagem-<slug>.pdf e raio-x/ENVIAR-PT-lote-3.md
"""
import base64, datetime, html as H, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gerar import RAIZ, RAMO, ler_candidatos, pdf

SAIDA = os.path.join(RAIZ, "raio-x", "triagens-pt")
RAW = f"https://github.com/tspacheco/Designerpacheco/raw/{RAMO}/raio-x/triagens-pt"
LEMA = "Encontramos a fuga. Desenhamos o sistema. Provamos o impacto."

CSS = """
@page{size:A4;margin:0}
:root{--c:#141210;--o:#EFEAE3;--o2:#F7F3EE;--l:#E8622C;--lt:#A64923;--sc:#A5A19B;--so:#4D4A47;--li:#D8D1C7}
*{box-sizing:border-box}html,body{margin:0}
body{font:400 9.2pt/1.45 'Inter',sans-serif;color:var(--c);-webkit-print-color-adjust:exact;print-color-adjust:exact}
.pag{width:210mm;height:297mm;background:var(--o);display:flex;flex-direction:column;overflow:hidden}
.mono{font:700 7.2pt/1 'Space Mono',monospace;letter-spacing:.14em;text-transform:uppercase}
.marca{font:400 10pt/1 'Archivo Black';letter-spacing:.06em;text-transform:uppercase}
.marca i{display:inline-block;width:.42em;height:.42em;border-radius:50%;background:var(--l);margin-left:.12em}
.topo{background:var(--c);color:var(--o);padding:9mm 14mm 8mm}
.topo .l1{display:flex;justify-content:space-between}.topo .l1 .mono{color:var(--sc)}
.topo .sup{color:var(--l);margin:7mm 0 2.5mm;display:block}
h1{font:400 20pt/1.12 'Archivo Black';text-transform:uppercase;margin:0}
h1 em{font-style:normal;color:var(--l);display:block;font-size:15pt;margin-top:1.5mm}
.aviso{margin:3mm 0 0;font-size:8.6pt;color:var(--sc)}
.corpo{flex:1;padding:6mm 14mm 0;display:flex;flex-direction:column;gap:5mm}
h3{font:700 7.4pt/1 'Space Mono';letter-spacing:.14em;text-transform:uppercase;color:var(--lt);margin:0 0 2.5mm;display:flex;gap:3mm;align-items:center}
h3::after{content:'';flex:1;height:1px;background:var(--li)}
.sinais{margin:0;padding:0;list-style:none;display:grid;grid-template-columns:repeat(3,1fr);gap:4mm}
.sinais li{border-top:2px solid var(--c);padding-top:2mm;font-size:8.8pt}
.rota{display:flex;gap:1.5mm;align-items:stretch}
.rota div{flex:1;background:var(--o2);box-shadow:inset 0 0 0 1px var(--li);border-radius:6px;padding:2.5mm;position:relative}
.rota b{display:block;font-weight:600;font-size:9pt}.rota span{font-size:7.8pt;color:var(--so)}
.rota div.r{box-shadow:inset 0 0 0 1.5px var(--l)}
.risco{margin-top:2mm;font:700 7.4pt/1.3 'Space Mono';color:var(--lt);text-transform:uppercase;letter-spacing:.1em}
.fut{display:grid;grid-template-columns:repeat(4,1fr);gap:3mm}
.fut div{background:var(--c);color:var(--o);border-radius:8px;padding:3.5mm}
.fut b{display:block;font:400 10pt/1 'Archivo Black';text-transform:uppercase;color:var(--l);margin-bottom:2mm}
.fut span{font-size:8.3pt;color:#D9D3CA;line-height:1.4}
.etapas{display:grid;grid-template-columns:repeat(3,1fr);gap:3mm}
.etapas div{background:var(--c);color:var(--o);border-radius:8px;padding:3.5mm;display:flex;flex-direction:column}
.etapas i{font:700 7.4pt/1 'Space Mono';color:var(--c);background:var(--l);padding:3px 5px;border-radius:3px;font-style:normal;align-self:flex-start}
.etapas b{display:block;font:400 11pt/1 'Archivo Black';text-transform:uppercase;color:var(--l);margin:2.5mm 0 1.8mm}
.etapas span{font-size:8.4pt;color:#E6E0D7;line-height:1.42}
.etapas em{font-style:normal;font-size:7.9pt;color:var(--sc);line-height:1.4;margin-top:auto;padding-top:2.5mm;border-top:1px solid #3A3631;margin-top:3mm}
.etapas em strong{color:var(--o);font-weight:600}
.topo{padding:7mm 14mm 6mm}.topo .sup{margin:5mm 0 2mm}h1{font-size:18pt}h1 em{font-size:12.5pt}
.corpo{gap:3.6mm;padding-top:5mm}.etapas div{padding:3mm}.etapas span{font-size:8pt}.etapas em{font-size:7.6pt}
.qw div{padding:3mm}.qw span{font-size:8pt}.prox{margin-bottom:5mm;padding:3.5mm 5mm}.prox small{display:block;font:400 8.8pt/1.4 'Inter';margin-top:1.2mm}
.qw{display:grid;grid-template-columns:repeat(3,1fr);gap:3mm}
.qw div{background:var(--o2);box-shadow:inset 0 0 0 1px var(--li);border-radius:8px;padding:3.5mm}
.qw b{display:block;font-weight:600;font-size:9.6pt;margin:1.5mm 0 1mm}.qw span{font-size:8.3pt;color:var(--so)}
.qw i{font:700 7.4pt/1 'Space Mono';color:var(--o);background:var(--l);padding:3px 5px;border-radius:3px;font-style:normal}
.alt{font-size:8.2pt;color:var(--so);margin:2.5mm 0 0}
.duas{display:grid;grid-template-columns:1.6fr 1fr;gap:5mm}
.duas ol{margin:0;padding-left:4.5mm;display:grid;gap:1.8mm;font-size:8.8pt}
.duas ul{margin:0;padding:0;list-style:none;display:grid;gap:1.8mm;font-size:8.8pt}
.duas ul li::before{content:'';display:inline-block;width:5px;height:5px;border-radius:50%;background:var(--l);margin-right:2mm;vertical-align:1px}
.prox{margin-top:auto;margin-bottom:6mm;background:var(--l);border-radius:8px;padding:4mm 5mm;font:600 10pt/1.35 'Inter'}
.rod{background:var(--c);color:var(--sc);padding:4.5mm 14mm;display:flex;justify-content:space-between;font-size:8pt}
.rod .marca{color:var(--o)}
"""
CSS += """
.sinais li{font-size:8.4pt}.sinais li b{display:block;font:700 7pt/1.2 'Space Mono';letter-spacing:.1em;text-transform:uppercase;color:var(--lt);margin-bottom:1mm}
.topo{padding:6mm 14mm 5mm}.topo .sup{margin:4mm 0 1.6mm}h1{font-size:17pt}h1 em{font-size:11pt}.aviso{font-size:8.2pt;margin-top:2mm}
.corpo{gap:3mm;padding-top:4mm}.etapas{gap:2.5mm}.etapas div{padding:2.6mm}.etapas b{font-size:10pt;margin:2mm 0 1.4mm}
.etapas span{font-size:7.7pt;line-height:1.36}.etapas em{font-size:7.3pt;padding-top:2mm;margin-top:2mm}
.qw div{padding:2.6mm}.qw span{font-size:7.8pt}.qw b{font-size:9.2pt}.alt{font-size:7.8pt;margin-top:1.8mm}
.duas ol,.duas ul{font-size:8.4pt;gap:1.2mm}h3{margin-bottom:2mm}
.prox{font-size:9.2pt;margin-bottom:4mm;padding:3mm 4.5mm}.prox .lema{display:block;font:400 9pt/1.2 'Archivo Black';text-transform:uppercase;letter-spacing:.02em;margin-top:2mm;color:var(--c)}
"""


def fonte(nome, ficheiro, peso):
    b = base64.b64encode(open(os.path.join(RAIZ, "marca", "fontes", ficheiro), "rb").read()).decode()
    return f"@font-face{{font-family:'{nome}';font-weight:{peso};src:url(data:font/woff2;base64,{b}) format('woff2')}}"


FONTES = "\n".join([fonte("Archivo Black", "archivo-black-ro.woff2", 400), fonte("Inter", "inter-400-ro.woff2", 400),
                    fonte("Inter", "inter-600-ro.woff2", 600), fonte("Space Mono", "space-mono-700-ro.woff2", 700)])

OU = "Ou, se preferirem:"
PROX = ("Próximo passo: escolham uma destas vertentes como primeira execução. Montamo-la e medimos desde a primeira semana; "
        "é um trabalho pago, com o valor fechado na reunião. Se o resultado aparecer, seguimos juntos para as próximas."
        f'<span class="lema">{LEMA}</span>')

# Sinais: só o que se vê de fora e foi verificado pela ponte (página lida e medida a 13/10/2026).
NEG = {
 "pt-agnus-dei": dict(
  sub="O caminho de um paciente, do primeiro contacto à próxima revisão.",
  sinais=[("WhatsApp", "No site, com o mesmo número da ficha Google."), ("Marcação", "Não há marcação online: tudo passa por mensagem ou telefone."),
          ("Página", "No telemóvel, o conteúdo principal aparece ao fim de 13,5 s.")],
  etapas=[("Pedido", "WhatsApp, telefone e site caem numa só lista; cada pedido tem resposta imediata e fica registado com o motivo (dor, revisão, estética).",
           "resposta automática só fora do horário; no horário responde a receção."),
          ("Marcação", "O paciente vê as horas livres e escolhe; urgências e primeiras consultas passam pela receção.",
           "a receção recebe o pedido já resumido e marca com um toque."),
          ("Véspera", "Lembrete com hora e morada; se o paciente não puder vir, a hora volta a ficar livre para quem está em espera.",
           "só o lembrete na véspera, sem lista de espera."),
          ("Orçamento", "Orçamentos de tratamentos maiores seguem por escrito no mesmo dia, com seguimento se não houver resposta.",
           "o sistema prepara o rascunho e o médico ajusta antes de sair."),
          ("Tratamento", "Planos com várias sessões ficam com as datas seguintes propostas antes de o paciente sair.",
           "a receção recebe a lista de quem saiu sem próxima marcação."),
          ("Depois", "Pedido de avaliação após o tratamento e convite para a revisão seguinte, na data certa.",
           "só o lembrete da revisão.")],
  qw=[("Atendimento automático", "Passos 1 e 2: resposta imediata e marcação nas horas livres, com a receção no controlo."),
      ("Gestão de clientes", "Passos 3 a 5: lembretes, orçamentos e planos de tratamento numa só lista."),
      ("Avaliações após o serviço", "Passo 6: avaliação e revisão seguinte, sem ninguém ter de se lembrar.")],
  alt="Outras vertentes: faturas e pagamentos · números do negócio (pedidos, faltas, orçamentos aceites).",
  perg=["Quem atende hoje o WhatsApp e o telefone, e em que horas?", "Que passo ocupa mais tempo à receção?",
        "Que tratamentos querem ver crescer: estética, implantes, revisões?"],
  met=["Tempo até à primeira resposta", "Faltas por semana", "Orçamentos aceites"]),
 "pt-barrigas-a-crescer-i-silvia-co": dict(
  nome="Sílvia Conde · Barrigas a Crescer",
  sub="O caminho de uma família, do primeiro pedido à consulta seguinte.",
  sinais=[("Pedido", "«Agendar consulta» abre um formulário: a família fica à espera de resposta."), ("WhatsApp", "Publicado no site."),
          ("Cursos", "O site tem cursos para pais, além das consultas.")],
  etapas=[("Pedido", "WhatsApp e formulário caem numa só lista; a família recebe logo a confirmação de que chegou e quando responde.",
           "resposta automática só quando está em consulta; o resto responde a Sílvia."),
          ("Perguntas", "Um assistente recolhe idade do bebé, motivo e quem encaminhou, e entrega-lhe um resumo.",
           "recebe tudo resumido e faz a Sílvia a conversa, já com os dados."),
          ("Marcação", "A família escolhe entre as horas livres; a primeira consulta é confirmada pela Sílvia.",
           "a Sílvia propõe duas horas com um toque."),
          ("Véspera", "Lembrete com hora, morada e o que trazer.", "só o lembrete, sem mais nada."),
          ("Entre sessões", "Exercícios para casa e a próxima sessão proposta no fim de cada consulta.", "só o lembrete da próxima sessão."),
          ("Depois", "Pedido de avaliação e convite para o curso certo para a idade do bebé.", "só o pedido de avaliação.")],
  qw=[("Atendimento automático", "Passos 1 e 2: nenhum pedido fica à espera enquanto está em consulta."),
      ("Gestão de clientes", "Passos 3 a 5: cada família numa só lista, com lembretes e próxima sessão."),
      ("Avaliações após o serviço", "Passo 6: avaliação e convite para os cursos no momento certo.")],
  alt="Outras vertentes: plano para escalar fontes de pedidos (pediatras, cursos de preparação para o parto) · conteúdo a partir das dúvidas mais frequentes dos pais.",
  perg=["Quando está em consulta, quem responde às mensagens?", "Que passo lhe ocupa mais tempo hoje?",
        "De onde vêm as famílias: pediatras, recomendação, redes?"],
  met=["Tempo até à primeira resposta", "Pedidos → primeira consulta", "Famílias que voltam ou vão aos cursos"]),
 "pt-physioalba-tavira": dict(
  nome="PhysioAlba Tavira",
  sub="O caminho de um paciente, da primeira sessão à alta e ao regresso.",
  sinais=[("Já têm", "Agenda online e WhatsApp no site."), ("Google", "5,0★ em 244 avaliações."),
          ("Página", "No telemóvel, o conteúdo principal aparece ao fim de 6,2 s.")],
  etapas=[("Pedido", "Já têm agenda online e WhatsApp. Passo seguinte: as dúvidas no WhatsApp recebem resposta imediata e acabam numa marcação.",
           "resposta automática só fora do horário."),
          ("Antes", "Ficha de entrada preenchida antes da primeira sessão (queixa, historial), já no processo do paciente.",
           "o fisioterapeuta recebe só um resumo."),
          ("Plano", "No fim da primeira sessão, o número de sessões e as datas seguintes ficam propostas.",
           "a equipa recebe a lista de quem saiu sem próxima marcação."),
          ("Sessões", "Lembrete na véspera e exercícios para casa; uma falta liberta a hora para quem está em espera.",
           "só o lembrete na véspera."),
          ("Alta", "Mensagem de alta com o plano para casa e pedido de avaliação.", "só a mensagem de alta."),
          ("Regresso", "Contacto de acompanhamento passado algum tempo, com marcação de manutenção para quem precisa.",
           "um lembrete anual de prevenção.")],
  qw=[("Gestão de clientes", "Passos 3 e 4: planos completos, lembretes e lista de espera numa só vista."),
      ("Atendimento automático", "Passo 1: o WhatsApp responde fora de horas e leva à agenda que já têm."),
      ("Números do negócio", "Sessões por plano, faltas e regressos, vistos todas as semanas.")],
  alt="Outras vertentes: avaliações após o serviço · plano para escalar fontes de pacientes (médicos, clubes, ginásios).",
  perg=["Quantos pacientes terminam o plano completo?", "Que passo ocupa mais tempo à equipa?",
        "De onde vêm os novos pacientes: médicos, recomendação, Google?"],
  met=["Planos concluídos", "Faltas por semana", "Pacientes que regressam"]),
 "pt-mary-estetica": dict(
  nome="Mary Estética e Massagens",
  sub="O caminho de uma cliente, da primeira mensagem à próxima sessão.",
  sinais=[("WhatsApp", "«Agende ou tire dúvidas pelo WhatsApp», no site, com o número da ficha."), ("Google", "5,0★ em 334 avaliações; no site há testemunhos em inglês."),
          ("Página", "No telemóvel, o conteúdo principal aparece ao fim de 11,4 s.")],
  etapas=[("Pedido", "O WhatsApp responde na hora, em português e em inglês: tratamentos, duração e horas livres.",
           "resposta automática só fora do horário ou durante as sessões."),
          ("Marcação", "A cliente escolhe tratamento e hora livre e a marcação fica na agenda.",
           "a equipa recebe o pedido resumido e confirma com um toque."),
          ("Véspera", "Lembrete com hora e morada; se não puder vir, a hora volta a ficar livre.", "só o lembrete na véspera."),
          ("Sessão", "Ficha da cliente (preferências, pele, pressão da massagem) à mão de quem a recebe.", "notas simples por cliente."),
          ("Pacotes", "Quem faz tratamentos em série recebe a próxima sessão proposta e o pacote pago por link.",
           "só o lembrete da próxima sessão."),
          ("Depois", "Pedido de avaliação; residentes recebem o convite para voltar, quem está de férias para a próxima estadia.",
           "só o pedido de avaliação.")],
  qw=[("Atendimento automático", "Passos 1 e 2: o WhatsApp responde e marca, em português e em inglês."),
      ("Gestão de clientes", "Passos 3 a 5: lembretes, ficha da cliente e próxima sessão numa só lista."),
      ("Faturas e pagamentos", "Passo 5: pacotes e sinal pagos por link, ligados à marcação.")],
  alt="Outras vertentes: avaliações após o serviço · conteúdo e calendário a partir dos tratamentos mais pedidos.",
  perg=["Quanto do dia vai para responder no WhatsApp?", "Que tratamentos querem encher mais?",
        "Residentes ou turistas: quem querem ver voltar mais?"],
  met=["Tempo até à primeira resposta", "Mensagens → marcações", "Clientes que voltam"]),
 "pt-vitalite": dict(
  nome="Vitalité",
  sub="O caminho de uma cliente, do primeiro contacto ao plano seguinte.",
  sinais=[("WhatsApp", "No site, com o número da ficha Google."), ("Três áreas", "Estética, saúde e fitness no mesmo espaço."),
          ("Página", "No telemóvel, o conteúdo principal aparece ao fim de 8,6 s.")],
  etapas=[("Pedido", "WhatsApp, telefone e site caem numa só lista, com resposta imediata e o pedido registado.",
           "resposta automática só fora do horário."),
          ("Perguntas", "Um assistente percebe o objetivo (pele, corpo, dor, forma física) e sugere a consulta certa.",
           "a equipa recebe o resumo e faz a conversa."),
          ("Marcação", "A cliente escolhe uma hora livre; procedimentos que pedem avaliação passam pela equipa.",
           "a equipa confirma cada marcação com um toque."),
          ("Véspera", "Lembrete com hora, morada e preparação; se não puder vir, a hora volta a ficar livre.", "só o lembrete na véspera."),
          ("Plano", "Tratamentos em várias sessões ficam com as datas seguintes propostas e o pacote pago por link.",
           "só o lembrete da próxima sessão."),
          ("Depois", "Pedido de avaliação e convite para a área seguinte (de estética para fitness, de saúde para estética).",
           "só o pedido de avaliação.")],
  qw=[("Atendimento automático", "Passos 1 e 2: resposta imediata que encaminha para a consulta certa."),
      ("Gestão de clientes", "Passos 3 a 5: cada cliente numa só lista, das três áreas, com lembretes."),
      ("Números do negócio", "Pedidos, marcações e clientes que passam de uma área para outra, vistos todas as semanas.")],
  alt="Outras vertentes: faturas e pagamentos · avaliações após o serviço.",
  perg=["Quem responde hoje ao WhatsApp e em que horas?", "Que área querem ver crescer: estética, saúde ou fitness?",
        "Que passo ocupa mais tempo à equipa?"],
  met=["Tempo até à primeira resposta", "Pedidos → marcações", "Clientes em mais de uma área"]),
}
ORDEM = ["pt-agnus-dei", "pt-mary-estetica", "pt-physioalba-tavira", "pt-vitalite", "pt-barrigas-a-crescer-i-silvia-co"]
CURTO = {"pt-agnus-dei": "Agnus Dei", "pt-mary-estetica": "Mary Estética", "pt-physioalba-tavira": "PhysioAlba",
         "pt-vitalite": "Vitalité", "pt-barrigas-a-crescer-i-silvia-co": "Barrigas a Crescer"}
CIDADE = {"pt-agnus-dei": "Olhão", "pt-mary-estetica": "Portimão", "pt-physioalba-tavira": "Tavira", "pt-vitalite": "Portimão",
          "pt-barrigas-a-crescer-i-silvia-co": "Faro"}


def nome(slug, c):
    return NEG[slug].get("nome") or c["nome"].split(" - ")[0]


def pagina(slug, c):
    t = NEG[slug]
    sinais = "".join(f"<li><b>{H.escape(a)}</b>{H.escape(b)}</li>" for a, b in t["sinais"])
    etapas = "".join(f'<div><i>0{i+1}</i><b>{H.escape(a)}</b><span>{H.escape(b)}</span><em><strong>{OU}</strong> {H.escape(x)}</em></div>'
                     for i, (a, b, x) in enumerate(t["etapas"]))
    qw = "".join(f"<div><i>0{i+1}</i><b>{H.escape(a)}</b><span>{H.escape(b)}</span></div>" for i, (a, b) in enumerate(t["qw"]))
    perg = "".join(f"<li>{H.escape(x)}</li>" for x in t["perg"])
    met = "".join(f"<li>{H.escape(x)}</li>" for x in t["met"])
    n = H.escape(nome(slug, c))
    return f"""<!doctype html><html lang="pt-PT"><head><meta charset="utf-8"><title>Triagem · {n}</title>
<style>{FONTES}{CSS}</style></head><body><section class="pag">
<div class="topo"><div class="l1"><span class="marca">Pacheco Studios<i></i></span><span class="mono">Outubro 2026</span></div>
<span class="mono sup">Triagem · Micro System Print</span><h1>{n}<br><em>{H.escape(t['sub'])}</em></h1>
<p class="aviso">Não é um diagnóstico do vosso negócio nem do vosso site: é a infraestrutura de atendimento que nós, Pacheco Studios, montaríamos, eficiente em cada passo. Cada equipa trabalha à sua maneira; escolham o que vos serve.</p></div>
<div class="corpo">
<div><h3>O que se vê de fora</h3><ul class="sinais">{sinais}</ul></div>
<div><h3>O caminho Pacheco Studios, passo a passo</h3><div class="etapas">{etapas}</div></div>
<div><h3>As nossas 3 sugestões</h3><div class="qw">{qw}</div><p class="alt">{H.escape(t['alt'])}</p></div>
<div class="duas"><div><h3>3 perguntas para vocês</h3><ol>{perg}</ol></div><div><h3>O que medimos</h3><ul>{met}</ul></div></div>
<div class="prox">{PROX}</div>
</div><footer class="rod"><span class="marca">Pacheco Studios<i></i></span><span>Tomás Pacheco · +351 967 117 357 · pachecost.com</span></footer>
</section></body></html>"""


def mensagem(slug, c):
    return (f"Boa tarde! Sou o Tomás, da Pacheco Studios (pachecost.com). O nosso lema é «{LEMA}» "
            f"Desenhámos numa página o caminho de um cliente da {CURTO[slug]}, do primeiro contacto à próxima visita, "
            f"com a infraestrutura de atendimento que montaríamos em cada passo e uma alternativa para cada preferência. Segue em anexo. "
            f"Não é sobre o site: é sobre o que acontece entre a mensagem e a marcação. Faz sentido marcarmos uma reunião para validar isto convosco?")


def main():
    cands = ler_candidatos()
    data = datetime.date.today().strftime("%d/%m/%Y")
    out = [f"# Agente 3 · Triagens Portugal para enviar ({data})", "",
           "Formato da triagem do Iulian (1 página): o caminho Pacheco Studios passo a passo, com «Ou, se preferirem» em cada etapa, "
           "3 sugestões, 3 perguntas e o que medimos. Só negócios com WhatsApp provado no site (Tomás, 13/10). Não sai grátis: a vertente "
           "escolhida é a primeira execução, paga, com valor fechado na reunião. A mensagem leva o lema e pachecost.com; o PDF vai anexado, nunca link.", ""]
    for i, s in enumerate(ORDEM, 1):
        c = cands[s]
        pasta = os.path.join(SAIDA, s)
        os.makedirs(pasta, exist_ok=True)
        h = os.path.join(pasta, f"triagem-{s}.html")
        open(h, "w", encoding="utf-8").write(pagina(s, c))
        pdf(h, h[:-5] + ".pdf")
        out += [f"## {i}. {nome(s, c)} · {c.get('categoria', '')}", "",
                f"- Telefone {c['telefone']} · WhatsApp: sim (no site) · Google {c['nota']} · {c['avaliacoes']} avaliações",
                f"- Morada: a confirmar ({CIDADE[s]}) · site {c['site']}",
                f"- PDF (dono): {RAW}/{s}/triagem-{s}.pdf", "", "```", mensagem(s, c), "```", ""]
        print("ok", s)
    open(os.path.join(RAIZ, "raio-x", "ENVIAR-PT-lote-3.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
