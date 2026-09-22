#!/usr/bin/env python3
"""Tabela mês a mês (clientes novos · que voltam · faturamento), atrás de um botão.
No ecrã abre com o botão; ao imprimir/exportar PDF fica sempre aberta no nível R$ 800."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "be-legend-olhao"))
from build import esc
from build_checklist import S, TICKET, RECOR

CHURN_REF = 0.15   # cenário de abandono usado só na nota de rodapé

def linhas(nivel, churn=0.0):
    novos = S[nivel]["novos"]
    out = []
    for m in range(1, 7):
        volta = sum(novos * RECOR * (1 - churn) ** (m - 1 - c) for c in range(m - 1))
        out.append((m, novos, volta, novos + volta, (novos + volta) * TICKET))
    return out

def total(nivel, churn=0.0):
    return sum(l[4] for l in linhas(nivel, churn))

def n0(x): return f"{x:,.0f}".replace(",", ".")
def r(x):  return "R$ " + n0(x)

def tabela(nivel):
    tr = "".join(
        f'<tr><td class="lab">Mês {m}</td><td>{n0(nv)}</td><td>{n0(v)}</td>'
        f'<td>{n0(a)}</td><td class="hl">{r(f)}</td></tr>'
        for m, nv, v, a, f in linhas(nivel))
    tot = total(nivel)
    return (f'<table class="tbl num2 mmt" data-n="{nivel}">'
            f'<thead><tr><th></th><th>Clientes novos</th><th>Que voltam</th>'
            f'<th>Atendimentos</th><th class="hl">Faturamento</th></tr></thead>'
            f'<tbody>{tr}</tbody>'
            f'<tfoot><tr><td class="lab">6 meses</td><td colspan="3"></td>'
            f'<td class="hl">{r(tot)}</td></tr></tfoot></table>')

def bloco():
    chips = "".join(
        f'<button type="button" class="mmc{" on" if b == 800 else ""}" data-n="{b}">{r(b)}/mês</button>'
        for b in (400, 800, 1500))
    tabs = "".join(
        f'<div class="mmw{" on" if b == 800 else ""}" data-n="{b}">{tabela(b)}</div>'
        for b in (400, 800, 1500))
    queda = 1 - total(800, CHURN_REF) / total(800)
    return f'''
<button type="button" class="mmb" id="mmb" aria-expanded="false" aria-controls="mm">
  <span class="ico" aria-hidden="true">+</span><span class="tx">Ver mês a mês</span>
</button>
<div class="mm" id="mm">
  <div class="mmchips" role="group" aria-label="Nível de investimento">{chips}</div>
  {tabs}
  <p class="fine">O investimento fica igual todos os meses: o que cresce é a camada de clientes que voltam. Se {CHURN_REF*100:.0f} % dos fidelizados deixarem de vir a cada mês, o total de seis meses cai cerca de {queda*100:.0f} %.</p>
</div>'''

JS = """
(function(){
  var b=document.getElementById('mmb'), m=document.getElementById('mm');
  if(!b||!m) return;
  b.addEventListener('click',function(){
    var o=b.getAttribute('aria-expanded')==='true';
    b.setAttribute('aria-expanded',!o);
    m.classList.toggle('on',!o);
    b.querySelector('.ico').textContent=o?'+':'\\u2212';
    b.querySelector('.tx').textContent=o?'Ver mês a mês':'Esconder';
  });
  document.querySelectorAll('.mmc').forEach(function(c){
    c.addEventListener('click',function(){
      var n=c.dataset.n;
      document.querySelectorAll('.mmc').forEach(function(x){x.classList.toggle('on',x===c)});
      document.querySelectorAll('.mmw').forEach(function(w){w.classList.toggle('on',w.dataset.n===n)});
    });
  });
})();
"""

CSS = """
.mmb{display:inline-flex;align-items:center;gap:8px;margin-top:10px;background:var(--navy);color:#fff;border:0;border-radius:999px;padding:8px 16px;font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:12.5pt;cursor:pointer}
.mmb .ico{display:inline-grid;place-items:center;width:17px;height:17px;border-radius:50%;background:var(--gold);color:var(--navy);font-size:11pt;line-height:1}
.mm{display:none;margin-top:8px;border:1px solid #EAE5DA;border-radius:12px;padding:12px 14px;background:var(--paper)}
.mm.on{display:block}
.mmchips{display:flex;gap:6px;margin-bottom:8px}
.mmc{border:1.5px solid var(--navy);background:#fff;color:var(--navy);border-radius:999px;padding:4px 12px;font-family:'JetBrains Mono',monospace;font-size:8.5pt;cursor:pointer}
.mmc.on{background:var(--navy);color:#fff}
.mmw{display:none}.mmw.on{display:block}
.tbl.mmt{margin:0}
.tbl.mmt td,.tbl.mmt th{padding:4.5px 8px;font-size:9.2pt}
.tbl.mmt tfoot td{border-top:1.5px solid var(--navy);border-bottom:0;font-weight:700;color:var(--navy);padding-top:6px}
.mm .fine{margin-top:6px}
@media print{
  .mmb{display:none}
  .tbl.mmt td,.tbl.mmt th{padding:3px 8px;font-size:8.8pt}
  .mm .fine{margin-top:4px}
  .mm{display:block;border:0;padding:0;background:transparent;margin-top:4px}
  .mmchips{display:none}
  .mmw{display:none}.mmw[data-n="800"]{display:block}
}
"""
