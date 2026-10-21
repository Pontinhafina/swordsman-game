@echo off
title Swordsman: Guerra na Floresta
echo ========================================================
echo   INICIANDO SWORDSMAN: GUERRA NA FLORESTA (HTML5)
echo ========================================================
echo.
echo Abrindo o jogo no seu navegador...
echo Para fechar o jogo, basta fechar esta janela.
echo.

start "" "http://localhost:8000/index.html"
python -m http.server 8000

pause
