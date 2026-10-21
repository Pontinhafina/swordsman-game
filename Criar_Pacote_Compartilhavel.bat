@echo off
title Criar Pacote Compartilhavel Swordsman
echo ========================================================
echo   GERANDO EXECUTAVEL STANDALONE E ARQUIVO ZIP
echo ========================================================
echo.
echo 1. Compilando com PyInstaller...
pyinstaller --noconsole --name "Swordsman" --icon "game_icon.ico" --add-data "SPRITES;SPRITES" --onedir --clean --noconfirm main.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERRO] Falha na compilacao com PyInstaller.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo 2. Copiando assets adicionais...
xcopy /E /I /Y "SPRITES" "dist\Swordsman\SPRITES" >nul
copy /Y "dist\Swordsman\LEIA-ME_COMO_JOGAR.txt" "dist\Swordsman\" >nul
copy /Y "dist\Swordsman\JOGAR.bat" "dist\Swordsman\" >nul

echo.
echo 3. Compactando em Swordsman_Jogo_Completo_v1.0.zip...
powershell -Command "Compress-Archive -Path 'dist/Swordsman/*' -DestinationPath 'Swordsman_Jogo_Completo_v1.0.zip' -Force"

echo.
echo ========================================================
echo   SUCESSO! O arquivo Swordsman_Jogo_Completo_v1.0.zip
echo   esta pronto na pasta raiz para voce enviar!
echo ========================================================
pause
