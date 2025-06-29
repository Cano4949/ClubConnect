# ClubConnect - Complete Edition

Eine vollständige Flask-Anwendung zur Verwaltung von Jugendmannschaften im Sportverein.

## 🚀 Schnellstart

### 1. Voraussetzungen
- Python 3.8 oder höher
- pip (Python Package Manager)

### 2. Installation

```bash
# 1. Virtuelle Umgebung erstellen
python -m venv venv

# 2. Virtuelle Umgebung aktivieren
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Dependencies installieren
pip install -r requirements.txt

# 4. Umgebungsvariablen kopieren
copy .env.example .env
# oder auf Linux/Mac:
# cp .env.example .env

# 5. Datenbank initialisieren
python init_db.py init

# 6. Testdaten laden (optional)
python init_db.py seed
```

### 3. Anwendung starten

```bash
python run.py
```

Die Anwendung ist dann unter http://localhost:5000 erreichbar.

## 📝 Standard-Login

- **Benutzername**: trainer
- **Passwort**: trainer123

## 📁 Projektstruktur

```
ClubConnect-Complete/
├── app/                    # Hauptanwendung
│   ├── __init__.py        # Flask App Factory
│   ├── models.py          # Datenbankmodelle
│   ├── forms.py           # WTForms Formulare
│   ├── static/            # CSS, JS, Bilder
│   ├── templates/         # HTML Templates
│   ├── main/              # Öffentliche Routen
│   ├── auth/              # Authentifizierung
│   └── admin/             # Admin-Bereich
├── config.py              # Konfiguration
├── run.py                 # Startskript
├── init_db.py             # DB-Initialisierung
├── requirements.txt       # Dependencies
├── .env.example           # Umgebungsvariablen
└── README.md              # Diese Datei
```

## 🔧 Konfiguration

Bearbeiten Sie die `.env` Datei für Ihre Einstellungen:

```env
# Flask
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Datenbank
DATABASE_URL=sqlite:///clubconnect.db

# Club
CLUB_NAME=Ihr Vereinsname
```

## 🎯 Features

- **Event-Management**: Trainings, Spiele, Turniere verwalten
- **Spielerverwaltung**: Teams, Positionen, Kontaktdaten
- **Einladungssystem**: Automatische Einladungen mit Status-Tracking
- **Kleidungsregeln**: Definierte Dress-Codes für Events
- **News-System**: Vereinsnachrichten veröffentlichen
- **Admin-Dashboard**: Übersichtliche Verwaltung

## 🛠️ Entwicklung

### Datenbank-Befehle

```bash
# Datenbank initialisieren
python init_db.py init

# Datenbank zurücksetzen
python init_db.py reset

# Testdaten einfügen
python init_db.py seed

# Datenbank-Info anzeigen
python init_db.py info
```

### Flask Shell

```bash
flask shell
```

In der Shell verfügbar:
- `db`: Datenbank-Instanz
- `User`, `Event`, `Player`, etc.: Alle Modelle

## 📚 Weitere Dokumentation

Siehe die Hauptdokumentation im übergeordneten Verzeichnis für:
- Technische Details
- Datenmodell
- API-Referenz
- Deployment-Anleitung

## 🐛 Fehlerbehebung

### Häufige Probleme

1. **ModuleNotFoundError**
   - Lösung: Virtuelle Umgebung aktivieren und `pip install -r requirements.txt` ausführen

2. **Datenbank-Fehler**
   - Lösung: `python init_db.py reset` ausführen

3. **Login funktioniert nicht**
   - Lösung: Prüfen Sie, ob die Datenbank initialisiert wurde

## 📄 Lizenz

MIT License - siehe LICENSE Datei

---

**ClubConnect** - Moderne Vereinsverwaltung für Jugendmannschaften
