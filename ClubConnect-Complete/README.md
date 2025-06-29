# ClubConnect - Vereinsmanagement-System

Ein modernes, webbasiertes Vereinsmanagement-System für Sportvereine, entwickelt mit Flask.

## 🚀 Features

### Für alle Benutzer
- **Startseite** mit Übersicht über kommende Events und Nachrichten
- **Kalenderansicht** aller Events mit Filteroptionen
- **Event-Details** mit Teilnehmerlisten und Statistiken
- **Einladungsübersicht** für Spieler
- **Kleidungsregeln** nach Event-Typ
- **Vereinsnachrichten** mit Paginierung
- **Responsive Design** für alle Geräte

### Für Trainer/Admins
- **Admin-Dashboard** mit Statistiken
- **Event-Verwaltung**: Erstellen, Bearbeiten, Löschen
- **Spieler-Verwaltung**: Vollständige CRUD-Operationen
- **Einladungsmanagement**: Bulk-Einladungen und Status-Tracking
- **News-Verwaltung**: Nachrichten erstellen und verwalten
- **Kleidungsregeln-Verwaltung**
- **Sichere Authentifizierung** mit Session-Management

## 🛠️ Technologie-Stack

- **Backend**: Flask 2.3.3
- **Frontend**: Bootstrap 5.3, HTML5, CSS3, JavaScript
- **Datenbank**: SQLite (entwicklung) / PostgreSQL (produktion)
- **Formulare**: Flask-WTF, WTForms
- **Sicherheit**: CSRF-Schutz, sichere Sessions
- **Icons**: Bootstrap Icons

## 📋 Voraussetzungen

- Python 3.8 oder höher
- pip (Python Package Manager)

## 🔧 Installation

### 1. Repository klonen
```bash
git clone <repository-url>
cd ClubConnect-Complete
```

### 2. Virtuelle Umgebung erstellen (empfohlen)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Abhängigkeiten installieren
```bash
pip install -r requirements.txt
```

### 4. Datenbank initialisieren
```bash
python init_db.py
```

### 5. Anwendung starten

**Option 1: Mit Flask CLI (empfohlen)**
```bash
flask run
```

**Option 2: Direkt mit Python**
```bash
python run.py
```

**Option 3: Windows Batch-Datei**
```bash
start.bat
```

Die Anwendung ist dann unter `http://localhost:5000` erreichbar.

## 👤 Standard-Login

Nach der Initialisierung können Sie sich mit folgenden Daten anmelden:

- **Benutzername**: `admin`
- **Passwort**: `admin123`

⚠️ **Wichtig**: Ändern Sie das Passwort nach der ersten Anmeldung!

## 📁 Projektstruktur

```
ClubConnect-Complete/
├── app/                          # Hauptanwendungspaket
│   ├── __init__.py              # Flask App Factory
│   ├── models.py                # Datenbankmodelle
│   ├── forms.py                 # WTForms Formulare
│   ├── main/                    # Main Blueprint (öffentliche Seiten)
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── auth/                    # Authentication Blueprint
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── admin/                   # Admin Blueprint (Verwaltung)
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── static/                  # Statische Assets
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── main.js
│   └── templates/               # Jinja2 Templates
│       ├── base.html
│       ├── index.html
│       └── auth/
│           └── login.html
├── config.py                    # Konfigurationsklassen
├── run.py                       # Anwendungsentry Point
├── init_db.py                   # Datenbank-Initialisierung
├── requirements.txt             # Python-Abhängigkeiten
└── README.md                    # Diese Datei
```

## 🔧 Konfiguration

### Umgebungsvariablen

Sie können folgende Umgebungsvariablen setzen:

```bash
# Konfigurationsmodus
export FLASK_CONFIG=development  # development, production, testing

# Sicherheit
export SECRET_KEY=your-secret-key-here

# Datenbank
export DATABASE_URL=sqlite:///clubconnect.db

# Vereinsname
export CLUB_NAME="Ihr Vereinsname"
```

