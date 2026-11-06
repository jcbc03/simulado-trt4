@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title Instalador Simulador TRT4 FCC
echo ============================================
echo  Simulador TRT4 FCC - Instalacao automatica
echo ============================================
echo.

where python >nul 2>&1
if errorlevel 1 (
  echo [ERRO] Python nao encontrado no PATH.
  echo Instale Python 3.11+ em https://www.python.org/downloads/
  echo Marque "Add python.exe to PATH" na instalacao.
  pause
  exit /b 1
)

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\instalar.ps1"
set ERR=%ERRORLEVEL%
if not %ERR%==0 (
  echo.
  echo [ERRO] Instalacao falhou. Codigo %ERR%.
  pause
  exit /b %ERR%
)

echo.
echo Instalacao concluida. Atalho criado na Area de Trabalho.
echo Abrindo o Simulador...
echo.
start "" "%USERPROFILE%\Desktop\Simulador TRT4.lnk"
timeout /t 3 /nobreak >nul
exit /b 0
