#!/usr/bin/env python3
"""
ClubConnect Datenbank-Initialisierung
Erstellt die Datenbank und fügt Beispieldaten hinzu
"""

import os
import sys
from datetime import datetime, date, timedelta
from werkzeug.security import generate_password_hash

# Flask-App importieren
from app import create_app
from app.models import (
    init_db, create_user, create_player, create_event, 
    create_news, create_clothing_rule, bulk_invite_players
)

def init_database():
    """Initialisiert die Datenbank mit Tabellen"""
    print("Erstelle Datenbanktabellen...")
    init_db()
    print("✓ Datenbanktabellen erstellt")

def create_admin_user():
    """Erstellt Standard-Admin-Benutzer"""
    print("Erstelle Admin-Benutzer...")
    try:
        password_hash = generate_password_hash('admin123')
        user_id = create_user('admin', password_hash, 'trainer')
        if user_id:
            print("✓ Admin-Benutzer erstellt (admin/admin123)")
        else:
            print("⚠ Admin-Benutzer existiert bereits")
    except Exception as e:
        print(f"✗ Fehler beim Erstellen des Admin-Benutzers: {e}")

def create_sample_players():
    """Erstellt Beispiel-Spieler"""
    print("Erstelle Beispiel-Spieler...")
    
    sample_players = [
        {
            'name': 'Max Mustermann',
            'team': 'Erste Mannschaft',
            'email': 'max.mustermann@example.com',
            'phone': '+49 123 456789',
            'birth_date': '1995-03-15',
            'position': 'midfielder',
            'jersey_number': 10
        },
        {
            'name': 'Anna Schmidt',
            'team': 'Erste Mannschaft',
            'email': 'anna.schmidt@example.com',
            'phone': '+49 123 456790',
            'birth_date': '1997-07-22',
            'position': 'forward',
            'jersey_number': 9
        },
        {
            'name': 'Tom Weber',
            'team': 'Erste Mannschaft',
            'email': 'tom.weber@example.com',
            'phone': '+49 123 456791',
            'birth_date': '1993-11-08',
            'position': 'goalkeeper',
            'jersey_number': 1
        },
        {
            'name': 'Lisa Müller',
            'team': 'Zweite Mannschaft',
            'email': 'lisa.mueller@example.com',
            'phone': '+49 123 456792',
            'birth_date': '1999-01-30',
            'position': 'defender',
            'jersey_number': 4
        },
        {
            'name': 'Jan Fischer',
            'team': 'Jugend',
            'email': 'jan.fischer@example.com',
            'phone': '+49 123 456793',
            'birth_date': '2005-05-12',
            'position': 'midfielder',
            'jersey_number': 8
        }
    ]
    
    created_players = []
    for player_data in sample_players:
        try:
            player_id = create_player(**player_data)
            if player_id:
                created_players.append(player_id)
                print(f"✓ Spieler '{player_data['name']}' erstellt")
        except Exception as e:
            print(f"✗ Fehler beim Erstellen von '{player_data['name']}': {e}")
    
    return created_players

def create_sample_events(player_ids):
    """Erstellt Beispiel-Events"""
    print("Erstelle Beispiel-Events...")
    
    today = date.today()
    
    sample_events = [
        {
            'title': 'Wöchentliches Training',
            'event_type': 'training',
            'date': (today + timedelta(days=1)).strftime('%Y-%m-%d'),
            'time': '18:00',
            'location': 'Sportplatz Hauptstraße',
            'clothing': 'training',
            'description': 'Reguläres Wochentraining für alle Mannschaften'
        },
        {
            'title': 'Spiel gegen FC Beispielstadt',
            'event_type': 'match',
            'date': (today + timedelta(days=5)).strftime('%Y-%m-%d'),
            'time': '15:00',
            'location': 'Auswärtsstadion Beispielstadt',
            'clothing': 'match',
            'description': 'Wichtiges Ligaspiel gegen FC Beispielstadt'
        },
        {
            'title': 'Vereinsversammlung',
            'event_type': 'meeting',
            'date': (today + timedelta(days=10)).strftime('%Y-%m-%d'),
            'time': '19:30',
            'location': 'Vereinsheim',
            'clothing': 'casual',
            'description': 'Monatliche Vereinsversammlung mit wichtigen Themen'
        },
        {
            'title': 'Stadtturnier',
            'event_type': 'tournament',
            'date': (today + timedelta(days=14)).strftime('%Y-%m-%d'),
            'time': '09:00',
            'location': 'Sportzentrum Innenstadt',
            'clothing': 'match',
            'description': 'Jährliches Stadtturnier mit mehreren Vereinen'
        },
        {
            'title': 'Konditionstraining',
            'event_type': 'training',
            'date': (today + timedelta(days=3)).strftime('%Y-%m-%d'),
            'time': '17:30',
            'location': 'Fitnessstudio Vereinsheim',
            'clothing': 'training',
            'description': 'Spezielles Konditionstraining für die Vorbereitung'
        }
    ]
    
    created_events = []
    for event_data in sample_events:
        try:
            event_id = create_event(**event_data)
            if event_id:
                created_events.append(event_id)
                print(f"✓ Event '{event_data['title']}' erstellt")
                
                # Spieler zu Events einladen (zufällige Auswahl)
                if player_ids and len(player_ids) > 0:
                    # Für Trainings alle Spieler einladen
                    if event_data['event_type'] == 'training':
                        invited = bulk_invite_players(event_id, player_ids)
                        print(f"  → {invited} Spieler eingeladen")
                    # Für Spiele nur erste 3 Spieler
                    elif event_data['event_type'] == 'match':
                        invited = bulk_invite_players(event_id, player_ids[:3])
                        print(f"  → {invited} Spieler eingeladen")
                        
        except Exception as e:
            print(f"✗ Fehler beim Erstellen von '{event_data['title']}': {e}")
    
    return created_events

