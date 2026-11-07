@echo off
title Simulador TRT4 - Acesso pela internet
cd /d "%~dp0"

echo ============================================
echo  Simulador TRT4 - servidor + tunel Cloudflare
echo ============================================
echo.

where python >nul 2>&1 || (
  echo [ERRO] Python nao encontrado no PATH.
  pause
  exit /b 1
)

REM 1) Garante banco
python -c "from modules.db import count_questoes, init_db; init_db(); import sys; sys.exit(0 if count_questoes()>0 else 1)" || python -m modules.importar_questoes

REM 2) Sobe o Streamlit em segundo plano (se ainda nao estiver rodando)
powershell -NoProfile -Command "if (-not (Test-NetConnection -ComputerName 127.0.0.1 -Port 8501 -InformationLevel Quiet)) { Start-Process -WindowStyle Minimized -FilePath 'python' -ArgumentList '-m','streamlit','run','app.py','--server.headless=true','--server.port=8501','--server.address=127.0.0.1'; Start-Sleep -Seconds 8 }"

REM 3) Abre o tunel e mostra o link
echo Abrindo tunel... o link publico aparece abaixo.
echo.
python tunel.py

echo.
echo Tunel encerrado. O app local continua em http://localhost:8501
pause
