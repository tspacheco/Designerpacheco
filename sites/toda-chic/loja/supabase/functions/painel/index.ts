// Edge Function "painel" — o que o painel.html da dona usa (mesmo contrato do servidor de teste).
// Protegido por uma palavra-passe longa no cabeçalho X-Painel (secret PAINEL_SENHA).
//   GET   /painel/encomendas            PATCH /painel/encomendas/:id {estado}
//   GET   /painel/pecas                 PATCH /painel/stock {peca, cor, stock}
//   POST  /painel/pecas {…, cores:[{nome,hex,stock,fotoBase64}]}   PATCH /painel/pecas/:id {campos}
// Deploy: supabase functions deploy painel --no-verify-jwt
import { createClient } from "jsr:@supabase/supabase-js@2";

const sb = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
const SENHA = Deno.env.get("PAINEL_SENHA")!;
const CORS = { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "Content-Type, X-Painel, Authorization", "Access-Control-Allow-Methods": "GET,POST,PATCH,OPTIONS" };
const json = (code: number, body: unknown) => new Response(JSON.stringify(body), { status: code, headers: { ...CORS, "Content-Type": "application/json; charset=utf-8" } });
const slug = (s: string) => s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "peca";

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: CORS });
  if (req.headers.get("x-painel") !== SENHA) return json(401, { erro: "Palavra-passe do painel errada" });
  const rota = new URL(req.url).pathname.replace(/^\/painel/, "");
  try {
    if (req.method === "GET" && rota === "/encomendas") {
      const { data } = await sb.from("encomendas").select("*").order("criada", { ascending: false }).limit(300);
      return json(200, data ?? []);
    }
    let m = rota.match(/^\/encomendas\/(\d+)$/);
    if (req.method === "PATCH" && m) {
      const { estado } = await req.json();
      const { data: e } = await sb.from("encomendas").select("id,estado").eq("id", m[1]).single();
      if (!e) return json(404, { erro: "Não existe" });
      if (estado === "enviada" && e.estado === "paga") await sb.from("encomendas").update({ estado: "enviada", enviada: new Date().toISOString(), atualizada: new Date().toISOString() }).eq("id", e.id);
      else if (estado === "cancelada" && e.estado === "pendente") await sb.rpc("libertar_encomenda", { p_id: e.id, p_estado: "cancelada", p_motivo: "Cancelada pela loja" });
      else if (estado === "cancelada" && e.estado === "paga") await sb.from("encomendas").update({ estado: "cancelada", atualizada: new Date().toISOString() }).eq("id", e.id);
      else return json(400, { erro: `Mudança de estado não permitida: ${e.estado} → ${estado}` });
      return json(200, { ok: true });
    }
    if (req.method === "GET" && rota === "/pecas") {
      const [{ data: pecas }, { data: cores }, cats, ests] = await Promise.all([
        sb.from("pecas").select("*").order("criada", { ascending: false }), sb.from("cores").select("*").order("posicao"),
        sb.from("categorias").select("*").order("ordem"), sb.from("estacoes").select("*").order("ordem"),
      ]);
      const porPeca: Record<string, unknown[]> = {};
      (cores ?? []).forEach((c) => { (porPeca[c.peca_id] ??= []).push(c); });
      return json(200, { categorias: cats.data ?? [], estacoes: ests.data ?? [], pecas: (pecas ?? []).map((p) => ({ ...p, precoAntigo: p.preco_antigo, desc: p.descricao, cores: porPeca[p.id] ?? [] })) });
    }
    if (req.method === "PATCH" && rota === "/stock") {
      const b = await req.json();
      const stock = Math.max(0, Math.round(Number(b.stock) || 0));
      const { data: c } = await sb.from("cores").update({ stock }).eq("peca_id", b.peca).eq("posicao", b.cor).select("stock,reservado").single();
      if (!c) return json(404, { erro: "Peça/cor não existe" });
      return json(200, { stock: c.stock, disponivel: Math.max(0, c.stock - c.reservado) });
    }
    if (req.method === "POST" && rota === "/pecas") {
      const b = await req.json();
      if (!b.nome || b.preco == null || !Array.isArray(b.cores) || !b.cores.length) return json(400, { erro: "Nome, preço e pelo menos uma cor são obrigatórios" });
      const id = `${slug(b.nome)}-${Date.now().toString(36)}`;
      const { error } = await sb.from("pecas").insert({ id, nome: b.nome, cat: b.cat ?? "blusas", preco: b.preco, preco_antigo: b.precoAntigo ?? null, tam: b.tam ?? "Tamanho único", tamanhos: b.tamanhos?.length ? b.tamanhos : ["Único"], descricao: b.desc ?? "", estacao: b.estacao ?? "meia", nova: true });
      if (error) return json(400, { erro: error.message });
      for (let i = 0; i < b.cores.length; i++) {
        const c = b.cores[i]; let foto: string | null = null;
        if (c.fotoBase64) {
          const bytes = Uint8Array.from(atob(c.fotoBase64.replace(/^data:image\/\w+;base64,/, "")), (ch) => ch.charCodeAt(0));
          const nome = `${id}-${i}.jpg`;
          const { error: eu } = await sb.storage.from("produtos").upload(nome, bytes, { contentType: "image/jpeg", upsert: true });
          if (!eu) foto = sb.storage.from("produtos").getPublicUrl(nome).data.publicUrl;
        }
        await sb.from("cores").insert({ peca_id: id, posicao: i, nome: c.nome || `Cor ${i + 1}`, hex: c.hex ?? "#CCCCCC", foto, stock: Math.max(0, Math.round(Number(c.stock) || 0)) });
      }
      return json(201, { id, nome: b.nome });
    }
    m = rota.match(/^\/pecas\/([a-z0-9-]+)$/);
    if (req.method === "PATCH" && m) {
      const b = await req.json(); const campos: Record<string, unknown> = {};
      for (const k of ["nome", "preco", "tam", "cat", "estacao", "ativo", "nova"]) if (k in b) campos[k] = b[k];
      if ("precoAntigo" in b) campos.preco_antigo = b.precoAntigo; if ("desc" in b) campos.descricao = b.desc;
      const { error } = await sb.from("pecas").update(campos).eq("id", m[1]);
      return error ? json(400, { erro: error.message }) : json(200, { ok: true });
    }
    return json(404, { erro: "Rota desconhecida" });
  } catch (err) { console.error(err); return json(500, { erro: (err as Error).message }); }
});
