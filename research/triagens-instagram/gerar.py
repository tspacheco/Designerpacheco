#!/usr/bin/env python3
"""Triagens (Micro System Print de 1 página) a partir do Instagram, no formato final do Iulian Paraschiv (11/10).

  python3 research/triagens-instagram/gerar.py   → <slug>.pdf e <slug>.png (o PNG vai na DM do Instagram)

Pedido do Tomás (12/10): ajudar e recomendar. Só sinais públicos dos posts; não é diagnóstico: em cada etapa o caminho
Pacheco Studios e, por baixo, a alternativa «se preferires». Sem preços nem números inventados. Fecho do Iulian + (Tomás, 12/10) criamos e apresentamos; se quiser ficar, só se cobra a manutenção.
"""
import base64, os, subprocess

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
CHROMIUM = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

BASE = dict(lang="pt-PT", supra="Triagem · Micro System Print", data="Outubro 2026", tel="+351 967 117 357", site="pachecost.com",
            aviso="Não é um diagnóstico do teu negócio: é o caminho que nós, Pacheco Studios, montaríamos, eficiente em cada passo. Cada um trabalha à sua maneira; escolhe o que te serve.",
            etapas_t="O caminho Pacheco Studios, passo a passo", ou="Ou, se preferires:", qw_t="As nossas 3 sugestões",
            perg_t="3 perguntas para ti", met_t="O que medimos",
            prox="Próximo passo: tu podes escolher 3 destas vertentes e implementamos sem qualquer custo.<small>O intuito é provar o nosso valor e, quando houver oportunidade de nos recomendares, fazer acontecer.</small><small>Nós vamos criar estas vertentes e apresentá-las a ti. Caso queiras ficar com elas, apenas cobramos o valor de manutenção, para as ferramentas poderem estar ativas e online.</small>")

T = {
 "cristina-tomas-fisio": dict(BASE, titulo="Cristina Tomás",
  h1="Cristina Tomás<br><em>O caminho de uma inscrição, do post à próxima formação.</em>",
  etapas=[("Interesse", "Cada post de evento ou formação leva um link de inscrição; as perguntas por DM, WhatsApp ou e-mail caem num só sítio, com resposta imediata.",
           "resposta automática só fora de horas ou durante as sessões; o resto respondes tu."),
          ("Inscrição", "Um formulário curto recolhe nome, contacto, evento e, na formação, experiência e objetivo; a vaga fica reservada e o número de lugares atualiza-se.",
           "recebes cada inscrição resumida e confirmas tu."),
          ("Pagamento", "Link de pagamento (MB Way ou cartão) e recibo automático; o lugar só fica garantido quando o pagamento entra.",
           "lembrete automático se o pagamento não entrar até à data combinada."),
          ("Antes", "Lembretes na véspera e no próprio dia (local, hora, o que levar); na formação online, os links e os conteúdos gravados chegam sozinhos.",
           "só uma mensagem de confirmação na véspera."),
          ("Sessão", "Presenças no telemóvel e, no fim, um QR para deixar opinião ou marcar uma consulta de fisioterapia.",
           "só a lista de presenças; o resto fica para depois."),
          ("Depois", "Cada participante recebe o evento seguinte que lhe interessa (energética, yin, fisioterapia) e os testemunhos viram conteúdo.",
           "um aviso por mês com a agenda, só para quem o pediu.")],
  qw=[("Inscrições e vagas", "Passos 1 e 2: cada post com inscrição direta, respostas imediatas e lugares contados."),
      ("Pagamentos e recibos", "Passo 3: link de pagamento e recibo, e o lugar confirma-se sozinho."),
      ("Lembretes e regresso", "Passos 4 e 6: ninguém falta por esquecimento e quem veio sabe do próximo evento.")],
  alt="Outras vertentes: uma só agenda para fisioterapia, eventos e formações · conteúdo a partir dos testemunhos · parcerias com outros espaços.",
  perg=["Que passos gostas de fazer pessoalmente?", "Onde se vai mais tempo hoje: perguntas, inscrições ou pagamentos?",
        "O que queres encher primeiro: formações, eventos ou consultas?"],
  met=["Tempo até à primeira resposta", "Interessados → inscritos → pagos", "Participantes que voltam a outro evento"]),
 "bruno-pereira-judo-lanheses": dict(BASE, titulo="Bruno Pereira · Judo em Lanheses",
  h1="Bruno Pereira · Judo em Lanheses<br><em>O caminho de um aluno, do primeiro contacto à próxima graduação.</em>",
  etapas=[("Contacto", "Quem liga ou escreve para o teu número recebe logo horários, idades e morada da Junta, e o contacto fica registado.",
           "resposta automática só durante as aulas; fora disso atendes tu."),
          ("Aula experimental", "Marcação da primeira aula numa segunda ou sexta, com lembrete na véspera e o que trazer.",
           "a marcação chega-te resumida e confirmas tu."),
          ("Inscrição", "Ficha do aluno (e do encarregado de educação, nas crianças) e autorizações preenchidas no telemóvel, antes do tatami.",
           "ficha em papel, passada a digital com uma fotografia."),
          ("Mensalidade", "Pagamento por MB Way ou referência, recibo automático e aviso só a quem estiver em atraso.",
           "registo dos pagamentos numa folha simples, com lembrete mensal para ti."),
          ("Aulas", "Presenças com um toque e aviso automático aos alunos e aos pais se uma aula mudar.",
           "só um grupo de WhatsApp com avisos."),
          ("Depois", "Cada graduação vira conteúdo (com autorização) e as famílias recebem um convite para trazer um amigo a uma aula.",
           "uma aula aberta por trimestre, anunciada a todos.")],
  qw=[("Primeiro contacto", "Passos 1 e 2: resposta imediata, mesmo durante a aula, e a aula experimental marcada."),
      ("Fichas e mensalidades", "Passos 3 e 4: inscrição no telemóvel, recibos e avisos de atraso sem conversas difíceis."),
      ("Recomendações", "Passo 6: as famílias que já estão trazem as próximas.")],
  alt="Outras vertentes: turmas por idade quando o grupo crescer · parcerias com escolas e associações · página simples com horários e inscrição.",
  perg=["Que passos queres continuar a fazer pessoalmente?", "O que te ocupa mais tempo fora do tatami?",
        "Que turma queres encher primeiro: crianças, jovens ou adultos?"],
  met=["Contactos → aula experimental → inscritos", "Alunos que continuam ao fim de 3 meses", "Novos alunos vindos de recomendação"]),
}


