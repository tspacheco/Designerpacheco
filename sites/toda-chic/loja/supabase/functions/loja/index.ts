// Edge Function "loja" — a API pública da loja (mesmo contrato do servidor de teste).
//   GET  /loja/catalogo                → catálogo com stock disponível
//   POST /loja/encomendas              → reserva stock, cria a encomenda, abre o Stripe Checkout (MB WAY) → { token, checkoutUrl }
//   GET  /loja/encomendas/:token       → estado da encomenda
// Deploy: supabase functions deploy loja --no-verify-jwt
// Secrets: SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY (automáticos), STRIPE_SECRET_KEY
import { createClient } from "jsr:@supabase/supabase-js@2";

const sb = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
const STRIPE = Deno.env.get("STRIPE_SECRET_KEY")!;
const CORS = { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "Content-Type, Authorization", "Access-Control-Allow-Methods": "GET,POST,OPTIONS" };
const json = (code: number, body: unknown) => new Response(JSON.stringify(body), { status: code, headers: { ...CORS, "Content-Type": "application/json; charset=utf-8" } });

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: CORS });
  const url = new URL(req.url);
  const rota = url.pathname.replace(/^\/loja/, "");
  try {
    if (req.method === "GET" && rota === "/catalogo") {
      const [{ data: pecas, error }, cats, ests] = await Promise.all([
        sb.from("catalogo_publico").select("*"),
        sb.from("categorias").select("*").order("ordem"),
        sb.from("estacoes").select("*").order("ordem"),
      ]);
      if (error) throw error;
      return json(200, { categorias: cats.data ?? [], estacoes: ests.data ?? [], pecas: (pecas ?? []).map((p) => ({ ...p, precoAntigo: p.preco_antigo })) });
    }

    if (req.method === "POST" && rota === "/encomendas") {
      const b = await req.json();
      const cl = b.cliente ?? {};
      for (const k of ["nome", "telemovel", "morada", "cp", "localidade"]) if (!cl[k] || String(cl[k]).trim().length < 2) return json(400, { erro: "Falta " + k });
      if (!/^9\d{8}$/.test(String(cl.telemovel).replace(/\s/g, ""))) return json(400, { erro: "O telemóvel tem de ter 9 dígitos e começar por 9" });
      if (!Array.isArray(b.linhas) || !b.linhas.length) return json(400, { erro: "Saco vazio" });
      const { data: e, error } = await sb.rpc("criar_encomenda", { p_linhas: b.linhas, p_cliente: { ...cl, telemovel: String(cl.telemovel).replace(/\s/g, "") } });
      if (error) return json(400, { erro: error.message.replace(/^.*?: /, "") });

      // Stripe Checkout com MB WAY (ativar MB WAY nos métodos de pagamento do painel Stripe; automatic_payment_methods escolhe-o)
      const retorno = (b.retorno || "https://todachic.pt/").replace(/#.*$/, "");
      const form = new URLSearchParams();
      form.set("mode", "payment");
      form.set("success_url", `${retorno}#/encomenda/${e.token}`);
      form.set("cancel_url", `${retorno}#/pagar`);
      form.set("client_reference_id", String(e.id));
      form.set("metadata[encomenda]", String(e.id));
      form.set("metadata[token]", e.token);
      form.set("locale", "pt");
      form.set("expires_at", String(Math.floor(Date.now() / 1000) + 60 * 60)); // 60 min = a reserva de stock
      if (cl.email) form.set("customer_email", cl.email);
      (e.linhas as Array<{ nome: string; corNome: string; tamNome: string; preco: number; qt: number }>).forEach((l, i) => {
        form.set(`line_items[${i}][quantity]`, String(l.qt));
        form.set(`line_items[${i}][price_data][currency]`, "eur");
        form.set(`line_items[${i}][price_data][unit_amount]`, String(Math.round(l.preco * 100)));
        form.set(`line_items[${i}][price_data][product_data][name]`, `${l.nome} · ${l.corNome} · ${l.tamNome}`);
      });
      const r = await fetch("https://api.stripe.com/v1/checkout/sessions", { method: "POST", headers: { Authorization: `Bearer ${STRIPE}`, "Content-Type": "application/x-www-form-urlencoded" }, body: form });
      const sess = await r.json();
      if (!r.ok) { await sb.rpc("libertar_encomenda", { p_id: e.id, p_estado: "falhada", p_motivo: "Stripe: " + (sess.error?.message ?? r.status) }); return json(502, { erro: "Não foi possível abrir o pagamento. Tenta outra vez." }); }
      await sb.from("encomendas").update({ stripe_session: sess.id }).eq("id", e.id);
      return json(201, { token: e.token, id: e.id, total: e.total, estado: e.estado, checkoutUrl: sess.url });
    }

    const m = rota.match(/^\/encomendas\/([a-f0-9]{32})$/);
    if (req.method === "GET" && m) {
      const { data: e } = await sb.from("encomendas").select("id,estado,total,linhas,motivo").eq("token", m[1]).maybeSingle();
      return e ? json(200, e) : json(404, { erro: "Encomenda não encontrada" });
    }
    return json(404, { erro: "Rota desconhecida" });
  } catch (err) {
    console.error(err);
    return json(500, { erro: (err as Error).message });
  }
});
