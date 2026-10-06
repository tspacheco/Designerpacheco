# Contador de Chamadas (Windows) - Pacheco Studios
# Conta as chamadas do WhatsApp para PC: uma chamada comeca quando o WhatsApp liga o microfone e acaba quando o
# desliga (o Windows regista isso em CapabilityAccessManager). Nao le nomes, numeros nem mensagens.
# Cada chamada vai como uma linha para o registo (issue) no GitHub. Icone na barra de tarefas com a contagem de hoje.
param([switch]$Teste)

$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$Pasta = Join-Path $env:LOCALAPPDATA 'ContadorChamadas'
$Raiz = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\microphone'
if ($Teste) {
    $Pasta = Join-Path $env:TEMP ('contador-teste-' + [guid]::NewGuid().ToString('N'))
    $Raiz = 'HKCU:\Software\ContadorChamadasTeste\microphone'
}
New-Item -ItemType Directory -Force -Path $Pasta | Out-Null
$FilaTxt = Join-Path $Pasta 'fila.txt'
$CfgJson = Join-Path $Pasta 'config.json'
$FolgaSeg = 4   # nao partir uma chamada em duas se o microfone piscar

$Cfg = [pscustomobject]@{ token = ''; repo = 'tspacheco/Designerpacheco'; issue = '3'; aparelho = 'pc1' }
if (Test-Path $CfgJson) {
    $lido = Get-Content $CfgJson -Raw | ConvertFrom-Json
    foreach ($n in 'token', 'repo', 'issue', 'aparelho') { if ($lido.$n) { $Cfg.$n = [string]$lido.$n } }
}

$script:EmChamada = $false
$script:Inicio = $null
$script:FimMarcado = $null
$script:Erro = ''
$script:UltimoEnvio = ''

function Test-WhatsAppMicrofone {
    # $true se alguma entrada do WhatsApp (app da Store ou instalada) esta a usar o microfone agora
    $chaves = @()
    if (Test-Path $Raiz) { $chaves += @(Get-ChildItem $Raiz -ErrorAction SilentlyContinue) }
    $np = Join-Path $Raiz 'NonPackaged'
    if (Test-Path $np) { $chaves += @(Get-ChildItem $np -ErrorAction SilentlyContinue) }
    foreach ($k in $chaves) {
        if ($k.PSChildName -notmatch '(?i)whatsapp') { continue }
        $p = Get-ItemProperty -Path $k.PSPath -ErrorAction SilentlyContinue
        if ($null -eq $p) { continue }
        $ini = $p.LastUsedTimeStart
        $fim = $p.LastUsedTimeStop
        if ($null -ne $ini -and [int64]$ini -gt 0 -and $null -ne $fim -and [int64]$fim -eq 0) { return $true }
    }
    return $false
}

function Format-Iso([datetime]$t) { $t.ToString("yyyy-MM-dd'T'HH:mm:sszzz") }

function Get-FicheiroDia([datetime]$t) { Join-Path $Pasta ('chamadas-' + $t.ToString('yyyy-MM-dd') + '.txt') }

function Get-ContagemHoje {
    $f = Get-FicheiroDia (Get-Date)
    if (Test-Path $f) { return @(Get-Content $f | Where-Object { $_ }).Count }
    return 0
}

function Add-Fila([string]$linha) {
    Add-Content -Path $FilaTxt -Value $linha -Encoding UTF8
}