def fonte(nome, ficheiro, peso):
    b = base64.b64encode(open(os.path.join(RAIZ, "marca", "fontes", ficheiro), "rb").read()).decode()
    return f"@font-face{{font-family:'{nome}';font-weight:{peso};src:url(data:font/woff2;base64,{b}) format('woff2')}}"


FONTES = "\n".join([fonte("Archivo Black", "archivo-black-ro.woff2", 400), fonte("Inter", "inter-400-ro.woff2", 400),
                    fonte("Inter", "inter-600-ro.woff2", 600), fonte("Space Mono", "space-mono-700-ro.woff2", 700)])

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


def html(t):
    etapas = "".join(f'<div><i>0{i+1}</i><b>{a}</b><span>{b}</span><em><strong>{t["ou"]}</strong> {c}</em></div>'
                     for i, (a, b, c) in enumerate(t["etapas"]))
    qw = "".join(f"<div><i>0{i+1}</i><b>{a}</b><span>{b}</span></div>" for i, (a, b) in enumerate(t["qw"]))
    perg = "".join(f"<li>{x}</li>" for x in t["perg"])
    met = "".join(f"<li>{x}</li>" for x in t["met"])
    return f"""<!doctype html><html lang="{t['lang']}"><head><meta charset="utf-8"><title>Triagem {t["titulo"]}</title>
<style>{FONTES}{CSS}</style></head><body><section class="pag">
<div class="topo"><div class="l1"><span class="marca">Pacheco Studios<i></i></span><span class="mono">{t['data']}</span></div>
<span class="mono sup">{t['supra']}</span><h1>{t['h1']}</h1><p class="aviso">{t['aviso']}</p></div>
<div class="corpo">
<div><h3>{t['etapas_t']}</h3><div class="etapas">{etapas}</div></div>
<div><h3>{t['qw_t']}</h3><div class="qw">{qw}</div><p class="alt">{t['alt']}</p></div>
<div class="duas"><div><h3>{t['perg_t']}</h3><ol>{perg}</ol></div><div><h3>{t['met_t']}</h3><ul>{met}</ul></div></div>
<div class="prox">{t['prox']}</div>
</div><footer class="rod"><span class="marca">Pacheco Studios<i></i></span><span>Tomás Pacheco · {t['tel']} · {t['site']}</span></footer>
</section></body></html>"""


for slug, t in T.items():
    h = os.path.join(AQUI, f"{slug}.html")
    open(h, "w", encoding="utf-8").write(html(t))
    p = h[:-5] + ".pdf"
    subprocess.run([CHROMIUM, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={p}", "file://" + h], check=True, capture_output=True)
    subprocess.run(["pdftoppm", "-png", "-r", "130", "-singlefile", p, h[:-5]], check=True)
    print("ok", os.path.relpath(p, RAIZ))
