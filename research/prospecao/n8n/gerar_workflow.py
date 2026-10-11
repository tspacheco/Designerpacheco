"""Gera prospecao-n8n.json (importar no n8n: Workflows → Import from File).

Depois de importar, só se mudam três coisas no n8n (nunca neste repositório):
  1. o URL da Google Sheet nos nós de Google Sheets (COLAR_URL_DA_FOLHA);
  2. a credencial Google Sheets e a credencial Gmail;
  3. o e-mail do Tomás no nó «Enviar fila ao Tomás» (COLAR_O_TEU_EMAIL).
"""
import json
import os

FOLHA = {"__rl": True, "mode": "url", "value": "COLAR_URL_DA_FOLHA"}
ABA = {"__rl": True, "mode": "name", "value": "Prospeção"}

PARSE = r"""
const hoje = new Date(); hoje.setHours(0,0,0,0);
function dataPT(v) {
  if (!v) return null;
  if (typeof v === 'number') { const d = new Date(Date.UTC(1899,11,30) + v*86400000); d.setHours(0,0,0,0); return d; }
  const m = String(v).match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})/);
  if (m) return new Date(+m[3], +m[2]-1, +m[1]);
  const d = new Date(v); return isNaN(d) ? null : d;
}
function fmt(d) { return String(d.getDate()).padStart(2,'0') + '/' + String(d.getMonth()+1).padStart(2,'0') + '/' + d.getFullYear(); }
function mais(dias) { const d = new Date(hoje); d.setDate(d.getDate()+dias); return fmt(d); }
const linhas = $input.all().map(i => i.json);
"""

ESCOLHER_EMAILS = PARSE + r"""
// E-mails novos (Validado, prioridade 4–5) e follow-ups vencidos. Máx. 15 por dia.
const novos = linhas.filter(r => r['Estado'] === 'Validado' && r['Canal'] === 'E-mail' && r['E-mail'] && Number(r['Prioridade']) >= 4)
  .sort((a,b) => Number(b['Score']) - Number(a['Score']))
  .map(r => ({ ID: r['ID'], para: r['E-mail'], assunto: r['Assunto e-mail'], corpo: r['Mensagem'],
               estado: 'Contactado', acao: 'Follow-up por e-mail', proxima: mais(5), contacto: fmt(hoje) }));
const follow = linhas.filter(r => r['Estado'] === 'Contactado' && r['Canal'] === 'E-mail' && r['E-mail'] && r['Follow-up']
    && dataPT(r['Data próxima acção']) && dataPT(r['Data próxima acção']) <= hoje)
  .map(r => ({ ID: r['ID'], para: r['E-mail'], assunto: 'Re: ' + r['Assunto e-mail'], corpo: r['Follow-up'],
               estado: 'Sem resposta', acao: 'Parar; voltar só com motivo novo', proxima: '', contacto: r['Data contacto'] || fmt(hoje) }));
return follow.concat(novos).slice(0, 15).map(j => ({ json: j }));
"""

FILA_DMS = PARSE + r"""
// Instagram não permite DMs automáticas a quem não escreveu primeiro: o n8n prepara a fila e o Tomás envia do telemóvel.
const dms = linhas.filter(r => r['Estado'] === 'Validado' && r['Canal'] === 'DM' && r['Link DM'] && Number(r['Prioridade']) >= 3)
  .sort((a,b) => Number(b['Score']) - Number(a['Score'])).slice(0, 10);
const follow = linhas.filter(r => r['Estado'] === 'Contactado' && r['Canal'] === 'DM' && r['Follow-up']
    && dataPT(r['Data próxima acção']) && dataPT(r['Data próxima acção']) <= hoje);
const coms = linhas.filter(r => r['Canal'] === 'Comentário' && ['Validado','Contactado'].includes(r['Estado'])).slice(0, 5);
if (!dms.length && !follow.length && !coms.length) return [];
const bloco = (r, txt) => `${r['Nome']} (${r['Instagram']}) · prioridade ${r['Prioridade']}\nAbrir DM: ${r['Link DM']}\n\n${txt}\n\n————————\n`;
let corpo = `Fila de hoje (${fmt(hoje)}). Envia 1 por minuto e marca «Contactado» na folha.\n\n`;
if (dms.length) corpo += `DMs NOVAS (${dms.length})\n\n` + dms.map(r => bloco(r, r['Mensagem'])).join('\n');
if (follow.length) corpo += `\nFOLLOW-UPS (${follow.length}) — depois marca «Sem resposta» se não responderem\n\n` + follow.map(r => bloco(r, r['Follow-up'])).join('\n');
if (coms.length) corpo += `\nCOMENTAR (${coms.length}) — um comentário útil no post de hoje; arranques na aba «Comentários»\n\n` +
  coms.map(r => `${r['Nome']} · ${r['URL Instagram'] || r['Instagram']}`).join('\n');
return [{ json: { assunto: `Instagram: ${dms.length} DMs, ${follow.length} follow-ups, ${coms.length} comentários`, corpo } }];
"""

