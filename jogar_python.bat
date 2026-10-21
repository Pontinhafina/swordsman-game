@echo off
title Swordsman: A Saga das 5 Fases (Python Native Edition)
echo ========================================================
echo   INICIANDO SWORDSMAN: A SAGA DAS 5 FASES (Pygame-CE)
echo ========================================================
echo.
echo Controles:
echo   [A] / [D] ou Setas : Mover
echo   [ESPACO] / [W]     : Pular (Solte rapido para pulo curto)
echo   [SHIFT] / [K]      : Dash (Arrancada rapida com invencibilidade)
echo   [S no ar] + Ataque : Pogo Attack (Pula sobre inimigos, espinhos e serras!)
echo   [J] / [Z]          : Atacar com a Espada (Corta correndo!)
echo   [Deslizar na Parede] + Pulo : Wall Jump!
echo   [E]                : Abrir Baus
echo   [F]                : Alternar Tela Cheia
echo   [ESC] / [P]        : Pausar
echo.
python main.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERRO] Ocorreu uma falha ao rodar o jogo.
    pause
)
