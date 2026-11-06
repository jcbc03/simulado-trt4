$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Out = Join-Path $Root "dist\SimuladorTRT4-Instalador"
$Zip = Join-Path $Root "dist\SimuladorTRT4-Instalador.zip"

Write-Host "Gerando icone..."
Set-Location $Root
python scripts\criar_icone.py

if (-not (Test-Path (Join-Path $Root "data\questoes_iniciais.json"))) {
    python scripts\gerar_questoes.py
}

Write-Host "Montando pasta do instalador..."
if (Test-Path $Out) { Remove-Item $Out -Recurse -Force }
New-Item -ItemType Directory -Force -Path $Out | Out-Null

$items = @(
    "app.py", "launcher.py", "requirements.txt", "README.md", "run.bat", "instalar.bat",
    "modules", "data", "assets", "scripts", ".streamlit", "docs"
)
foreach ($item in $items) {
    $src = Join-Path $Root $item
    if (-not (Test-Path $src)) { continue }
    Copy-Item $src (Join-Path $Out $item) -Recurse -Force
}

# remove DB local do pacote (sera gerado na instalacao)
$db = Join-Path $Out "data\trt4.db"
if (Test-Path $db) { Remove-Item $db -Force }
Get-ChildItem (Join-Path $Out "data") -Filter "_upload_tmp*" -ErrorAction SilentlyContinue | Remove-Item -Force
Get-ChildItem (Join-Path $Out "data") -Filter "launcher.log" -ErrorAction SilentlyContinue | Remove-Item -Force

$LeiaMe = @"
SIMULADOR TRT4 FCC - INSTALACAO
================================

1. Certifique-se de ter Python 3.11+ instalado (com PATH).
2. Execute instalar.bat (duplo clique).
3. A instalacao e automatica: copia arquivos, cria venv, importa questoes
   e cria o atalho "Simulador TRT4" na Area de Trabalho.
4. O app abre sozinho no navegador ao final.

Pasta de instalacao: %LOCALAPPDATA%\SimuladorTRT4
Desinstalar: rode desinstalar.bat nessa pasta.

Offline apos a instalacao (nao precisa de internet para estudar).
"@
Set-Content -Path (Join-Path $Out "LEIA-ME.txt") -Value $LeiaMe -Encoding UTF8

Write-Host "Compactando ZIP..."
New-Item -ItemType Directory -Force -Path (Split-Path $Zip) | Out-Null
if (Test-Path $Zip) { Remove-Item $Zip -Force }
Compress-Archive -Path (Join-Path $Out "*") -DestinationPath $Zip -Force

Write-Host "Pacote pronto:"
Write-Host "  $Out"
Write-Host "  $Zip"
Get-Item $Zip | Format-List FullName, Length
