# Plano de perguntas da auditoria Magic Key. Gera plano.html e Magic-Key-plano-de-perguntas.pdf.
# Uso: python3 gerar.py  (precisa do Chromium do Playwright)
import html, pathlib
from dados import A, B, NUMEROS, HIPOTESES, SYSTEM_PRINT

AQUI = pathlib.Path(__file__).parent
FONTES = (AQUI / "../../../marca/fontes").resolve()
e = html.escape

def bloco(num, titulo, quem, nota, perguntas, cont):
    li = []
    for ess, pt, ro, dica in perguntas:
        cont[0] += 1
        li.append(f"""<li class="q{' ess' if ess else ''}"><span class="n">{cont[0]:02d}</span><div class="corpo">
<p class="pt">{e(pt)}</p><p class="ro" lang="en">{e(ro)}</p>{f'<p class="dica">{e(dica)}</p>' if dica else ''}
<div class="linhas" aria-hidden="true"><i></i><i></i></div></div></li>""")
    return f"""<section class="bloco"><header class="bloco-cab"><span class="bn">{e(num)}</span>
<div><h2>{e(titulo)}</h2><p class="quem">{e(quem)}</p></div></header>
{f'<p class="bnota">{e(nota)}</p>' if nota else ''}<ol class="qs">{''.join(li)}</ol></section>"""

