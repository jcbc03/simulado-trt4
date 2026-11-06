$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$InstallDir = Join-Path $env:LOCALAPPDATA "SimuladorTRT4"
$VenvDir = Join-Path $InstallDir ".venv"
$Python = "python"

Write-Host "[1/6] Preparando pasta em $InstallDir"
New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null

$copyItems = @(
    "app.py", "launcher.py", "requirements.txt", "README.md", "run.bat",
    "modules", "data", "assets", "scripts", ".streamlit"
)
foreach ($item in $copyItems) {
    $src = Join-Path $Root $item
    $dst = Join-Path $InstallDir $item
    if (-not (Test-Path $src)) { continue }
    if (Test-Path $src -PathType Container) {
        if (Test-Path $dst) { Remove-Item $dst -Recurse -Force }
        Copy-Item $src $dst -Recurse -Force
    } else {
        Copy-Item $src $dst -Force
    }
}

# nao copiar DB de teste sujo: regenerar no destino
$db = Join-Path $InstallDir "data\trt4.db"
if (Test-Path $db) { Remove-Item $db -Force }

Write-Host "[2/6] Criando ambiente virtual"
& $Python -m venv $VenvDir
$Py = Join-Path $VenvDir "Scripts\python.exe"
$PyW = Join-Path $VenvDir "Scripts\pythonw.exe"
$Pip = Join-Path $VenvDir "Scripts\pip.exe"
if (-not (Test-Path $Py)) { throw "Falha ao criar venv" }

Write-Host "[3/6] Instalando dependencias"
& $Py -m pip install --upgrade pip | Out-Null
& $Py -m pip install -r (Join-Path $InstallDir "requirements.txt")

Write-Host "[4/6] Gerando icone e banco de questoes"
Set-Location $InstallDir
$env:PYTHONPATH = $InstallDir
& $Py (Join-Path $InstallDir "scripts\criar_icone.py")
& $Py -m modules.importar_questoes

Write-Host "[5/6] Criando atalho na Area de Trabalho"
$Icon = Join-Path $InstallDir "assets\icon.ico"
$TargetPy = if (Test-Path $PyW) { $PyW } else { $Py }
& powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $InstallDir "scripts\criar_atalho.ps1") `
    -InstallDir $InstallDir -PythonExe $TargetPy -IconPath $Icon

# tambem Start Menu
$StartMenu = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs"
$SmShortcut = Join-Path $StartMenu "Simulador TRT4.lnk"
$W = New-Object -ComObject WScript.Shell
$S = $W.CreateShortcut($SmShortcut)
$S.TargetPath = $TargetPy
$S.Arguments = "`"$(Join-Path $InstallDir 'launcher.py')`""
$S.WorkingDirectory = $InstallDir
$S.WindowStyle = 7
$S.Description = "Simulador TRT4 FCC"
if (Test-Path $Icon) { $S.IconLocation = "$Icon,0" }
$S.Save()

Write-Host "[6/6] Gravando desinstalador"
$Uninstall = @"
@echo off
echo Removendo Simulador TRT4...
del /f /q "%USERPROFILE%\Desktop\Simulador TRT4.lnk" 2>nul
del /f /q "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Simulador TRT4.lnk" 2>nul
rmdir /s /q "%LOCALAPPDATA%\SimuladorTRT4"
echo Removido.
pause
"@
Set-Content -Path (Join-Path $InstallDir "desinstalar.bat") -Value $Uninstall -Encoding ASCII

Write-Host "OK - Instalado em $InstallDir"
exit 0
