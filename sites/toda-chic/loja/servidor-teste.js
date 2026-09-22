#!/usr/bin/env node
// Servidor de TESTE da loja Toda Chic — corre no teu PC, sem dependências, sem rede.
//   node loja/servidor-teste.js            → http://localhost:8080  (loja)  ·  /painel.html (dona)
// O que faz: serve a pasta do site, guarda stock e encomendas em loja/dados/loja.json,
// reserva stock ao criar a encomenda, e SIMULA o MB WAY (confirma sozinho ao fim de 6 s;
// um telemóvel terminado em 0 faz o pagamento falhar, para testares esse caminho).
// A API é exatamente a mesma que a produção (Supabase + Easypay) implementa — ver loja/README.md.
'use strict';
const http = require('http'), fs = require('fs'), path = require('path'), crypto = require('crypto');

const RAIZ = path.resolve(__dirname, '..');
const DADOS = path.join(__dirname, 'dados', 'loja.json');
const PORTA = +process.env.PORTA || 8080;
const SENHA_PAINEL = process.env.PAINEL_SENHA || '123';          // troca em produção
const RESERVA_MIN = 60;                                              // minutos que uma encomenda pendente segura o stock
const MIME = {'.html':'text/html; charset=utf-8','.js':'text/javascript','.json':'application/json','.jpg':'image/jpeg','.jpeg':'image/jpeg','.png':'image/png','.svg':'image/svg+xml','.txt':'text/plain; charset=utf-8','.mp4':'video/mp4','.css':'text/css'};

/* ---------- base de dados: um ficheiro JSON ---------- */
function carrega(){
  if (!fs.existsSync(DADOS)) {
    const cat = JSON.parse(fs.readFileSync(path.join(RAIZ, 'catalogo.json'), 'utf8'));
    cat.pecas.forEach(p => p.cores.forEach(c => { if (typeof c.stock !== 'number') c.stock = 0; c.reservado = 0; c.foto = c.foto != null ? nomeFoto(c.foto) : null; }));
    cat.pecas.forEach(p => { if (p.fotos) p.fotos = p.fotos.map(nomeFoto); p.ativo = true; });
    fs.mkdirSync(path.dirname(DADOS), { recursive: true });
    fs.writeFileSync(DADOS, JSON.stringify({ categorias: cat.categorias, estacoes: cat.estacoes, pecas: cat.pecas, encomendas: [], seq: 1000 }, null, 1));
  }
  return JSON.parse(fs.readFileSync(DADOS, 'utf8'));
}
function nomeFoto(ref){ return typeof ref === 'object' ? `f${String(ref.ficha).padStart(3,'0')}-c${ref.cel}.jpg` : `f${String(ref).padStart(3,'0')}.jpg`; }
function grava(db){ fs.writeFileSync(DADOS, JSON.stringify(db, null, 1)); }
function agora(){ return new Date().toISOString(); }

/* ---------- regras de stock ---------- */
function expiraReservas(db){
  const limite = Date.now() - RESERVA_MIN * 60000;
  db.encomendas.forEach(e => {
    if (e.estado === 'pendente' && new Date(e.criada).getTime() < limite) { liberta(db, e); e.estado = 'expirada'; e.atualizada = agora(); }
  });
}
function liberta(db, e){ e.linhas.forEach(l => { const c = cor(db, l.peca, l.cor); if (c) c.reservado = Math.max(0, c.reservado - l.qt); }); }
function cor(db, pecaId, i){ const p = db.pecas.find(x => x.id === pecaId); return p && p.cores[i]; }
function disponivel(c){ return Math.max(0, (c.stock || 0) - (c.reservado || 0)); }
function catalogoPublico(db){
  return { categorias: db.categorias, estacoes: db.estacoes,
    pecas: db.pecas.filter(p => p.ativo !== false).map(p => Object.assign({}, p, { cores: p.cores.map(c => ({ nome: c.nome, hex: c.hex, foto: c.foto, stock: disponivel(c) })) })) };
}

