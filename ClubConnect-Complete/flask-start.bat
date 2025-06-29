@echo off
echo ================================================
echo ClubConnect - Flask Run
echo ================================================
echo.

cd /d "%~dp0"

echo Setze Umgebungsvariablen...
set FLASK_APP=run.py
set FLASK_ENV=development
set FLASK_DEBUG=1

echo Starte Flask...
echo.
echo Öffnen Sie Ihren Browser und gehen Sie zu:
echo http://localhost:5000
echo.
echo Login: admin / admin123
echo.
echo Drücken Sie Ctrl+C um zu stoppen.
echo ================================================

flask run

pause
