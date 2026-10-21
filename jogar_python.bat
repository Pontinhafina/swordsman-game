@echo off
title Swordsman: Guerra Orc (Python Native Edition)
echo ========================================================
echo   INICIANDO SWORDSMAN: GUERRA ORC (Pygame-CE)
echo ========================================================
echo.
echo Controles:
echo   [A] / [D] ou Setas : Mover
echo   [W] / Espaco / C   : Pular
echo   [S] no ar          : Pogo Attack (Golpe para Baixo)
echo   [J] / X            : Atacar com a Espada
echo   [F]                : Alternar Tela Cheia
echo   [ESC] / [P]        : Pausar
echo.
python main.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERRO] Ocorreu uma falha ao rodar o jogo.
    pause
)