def gerar():
    cont = [0]
    ba = "".join(bloco(*b, cont) for b in A); na = cont[0]
    bb = "".join(bloco(*b, cont) for b in B); nb = cont[0] - na
    ess = sum(q[0] for g in A + B for q in g[4])
    num = "".join(f"<tr><td>{e(a)}</td><td class='un'>{e(u)}</td><td class='val'></td><td class='ja'>{e(j)}</td></tr>" for a, u, j in NUMEROS)
    hip = "".join(f"<li><b>{e(a)}.</b> {e(b)}</li>" for a, b in HIPOTESES)
    sp = "".join(f"<tr><td>{e(a)}</td><td>{e(b)}</td><td class='em'></td></tr>" for a, b in SYSTEM_PRINT)
    css = (AQUI / "estilo.css").read_text(encoding="utf-8").replace("FONTES/", FONTES.as_uri() + "/")
    doc = f"""<!doctype html><html lang="pt-PT"><head><meta charset="utf-8"><title>Magic Key — plano de perguntas da auditoria</title>
<style>{css}</style></head><body>
<section class="capa"><div class="marca">PACHECO STUDIOS<span class="ponto"></span></div>
<div class="capa-meio"><p class="kicker">Auditoria de sistemas com IA · plano de perguntas</p>
<h1>Magic Key<br>chei auto</h1><p class="sub">Iași · Selgros, Șos. Nicolina 57A</p></div>
<dl class="capa-dados"><div><dt>Para</dt><dd>Tomás Pacheco (uso interno)</dd></div><div><dt>Data</dt><dd>outubro de 2026</dd></div>
<div><dt>Perguntas</dt><dd>{na + nb} · {ess} essenciais ★</dd></div><div><dt>Línguas</dt><dd>PT para ti, EN para perguntar</dd></div></dl></section>

<section class="pagina intro"><h2 class="titulo">Como usar</h2>
<p class="honesto"><b>Estado da Parte A.</b> A transcrição do vídeo de 2 horas ainda não foi obtida: o YouTube bloqueia as legendas nesta sessão. A Parte A foi reconstruída dos artigos do autor (Andrew Dunn) e do guião que já usámos no Society Salon. Quando tivermos a transcrição, confirma-se palavra a palavra e acrescenta-se o que o vídeo diga a mais.</p>
<div class="duas"><div>
<h3>Como se lê</h3>
<ul class="pts"><li><b>Parte A, o método.</b> Perguntas que servem em qualquer auditoria. Ordem do vídeo: objetivo, o dia de ontem, os três motores, o fecho.</li>
<li><b>Parte B, Magic Key.</b> Perguntas só deste negócio, com o que já sabemos (ficha Google, lista de preços do stand, os 3 quick wins).</li>
<li><b>★</b> marca as essenciais. Pouco tempo? Faz só essas.</li>
<li>Cada pergunta tem a versão em inglês para ler ao dono e linhas para as respostas.</li></ul>
<h3>Regras da conversa</h3>
<ul class="pts"><li><b>Pedir para gravar</b> (com autorização e o acordo de confidencialidade assinado) e transcrever depois.</li>
<li><b>Perguntar sempre «e depois?»</b> até a tarefa não dar para partir mais.</li>
<li><b>Não sugerir soluções.</b> Só ouvir e anotar tempos.</li>
<li><b>Cada problema sai com um número:</b> estado atual, alvo e valor em lei.</li>
<li>Dado não confirmado fica «a confirmar». Nada de números inventados.</li></ul></div>
<div><h3>Abertura (dizer assim)</h3><blockquote>
<p>«Isto não é uma venda. Vou fazer-te perguntas sobre como o stand funciona no dia a dia. Depois volto com o mapa de onde se perdem pedidos, tempo e dinheiro e o que vale a pena fazer primeiro, com as contas. Decides tu.»</p>
<p lang="en" class="ro">"This is not a sales pitch. I'll ask you how the stand works day to day. Then I'll come back with a map of where requests, time and money get lost and what is worth doing first, with the numbers. You decide."</p></blockquote>
<h3>O que desenhas a seguir</h3><div class="motores"><div><b>Clientes novos</b><span>como os encontram</span></div><div><b>O trabalho</b><span>o pedido e a chave</span></div><div><b>Retorno</b><span>avaliações e indicações</span></div></div>
<p class="leg"><span class="tag t">Tempo</span> manual e repetitivo · <span class="tag r">Risco</span> onde há erros</p>
<h3>Antes de ir</h3><ul class="pts"><li>Levar a foto da lista de preços de 09/10 e a Parte 1 da auditoria (vista de fora).</li><li>Confirmar no telemóvel as avaliações do Google (4,5 em 53 na última leitura).</li><li>Acordo de confidencialidade assinado antes de gravar.</li></ul></div></div></section>

<section class="parte"><p class="k">Parte A</p><h2>O método</h2><p>As perguntas do curso de consultoria de IA, para qualquer auditoria: objetivo, o dia de ontem, os três motores e a validação. {na} perguntas.</p></section>
{ba}
<section class="parte"><p class="k">Parte B</p><h2>Magic Key</h2><p>As perguntas só deste negócio, em torno dos três quick wins do piloto: pedido de chave auto pelo telemóvel, pedidos de avaliação e assistente no WhatsApp. {nb} perguntas.</p></section>
{bb}

<section class="pagina"><h2 class="titulo">System Print a validar</h2>
<p class="lead">A hipótese da rececionista, na estrutura Trigger, Dono, Regra e Handoff. Preenche com as palavras do dono, não com as nossas.</p>
<table class="sp"><thead><tr><th></th><th>Hipótese nossa</th><th>O que o dono diz</th></tr></thead><tbody>{sp}</tbody></table>
<h3 style="margin-top:8mm">Hipóteses a confirmar</h3><p class="aviso">Não dizer ao dono antes de ele falar. Servem só para saberes onde escavar.</p><ul class="pts">{hip}</ul></section>

<section class="pagina"><h2 class="titulo">Números para as contas</h2>
<p class="lead">Preencher na conversa. Se for estimativa do dono, escrever «est.» ao lado.</p>
<table class="num"><thead><tr><th>O quê</th><th>Unidade</th><th>Valor</th><th>O que já sabemos</th></tr></thead><tbody>{num}</tbody></table>
<div class="formula"><p class="k">A conta de cada problema</p>
<p class="f">pedidos perdidos por semana × preço médio × 52 = <b>receita perdida por ano</b></p>
<p class="f">horas por semana × custo de 1 hora × 52 = <b>custo do tempo por ano</b></p></div></section>

<section class="pagina"><h2 class="titulo">Depois da conversa</h2><div class="duas"><div>
<h3>1. Filtro das 4 perguntas</h3><p>Para cada passo do mapa. Quatro «sim» = candidato a automatizar.</p>
<ol class="filtro"><li>A entrada é estruturada? (formulário, mensagem)</li><li>A saída é previsível? (resposta padrão, lembrete)</li><li>A decisão segue regras? (se… então…)</li><li>Repete-se todos os dias ou todas as semanas?</li></ol>
<h3>2. Validação com o dono</h3><p>Antes de entregar: «Destas três vitórias rápidas, qual bate mais com o que vives? Falta alguma coisa?»</p></div>
<div><h3>3. Matriz de oportunidades</h3><div class="matriz"><span class="eixo y">valor para o negócio ↑</span>
<div class="q1"><b>Vitórias rápidas</b><span>fácil · valor alto · começar aqui</span></div><div class="q2"><b>Grandes apostas</b><span>difícil · valor alto · fase 2</span></div>
<div class="q3"><b>Extras</b><span>fácil · valor baixo · mais tarde</span></div><div class="q4"><b>Evitar</b><span>difícil · valor baixo</span></div><span class="eixo x">dificuldade →</span></div>
<h3>4. O que o dono recebe</h3><ol class="entrega"><li>O que nos pediu para ver</li><li>O mapa do negócio, com tempo e erros marcados</li><li>A matriz de oportunidades</li><li>As 3 vitórias rápidas: antes e depois, contas</li><li>Quanto vale tudo junto por ano</li><li>Plano de 90 dias</li></ol></div></div></section>
</body></html>"""
    (AQUI / "plano.html").write_text(doc, encoding="utf-8")
    return na, nb, ess

def pdf():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        pg = b.new_page(); pg.goto((AQUI / "plano.html").as_uri(), wait_until="networkidle"); pg.evaluate("document.fonts.ready")
        pg.pdf(path=str(AQUI / "Magic-Key-plano-de-perguntas.pdf"), format="A4", print_background=True,
               margin={"top": "0", "bottom": "0", "left": "0", "right": "0"}, prefer_css_page_size=True)
        b.close()

if __name__ == "__main__":
    print(gerar()); pdf()
