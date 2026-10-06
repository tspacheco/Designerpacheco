package pt.pachecost.contador;

import android.app.Activity;
import android.content.ComponentName;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.graphics.Typeface;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.provider.Settings;
import android.text.InputType;
import android.view.Gravity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONArray;

/** Ecrã único: estado, contagem de hoje, últimas chamadas e configuração. */
public class MainActivity extends Activity {
    private static final int LARANJA = Color.rgb(0xF2, 0x6B, 0x1D);

    private final Handler h = new Handler(Looper.getMainLooper());
    private final Runnable tique = new Runnable() {
        @Override public void run() {
            atualizar();
            h.postDelayed(this, 2000);
        }
    };

    private TextView acesso, numero, detalhe, ultimas, envio, diag;
    private Button botaoAcesso;
    private EditText token, repo, issue, aparelho;

    @Override
    protected void onCreate(Bundle b) {
        super.onCreate(b);
        int pad = dp(18);
        LinearLayout col = new LinearLayout(this);
        col.setOrientation(LinearLayout.VERTICAL);
        col.setPadding(pad, pad, pad, pad);

        col.addView(texto("Contador de Chamadas", 22, true));
        col.addView(texto("Conta as chamadas de WhatsApp (início e fim) e envia as horas para a Pacheco Studios. "
                + "Não lê nomes, números nem mensagens.", 14, false));

        acesso = texto("", 15, true);
        col.addView(espaco(acesso));
        botaoAcesso = botao("Dar acesso às notificações", new View.OnClickListener() {
            @Override public void onClick(View v) {
                startActivity(new Intent(Settings.ACTION_NOTIFICATION_LISTENER_SETTINGS));
            }
        });
        col.addView(botaoAcesso);

        numero = texto("0", 64, true);
        numero.setTextColor(LARANJA);
        numero.setGravity(Gravity.CENTER_HORIZONTAL);
        col.addView(espaco(numero));
        detalhe = texto("", 15, false);
        detalhe.setGravity(Gravity.CENTER_HORIZONTAL);
        col.addView(detalhe);

        col.addView(espaco(texto("Últimas chamadas", 16, true)));
        ultimas = texto("", 14, false);
        ultimas.setTypeface(Typeface.MONOSPACE);
        col.addView(ultimas);

        envio = texto("", 14, false);
        col.addView(espaco(envio));

        col.addView(espaco(texto("Configuração", 16, true)));
        SharedPreferences sp = Registo.p(this);
        token = campo("Código de acesso (token do GitHub)", sp.getString("token", ""), true);
        repo = campo("Repositório", sp.getString("repo", Registo.REPO_DEF), false);
        issue = campo("Número do registo", sp.getString("issue", Registo.ISSUE_DEF), false);
        issue.setInputType(InputType.TYPE_CLASS_NUMBER);
        aparelho = campo("Nome deste telemóvel (ex.: cc1)", sp.getString("aparelho", Registo.APARELHO_DEF), false);
        col.addView(token);
        col.addView(repo);
        col.addView(issue);
        col.addView(aparelho);
        col.addView(botao("Guardar", new View.OnClickListener() {
            @Override public void onClick(View v) {
                guardar();
                Toast.makeText(MainActivity.this, "Guardado", Toast.LENGTH_SHORT).show();
                Registo.enviar(MainActivity.this);
            }
        }));
        col.addView(botao("Enviar teste", new View.OnClickListener() {
            @Override public void onClick(View v) {
                guardar();
                long t = System.currentTimeMillis();
                Registo.enfileirar(MainActivity.this, "teste v1 | ap="
                        + Registo.p(MainActivity.this).getString("aparelho", Registo.APARELHO_DEF)
                        + " | hora=" + Registo.iso(t));
                Toast.makeText(MainActivity.this, "Teste enviado. Vê o estado do envio acima.", Toast.LENGTH_LONG).show();
            }
        }));
        col.addView(botao("Não deixar a bateria desligar a app", new View.OnClickListener() {
            @Override public void onClick(View v) {
                startActivity(new Intent(Settings.ACTION_IGNORE_BATTERY_OPTIMIZATION_SETTINGS));
            }
        }));

        col.addView(espaco(texto("Diagnóstico (última notificação do WhatsApp)", 14, true)));
        diag = texto("", 12, false);
        diag.setTypeface(Typeface.MONOSPACE);
        col.addView(diag);

        ScrollView sv = new ScrollView(this);
        sv.addView(col);
        setContentView(sv);
    }

