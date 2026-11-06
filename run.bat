@echo off
cd /d "%~dp0"
where python >nul 2>&1 || (
  echo Python nao encontrado no PATH.
  pause
  exit /b 1
)
python -c "from modules.db import count_questoes, init_db; init_db(); import sys; sys.exit(0 if count_questoes()>0 else 1)" || python -m modules.importar_questoes
echo.
echo Abrindo Simulador TRT4 FCC em http://localhost:8501
echo.
streamlit run app.py --server.port 8501
pause
