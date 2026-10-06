# Instala o Contador de Chamadas para o utilizador atual (sem administrador):
# copia o programa para %LOCALAPPDATA%\ContadorChamadas, guarda o codigo de acesso, arranca com o Windows e abre ja.
$ErrorActionPreference = 'Stop'
$origem = Split-Path -Parent $MyInvocation.MyCommand.Path
$pasta = Join-Path $env:LOCALAPPDATA 'ContadorChamadas'
New-Item -ItemType Directory -Force -Path $pasta | Out-Null

# Fechar uma versao antiga que esteja a correr
Get-CimInstance Win32_Process -Filter "Name='powershell.exe'" -ErrorAction SilentlyContinue |
    Where-Object { $_.CommandLine -like '*ContadorChamadas\contador.ps1*' } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }

Copy-Item (Join-Path $origem 'contador.ps1') (Join-Path $pasta 'contador.ps1') -Force
Unblock-File (Join-Path $pasta 'contador.ps1') -ErrorAction SilentlyContinue

$cfgPath = Join-Path $pasta 'config.json'
$cfg = @{ token = ''; repo = 'tspacheco/Designerpacheco'; issue = '3'; aparelho = 'pc1' }
if (Test-Path $cfgPath) {
    $velho = Get-Content $cfgPath -Raw | ConvertFrom-Json
    foreach ($n in 'token', 'repo', 'issue', 'aparelho') { if ($velho.$n) { $cfg[$n] = [string]$velho.$n } }
}
Write-Host ''
Write-Host 'Contador de Chamadas - instalacao' -ForegroundColor Yellow
Write-Host ''
$pergunta = if ($cfg.token) { 'Cola o codigo de acesso (Enter para manter o atual)' } else { 'Cola o codigo de acesso (comeca por github_pat_)' }
$novo = (Read-Host $pergunta).Trim()
if ($novo) { $cfg.token = $novo }
($cfg | ConvertTo-Json) | Set-Content -Path $cfgPath -Encoding UTF8

# Arranque automatico: atalho na pasta Arranque do utilizador
$args_ = "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$pasta\contador.ps1`""
$arranque = [Environment]::GetFolderPath('Startup')
$sh = New-Object -ComObject WScript.Shell
$lnk = $sh.CreateShortcut((Join-Path $arranque 'Contador de Chamadas.lnk'))
$lnk.TargetPath = (Get-Command powershell.exe).Source
$lnk.Arguments = $args_
$lnk.WindowStyle = 7
$lnk.Save()

Start-Process powershell.exe -ArgumentList $args_ -WindowStyle Hidden
Write-Host ''
Write-Host 'Pronto. Aparece um icone (i) junto ao relogio do Windows.' -ForegroundColor Green
Write-Host 'Botao direito no icone > Enviar teste, para confirmar que esta ligado.'
Write-Host ''
Read-Host 'Enter para fechar'