    @Override
    protected void onResume() {
        super.onResume();
        Registo.enviar(this);
        h.post(tique);
    }

    @Override
    protected void onPause() {
        super.onPause();
        h.removeCallbacks(tique);
    }

    private void guardar() {
        Registo.p(this).edit()
                .putString("token", token.getText().toString().trim())
                .putString("repo", repo.getText().toString().trim())
                .putString("issue", issue.getText().toString().trim())
                .putString("aparelho", aparelho.getText().toString().trim().replace("|", ""))
                .apply();
    }

    private boolean temAcesso() {
        String ativos = Settings.Secure.getString(getContentResolver(), "enabled_notification_listeners");
        return ativos != null && ativos.contains(new ComponentName(this, Ouvinte.class).flattenToString());
    }

    private void atualizar() {
        SharedPreferences sp = Registo.p(this);
        boolean ok = temAcesso();
        acesso.setText(ok ? "✅ A ouvir as chamadas do WhatsApp" : "❌ Sem acesso às notificações: carrega no botão e ativa «Contador de Chamadas».");
        acesso.setTextColor(ok ? Color.rgb(0x1B, 0x8A, 0x3C) : Color.rgb(0xC6, 0x28, 0x28));
        botaoAcesso.setVisibility(ok ? View.GONE : View.VISIBLE);

        String hoje = Registo.dia(System.currentTimeMillis());
        boolean deHoje = hoje.equals(sp.getString("dia", ""));
        int n = deHoje ? sp.getInt("n", 0) : 0;
        long seg = deHoje ? sp.getLong("seg", 0) : 0;
        numero.setText(String.valueOf(n));
        String emCurso = sp.getBoolean("emChamada", false)
                ? "\n🔴 Chamada em curso desde " + Registo.hora(sp.getLong("inicio", 0)) : "";
        detalhe.setText((n == 1 ? "chamada hoje" : "chamadas hoje") + " · " + seg / 60 + " min ao telefone" + emCurso);

        JSONArray u = Registo.lerArray(deHoje ? sp.getString("ultimas", "[]") : "[]");
        StringBuilder sb = new StringBuilder();
        for (int i = u.length() - 1; i >= 0; i--) sb.append(u.optString(i)).append('\n');
        ultimas.setText(sb.length() == 0 ? "Ainda nenhuma hoje." : sb.toString().trim());

        int pendentes = Registo.lerArray(sp.getString("fila", "[]")).length();
        String erro = sp.getString("erro", "");
        String ultimoEnvio = sp.getString("envio", "");
        envio.setText("Envio: " + (pendentes == 0 ? "tudo enviado" : pendentes + " por enviar")
                + (ultimoEnvio.isEmpty() ? "" : " · último às " + ultimoEnvio)
                + (erro.isEmpty() ? "" : "\n⚠️ " + erro));
        diag.setText(sp.getString("diag", "Ainda nada. Faz uma chamada de teste no WhatsApp."));
    }

    private TextView texto(String s, int sp, boolean negrito) {
        TextView t = new TextView(this);
        t.setText(s);
        t.setTextSize(sp);
        if (negrito) t.setTypeface(Typeface.DEFAULT_BOLD);
        return t;
    }

    private View espaco(View v) {
        v.setPadding(0, dp(18), 0, dp(4));
        return v;
    }

    private Button botao(String s, View.OnClickListener l) {
        Button b = new Button(this);
        b.setText(s);
        b.setAllCaps(false);
        b.setOnClickListener(l);
        return b;
    }

    private EditText campo(String dica, String valor, boolean secreto) {
        EditText e = new EditText(this);
        e.setHint(dica);
        e.setText(valor);
        e.setSingleLine(true);
        if (secreto) e.setInputType(InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_VARIATION_PASSWORD);
        return e;
    }

    private int dp(int v) {
        return Math.round(v * getResources().getDisplayMetrics().density);
    }
}
