@echo off
title Sistema de Almoxarifado - Flexcolor

echo ===========================================
echo    INICIANDO SISTEMA DE NOTAS FISCAIS
echo ===========================================
echo.

cd /d %~dp0

echo Verificando dependencias...

pip show flask >nul 2>&1 || pip install flask
pip show pandas >nul 2>&1 || pip install pandas
pip show openpyxl >nul 2>&1 || pip install openpyxl
pip show psycopg2 >nul 2>&1 || pip install psycopg2-binary

echo.
echo Iniciando servidor Flask...
echo.

start http://127.0.0.1:5000

python app.py

echo.
echo Servidor encerrado.
pause