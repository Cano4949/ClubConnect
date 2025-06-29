---
title: Design Decisions
nav_order: 1
---

{: .label }
Design Documentation

# Design Decisions

Diese Dokumentation erläutert die zentralen Designentscheidungen, die im Verlauf der Entwicklung von *ClubConnect* getroffen wurden, und gibt jeweils eine Begründung, warum diese Ansätze gewählt wurden.

## Architekturentscheidungen

### 1. Wahl des Web-Frameworks: Flask

**Entscheidung:** Einsatz von Flask als Web-Framework.

**Begründung:**
- Flask ist ein schlankes und leicht verständliches Framework, das sich gut für kleinere Projekte und Lernzwecke eignet.
- Die modulare Struktur (z. B. Blueprints) ermöglicht eine gute Organisation des Codes.
- Flask wurde als Empfehlung im Kurs genannt.
- Die geringe Einstiegshürde und die umfangreiche Dokumentation erleichtern die Umsetzung.

**Abgewogene Alternativen:**
- Django: Umfangreicher, aber für den Projektumfang zu schwergewichtig.
- FastAPI: Modern, aber im Kurszusammenhang zu komplex.

### 2. Modularer Aufbau mit Blueprints

**Entscheidung:** Strukturierung der Anwendung mit drei Blueprints: `main`, `auth`, `admin`.

**Begründung:**
- Der modulare Aufbau fördert die Wartbarkeit und erleichtert die Arbeit im Team.
- Verantwortlichkeiten sind klar getrennt.
- Neue Features lassen sich einfacher integrieren.

**Projektstruktur:**
app/
├── main/ # Öffentliche Inhalte
├── auth/ # Login/Registrierung
└── admin/ # Verwaltungsbereich


### 3. Datenbank: SQLite in der Entwicklung

**Entscheidung:** Verwendung von SQLite für die Entwicklung, geplant: PostgreSQL für die Produktion.

**Begründung:**
- SQLite ist leichtgewichtig und benötigt keine zusätzliche Installation.
- Die Datenbankdatei kann einfach versioniert und verschoben werden.
- Für Test- und Entwicklungszwecke völlig ausreichend.
- Für spätere produktive Einsätze ist PostgreSQL vorgesehen.

## UI/UX Designentscheidungen

### 1. Verwendung von Bootstrap (Version 5.3)

**Entscheidung:** Bootstrap als CSS-Framework.

**Begründung:**
- Schneller Aufbau einer konsistenten Benutzeroberfläche.
- Responsive Design ist bereits integriert.
- Der Einsatz fertiger Komponenten spart Entwicklungszeit.
- Keine eigenen JavaScript-Implementierungen notwendig.

**Genutzte Elemente:**
- Grid-System für Layouts
- Cards zur Gruppierung von Inhalten
- Navigation, Formulare, Alerts, Badges usw.

### 2. Farbgebung und visuelle Identität

**Entscheidung:** Blau/Rot/Grün als sportlich-dynamisches Farbschema.

**Begründung:**
- Farben erzeugen einen sportlichen Gesamteindruck.
- Kontraste sorgen für gute Lesbarkeit.
- Emotionale Assoziationen: Blau steht für Vertrauen, Rot für Aktivität, Grün für Bestätigung.

