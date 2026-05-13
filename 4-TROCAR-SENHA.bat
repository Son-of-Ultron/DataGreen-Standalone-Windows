@echo off
setlocal
cd /d "%~dp0backend"
set DATAGREEN_DESKTOP=1
set USE_SQLITE=1
if exist ".venv\Scripts\activate.bat" call ".venv\Scripts\activate.bat"
echo.
echo Troca de senha do DataGreen
echo Usuario recomendado para trocar primeiro: dono
echo.
set /p DG_USER=Digite o usuario para trocar a senha: 
if "%DG_USER%"=="" set DG_USER=dono
python manage.py changepassword %DG_USER%
echo.
echo Se a mensagem acima confirmou sucesso, a senha foi alterada.
pause
