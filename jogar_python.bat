@echo off
title Swordsman: A Saga das 10 Fases (Python Native Edition)
echo ========================================================
echo   INICIANDO SWORDSMAN: A SAGA DAS 10 FASES (Pygame-CE)
echo ========================================================
echo.
echo Controles:
echo   [A] / [D] ou Setas : Mover (Movimentacao fluida e estavel)
echo   [ESPACO] / [W]     : Pular (Toque rapido para pulo curto)
echo   [SHIFT] / [K] / [C]: Dash (Arrancada rapida com invencibilidade)
echo   [J] / [Z]          : Atacar com a Espada (Corta correndo!)
echo   [S no ar] + Ataque : Pogo Attack (Pula sobre orcs, espinhos e serras!)
echo   [Deslizar Parede] + Pulo : Wall Jump!
echo   [E]                : Abrir Baus
echo   [M]                : Ligar / Desligar Musica Chiptune
echo   [F]                : Alternar Tela Cheia
echo   [ESC] / [P]        : Pausar
echo.
python main.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERRO] Ocorreu uma falha ao rodar o jogo.
    pause
)
