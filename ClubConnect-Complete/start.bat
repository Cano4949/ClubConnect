@echo off
echo ================================================
echo ClubConnect - Vereinsmanagement-System
echo ================================================
echo.

REM Prüfen ob Python installiert ist
python --version >nul 2>&1
if errorlevel 1 (
    echo FEHLER: Python ist nicht installiert oder nicht im PATH.
    echo Bitte installieren Sie Python 3.8 oder höher.
    pause
    exit /b 1
)

echo Python gefunden.

REM Prüfen ob virtuelle Umgebung existiert
if not exist "venv" (
    echo Erstelle virtuelle Umgebung...
    python -m venv venv
    if errorlevel 1 (
        echo FEHLER: Konnte virtuelle Umgebung nicht erstellen.
        pause
        exit /b 1
    )
)

echo Aktiviere virtuelle Umgebung...
call venv\Scripts\activate.bat

echo Installiere Abhängigkeiten...
pip install -r requirements.txt
if errorlevel 1 (
    echo FEHLER: Konnte Abhängigkeiten nicht installieren.
    pause
    exit /b 1
)

REM Prüfen ob Datenbank existiert
if not exist "clubconnect_dev.db" (
    echo Initialisiere Datenbank...
    python init_db.py
    if errorlevel 1 (
        echo FEHLER: Konnte Datenbank nicht initialisieren.
        pause
        exit /b 1
    )
)

echo.
echo ================================================
echo ClubConnect wird gestartet...
echo ================================================
echo.
echo Öffnen Sie Ihren Browser und gehen Sie zu:
echo http://localhost:5000
echo.
echo Login-Daten:
echo Benutzername: admin
echo Passwort: admin123
echo.
echo Drücken Sie Ctrl+C um den Server zu stoppen.
echo ================================================
echo.

REM Server starten
python run.py

pause
