@echo off
setlocal
cd /d "%~dp0backend"
set DATAGREEN_DESKTOP=1
set USE_SQLITE=1
if exist ".venv\Scripts\activate.bat" call ".venv\Scripts\activate.bat"
python manage.py backup_sqlite
pause
