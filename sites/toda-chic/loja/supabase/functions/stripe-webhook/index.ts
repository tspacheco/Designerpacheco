// Edge Function "stripe-webhook" — a Stripe chama isto quando o pagamento fica concluído ou a sessão expira.
// Deploy: supabase functions deploy stripe-webhook --no-verify-jwt
// Secrets: STRIPE_WEBHOOK_SECRET (do endpoint criado no painel Stripe → Developers → Webhooks)
// Eventos a subscrever: checkout.session.completed, checkout.session.async_payment_succeeded,
//                       checkout.session.async_payment_failed, checkout.session.expired
import { createClient } from "jsr:@supabase/supabase-js@2";

const sb = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
const SEGREDO = Deno.env.get("STRIPE_WEBHOOK_SECRET")!;

async function assinaturaValida(corpo: string, cabecalho: string | null): Promise<boolean> {
  if (!cabecalho) return false;
  const partes = Object.fromEntries(cabecalho.split(",").map((p) => p.split("=") as [string, string]));
  const t = partes.t, v1 = partes.v1;
  if (!t || !v1 || Math.abs(Date.now() / 1000 - Number(t)) > 300) return false;
  const chave = await crypto.subtle.importKey("raw", new TextEncoder().encode(SEGREDO), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const mac = await crypto.subtle.sign("HMAC", chave, new TextEncoder().encode(`${t}.${corpo}`));
  const hex = Array.from(new Uint8Array(mac)).map((b) => b.toString(16).padStart(2, "0")).join("");
  return hex === v1;
}

Deno.serve(async (req) => {
  const corpo = await req.text();
  if (!(await assinaturaValida(corpo, req.headers.get("stripe-signature")))) return new Response("assinatura inválida", { status: 400 });
  const ev = JSON.parse(corpo);
  const s = ev.data?.object ?? {};
  const id = Number(s.metadata?.encomenda ?? s.client_reference_id);
  if (!id) return new Response("sem encomenda", { status: 200 });
  switch (ev.type) {
    case "checkout.session.completed":
      // MB WAY é assíncrono: "completed" pode chegar com payment_status "unpaid"; só marcar paga quando estiver "paid"
      if (s.payment_status === "paid") await sb.rpc("marcar_paga", { p_id: id, p_payment: s.payment_intent });
      break;
    case "checkout.session.async_payment_succeeded":
      await sb.rpc("marcar_paga", { p_id: id, p_payment: s.payment_intent });
      break;
    case "checkout.session.async_payment_failed":
      await sb.rpc("libertar_encomenda", { p_id: id, p_estado: "falhada", p_motivo: "O pagamento MB WAY não foi confirmado" });
      break;
    case "checkout.session.expired":
      await sb.rpc("libertar_encomenda", { p_id: id, p_estado: "expirada", p_motivo: "Expirou sem pagamento" });
      break;
  }
  return new Response("ok", { status: 200 });
});
