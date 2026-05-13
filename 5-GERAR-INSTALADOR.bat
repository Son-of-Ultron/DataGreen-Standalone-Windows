@echo off
setlocal EnableExtensions
chcp 65001 >nul
cd /d "%~dp0"

where powershell >nul 2>&1
if errorlevel 1 (
  echo PowerShell nao encontrado neste Windows.
  pause
  exit /b 1
)

echo.
echo ============================================================
echo  DataGreen - gerar instalador .exe
echo ============================================================
echo.

powershell -NoProfile -ExecutionPolicy Bypass -File "%CD%\windows\build-installer.ps1"
if errorlevel 1 (
  echo.
  echo Falha ao gerar o instalador.
  pause
  exit /b 1
)

echo.
echo Instalador pronto em:
echo   release\installer\DataGreen_Setup.exe
echo.
pause
endlocal
exit /b 0
