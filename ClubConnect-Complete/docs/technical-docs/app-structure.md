---
title: App Structure
parent: Technical Docs
nav_order: 1
---

{: .label }
Technical Documentation

# App Structure

ClubConnect folgt einer modularen Flask-Architektur mit Blueprint-Pattern für bessere Skalierbarkeit und Wartbarkeit.

## 🏗️ Architektur-Übersicht

```
ClubConnect/
├── app/                          # Hauptanwendungspaket
│   ├── __init__.py              # Flask App Factory
│   ├── models.py                # Datenbankmodelle
│   ├── forms.py                 # WTForms Formulare
│   ├── main/                    # Main Blueprint
│   ├── auth/                    # Authentication Blueprint
│   ├── admin/                   # Admin Blueprint
│   ├── static/                  # Statische Assets
│   └── templates/               # Jinja2 Templates
├── config.py                    # Konfigurationsklassen
├── run.py                       # Anwendungsentry Point
└── instance/                    # Instanz-spezifische Dateien
```

## 📦 Blueprint-Architektur

### Main Blueprint (`app/main/`)
**Zweck**: Öffentliche Seiten für alle Benutzer

**Routen**:
- `/` - Startseite mit Übersicht
- `/calendar` - Kalenderansicht aller Events
- `/event/<id>` - Event-Detailseite
- `/invites` - Einladungsübersicht
- `/clothing` - Kleidungsregeln
- `/news` - Vereinsnachrichten

**Funktionen**:
- Event-Anzeige und -Filterung
- Spieler-Einladungsstatus
- Responsive Kalenderansicht
- News-Paginierung

### Authentication Blueprint (`app/auth/`)
**Zweck**: Benutzeranmeldung und Session-Management

**Routen**:
- `/auth/login` - Login-Formular
- `/auth/logout` - Benutzer abmelden

**Funktionen**:
- Sichere Passwort-Authentifizierung
- Session-Management
- Login-Required Decorator
- Trainer-Role Validation

### Admin Blueprint (`app/admin/`)
**Zweck**: Verwaltungsfunktionen für Trainer

**Routen**:
- `/admin/` - Admin-Dashboard
- `/admin/events` - Event-Verwaltung
- `/admin/events/create` - Neues Event erstellen
- `/admin/events/<id>/edit` - Event bearbeiten
- `/admin/events/<id>/invites` - Einladungen verwalten
- `/admin/players` - Spieler-Verwaltung
- `/admin/news` - News-Verwaltung
- `/admin/clothing` - Kleidungsregeln-Verwaltung

**Funktionen**:
- CRUD-Operationen für alle Entitäten
- Bulk-Einladungen
- Statistiken und Reports
- Datenexport

## 🗄️ Datenschicht

### Models (`app/models.py`)

**Hauptmodelle**:
```python
# Event-Modell
events:
  - id (Primary Key)
  - title, type, date, time
  - location, clothing
  - description
  - timestamps

# Player-Modell  
players:
  - id (Primary Key)
  - name, team, email, phone
  - birth_date, position
  - jersey_number, active
  - timestamps

# Invite-Modell (Many-to-Many)
invites:
  - id (Primary Key)
  - player_id (Foreign Key)
  - event_id (Foreign Key)
  - status, notes
  - timestamps
```

**Hilfsfunktionen**:
- `get_db_connection()` - Datenbankverbindung
- `get_upcoming_events()` - Nächste Events
- `get_latest_news()` - Aktuelle Nachrichten
- `get_player_invites_for_event()` - Event-Einladungen

### Database Connection
```python
def get_db_connection():
    """Erstellt SQLite-Verbindung mit Row Factory"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn
```

## 🎨 Presentation Layer

### Templates (`app/templates/`)

**Base Template** (`base.html`):
- Bootstrap 5.3 Integration
- Responsive Navigation
- Flash Message System
- Custom CSS Variables
- Icon Integration (Bootstrap Icons)

**Template-Hierarchie**:
```
base.html
├── index.html (Startseite)
├── calendar.html (Kalender)
├── event_detail.html (Event-Details)
├── invites.html (Einladungen)
├── clothing.html (Kleidungsregeln)
├── news.html (Nachrichten)
└── auth/
    └── login.html (Login)
```