**Farbdefinition:**
```css
:root {
    --primary-color: #2C3E50;
    --secondary-color: #3498DB;
    --success-color: #27AE60;
    --danger-color: #E74C3C;
    --background-color: #F5F6FA;
}
3. Navigationskonzept
Entscheidung: Horizontale Navigation mit Rollenabhängigkeit.

Begründung:
Bekannte Struktur sorgt für einfache Orientierung.
Mobile Darstellung erfolgt über Hamburger-Menü.
Menüpunkte passen sich je nach Nutzerrolle an.
Breadcrumbs helfen bei der Orientierung innerhalb der App.

Datenmodell
1. Relationale Struktur mit Foreign Keys
Entscheidung: Verwendung eines normalisierten Schemas.

Begründung:
Einhaltung von Datenintegrität durch Foreign Keys.
Tabellen lassen sich bei Bedarf leicht erweitern.
Effiziente Datenabfragen durch Indizes.

2. Many-to-Many über Junction Table
Entscheidung: Verknüpfung von Spielern und Events über eine invites-Tabelle.

Begründung:
Die Tabelle enthält zusätzliche Informationen (z. B. Status, Notizen).
Eindeutige Einträge werden durch Constraints abgesichert.
Änderungen an Einladungen lassen sich nachverfolgen.

3. Speicherung von Datum/Zeit als Text
Entscheidung: Speicherung von Zeitangaben als TEXT.

Begründung:
SQLite unterstützt keine echten Datums-Typen.
Textwerte sind einfach zu formatieren und zu vergleichen.
Portabel und ausreichend für den aktuellen Einsatzzweck.

Sicherheit
1. Sessionbasierte Authentifizierung
Entscheidung: Nutzung der Flask-internen Session-Verwaltung.

Begründung:
Einfach in der Umsetzung.
Sessions werden serverseitig gespeichert.

Die Lösung erfüllt die Anforderungen im Kurskontext.
Zusätzliche Maßnahmen:

HTTPOnly Cookies

Secure-Flag im Produktivmodus

Session-Timeout

CSRF-Schutz

2. CSRF-Absicherung
Entscheidung: Verwendung von Flask-WTF zur Absicherung aller Formulare.

Begründung:
Schutz vor Cross-Site Request Forgery.
Nahtlose Integration in das Formularhandling.
Entspricht gängigen Sicherheitsstandards.

3. Klartext-Passwörter (nur Entwicklung)
Entscheidung: Temporäre Speicherung von Passwörtern im Klartext für Entwicklung und Tests.

Begründung:
Schnellere Entwicklung und einfaches Testen.
Im Code klar als Übergangslösung dokumentiert.
In einer produktiven Umgebung müssen Passwörter gehasht werden.

Benutzeroberfläche
1. Verwendung von Cards
Entscheidung: Inhalte werden mithilfe von Bootstrap-Cards strukturiert.

Begründung:
Inhalte sind visuell klar getrennt.
Moderne Optik und gute Skalierbarkeit.
Cards lassen sich leicht erweitern und neu anordnen.

2. Einsatz von Icons
Entscheidung: Bootstrap Icons werden für eine bessere Benutzerführung eingesetzt.

Begründung:
Vektorbasierte Icons sind leichtgewichtig.
Sie steigern die Übersichtlichkeit und Verständlichkeit.
Unterstützung für Screenreader ist gegeben.

3. Visualisierung von Statuswerten
Entscheidung: Einladungsstatus wird über farbige Badges angezeigt.

Begründung:
Farbgebung erlaubt eine schnelle Erfassung des Status.
Farben werden konsistent in der Anwendung verwendet.
Textliche Ergänzung stellt Barrierefreiheit sicher.

Mobile-First Design
1. Grid-System für Responsivität
Entscheidung: Einsatz des Bootstrap-Grid-Systems.

Begründung:
Darstellung passt sich automatisch verschiedenen Bildschirmgrößen an.
Gute Benutzererfahrung auf Mobilgeräten.
Mobile-First-Ansatz wurde bewusst gewählt.

2. Bedienung auf Touchgeräten
Entscheidung: Große Buttons und klar erkennbare Bedienelemente.

Begründung:
Erhöhte Benutzerfreundlichkeit auf Smartphones und Tablets.
Verringerung von Fehleingaben durch größere Ziele.
Berücksichtigung moderner Designrichtlinien.

Entwicklungsentscheidungen
1. Konfigurationsklassen
Entscheidung: Getrennte Konfigurationsklassen für verschiedene Umgebungen.

Begründung:
Lokale Entwicklung und Produktion lassen sich getrennt verwalten.
Zugangsdaten werden über Umgebungsvariablen geschützt.
Alle Einstellungen sind zentral an einer Stelle gepflegt.

2. App Factory Pattern
Entscheidung: Die Anwendung wird über eine App-Factory erstellt.

Begründung:
Erleichtert das Testen einzelner Komponenten.
Verschiedene Konfigurationen können zur Laufzeit geladen werden.
Die Struktur ist langfristig wartbar.

3. Hilfsskripte für Datenbankaktionen
Entscheidung: Eigene Python-Skripte zur Verwaltung der Datenbank.

Begründung:
Trennung von Anwendung und Verwaltung.
Erleichtert das Debugging und lokale Tests.
Wiederverwendbarkeit für Initialisierung oder Seed-Daten.

Performance
1. Minimale Verwendung von JavaScript
Entscheidung: Kein eigenes JavaScript (gemäß Kursvorgabe).

Begründung:
Vereinfachung des Projekts.
Konzentration auf serverseitige Logik.
Anwendung funktioniert auch bei deaktiviertem JavaScript.

2. Serverseitiges Rendering
Entscheidung: HTML-Templates mit Jinja2 werden auf dem Server gerendert.

Begründung:
Bessere Kontrolle über das ausgelieferte HTML.
Schnelle Ladezeiten und bessere Performance.
Ideal für klassische Webanwendungen mit Formularen.

Bildungskontext
1. Umfangreiche Dokumentation
Entscheidung: Ausführliche Beschreibung aller Designentscheidungen.

Begründung:
Dokumentation dient als Lernnachweis.
Erleichtert die spätere Wartung und Weiterentwicklung.
Hilft bei der Bewertung im Kurskontext.

2. Realitätsnahe Seed-Daten
Entscheidung: Erzeugung realistischer Testdaten für die Entwicklung.

Begründung:
Erlaubt vollständige Demonstrationen und Tests.
Gibt einen professionellen Eindruck bei Präsentationen.
Unterstützt alle Features der App bereits in der Entwicklung.

3. Detaillierte Git-Kommentierung
Entscheidung: Kleine, nachvollziehbare Commits mit erklärenden Nachrichten.

Begründung:
Klare Nachvollziehbarkeit des Entwicklungsprozesses.
Git-Historie zeigt Lernfortschritt.
Best Practice für Softwareentwicklung.

Zukunftssicherheit
1. Erweiterbare Code-Struktur
Entscheidung: Modulares Design mit Erweiterbarkeit im Blick.

Begründung:
Neue Funktionen können ohne große Umbauten ergänzt werden.
Einzelne Komponenten bleiben übersichtlich.
Gute Grundlage für spätere Weiterentwicklung.

2. Nutzung von Umgebungsvariablen
Entscheidung: Konfiguration erfolgt über .env-Dateien und Umgebungsvariablen.

Begründung:
Sensible Daten bleiben außerhalb des Codes.
Deployment ist dadurch flexibler und sicherer.
Entspricht gängigen Standards in der Webentwicklung.





