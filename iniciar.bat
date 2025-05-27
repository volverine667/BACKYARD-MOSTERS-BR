@echo off
cd /d "%~dp0"
echo Iniciando o servidor...
python app.py
start http://localhost:3001
pause