**Template-Features**:
- Jinja2 Template-Vererbung
- Custom Template-Filter
- Responsive Grid-Layout
- Component-basierte Struktur

### Static Assets (`app/static/`)

**CSS** (`static/css/`):
- Custom CSS-Variablen
- Responsive Breakpoints
- Component-spezifische Styles
- Print-Styles

**JavaScript** (`static/js/`):
- Minimales JavaScript (gemäß Anforderung)
- Bootstrap-Komponenten
- Form-Validierung
- AJAX-Funktionen (falls benötigt)

**Images** (`static/img/`):
- Logo und Branding
- Placeholder-Bilder
- Icons und Grafiken

## ⚙️ Konfiguration

### Config Classes (`config.py`)

**Umgebungen**:
- `DevelopmentConfig` - Entwicklung
- `TestingConfig` - Tests
- `ProductionConfig` - Produktion
- `HerokuConfig` - Heroku-Deployment
- `DockerConfig` - Container-Deployment

**Konfigurationsparameter**:
```python
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DATABASE_URL = os.environ.get('DATABASE_URL')
    CLUB_NAME = os.environ.get('CLUB_NAME')
    WTF_CSRF_ENABLED = True
    SESSION_COOKIE_HTTPONLY = True
```

### App Factory (`app/__init__.py`)

**Initialisierung**:
```python
def create_app(config_name=None):
    app = Flask(__name__)
    
    # Konfiguration laden
    config_class = config.get(config_name, config['development'])
    app.config.from_object(config_class)
    
    # Extensions initialisieren
    csrf.init_app(app)
    
    # Blueprints registrieren
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    return app
```

## 🔐 Sicherheitsarchitektur

### CSRF Protection
- Flask-WTF CSRF-Token
- Alle Formulare geschützt
- Automatische Token-Validierung

### Session Management
- Sichere Cookie-Konfiguration
- HTTPOnly und Secure Flags
- Session-Timeout

### Input Validation
- WTForms Server-seitige Validierung
- HTML5 Client-seitige Validierung
- SQL-Injection-Schutz durch Parametrisierung

### Authentication Flow
```
1. Benutzer → Login-Formular
2. Server → Credentials validieren
3. Session → User-ID und Role speichern
4. Decorator → Route-Zugriff prüfen
5. Template → Benutzer-spezifische Inhalte
```

## 🔄 Request-Response Cycle

### Typischer Request Flow:
```
1. Browser → HTTP Request
2. Flask → Route-Matching
3. Blueprint → Route-Handler
4. Decorator → Authentifizierung prüfen
5. Model → Daten aus Datenbank
6. Template → HTML generieren
7. Response → Browser senden
```

### Error Handling:
- 404 - Seite nicht gefunden
- 500 - Server-Fehler
- 403 - Zugriff verweigert
- Custom Error-Templates

## 📊 Performance Considerations

### Database Optimization:
- Indizierte Spalten (id, date, player_id, event_id)
- Effiziente Queries mit JOINs
- Connection Pooling (in Produktion)

### Template Optimization:
- Template-Caching
- Minimierte CSS/JS
- Optimierte Bilder
- Lazy Loading

### Caching Strategy:
- Flask-Caching für statische Inhalte
- Browser-Caching für Assets
- Database Query-Caching

## 🧪 Testing Architecture

### Test Structure:
```
tests/
├── test_models.py      # Model-Tests
├── test_routes.py      # Route-Tests
├── test_forms.py       # Form-Tests
└── conftest.py         # Test-Konfiguration
```

### Test Types:
- **Unit Tests**: Einzelne Funktionen
- **Integration Tests**: Blueprint-Interaktion
- **Functional Tests**: End-to-End Workflows

## 🚀 Deployment Architecture

### Development:
- SQLite Database
- Flask Development Server
- Debug Mode aktiviert

### Production:
- PostgreSQL Database
- Gunicorn WSGI Server
- Nginx Reverse Proxy
- SSL/TLS Encryption

### Container Deployment:
- Docker Multi-Stage Build
- Environment-basierte Konfiguration
- Health Checks
- Log Aggregation

---

Diese Architektur gewährleistet Skalierbarkeit, Wartbarkeit und Sicherheit für das ClubConnect-System.
