@echo off
title Abrindo Projeto no Godot 4
echo ========================================================
echo   ABRINDO "SWORDSMAN" NO GODOT ENGINE 4
echo ========================================================
echo.
echo Iniciando o editor do Godot com seu projeto...
echo.

set GODOT_EXE=%USERPROFILE%\Downloads\Godot_v4.7.2-stable_win64.exe\Godot_v4.7.2-stable_win64.exe

if exist %GODOT_EXE% (
    start "" "%GODOT_EXE%" -e --path "%~dp0."
) else (
    echo [AVISO] Nao encontramos o Godot no caminho de Downloads.
    echo Por favor, abra o seu Godot e selecione a pasta:
    echo "%~dp0."
    pause
)
