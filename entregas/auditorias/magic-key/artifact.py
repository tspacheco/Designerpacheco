# Gera artifact.html (leitura no telemóvel) a partir de dados.py. Uso: python3 artifact.py
import html, pathlib
from dados import A, B, NUMEROS, HIPOTESES, SYSTEM_PRINT
e = html.escape
def parte(titulo, grupos, c):
    out = [f"<h2 class='parte'>{e(titulo)}</h2>"]
    for num, tit, quem, nota, qs in grupos:
        li = ""
        for ess, pt, ro, dica in qs:
            c[0] += 1
            li += f"<li><span class='n'>{c[0]:02d}{' ★' if ess else ''}</span><p class='pt'>{e(pt)}</p><p class='ro' lang='ro'>{e(ro)}</p>{f'<p class=dica>{e(dica)}</p>' if dica else ''}</li>"
        out.append(f"<details open><summary><b>{e(num)}</b> {e(tit)}<small>{e(quem)}</small></summary>{f'<p class=nota>{e(nota)}</p>' if nota else ''}<ol>{li}</ol></details>")
    return "".join(out)
c = [0]
a = parte("Parte A · O método", A, c); b = parte("Parte B · Magic Key", B, c)
sp = "".join(f"<tr><th>{e(x)}</th><td>{e(y)}</td></tr>" for x, y in SYSTEM_PRINT)
nm = "".join(f"<tr><td>{e(x)}</td><td>{e(u)}</td><td class=j>{e(j)}</td></tr>" for x, u, j in NUMEROS)
hp = "".join(f"<li><b>{e(x)}.</b> {e(y)}</li>" for x, y in HIPOTESES)
page = f"""<title>Magic Key, plano de perguntas</title>
<style>
:root{{--bg:#f6f3ee;--fg:#1c1a18;--mut:#5b5650;--card:#fff;--line:#ddd6cb;--acc:#a64923;--hi:#e8622c}}
@media (prefers-color-scheme:dark){{:root:not([data-theme=light]){{--bg:#141210;--fg:#efeae3;--mut:#a5a19b;--card:#1f1c19;--line:#3a3632;--acc:#f08a5d;--hi:#e8622c;color-scheme:dark}}}}
:root[data-theme=dark]{{--bg:#141210;--fg:#efeae3;--mut:#a5a19b;--card:#1f1c19;--line:#3a3632;--acc:#f08a5d;--hi:#e8622c;color-scheme:dark}}
body{{background:var(--bg);color:var(--fg);font:16px/1.5 system-ui,sans-serif;padding-inline:16px;padding-block:20px;max-width:720px;margin-inline:auto}}
h1{{font:800 28px/1.1 system-ui,sans-serif;text-transform:uppercase;margin:0 0 6px;text-wrap:balance}}
.sub{{color:var(--mut);margin:0 0 16px}}
.aviso{{background:var(--card);border:1px solid var(--hi);border-radius:8px;padding:12px;font-size:14px;margin-bottom:16px}}
h2{{font:700 13px system-ui;letter-spacing:.1em;text-transform:uppercase;color:var(--acc);margin:28px 0 8px}}
details{{background:var(--card);border:1px solid var(--line);border-radius:8px;margin-bottom:10px}}
summary{{padding:12px;cursor:pointer;font-weight:600;display:grid;gap:2px}}
summary b{{color:var(--acc)}} summary small{{color:var(--mut);font-weight:400}}
summary:focus-visible{{outline:2px solid var(--hi)}}
.nota{{margin:0 12px 8px;color:var(--mut);font-size:14px}}
ol{{list-style:none;margin:0;padding:0 12px 4px}} li{{border-top:1px solid var(--line);padding:10px 0}}
.n{{font:700 12px ui-monospace,monospace;color:var(--acc)}} p{{margin:2px 0}} .pt{{font-weight:600}} .ro{{color:var(--mut);font-style:italic;font-size:15px}} .dica{{font-size:13px;color:var(--acc)}}
table{{border-collapse:collapse;width:100%;font-size:14px}} td,th{{border-bottom:1px solid var(--line);padding:8px 6px;text-align:left;vertical-align:top}} th{{color:var(--acc);width:5.5em}} .j{{color:var(--mut)}}
.wrap{{overflow-x:auto}} ul{{padding-left:18px}}
</style>
<h1>Magic Key, plano de perguntas</h1>
<p class="sub">Auditoria · Iași · {c[0]} perguntas, ★ = essenciais · PT para ti, RO para o dono</p>
<p class="aviso"><b>Parte A por confirmar.</b> A transcrição do vídeo de 2 horas ainda não foi obtida (o YouTube bloqueia as legendas). A Parte A vem dos artigos do autor e do guião do Society Salon; confirma-se quando houver a transcrição.</p>
{a}{b}
<h2 class="parte">System Print a validar</h2><div class="wrap"><table>{sp}</table></div>
<h2 class="parte">Hipóteses (não dizer antes de ele falar)</h2><ul>{hp}</ul>
<h2 class="parte">Números para as contas</h2><div class="wrap"><table>{nm}</table></div>
"""
pathlib.Path(__file__).with_name("artifact.html").write_text(page, encoding="utf-8")
