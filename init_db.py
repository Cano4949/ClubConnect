#!/usr/bin/env python
"""Database initialization script for ClubConnect."""

import os
import sys
from datetime import datetime, date, time
from app import create_app, db
from app.models import User, Event, Player, News, ClothingRule, Invite

def init_database():
    """Initialize the database with tables."""
    app = create_app(os.getenv('FLASK_CONFIG') or 'default')
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✓ Database tables created successfully!")
        
        # Check if admin user exists
        if not User.query.filter_by(username='trainer').first():
            create_default_admin()
        
        return True

def create_default_admin():
    """Create default admin user."""
    admin = User(
        username='trainer',
        email='trainer@clubconnect.de'
    )
    admin.set_password('trainer123')
    db.session.add(admin)
    db.session.commit()
    print("✓ Default admin user created (username: trainer, password: trainer123)")

def reset_database():
    """Drop all tables and recreate them."""
    app = create_app(os.getenv('FLASK_CONFIG') or 'default')
    
    with app.app_context():
        db.drop_all()
        print("✓ All tables dropped")
        db.create_all()
        print("✓ Database tables recreated")
        create_default_admin()

def seed_database():
    """Seed database with sample data."""
    app = create_app(os.getenv('FLASK_CONFIG') or 'default')
    
    with app.app_context():
        # Check if data already exists
        if Player.query.first():
            print("⚠ Database already contains data. Use 'reset' to clear first.")
            return
        
        # Create sample players
        players = [
            Player(
                first_name='Max', last_name='Mustermann', 
                email='max.mustermann@example.com',
                phone='0171-1234567',
                position='Stürmer', jersey_number=9, 
                team='A-Team', birth_date=date(2005, 3, 15)
            ),
            Player(
                first_name='Lisa', last_name='Schmidt', 
                email='lisa.schmidt@example.com',
                phone='0172-2345678',
                position='Mittelfeld', jersey_number=10, 
                team='A-Team', birth_date=date(2006, 7, 22)
            ),
            Player(
                first_name='Tom', last_name='Weber', 
                email='tom.weber@example.com',
                phone='0173-3456789',
                position='Verteidiger', jersey_number=4, 
                team='A-Team', birth_date=date(2005, 11, 8)
            ),
            Player(
                first_name='Anna', last_name='Meyer', 
                email='anna.meyer@example.com',
                phone='0174-4567890',
                position='Torwart', jersey_number=1, 
                team='A-Team', birth_date=date(2006, 1, 30)
            ),
            Player(
                first_name='Jonas', last_name='Fischer', 
                email='jonas.fischer@example.com',
                phone='0175-5678901',
                position='Mittelfeld', jersey_number=8, 
                team='B-Team', birth_date=date(2007, 5, 12)
            ),
            Player(
                first_name='Sarah', last_name='Wagner', 
                email='sarah.wagner@example.com',
                phone='0176-6789012',
                position='Stürmer', jersey_number=11, 
                team='B-Team', birth_date=date(2007, 9, 3)
            ),
        ]
        
        for player in players:
            db.session.add(player)
        
        # Create sample events
        events = [
            Event(
                title='Wochentraining', 
                event_type='training',
                date=date(2025, 7, 1), 
                time=time(18, 0),
                location='Sportplatz Hauptstraße',
                description='Reguläres Wochentraining. Schwerpunkt: Passübungen und Spielaufbau.',
                max_participants=20,
                created_by=1
            ),
            Event(
                title='Heimspiel gegen FC Beispiel', 
                event_type='game',
                date=date(2025, 7, 5), 
                time=time(15, 0),
                location='Heimstadion',
                description='Wichtiges Ligaspiel gegen unseren Lokalrivalen. Bitte 45 Minuten vor Spielbeginn da sein!',
                max_participants=15,
                created_by=1
            ),
            Event(
                title='Sommerturnier', 
                event_type='tournament',
                date=date(2025, 7, 12), 
                time=time(9, 0),
                location='Sportpark Musterstadt',
                description='Ganztägiges Turnier mit 8 Mannschaften. Verpflegung wird gestellt.',
                max_participants=18,
                created_by=1
            ),
            Event(
                title='Mannschaftsbesprechung', 
                event_type='meeting',
                date=date(2025, 6, 28), 
                time=time(19, 0),
                location='Vereinsheim',
                description='Besprechung der Saisonziele und Trainingsplan.',
                created_by=1
            ),
        ]
        
        for event in events:
            db.session.add(event)
        
        db.session.commit()
        
        # Create invitations for first two events
        all_players = Player.query.all()
        first_event = Event.query.first()
        second_event = Event.query.offset(1).first()
        
        for player in all_players:
            # Invite all to first event
            invite1 = Invite(
                event_id=first_event.id,
                player_id=player.id,
                status='pending'
            )
            db.session.add(invite1)
            
            # Invite A-Team to second event
            if player.team == 'A-Team':
                invite2 = Invite(
                    event_id=second_event.id,
                    player_id=player.id,
                    status='pending'
                )
                db.session.add(invite2)
        
        # Create clothing rules
        rules = [
            ClothingRule(
                event_type='training',
                description='Schwarze Trainingshose, weißes Trainingsshirt, Stollenschuhe. Bei kaltem Wetter: Trainingsanzug erlaubt.'
            ),
            ClothingRule(
                event_type='game',
                description='Komplettes Vereinstrikot (Trikot, schwarze Hose, Vereinsstutzen), Stollenschuhe, Schienbeinschoner Pflicht!'
            ),
            ClothingRule(
                event_type='meeting',
                description='Vereinskleidung oder gepflegte Freizeitkleidung. Keine Sportkleidung.'
            ),
            ClothingRule(
                event_type='tournament',
                description='Komplette Vereinsausrüstung: Spielkleidung + Trainingsanzug für Pausen. Ersatztrikot mitbringen!'
            ),
        ]
        
        for rule in rules:
            db.session.add(rule)
        
        # Create sample news
        news_items = [
            News(
                title='Willkommen zur neuen Saison 2025/2026!',
                content='''Die Sommerpause ist vorbei und wir starten voller Energie in die neue Saison! 
                
Unser erstes Training findet am 1. Juli um 18:00 Uhr statt. Bitte bringt eure komplette Ausrüstung mit.

Wir haben einige spannende Neuerungen:
- Neue Trainingszeiten: Di & Do 18:00-20:00 Uhr
- Zusätzliches Torwarttraining freitags
- Monatliche Teamevents

Lasst uns gemeinsam eine erfolgreiche Saison spielen!''',
                author_id=1,
                published=True
            ),
            News(
                title='Neue Trikots sind da!',
                content='''Unsere neuen Vereinstrikots für die Saison 2025/2026 sind eingetroffen!

Die Trikots können ab sofort im Vereinsheim abgeholt werden:
- Öffnungszeiten: Di & Do 17:00-19:00 Uhr
- Preis: 45€ pro Trikot
- Verfügbare Größen: XS bis XXL

Bitte meldet euch bei Trainer Schmidt für die Trikotnummern.''',
                author_id=1,
                published=True
            ),
            News(
                title='Erfolgreicher Saisonabschluss',
                content='''Mit einem 3:1 Sieg im letzten Spiel haben wir die vergangene Saison erfolgreich beendet!

Highlights der Saison:
- 3. Platz in der Liga
- Pokal-Halbfinale
- Fairplay-Auszeichnung

Vielen Dank an alle Spieler, Trainer und Unterstützer!''',
                author_id=1,
                published=True,
                created_at=datetime(2025, 6, 15, 10, 0, 0)
            ),
        ]
        
        for news in news_items:
            db.session.add(news)
        
        db.session.commit()
        print("✓ Sample data created successfully!")
        print("\nCreated:")
        print(f"  - {len(players)} players")
        print(f"  - {len(events)} events")
        print(f"  - {Invite.query.count()} invitations")
        print(f"  - {len(rules)} clothing rules")
        print(f"  - {len(news_items)} news articles")