function Send-Fila {
    if (-not (Test-Path $FilaTxt)) { return }
    $fila = @(Get-Content $FilaTxt -Encoding UTF8 | Where-Object { $_ })
    if ($fila.Count -eq 0) { return }
    if (-not $Cfg.token) { $script:Erro = 'Falta o codigo de acesso (token).'; return }
    $url = "https://api.github.com/repos/$($Cfg.repo)/issues/$($Cfg.issue)/comments"
    $cab = @{ Authorization = "Bearer $($Cfg.token)"; Accept = 'application/vnd.github+json'; 'User-Agent' = 'contador-chamadas' }
    while ($fila.Count -gt 0) {
        try {
            $corpo = [Text.Encoding]::UTF8.GetBytes((@{ body = $fila[0] } | ConvertTo-Json -Compress))
            Invoke-RestMethod -Method Post -Uri $url -Headers $cab -ContentType 'application/json; charset=utf-8' -Body $corpo -TimeoutSec 20 | Out-Null
            $fila = @($fila | Select-Object -Skip 1)
            if ($fila.Count) { Set-Content -Path $FilaTxt -Value $fila -Encoding UTF8 } else { Clear-Content -Path $FilaTxt }
            $script:Erro = ''
            $script:UltimoEnvio = (Get-Date).ToString('HH:mm')
        } catch {
            $codigo = $null
            if ($_.Exception.Response) { $codigo = [int]$_.Exception.Response.StatusCode }
            $script:Erro = if ($codigo -eq 401) { 'Token invalido ou expirado (401).' }
                elseif ($codigo -eq 403 -or $codigo -eq 404) { "Token sem acesso ao registo ($codigo)." }
                elseif ($codigo) { "O GitHub respondeu $codigo." }
                else { 'Sem internet. Volta a tentar na proxima chamada.' }
            return
        }
    }
}

function Complete-Chamada([datetime]$fim) {
    $dur = [int][math]::Max(0, ($fim - $script:Inicio).TotalSeconds)
    $unix = [int64]([DateTimeOffset]$script:Inicio).ToUnixTimeSeconds()
    $linha = "chamada v1 | id=$([Convert]::ToString($unix, 16)) | ap=$($Cfg.aparelho) | inicio=$(Format-Iso $script:Inicio) | fim=$(Format-Iso $fim) | dur=$dur"
    Add-Content -Path (Get-FicheiroDia $script:Inicio) -Value ("{0}  {1} min {2:00} s" -f $script:Inicio.ToString('HH:mm'), [int][math]::Floor($dur / 60), ($dur % 60)) -Encoding UTF8
    Add-Fila $linha
    $script:EmChamada = $false
    $script:Inicio = $null
    Send-Fila
}

function Invoke-Tique {
    $agora = Get-Date
    $ativo = Test-WhatsAppMicrofone
    if ($ativo) {
        $script:FimMarcado = $null
        if (-not $script:EmChamada) { $script:EmChamada = $true; $script:Inicio = $agora }
    } elseif ($script:EmChamada) {
        if ($null -eq $script:FimMarcado) { $script:FimMarcado = $agora }
        elseif (($agora - $script:FimMarcado).TotalSeconds -ge $FolgaSeg) {
            $fim = $script:FimMarcado
            $script:FimMarcado = $null
            Complete-Chamada $fim
        }
    }
}

# ---------- Teste automatico (corre no GitHub Actions em Windows) ----------
if ($Teste) {
    $chave = Join-Path $Raiz '5319275A.WhatsAppDesktop_cv1g1gvanyjgm'
    New-Item -Path $chave -Force | Out-Null
    New-Item -Path (Join-Path $Raiz 'Microsoft.WindowsSoundRecorder_8wekyb3d8bbwe') -Force | Out-Null
    New-ItemProperty -Path (Join-Path $Raiz 'Microsoft.WindowsSoundRecorder_8wekyb3d8bbwe') -Name LastUsedTimeStart -PropertyType QWord -Value 5 -Force | Out-Null
    New-ItemProperty -Path (Join-Path $Raiz 'Microsoft.WindowsSoundRecorder_8wekyb3d8bbwe') -Name LastUsedTimeStop -PropertyType QWord -Value 0 -Force | Out-Null
    New-ItemProperty -Path $chave -Name LastUsedTimeStart -PropertyType QWord -Value 1 -Force | Out-Null
    New-ItemProperty -Path $chave -Name LastUsedTimeStop -PropertyType QWord -Value 2 -Force | Out-Null
    $falhas = 0
    function Confirma($cond, $msg) { if ($cond) { Write-Host "OK   $msg" } else { Write-Host "FALHA $msg"; $script:falhas++ } }

    Invoke-Tique
    Confirma (-not $script:EmChamada) 'gravador de som a usar o microfone nao conta'
    Set-ItemProperty -Path $chave -Name LastUsedTimeStop -Value 0
    Invoke-Tique
    Confirma $script:EmChamada 'WhatsApp a usar o microfone = chamada em curso'
    Start-Sleep -Seconds 3
    Set-ItemProperty -Path $chave -Name LastUsedTimeStop -Value 9
    Invoke-Tique
    Confirma $script:EmChamada 'microfone desligado ha menos de 4 s: ainda em curso'
    Set-ItemProperty -Path $chave -Name LastUsedTimeStop -Value 0
    Invoke-Tique
    Confirma ($script:EmChamada -and $null -eq $script:FimMarcado) 'microfone volta: mesma chamada'
    Set-ItemProperty -Path $chave -Name LastUsedTimeStop -Value 9
    Invoke-Tique
    Start-Sleep -Seconds 5
    Invoke-Tique
    Confirma (-not $script:EmChamada) 'microfone desligado 4 s: chamada terminada'
    Confirma ((Get-ContagemHoje) -eq 1) 'contagem de hoje = 1'
    $fila = @(Get-Content $FilaTxt -Encoding UTF8 | Where-Object { $_ })
    Confirma ($fila.Count -eq 1 -and $fila[0] -match '^chamada v1 \| id=[0-9a-f]+ \| ap=pc1 \| inicio=\S+ \| fim=\S+ \| dur=\d+$') "linha na fila: $($fila[0])"
    Confirma ($script:Erro -match 'token') 'sem token fica na fila com aviso'
    Remove-Item -Recurse -Force 'HKCU:\Software\ContadorChamadasTeste', $Pasta
    if ($falhas) { exit 1 } else { Write-Host 'Tudo certo.'; exit 0 }
}