### Konfigurationsmodi

- **Development**: Debug-Modus aktiviert, SQLite-Datenbank
- **Production**: Optimiert für Produktion, sichere Cookies
- **Testing**: Für Unit-Tests, In-Memory-Datenbank

## 🚀 Deployment

### Heroku
```bash
# Heroku CLI installieren und einloggen
heroku create your-app-name
heroku config:set FLASK_CONFIG=heroku
heroku config:set SECRET_KEY=your-secret-key
git push heroku main
```

### Docker
```bash
# Dockerfile erstellen (nicht enthalten)
docker build -t clubconnect .
docker run -p 5000:5000 clubconnect
```

## 📊 Datenmodell

### Hauptentitäten

- **Events**: Trainings, Spiele, Turniere, Meetings
- **Players**: Spielerinformationen mit Teams und Positionen
- **Invites**: Many-to-Many Beziehung zwischen Events und Players
- **News**: Vereinsnachrichten
- **Clothing Rules**: Kleidungsregeln nach Event-Typ
- **Users**: Admin-Benutzer für Verwaltung

## 🔒 Sicherheit

- CSRF-Schutz für alle Formulare
- Sichere Session-Cookies
- SQL-Injection-Schutz durch parametrisierte Queries
- Passwort-Hashing mit Werkzeug
- Login-Required Decorators für geschützte Bereiche

## 🎨 Anpassung

### Design anpassen
- CSS-Variablen in `app/static/css/style.css` bearbeiten
- Bootstrap-Klassen in Templates anpassen
- Eigene CSS-Regeln hinzufügen

### Funktionen erweitern
- Neue Blueprints in `app/` erstellen
- Datenbankmodelle in `app/models.py` erweitern
- Neue Formulare in `app/forms.py` hinzufügen

## 🐛 Troubleshooting

### Häufige Probleme

1. **Datenbank-Fehler**
   ```bash
   # Datenbank neu initialisieren
   rm clubconnect_dev.db
   python init_db.py
   ```

2. **Import-Fehler**
   ```bash
   # Virtuelle Umgebung aktivieren
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

3. **Port bereits belegt**
   ```bash
   # Anderen Port verwenden
   export PORT=8000
   python run.py
   ```

## 📝 Entwicklung

### Neue Features hinzufügen

1. **Neues Datenmodell**:
   - Tabelle in `init_db()` hinzufügen
   - CRUD-Funktionen in `models.py` erstellen

2. **Neue Route**:
   - Route in entsprechendem Blueprint hinzufügen
   - Template erstellen
   - Formular definieren (falls nötig)

3. **Frontend-Änderungen**:
   - Templates in `app/templates/` bearbeiten
   - CSS in `app/static/css/style.css` anpassen
   - JavaScript in `app/static/js/main.js` erweitern

### Testing

```bash
# Unit-Tests ausführen (wenn vorhanden)
python -m pytest

# Manuelle Tests
python run.py
# Browser öffnen: http://localhost:5000
```

## 📄 Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Siehe LICENSE-Datei für Details.

## 🤝 Beitragen

1. Fork des Repositories erstellen
2. Feature-Branch erstellen (`git checkout -b feature/AmazingFeature`)
3. Änderungen committen (`git commit -m 'Add some AmazingFeature'`)
4. Branch pushen (`git push origin feature/AmazingFeature`)
5. Pull Request erstellen

## 📞 Support

Bei Fragen oder Problemen:

1. Issues im Repository erstellen
2. Dokumentation prüfen
3. Code-Kommentare lesen

## 🔄 Updates

### Version 1.0.0
- Grundfunktionalität implementiert
- Event-Management
- Spieler-Verwaltung
- Einladungssystem
- News-System
- Responsive Design

---

**ClubConnect** - Vereinsmanagement leicht gemacht! 🏆