def show_info():
    """Show database information."""
    app = create_app(os.getenv('FLASK_CONFIG') or 'default')
    
    with app.app_context():
        print("\n=== ClubConnect Database Info ===")
        print(f"Database: {app.config['SQLALCHEMY_DATABASE_URI']}")
        print("\nTable Statistics:")
        print(f"  - Users: {User.query.count()}")
        print(f"  - Players: {Player.query.count()}")
        print(f"  - Events: {Event.query.count()}")
        print(f"  - Invitations: {Invite.query.count()}")
        print(f"  - News: {News.query.count()}")
        print(f"  - Clothing Rules: {ClothingRule.query.count()}")
        
        # Show admin users
        admins = User.query.all()
        if admins:
            print("\nAdmin Users:")
            for admin in admins:
                print(f"  - {admin.username} ({admin.email})")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'init':
            init_database()
        elif command == 'reset':
            response = input("⚠️  This will delete all data! Continue? (y/N): ")
            if response.lower() == 'y':
                reset_database()
            else:
                print("Reset cancelled.")
        elif command == 'seed':
            seed_database()
        elif command == 'info':
            show_info()
        else:
            print(f"Unknown command: {command}")
            print("\nAvailable commands:")
            print("  python init_db.py init   - Initialize database")
            print("  python init_db.py reset  - Reset database (delete all data)")
            print("  python init_db.py seed   - Add sample data")
            print("  python init_db.py info   - Show database information")
    else:
        print("Usage: python init_db.py [init|reset|seed|info]")