def create_sample_news():
    """Erstellt Beispiel-Nachrichten"""
    print("Erstelle Beispiel-Nachrichten...")
    
    sample_news = [
        {
            'title': 'Willkommen bei ClubConnect!',
            'content': 'Unser neues Vereinsmanagement-System ist jetzt online! Hier können Sie alle wichtigen Informationen zu Trainings, Spielen und Vereinsaktivitäten finden.',
            'author': 'Vereinsvorstand',
            'published': True
        },
        {
            'title': 'Neue Trainingszeiten ab nächster Woche',
            'content': 'Aufgrund der Platzrenovierung ändern sich die Trainingszeiten. Das Training findet ab nächster Woche immer dienstags und donnerstags um 18:00 Uhr statt.',
            'author': 'Trainer Schmidt',
            'published': True
        },
        {
            'title': 'Erfolgreicher Saisonstart',
            'content': 'Mit einem 3:1 Sieg gegen den Tabellenführer sind wir erfolgreich in die neue Saison gestartet. Herzlichen Glückwunsch an die gesamte Mannschaft!',
            'author': 'Sportlicher Leiter',
            'published': True
        }
    ]
    
    for news_data in sample_news:
        try:
            news_id = create_news(**news_data)
            if news_id:
                print(f"✓ Nachricht '{news_data['title']}' erstellt")
        except Exception as e:
            print(f"✗ Fehler beim Erstellen der Nachricht '{news_data['title']}': {e}")

def create_sample_clothing_rules():
    """Erstellt Beispiel-Kleidungsregeln"""
    print("Erstelle Kleidungsregeln...")
    
    clothing_rules = [
        {
            'event_type': 'training',
            'description': 'Sportkleidung: Trainingsanzug oder Shorts mit T-Shirt, Sportschuhe mit Stollen oder Hallenschuhe je nach Trainingsort.'
        },
        {
            'event_type': 'match',
            'description': 'Vereinstrikot (Heim oder Auswärts), schwarze Hose, Stutzen in Vereinsfarben, Fußballschuhe mit entsprechenden Stollen.'
        },
        {
            'event_type': 'tournament',
            'description': 'Komplette Vereinsausrüstung: Trikot, Hose, Stutzen in Vereinsfarben. Zusätzlich Trainingsanzug für Aufwärmen.'
        },
        {
            'event_type': 'meeting',
            'description': 'Freizeitkleidung oder Vereinskleidung. Bei offiziellen Anlässen bitte gepflegte Kleidung.'
        }
    ]
    
    for rule_data in clothing_rules:
        try:
            rule_id = create_clothing_rule(**rule_data)
            if rule_id:
                print(f"✓ Kleidungsregel für '{rule_data['event_type']}' erstellt")
        except Exception as e:
            print(f"✗ Fehler beim Erstellen der Kleidungsregel: {e}")

def main():
    """Hauptfunktion für Datenbankinitialisierung"""
    print("=" * 50)
    print("ClubConnect - Datenbank Initialisierung")
    print("=" * 50)
    
    # Flask-App erstellen
    app = create_app('development')
    
    with app.app_context():
        try:
            # Datenbank initialisieren
            init_database()
            
            # Admin-Benutzer erstellen
            create_admin_user()
            
            # Beispieldaten erstellen
            player_ids = create_sample_players()
            event_ids = create_sample_events(player_ids)
            create_sample_news()
            create_sample_clothing_rules()
            
            print("\n" + "=" * 50)
            print("✓ Datenbank erfolgreich initialisiert!")
            print("=" * 50)
            print("\nZusammenfassung:")
            print(f"- {len(player_ids)} Spieler erstellt")
            print(f"- {len(event_ids)} Events erstellt")
            print("- 3 Nachrichten erstellt")
            print("- 4 Kleidungsregeln erstellt")
            print("- 1 Admin-Benutzer erstellt")
            print("\nLogin-Daten:")
            print("Benutzername: admin")
            print("Passwort: admin123")
            print("\nStarten Sie die Anwendung mit: python run.py")
            
        except Exception as e:
            print(f"\n✗ Fehler bei der Initialisierung: {e}")
            sys.exit(1)

if __name__ == '__main__':
    main()
