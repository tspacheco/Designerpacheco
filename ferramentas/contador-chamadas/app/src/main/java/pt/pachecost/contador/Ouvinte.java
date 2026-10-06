package pt.pachecost.contador;

import android.app.Notification;
import android.os.Build;
import android.os.Handler;
import android.os.Looper;
import android.service.notification.NotificationListenerService;
import android.service.notification.StatusBarNotification;

import java.util.HashSet;
import java.util.Set;

/**
 * Lê as notificações do WhatsApp. Uma chamada começa quando aparece a notificação de chamada
 * (a chamar, a tocar ou em curso) e acaba quando ela desaparece. Não lê nomes, números nem mensagens.
 */
public class Ouvinte extends NotificationListenerService {
    /** Tempo de espera depois de a notificação sair, para não partir uma chamada em duas
     *  quando o WhatsApp troca a notificação de «a chamar» para «em curso». */
    private static final long FOLGA_MS = 4000;

    private final Handler h = new Handler(Looper.getMainLooper());
    private final Set<String> ativas = new HashSet<>();
    private Runnable fecho;

    static boolean eWhatsApp(StatusBarNotification sbn) {
        String pkg = sbn.getPackageName();
        return "com.whatsapp".equals(pkg) || "com.whatsapp.w4b".equals(pkg);
    }

    static boolean eChamada(Notification n) {
        String cat = n.category;
        String canal = Build.VERSION.SDK_INT >= 26 && n.getChannelId() != null ? n.getChannelId().toLowerCase() : "";
        boolean fixa = (n.flags & Notification.FLAG_ONGOING_EVENT) != 0;
        if (canal.contains("missed") || "missed_call".equals(cat)) return false;
        if (Notification.CATEGORY_CALL.equals(cat)) return true;
        return fixa && (canal.contains("call") || canal.contains("voip"));
    }

    static boolean temCronometro(Notification n) {
        return n.extras != null && n.extras.getBoolean(Notification.EXTRA_SHOW_CHRONOMETER, false);
    }

    @Override
    public void onListenerConnected() {
        ativas.clear();
        long agora = System.currentTimeMillis();
        try {
            StatusBarNotification[] todas = getActiveNotifications();
            if (todas != null) {
                for (StatusBarNotification sbn : todas) {
                    if (eWhatsApp(sbn) && eChamada(sbn.getNotification())) ativas.add(sbn.getKey());
                }
            }
        } catch (Exception ignorada) {
            // Sem acesso ainda: fica vazio.
        }
        if (ativas.isEmpty()) {
            Registo.terminar(this, agora);
        } else {
            Registo.iniciar(this, agora);
        }
        Registo.enviar(this);
    }

    @Override
    public void onNotificationPosted(StatusBarNotification sbn) {
        if (!eWhatsApp(sbn)) return;
        Notification n = sbn.getNotification();
        boolean chamada = eChamada(n);
        String canal = Build.VERSION.SDK_INT >= 26 ? String.valueOf(n.getChannelId()) : "-";
        Registo.diag(this, "WhatsApp: categoria=" + n.category + " canal=" + canal
                + " fixa=" + ((n.flags & Notification.FLAG_ONGOING_EVENT) != 0 ? 1 : 0)
                + " cronómetro=" + (temCronometro(n) ? 1 : 0)
                + (chamada ? "  → CHAMADA" : ""));
        if (!chamada) return;
        long agora = System.currentTimeMillis();
        ativas.add(sbn.getKey());
        if (fecho != null) {
            h.removeCallbacks(fecho);
            fecho = null;
        }
        Registo.iniciar(this, agora);
        if (temCronometro(n)) Registo.ligada(this, agora);
    }

    @Override
    public void onNotificationRemoved(StatusBarNotification sbn) {
        if (!eWhatsApp(sbn)) return;
        if (!ativas.remove(sbn.getKey()) || !ativas.isEmpty()) return;
        final long fim = System.currentTimeMillis();
        if (fecho != null) h.removeCallbacks(fecho);
        fecho = new Runnable() {
            @Override public void run() {
                fecho = null;
                if (ativas.isEmpty()) Registo.terminar(Ouvinte.this, fim);
            }
        };
        h.postDelayed(fecho, FOLGA_MS);
    }
}
