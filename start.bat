@echo off
echo Iniciando servidor e redirecionador...

REM Iniciar o servidor Python na porta 8000
start cmd /k python server.py

REM Aguardar um momento para o servidor iniciar
timeout /t 2 /nobreak > nul

REM Iniciar o redirecionador (requer privilégios de administrador)
echo Iniciando redirecionador (requer privilégios de administrador)...
powershell -Command "Start-Process python -ArgumentList 'redirect.py' -Verb RunAs"

echo.
echo Servidor rodando em:
echo http://localhost
echo http://localhost:8000
echo.
echo Pressione Ctrl+C para parar os servidores