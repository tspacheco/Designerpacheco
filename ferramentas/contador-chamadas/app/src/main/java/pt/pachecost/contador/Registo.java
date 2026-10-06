package pt.pachecost.contador;

import android.content.Context;
import android.content.SharedPreferences;

import org.json.JSONArray;

import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

/**
 * Estado da chamada em curso, contagem do dia e fila de envio para o GitHub.
 * Só guarda horas e durações: nunca números, nomes ou texto das notificações.
 */
final class Registo {
    static final String REPO_DEF = "tspacheco/Designerpacheco";
    static final String ISSUE_DEF = "3";
    static final String APARELHO_DEF = "cc1";

    private static final Object TRAVA = new Object();

    private Registo() {}

    static SharedPreferences p(Context c) {
        return c.getApplicationContext().getSharedPreferences("contador", Context.MODE_PRIVATE);
    }

    static String iso(long t) {
        return new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ssXXX", Locale.US).format(new Date(t));
    }

    static String hora(long t) {
        return new SimpleDateFormat("HH:mm", Locale.US).format(new Date(t));
    }

    static String dia(long t) {
        return new SimpleDateFormat("yyyy-MM-dd", Locale.US).format(new Date(t));
    }

    /** O WhatsApp mostrou uma notificação de chamada. */
    static void iniciar(Context c, long t) {
        synchronized (TRAVA) {
            SharedPreferences sp = p(c);
            if (sp.getBoolean("emChamada", false)) return;
            sp.edit().putBoolean("emChamada", true).putLong("inicio", t).putLong("ligada", 0).apply();
        }
    }

    /** A chamada foi atendida (o WhatsApp passou a mostrar o cronómetro). */
    static void ligada(Context c, long t) {
        synchronized (TRAVA) {
            SharedPreferences sp = p(c);
            if (sp.getBoolean("emChamada", false) && sp.getLong("ligada", 0) == 0) {
                sp.edit().putLong("ligada", t).apply();
            }
        }
    }

    /** Desapareceram todas as notificações de chamada do WhatsApp. */
    static void terminar(Context c, long t) {
        synchronized (TRAVA) {
            SharedPreferences sp = p(c);
            if (!sp.getBoolean("emChamada", false)) return;
            long inicio = sp.getLong("inicio", t);
            long ligada = sp.getLong("ligada", 0);
            long dur = Math.max(0, (t - inicio) / 1000);
            String ap = sp.getString("aparelho", APARELHO_DEF);
            StringBuilder linha = new StringBuilder("chamada v1")
                    .append(" | id=").append(Long.toString(inicio / 1000, 36))
                    .append(" | ap=").append(ap)
                    .append(" | inicio=").append(iso(inicio))
                    .append(" | fim=").append(iso(t))
                    .append(" | dur=").append(dur);
            if (ligada > 0) linha.append(" | conv=").append(Math.max(0, (t - ligada) / 1000));

            String hoje = dia(t);
            int n = hoje.equals(sp.getString("dia", "")) ? sp.getInt("n", 0) : 0;
            long seg = hoje.equals(sp.getString("dia", "")) ? sp.getLong("seg", 0) : 0;
            JSONArray ultimas = lerArray(sp.getString("ultimas", "[]"));
            ultimas.put(hora(inicio) + "  " + dur / 60 + " min " + dur % 60 + " s" + (ligada > 0 ? "  (atendida)" : ""));
            while (ultimas.length() > 15) ultimas.remove(0);
            JSONArray fila = lerArray(sp.getString("fila", "[]"));
            fila.put(linha.toString());

            sp.edit().putBoolean("emChamada", false)
                    .putString("dia", hoje).putInt("n", n + 1).putLong("seg", seg + dur)
                    .putString("ultimas", ultimas.toString())
                    .putString("fila", fila.toString())
                    .apply();
        }
        enviar(c);
    }

    static void diag(Context c, String texto) {
        p(c).edit().putString("diag", hora(System.currentTimeMillis()) + "  " + texto).apply();
    }

    static void enfileirar(Context c, String linha) {
        synchronized (TRAVA) {
            SharedPreferences sp = p(c);
            JSONArray fila = lerArray(sp.getString("fila", "[]"));
            fila.put(linha);
            sp.edit().putString("fila", fila.toString()).apply();
        }
        enviar(c);
    }

    /** Envia a fila por ordem, um comentário por chamada. O que falhar fica para a próxima. */
    static void enviar(final Context c) {
        final Context app = c.getApplicationContext();
        new Thread(new Runnable() {
            @Override public void run() {
                synchronized (Registo.class) {
                    while (true) {
                        SharedPreferences sp = p(app);
                        String token = sp.getString("token", "").trim();
                        JSONArray fila = lerArray(sp.getString("fila", "[]"));
                        if (fila.length() == 0) return;
                        if (token.isEmpty()) {
                            sp.edit().putString("erro", "Falta o código de acesso (token).").apply();
                            return;
                        }
                        String linha = fila.optString(0);
                        int codigo = publicar(sp, token, linha);
                        if (codigo == 201) {
                            synchronized (TRAVA) {
                                JSONArray atual = lerArray(sp.getString("fila", "[]"));
                                if (atual.length() > 0 && linha.equals(atual.optString(0))) atual.remove(0);
                                sp.edit().putString("fila", atual.toString())
                                        .putString("erro", "")
                                        .putString("envio", hora(System.currentTimeMillis()))
                                        .apply();
                            }
                        } else {
                            String msg = codigo == 401 ? "Token inválido ou expirado (401)."
                                    : codigo == 403 || codigo == 404 ? "Token sem acesso ao registo (" + codigo + ")."
                                    : codigo < 0 ? "Sem internet. Volta a tentar na próxima chamada."
                                    : "O GitHub respondeu " + codigo + ".";
                            sp.edit().putString("erro", hora(System.currentTimeMillis()) + "  " + msg).apply();
                            return;
                        }
                    }
                }
            }
        }).start();
    }

    private static int publicar(SharedPreferences sp, String token, String linha) {
        HttpURLConnection con = null;
        try {
            String repo = sp.getString("repo", REPO_DEF).trim();
            String issue = sp.getString("issue", ISSUE_DEF).trim();
            URL url = new URL("https://api.github.com/repos/" + repo + "/issues/" + issue + "/comments");
            con = (HttpURLConnection) url.openConnection();
            con.setConnectTimeout(15000);
            con.setReadTimeout(20000);
            con.setRequestMethod("POST");
            con.setDoOutput(true);
            con.setRequestProperty("Authorization", "Bearer " + token);
            con.setRequestProperty("Accept", "application/vnd.github+json");
            con.setRequestProperty("User-Agent", "contador-chamadas");
            con.setRequestProperty("Content-Type", "application/json; charset=utf-8");
            String corpo = new org.json.JSONObject().put("body", linha).toString();
            OutputStream os = con.getOutputStream();
            os.write(corpo.getBytes(StandardCharsets.UTF_8));
            os.close();
            return con.getResponseCode();
        } catch (Exception e) {
            return -1;
        } finally {
            if (con != null) con.disconnect();
        }
    }

    static JSONArray lerArray(String s) {
        try {
            return new JSONArray(s);
        } catch (Exception e) {
            return new JSONArray();
        }
    }
}
