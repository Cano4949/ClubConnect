import os
from app import create_app, db
from app.models import User, Event, Player, News, ClothingRule, Invite

# Create application instance
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.shell_context_processor
def make_shell_context():
    """Make database models available in flask shell."""
    return {
        'db': db,
        'User': User,
        'Event': Event,
        'Player': Player,
        'News': News,
        'ClothingRule': ClothingRule,
        'Invite': Invite
    }

@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    print('Database initialized!')

@app.cli.command()
def seed_db():
    """Seed database with sample data."""
    from datetime import datetime, date, time
    
    # Check if data already exists
    if User.query.first():
        print('Database already contains data. Skipping seed.')
        return
    
    # Create admin user
    admin = User(
        username='trainer',
        email='trainer@clubconnect.de'
    )
    admin.set_password('trainer123')
    db.session.add(admin)
    
    # Create sample players
    players = [
        Player(first_name='Max', last_name='Mustermann', email='max@example.com', 
               position='Stürmer', jersey_number=9, team='A-Team'),
        Player(first_name='Lisa', last_name='Schmidt', email='lisa@example.com', 
               position='Mittelfeld', jersey_number=10, team='A-Team'),
        Player(first_name='Tom', last_name='Weber', email='tom@example.com', 
               position='Verteidiger', jersey_number=4, team='A-Team'),
        Player(first_name='Anna', last_name='Meyer', email='anna@example.com', 
               position='Torwart', jersey_number=1, team='A-Team'),
    ]
    
    for player in players:
        db.session.add(player)
    
    # Create sample events
    events = [
        Event(title='Wochentraining', event_type='training', 
              date=date(2025, 7, 1), time=time(18, 0),
              location='Sportplatz Hauptstraße', 
              description='Reguläres Wochentraining'),
        Event(title='Heimspiel gegen FC Beispiel', event_type='game', 
              date=date(2025, 7, 5), time=time(15, 0),
              location='Heimstadion', 
              description='Wichtiges Ligaspiel'),
    ]
    
    for event in events:
        db.session.add(event)
    
    # Create clothing rules
    rules = [
        ClothingRule(event_type='training', 
                    description='Schwarze Hose, weißes Trainingsshirt, Stollenschuhe'),
        ClothingRule(event_type='game', 
                    description='Vereinstrikot, schwarze Hose, Stutzen, Stollenschuhe'),
        ClothingRule(event_type='meeting', 
                    description='Vereinskleidung oder smart casual'),
        ClothingRule(event_type='tournament', 
                    description='Komplette Vereinsausrüstung inkl. Trainingsanzug'),
    ]
    
    for rule in rules:
        db.session.add(rule)
    
    # Create sample news
    news = News(
        title='Saisonstart 2025/2026',
        content='Die neue Saison beginnt am 1. Juli mit dem ersten Training. Wir freuen uns auf ein erfolgreiches Jahr!',
        author_id=1,
        published=True
    )
    db.session.add(news)
    
    # Commit all changes
    db.session.commit()
    print('Database seeded with sample data!')

if __name__ == '__main__':
    app.run(debug=True)
