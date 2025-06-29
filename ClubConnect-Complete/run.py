#!/usr/bin/env python3
"""
ClubConnect - Vereinsmanagement-System
Entry Point für die Flask-Anwendung
"""

import os
import sys

# Stelle sicher, dass der aktuelle Ordner im Python-Pfad ist
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import create_app
    from app.models import init_db
    
    print("Importiere Flask-App...")
    
    # Konfiguration aus Umgebungsvariable oder Standard
    config_name = os.environ.get('FLASK_CONFIG') or 'development'
    
    # Flask-App erstellen
    print("Erstelle Flask-App...")
    app = create_app(config_name)
    
    # Datenbank initialisieren falls nötig
    with app.app_context():
        try:
            init_db()
            print("Datenbank initialisiert.")
        except Exception as e:
            print(f"Datenbank bereits vorhanden: {e}")
    
    print("Flask-App erfolgreich erstellt!")
    print("Starte Server auf http://localhost:5000")
    print("Login: admin / admin123")
    
    if __name__ == '__main__':
        # Entwicklungsserver starten
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=True)
        
except ImportError as e:
    print(f"Import-Fehler: {e}")
    print("Installiere Dependencies mit: pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"Fehler beim Starten der App: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