DATAR_DMS = PARSE + r"""
// DMs que o Tomás marcou «Contactado» sem data: data de hoje e follow-up a 5 dias.
return linhas.filter(r => r['Estado'] === 'Contactado' && r['Canal'] === 'DM' && !r['Data contacto'])
  .map(r => ({ json: { ID: r['ID'], contacto: fmt(hoje), proxima: mais(5), acao: 'Follow-up por DM' } }));
"""


def schema(cols):
    return [{"id": c, "displayName": c, "required": False, "defaultMatch": c == "ID", "display": True,
             "type": "string", "canBeUsedToMatch": True} for c in cols]


def atualizar(nome, pos, valores):
    return {
        "parameters": {
            "operation": "update", "documentId": FOLHA, "sheetName": ABA,
            "columns": {"mappingMode": "defineBelow", "value": valores, "matchingColumns": ["ID"],
                        "schema": schema(list(valores))},
            "options": {},
        },
        "name": nome, "type": "n8n-nodes-base.googleSheets", "typeVersion": 4.5, "position": pos,
    }


def code(nome, js, pos):
    return {"parameters": {"jsCode": js.strip()}, "name": nome, "type": "n8n-nodes-base.code",
            "typeVersion": 2, "position": pos}


nodes = [
    {"parameters": {"rule": {"interval": [{"field": "cronExpression", "expression": "0 10 * * 1-5"}]}},
     "name": "Dias úteis 10h", "type": "n8n-nodes-base.scheduleTrigger", "typeVersion": 1.2, "position": [0, 300]},
    {"parameters": {"operation": "read", "documentId": FOLHA, "sheetName": ABA, "options": {}},
     "name": "Ler base", "type": "n8n-nodes-base.googleSheets", "typeVersion": 4.5, "position": [220, 300],
     "alwaysOutputData": True},
    code("Escolher e-mails", ESCOLHER_EMAILS, [460, 120]),
    {"parameters": {"options": {}}, "name": "Um de cada vez", "type": "n8n-nodes-base.splitInBatches",
     "typeVersion": 3, "position": [680, 120]},
    {"parameters": {"sendTo": "={{ $json.para }}", "subject": "={{ $json.assunto }}", "emailType": "text",
                    "message": "={{ $json.corpo }}", "options": {"appendAttribution": False}},
     "name": "Enviar e-mail", "type": "n8n-nodes-base.gmail", "typeVersion": 2.1, "position": [900, 200]},
    atualizar("Marcar enviado", [1120, 200], {
        "ID": "={{ $('Um de cada vez').item.json.ID }}",
        "Estado": "={{ $('Um de cada vez').item.json.estado }}",
        "Data contacto": "={{ $('Um de cada vez').item.json.contacto }}",
        "Próxima acção": "={{ $('Um de cada vez').item.json.acao }}",
        "Data próxima acção": "={{ $('Um de cada vez').item.json.proxima }}",
    }),
    {"parameters": {"amount": 60}, "name": "Esperar 1 minuto", "type": "n8n-nodes-base.wait",
     "typeVersion": 1.1, "position": [1340, 200], "webhookId": "b3c1e0de-6a1f-4c55-9a7e-1f0a2d9c4e11"},
    code("Fila de DMs", FILA_DMS, [460, 380]),
    {"parameters": {"sendTo": "COLAR_O_TEU_EMAIL", "subject": "={{ $json.assunto }}", "emailType": "text",
                    "message": "={{ $json.corpo }}", "options": {"appendAttribution": False}},
     "name": "Enviar fila ao Tomás", "type": "n8n-nodes-base.gmail", "typeVersion": 2.1, "position": [680, 380]},
    code("Datar DMs enviadas", DATAR_DMS, [460, 560]),
    atualizar("Gravar datas das DMs", [680, 560], {
        "ID": "={{ $json.ID }}", "Data contacto": "={{ $json.contacto }}",
        "Próxima acção": "={{ $json.acao }}", "Data próxima acção": "={{ $json.proxima }}",
    }),
]

ligar = lambda *destinos: {"main": [[{"node": d, "type": "main", "index": 0} for d in destinos]]}
connections = {
    "Dias úteis 10h": ligar("Ler base"),
    "Ler base": ligar("Escolher e-mails", "Fila de DMs", "Datar DMs enviadas"),
    "Escolher e-mails": ligar("Um de cada vez"),
    "Um de cada vez": {"main": [[], [{"node": "Enviar e-mail", "type": "main", "index": 0}]]},
    "Enviar e-mail": ligar("Marcar enviado"),
    "Marcar enviado": ligar("Esperar 1 minuto"),
    "Esperar 1 minuto": ligar("Um de cada vez"),
    "Fila de DMs": ligar("Enviar fila ao Tomás"),
    "Datar DMs enviadas": ligar("Gravar datas das DMs"),
}

wf = {"name": "Pacheco Studios · Prospeção (e-mail + fila de Instagram)", "nodes": nodes,
      "connections": connections, "settings": {"executionOrder": "v1", "timezone": "Europe/Bucharest"},
      "active": False}
saida = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prospecao-n8n.json")
json.dump(wf, open(saida, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(saida)