# ---------- Execucao normal: icone na barra de tarefas ----------
$mutex = New-Object System.Threading.Mutex($false, 'Local\ContadorChamadasPacheco')
if (-not $mutex.WaitOne(0)) { exit 0 }   # ja esta a correr

Add-Type -AssemblyName System.Windows.Forms, System.Drawing
$icone = New-Object System.Windows.Forms.NotifyIcon
$icone.Icon = [System.Drawing.SystemIcons]::Information
$icone.Visible = $true
$menu = New-Object System.Windows.Forms.ContextMenuStrip
$null = $menu.Items.Add('Chamadas de hoje', $null, {
    $f = Get-FicheiroDia (Get-Date)
    $txt = if (Test-Path $f) { (Get-Content $f -Encoding UTF8) -join "`r`n" } else { 'Ainda nenhuma hoje.' }
    $estado = if ($script:Erro) { "`r`n`r`nAviso: $($script:Erro)" } elseif ($script:UltimoEnvio) { "`r`n`r`nUltimo envio as $($script:UltimoEnvio)" } else { '' }
    [System.Windows.Forms.MessageBox]::Show("$(Get-ContagemHoje) chamadas hoje`r`n`r`n$txt$estado", 'Contador de Chamadas') | Out-Null
})
$null = $menu.Items.Add('Enviar teste', $null, {
    Add-Fila "teste v1 | ap=$($Cfg.aparelho) | hora=$(Format-Iso (Get-Date))"
    Send-Fila
    $msg = if ($script:Erro) { "Falhou: $($script:Erro)" } else { 'Teste enviado. Esta tudo ligado.' }
    [System.Windows.Forms.MessageBox]::Show($msg, 'Contador de Chamadas') | Out-Null
})
$null = $menu.Items.Add('Sair', $null, { $icone.Visible = $false; [System.Windows.Forms.Application]::Exit() })
$icone.ContextMenuStrip = $menu

$timer = New-Object System.Windows.Forms.Timer
$timer.Interval = 2000
$script:Ciclos = 0
$timer.add_Tick({
    try {
        Invoke-Tique
        $script:Ciclos++
        if ($script:Ciclos % 150 -eq 0) { Send-Fila }   # de 5 em 5 min tenta o que ficou por enviar
        $t = "Chamadas hoje: $(Get-ContagemHoje)"
        if ($script:EmChamada) { $t += ' (em chamada)' }
        if ($script:Erro) { $t += ' - aviso' }
        $icone.Text = $t.Substring(0, [math]::Min(63, $t.Length))
    } catch { $script:Erro = $_.Exception.Message }
})
$timer.Start()
Send-Fila
[System.Windows.Forms.Application]::Run()
$mutex.ReleaseMutex()