/* ---------- encomendas ---------- */
function criaEncomenda(db, corpo){
  const erros = [];
  const cl = corpo.cliente || {};
  ['nome', 'telemovel', 'morada', 'cp', 'localidade'].forEach(k => { if (!cl[k] || String(cl[k]).trim().length < 2) erros.push('Falta ' + k); });
  if (!/^9\d{8}$/.test(String(cl.telemovel || '').replace(/\s/g, ''))) erros.push('O número MB WAY tem de ser um telemóvel português (9 dígitos, começa por 9)');
  if (!Array.isArray(corpo.linhas) || !corpo.linhas.length) erros.push('Saco vazio');
  if (erros.length) return { erro: erros.join(' · ') };
  const linhas = []; let total = 0;
  for (const l of corpo.linhas) {
    const p = db.pecas.find(x => x.id === l.peca && x.ativo !== false); const c = p && p.cores[l.cor];
    if (!p || !c) return { erro: 'Peça já não existe: ' + l.peca };
    if (p.preco == null) return { erro: p.nome + ' ainda não tem preço' };
    const qt = Math.max(1, Math.min(9, +l.qt || 1));
    if (disponivel(c) < qt) return { erro: 'Já não há stock suficiente de "' + p.nome + '" em ' + c.nome + ' (restam ' + disponivel(c) + ')' };
    linhas.push({ peca: p.id, nome: p.nome, cor: l.cor, corNome: c.nome, tam: l.tam, tamNome: (l.tam >= 0 && p.tamanhos[l.tam]) || 'Único', qt, preco: p.preco, foto: c.foto });
    total += p.preco * qt;
  }
  linhas.forEach(l => { cor(db, l.peca, l.cor).reservado += l.qt; });
  const e = { id: ++db.seq, token: crypto.randomBytes(16).toString('hex'), estado: 'pendente', linhas, cliente: { nome: cl.nome, telemovel: String(cl.telemovel).replace(/\s/g, ''), email: cl.email || '', morada: cl.morada, cp: cl.cp, localidade: cl.localidade, nif: cl.nif || '' },
    total: Math.round(total * 100) / 100, portes: 0, criada: agora(), atualizada: agora(), pagamento: null };
  db.encomendas.push(e);
  return { encomenda: e };
}
function marcaPaga(db, e){
  if (e.estado !== 'pendente') return;
  e.linhas.forEach(l => { const c = cor(db, l.peca, l.cor); if (c) { c.stock = Math.max(0, c.stock - l.qt); c.reservado = Math.max(0, c.reservado - l.qt); } });
  e.estado = 'paga'; e.paga = agora(); e.atualizada = agora();
}
function marcaFalhada(db, e, motivo){ if (e.estado !== 'pendente') return; liberta(db, e); e.estado = 'falhada'; e.motivo = motivo; e.atualizada = agora(); }

/* ---------- MB WAY simulado (no lugar da Easypay) ---------- */
function easypaySimulado(e){
  e.pagamento = { fornecedor: 'simulado', id: 'sim-' + e.token.slice(0, 8), metodo: 'mbw', estado: 'pendente', criado: agora() };
  const falha = /0$/.test(e.cliente.telemovel);
  setTimeout(() => {
    const db = carrega(); const en = db.encomendas.find(x => x.token === e.token); if (!en) return;
    // é isto que o webhook da Easypay faz na produção
    if (falha) { en.pagamento.estado = 'falhado'; marcaFalhada(db, en, 'MB WAY recusado (simulação: telemóvel termina em 0)'); }
    else { en.pagamento.estado = 'pago'; marcaPaga(db, en); }
    grava(db); log(`MB WAY simulado → encomenda #${en.id} ${en.estado}`);
  }, 6000);
}

