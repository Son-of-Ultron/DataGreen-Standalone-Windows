@echo off
setlocal EnableExtensions
chcp 65001 >nul
title DataGreen — primeira configuração

set "WINGET_TRIED=0"

REM Raiz do projeto (pasta que contém "backend" e "windows")
cd /d "%~dp0\.."
if not exist "backend\manage.py" (
  echo.
  echo [DataGreen] Pasta incorreta: não encontrei backend\manage.py
  echo Certifique-se de que este arquivo está em ...\DataGreen\windows\
  echo.
  pause
  exit /b 1
)

echo.
echo ============================================================
echo  DataGreen — primeira configuração
echo  Instala dependências com: python -m pip  ^(ou py -3 -m pip^)
echo ============================================================
echo.

:find_python
set "RUNPIP="
py -3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>&1
if not errorlevel 1 set "RUNPIP=py -3 -m pip"

if not defined RUNPIP (
  python -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>&1
  if not errorlevel 1 set "RUNPIP=python -m pip"
)

if defined RUNPIP goto :install_deps

REM --- Python não encontrado ---
if "%WINGET_TRIED%"=="1" (
  echo.
  echo [DataGreen] Python foi instalado, mas esta janela ainda não "vê" o comando.
  echo.
  echo Feche esta janela e execute "PrimeiraConfiguracao.bat" de novo.
  echo ^(Se continuar falhando, reinicie o computador uma vez.^)
  echo.
  pause
  exit /b 1
)

echo [DataGreen] Não encontrei Python 3.10 ou mais novo no PATH.
echo.

where winget >nul 2>&1
if errorlevel 1 goto :no_winget

echo Opcional: o Windows pode instalar o Python por aqui ^(winget^).
echo Precisa de internet. Pode pedir permissão de administrador.
echo.
choice /c SN /m "Tentar instalar Python 3.12 automaticamente? [S]im ou [N]ao"
if errorlevel 2 goto :manual_install
if errorlevel 1 goto :try_winget

:try_winget
echo.
echo [DataGreen] Instalando Python.Python.3.12 via winget...
winget install -e --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements --disable-interactivity
if errorlevel 1 (
  echo.
  echo [DataGreen] O winget não concluiu. Tente instalar o Python manualmente ^(abaixo^).
  goto :manual_install
)

echo.
echo [DataGreen] Ajustando PATH nesta janela para a instalação típica do winget...
if exist "%LocalAppData%\Programs\Python\Python312\python.exe" (
  set "PATH=%LocalAppData%\Programs\Python\Python312;%LocalAppData%\Programs\Python\Python312\Scripts;%PATH%"
)
if exist "%LocalAppData%\Programs\Python\Python313\python.exe" (
  set "PATH=%LocalAppData%\Programs\Python\Python313;%LocalAppData%\Programs\Python\Python313\Scripts;%PATH%"
)

set "WINGET_TRIED=1"
goto :find_python

:no_winget
echo Este Windows não tem "winget" no PATH ^(ou é uma versão antiga^).
echo.
goto :manual_install

:manual_install
echo ------------------------------------------------------------
echo  Instale o Python manualmente:
echo  1^) Abra https://www.python.org/downloads/
echo  2^) Baixe o instalador ^(3.10 ou mais novo^)
echo  3^) Marque "Add python.exe to PATH"
echo  4^) Feche esta janela e execute "PrimeiraConfiguracao.bat" de novo
echo ------------------------------------------------------------
echo.
pause
exit /b 1

:install_deps
echo [DataGreen] Comando pip: %RUNPIP%
echo.

echo [1/3] Atualizando o pip...
%RUNPIP% install --upgrade pip
if errorlevel 1 (
  echo.
  echo [DataGreen] Falha ao atualizar o pip. Verifique a internet e tente de novo.
  pause
  exit /b 1
)

echo.
echo [2/3] Instalando dependências do servidor ^(Django, etc.^)...
%RUNPIP% install -r "%CD%\backend\requirements.txt"
if errorlevel 1 (
  echo.
  echo [DataGreen] Falha ao instalar backend\requirements.txt
  pause
  exit /b 1
)

echo.
echo [3/3] Instalando dependências do ícone na bandeja ^(pystray, Pillow^)...
%RUNPIP% install -r "%CD%\windows\requirements-launcher.txt"
if errorlevel 1 (
  echo.
  echo [DataGreen] Falha ao instalar windows\requirements-launcher.txt
  pause
  exit /b 1
)

echo.
echo ============================================================
echo  Concluído com sucesso.
echo.
echo  Próximo passo: dê duplo clique em "Iniciar DataGreen.bat"
echo  ^(na pasta windows^). O navegador abrirá e o ícone aparecerá
echo  perto do relógio.
echo ============================================================
echo.
pause
endlocal
exit /b 0
