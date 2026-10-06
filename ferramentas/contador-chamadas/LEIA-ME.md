# Contador de Chamadas (cold caller)

Duas versões: **Windows** (o cold caller usa o WhatsApp no PC, 06/10/2026) e **Android**. As duas contam as chamadas de WhatsApp do cold caller. Cada vez que uma chamada começa e acaba, guarda a hora
de início, a hora de fim e a duração, e envia uma linha para o registo
[issue #3](https://github.com/tspacheco/Designerpacheco/issues/3). Não lê nomes, números nem mensagens.

Uma rotina do projeto corre `relatorio.py` às 11:55, 14:55, 17:55 e 20:55 (seg–sáb, hora de Lisboa) e publica o
resumo no thread «Contador de chamadas»: total do dia, tempo ao telefone, chamadas com 30 s ou mais, atendidas e
chamadas desde o relatório anterior.

## Windows (WhatsApp no PC)

Zip: https://github.com/tspacheco/Designerpacheco/raw/claude/contador-chamadas-cold-caller-qo3dyp/ferramentas/contador-chamadas/ContadorChamadas-Windows.zip

Deteta a chamada pelo microfone: o Windows regista quando cada app liga e desliga o microfone, e o programa vê
quando é o WhatsApp. Funciona com a app WhatsApp para Windows; não funciona com o WhatsApp Web no browser.
Uma nota de voz gravada no PC também conta como chamada (curta).

1. Criar o código de acesso (secção 1 abaixo).
2. No PC dele: descarregar o zip → Extrair tudo → duplo clique em `instalar.cmd` (SmartScreen: Mais informações →
   Executar mesmo assim) → colar o código → Enter.
3. Aparece um ícone (i) junto ao relógio com «Chamadas hoje: N». Botão direito → **Enviar teste**.
4. Arranca sozinho quando o PC liga. Sem administrador. Dados em `%LOCALAPPDATA%\ContadorChamadas`.

Código em `windows/` (PowerShell 5.1, que vem no Windows). Teste automático no workflow `contador-windows.yml`.

## Android

APK: https://github.com/tspacheco/Designerpacheco/raw/claude/contador-chamadas-cold-caller-qo3dyp/ferramentas/contador-chamadas/ContadorChamadas.apk

## 1. Criar o código de acesso (Tomás, uma vez, 2 min)

1. Em github.com → foto → **Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token**.
2. Nome: `contador-chamadas`. Expiração: 1 ano.
3. **Repository access → Only select repositories → Designerpacheco.**
4. **Permissions → Repository permissions → Issues: Read and write.** Mais nada.
5. Gerar e copiar o código (começa por `github_pat_`). Enviar ao cold caller por WhatsApp para ele colar na app.

Este código só consegue escrever comentários em issues deste repositório. Nunca o pôr no repositório.

## 2. Instalar no telemóvel do cold caller (5 min)

1. Abrir o link do APK no telemóvel → descarregar → abrir → permitir «instalar apps desconhecidas» → Instalar.
2. Abrir **Contador de Chamadas** → **Dar acesso às notificações** → ativar «Contador de Chamadas».
   - Android 13 ou mais recente pode dizer **«Definição restrita»**. Nesse caso: Definições → Apps → Contador de
     Chamadas → menu ⋮ (canto superior direito) → **Permitir definições restritas** → voltar e ativar o acesso.
3. Colar o código no campo **Código de acesso** → **Guardar** → **Enviar teste**. «Envio: tudo enviado» = ligado.
4. **Não deixar a bateria desligar a app** → Contador de Chamadas → **Sem restrições** / **Não otimizar**.
   Em Xiaomi, Huawei, Oppo e Samsung, ativar também o «início automático» da app, se existir.
5. Fazer uma chamada de WhatsApp de teste: o número grande sobe para 1 e aparece em «Últimas chamadas».

Se o número não subir: tirar um print à secção **Diagnóstico** logo durante uma chamada e mandar ao Claude no projeto.

## Como conta

- **Início:** aparece a notificação de chamada do WhatsApp (a chamar, a tocar ou em curso).
- **Fim:** a notificação desaparece (com 4 s de folga para não partir uma chamada em duas).
- **Atendida:** quando o WhatsApp mostra o cronómetro da chamada (depende da versão; se não aparecer, o relatório usa
  «30 s ou mais» como sinal de conversa).
- Conta chamadas feitas e recebidas, de voz e vídeo, do WhatsApp e do WhatsApp Business.
- Sem rede, as chamadas ficam em fila e seguem na próxima chamada ou quando se abre a app.

## iPhone

Não funciona: o iOS não deixa nenhuma app ver as notificações nem as chamadas de outra app. No iPhone a alternativa é
o cold caller usar um Atalho manual (botão «comecei»/«acabei») ou fazer as chamadas a partir de um Android.

## Para o Claude

- Código: `app/src/main/java/pt/pachecost/contador/` (Java puro, sem dependências). O APK é construído pelo workflow
  `.github/workflows/contador-apk.yml` em cada push ao código e gravado aqui como `ContadorChamadas.apk`.
- Formato de cada comentário: `chamada v1 | id=… | ap=cc1 | inicio=ISO | fim=ISO | dur=seg [| conv=seg]`.
- Relatório: `python3 relatorio.py [--data AAAA-MM-DD] [--desde HH:MM]`.