/* ---------- servidor ---------- */
function log(m){ console.log(new Date().toLocaleTimeString('pt-PT'), m); }
function json(res, code, obj){ res.writeHead(code, { 'Content-Type': 'application/json; charset=utf-8', 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': 'Content-Type, X-Painel', 'Access-Control-Allow-Methods': 'GET,POST,PATCH,OPTIONS' }); res.end(JSON.stringify(obj)); }
function corpoJSON(req){ return new Promise((ok, ko) => { let s = ''; req.on('data', d => { s += d; if (s.length > 15e6) ko(new Error('grande')); }); req.on('end', () => { try { ok(s ? JSON.parse(s) : {}); } catch (e) { ko(e); } }); }); }

const servidor = http.createServer(async (req, res) => {
  const url = new URL(req.url, 'http://x'); const p = url.pathname;
  if (req.method === 'OPTIONS') return json(res, 204, {});
  try {
    if (p.startsWith('/api/')) {
      const db = carrega(); expiraReservas(db);
      const rota = p.slice(4);
      /* público */
      if (req.method === 'GET' && rota === '/catalogo') return json(res, 200, catalogoPublico(db));
      if (req.method === 'POST' && rota === '/encomendas') {
        const r = criaEncomenda(db, await corpoJSON(req));
        if (r.erro) { grava(db); return json(res, 400, { erro: r.erro }); }
        easypaySimulado(r.encomenda); grava(db); log(`encomenda #${r.encomenda.id} criada · ${r.encomenda.total} € · stock reservado`);
        return json(res, 201, { token: r.encomenda.token, id: r.encomenda.id, total: r.encomenda.total, estado: r.encomenda.estado });
      }
      let m = rota.match(/^\/encomendas\/([a-f0-9]{32})$/);
      if (req.method === 'GET' && m) { const e = db.encomendas.find(x => x.token === m[1]); grava(db); return e ? json(res, 200, { id: e.id, estado: e.estado, total: e.total, linhas: e.linhas, motivo: e.motivo || null }) : json(res, 404, { erro: 'Encomenda não encontrada' }); }
      if (req.method === 'POST' && rota === '/easypay') { /* na produção: notificação da Easypay; aqui não é usado */ return json(res, 200, { ok: true }); }
      /* painel */
      if (rota.startsWith('/painel/')) {
        if (req.headers['x-painel'] !== SENHA_PAINEL) return json(res, 401, { erro: 'Palavra-passe do painel errada' });
        if (req.method === 'GET' && rota === '/painel/encomendas') { grava(db); return json(res, 200, db.encomendas.slice().reverse()); }
        m = rota.match(/^\/painel\/encomendas\/(\d+)$/);
        if (req.method === 'PATCH' && m) {
          const e = db.encomendas.find(x => x.id === +m[1]); if (!e) return json(res, 404, { erro: 'Não existe' });
          const b = await corpoJSON(req);
          if (b.estado === 'enviada' && e.estado === 'paga') { e.estado = 'enviada'; e.enviada = agora(); }
          else if (b.estado === 'cancelada' && (e.estado === 'pendente' || e.estado === 'paga')) { if (e.estado === 'pendente') liberta(db, e); e.estado = 'cancelada'; }
          else return json(res, 400, { erro: 'Mudança de estado não permitida: ' + e.estado + ' → ' + b.estado });
          e.atualizada = agora(); grava(db); return json(res, 200, e);
        }
        if (req.method === 'GET' && rota === '/painel/pecas') { grava(db); return json(res, 200, { categorias: db.categorias, estacoes: db.estacoes, pecas: db.pecas }); }
        if (req.method === 'PATCH' && rota === '/painel/stock') {
          const b = await corpoJSON(req); const c = cor(db, b.peca, +b.cor); if (!c) return json(res, 404, { erro: 'Peça/cor não existe' });
          c.stock = Math.max(0, Math.round(+b.stock || 0)); grava(db); log(`stock ${b.peca} [${c.nome}] = ${c.stock}`); return json(res, 200, { stock: c.stock, disponivel: disponivel(c) });
        }
        if (req.method === 'POST' && rota === '/painel/pecas') {
          const b = await corpoJSON(req);
          if (!b.nome || b.preco == null || !Array.isArray(b.cores) || !b.cores.length) return json(res, 400, { erro: 'Nome, preço e pelo menos uma cor são obrigatórios' });
          const id = (b.nome.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'peca') + '-' + (db.seq + 1);
          const cores = b.cores.map((c, i) => {
            let foto = null;
            if (c.fotoBase64) { foto = `${id}-${i}.jpg`; fs.writeFileSync(path.join(RAIZ, 'media', 'produtos', foto), Buffer.from(c.fotoBase64.replace(/^data:image\/\w+;base64,/, ''), 'base64')); }
            return { nome: c.nome || 'Cor ' + (i + 1), hex: c.hex || '#CCCCCC', foto, stock: Math.max(0, Math.round(+c.stock || 0)), reservado: 0 };
          });
          const peca = { id, nome: b.nome, cat: b.cat || 'blusas', preco: +b.preco, precoAntigo: b.precoAntigo ? +b.precoAntigo : undefined, promo: !!b.precoAntigo, tam: b.tam || 'Tamanho único', tamanhos: b.tamanhos && b.tamanhos.length ? b.tamanhos : ['Único'], cores, desc: b.desc || '', estacao: b.estacao || 'meia', nova: true, ativo: true };
          db.pecas.unshift(peca); db.seq++; grava(db); log(`peça nova: ${peca.nome}`); return json(res, 201, peca);
        }
        m = rota.match(/^\/painel\/pecas\/([a-z0-9-]+)$/);
        if (req.method === 'PATCH' && m) {
          const pe = db.pecas.find(x => x.id === m[1]); if (!pe) return json(res, 404, { erro: 'Não existe' });
          const b = await corpoJSON(req);
          ['nome', 'preco', 'precoAntigo', 'desc', 'tam', 'cat', 'estacao', 'ativo', 'nova'].forEach(k => { if (k in b) pe[k] = b[k]; });
          pe.promo = pe.precoAntigo != null && pe.precoAntigo > pe.preco; grava(db); return json(res, 200, pe);
        }
      }
      return json(res, 404, { erro: 'Rota desconhecida' });
    }
    /* ficheiros do site */
    let f = path.join(RAIZ, decodeURIComponent(p === '/' ? '/index.html' : p));
    if (!f.startsWith(RAIZ) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end('não encontrado'); }
    let dados = fs.readFileSync(f);
    if (f.endsWith('.html')) dados = Buffer.from(dados.toString('utf8').replace('</head>', '<script>window.LOJA_API="/api"</script></head>'));
    res.writeHead(200, { 'Content-Type': MIME[path.extname(f)] || 'application/octet-stream', 'Cache-Control': 'no-store' }); res.end(dados);
  } catch (e) { log('erro: ' + e.message); json(res, 500, { erro: e.message }); }
});
servidor.listen(PORTA, () => {
  carrega();
  console.log(`\nToda Chic — servidor de teste\n  loja:    http://localhost:${PORTA}\n  painel:  http://localhost:${PORTA}/painel.html   (palavra-passe: ${SENHA_PAINEL})\n  dados:   ${DADOS}\n  MB WAY simulado: confirma em 6 s; telemóvel terminado em 0 falha.\n`);
});
