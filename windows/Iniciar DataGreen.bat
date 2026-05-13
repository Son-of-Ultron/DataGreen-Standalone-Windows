@echo off
chcp 65001 >nul
cd /d "%~dp0\.."

where pythonw >nul 2>&1
if errorlevel 1 (
  echo.
  echo [DataGreen] Python não encontrado no PATH.
  echo Instale Python 3.10 ou mais novo em https://www.python.org/downloads/
  echo e marque "Add python.exe to PATH".
  echo.
  pause
  exit /b 1
)

REM Preferir pythonw para não abrir janela preta; se falhar, tenta python.
pythonw "%~dp0datagreen_tray.py" 2>nul
if errorlevel 1 (
  start "DataGreen" /min python "%~dp0datagreen_tray.py"
)
