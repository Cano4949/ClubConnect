"""
ClubConnect Datenbankmodelle
"""

import sqlite3
import os
from datetime import datetime, date
from flask import current_app

def get_db_path():
    """Datenbankpfad ermitteln"""
    if current_app:
        db_url = current_app.config.get('DATABASE_URL', 'sqlite:///clubconnect.db')
        if db_url.startswith('sqlite:///'):
            return db_url.replace('sqlite:///', '')
    return 'clubconnect.db'

def get_db_connection():
    """Erstellt SQLite-Verbindung mit Row Factory"""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialisiert die Datenbank mit allen Tabellen"""
    conn = get_db_connection()
    
    # Events Tabelle
    conn.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            type TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            location TEXT,
            clothing TEXT,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Players Tabelle
    conn.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            team TEXT,
            email TEXT,
            phone TEXT,
            birth_date TEXT,
            position TEXT,
            jersey_number INTEGER,
            active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Invites Tabelle (Many-to-Many zwischen Events und Players)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS invites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER NOT NULL,
            event_id INTEGER NOT NULL,
            status TEXT DEFAULT 'pending',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (player_id) REFERENCES players (id),
            FOREIGN KEY (event_id) REFERENCES events (id),
            UNIQUE(player_id, event_id)
        )
    ''')
    
    # News Tabelle
    conn.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author TEXT DEFAULT 'Admin',
            published BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Clothing Rules Tabelle
    conn.execute('''
        CREATE TABLE IF NOT EXISTS clothing_rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            description TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Users Tabelle für Admin-Login
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'trainer',
            active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# Event-Funktionen
def get_upcoming_events(limit=10):
    """Holt kommende Events"""
    conn = get_db_connection()
    events = conn.execute('''
        SELECT * FROM events 
        WHERE date >= date('now') 
        ORDER BY date ASC, time ASC 
        LIMIT ?
    ''', (limit,)).fetchall()
    conn.close()
    return events

def get_event_by_id(event_id):
    """Holt ein Event nach ID"""
    conn = get_db_connection()
    event = conn.execute('SELECT * FROM events WHERE id = ?', (event_id,)).fetchone()
    conn.close()
    return event

def create_event(title, event_type, date, time, location=None, clothing=None, description=None):
    """Erstellt ein neues Event"""
    conn = get_db_connection()
    cursor = conn.execute('''
        INSERT INTO events (title, type, date, time, location, clothing, description)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (title, event_type, date, time, location, clothing, description))
    event_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return event_id

def update_event(event_id, title, event_type, date, time, location=None, clothing=None, description=None):
    """Aktualisiert ein Event"""
    conn = get_db_connection()
    conn.execute('''
        UPDATE events 
        SET title=?, type=?, date=?, time=?, location=?, clothing=?, description=?, updated_at=CURRENT_TIMESTAMP
        WHERE id=?
    ''', (title, event_type, date, time, location, clothing, description, event_id))
    conn.commit()
    conn.close()

def delete_event(event_id):
    """Löscht ein Event und alle zugehörigen Einladungen"""
    conn = get_db_connection()
    conn.execute('DELETE FROM invites WHERE event_id = ?', (event_id,))
    conn.execute('DELETE FROM events WHERE id = ?', (event_id,))
    conn.commit()
    conn.close()

# Player-Funktionen
def get_all_players():
    """Holt alle aktiven Spieler"""
    conn = get_db_connection()
    players = conn.execute('SELECT * FROM players WHERE active = 1 ORDER BY name').fetchall()
    conn.close()
    return players

def get_player_by_id(player_id):
    """Holt einen Spieler nach ID"""
    conn = get_db_connection()
    player = conn.execute('SELECT * FROM players WHERE id = ?', (player_id,)).fetchone()
    conn.close()
    return player

def create_player(name, team=None, email=None, phone=None, birth_date=None, position=None, jersey_number=None):
    """Erstellt einen neuen Spieler"""
    conn = get_db_connection()
    cursor = conn.execute('''
        INSERT INTO players (name, team, email, phone, birth_date, position, jersey_number)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, team, email, phone, birth_date, position, jersey_number))
    player_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return player_id

def update_player(player_id, name, team=None, email=None, phone=None, birth_date=None, position=None, jersey_number=None, active=True):
    """Aktualisiert einen Spieler"""
    conn = get_db_connection()
    conn.execute('''
        UPDATE players 
        SET name=?, team=?, email=?, phone=?, birth_date=?, position=?, jersey_number=?, active=?, updated_at=CURRENT_TIMESTAMP
        WHERE id=?
    ''', (name, team, email, phone, birth_date, position, jersey_number, active, player_id))
    conn.commit()
    conn.close()

# Invite-Funktionen
def get_player_invites_for_event(event_id):
    """Holt alle Einladungen für ein Event mit Spieler-Details"""
    conn = get_db_connection()
    invites = conn.execute('''
        SELECT i.*, p.name as player_name, p.team, p.email, p.phone
        FROM invites i
        JOIN players p ON i.player_id = p.id
        WHERE i.event_id = ?
        ORDER BY p.name
    ''', (event_id,)).fetchall()
    conn.close()
    return invites

def get_player_invites(player_id, limit=10):
    """Holt Einladungen für einen Spieler"""
    conn = get_db_connection()
    invites = conn.execute('''
        SELECT i.*, e.title, e.type, e.date, e.time, e.location
        FROM invites i
        JOIN events e ON i.event_id = e.id
        WHERE i.player_id = ? AND e.date >= date('now')
        ORDER BY e.date ASC, e.time ASC
        LIMIT ?
    ''', (player_id, limit)).fetchall()
    conn.close()
    return invites

def create_invite(player_id, event_id, status='pending', notes=None):
    """Erstellt eine Einladung"""
    conn = get_db_connection()
    try:
        cursor = conn.execute('''
            INSERT INTO invites (player_id, event_id, status, notes)
            VALUES (?, ?, ?, ?)
        ''', (player_id, event_id, status, notes))
        invite_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return invite_id
    except sqlite3.IntegrityError:
        conn.close()
        return None  # Einladung existiert bereits

def update_invite_status(player_id, event_id, status, notes=None):
    """Aktualisiert den Status einer Einladung"""
    conn = get_db_connection()
    conn.execute('''
        UPDATE invites 
        SET status=?, notes=?, updated_at=CURRENT_TIMESTAMP
        WHERE player_id=? AND event_id=?
    ''', (status, notes, player_id, event_id))
    conn.commit()
    conn.close()

def bulk_invite_players(event_id, player_ids):
    """Lädt mehrere Spieler zu einem Event ein"""
    conn = get_db_connection()
    created_count = 0
    for player_id in player_ids:
        try:
            conn.execute('''
                INSERT INTO invites (player_id, event_id, status)
                VALUES (?, ?, 'pending')
            ''', (player_id, event_id))
            created_count += 1
        except sqlite3.IntegrityError:
            continue  # Einladung existiert bereits
    conn.commit()
    conn.close()
    return created_count

# News-Funktionen
def get_latest_news(limit=5):
    """Holt die neuesten Nachrichten"""
    conn = get_db_connection()
    news = conn.execute('''
        SELECT * FROM news 
        WHERE published = 1 
        ORDER BY created_at DESC 
        LIMIT ?
    ''', (limit,)).fetchall()
    conn.close()
    return news

def get_all_news():
    """Holt alle Nachrichten für Admin"""
    conn = get_db_connection()
    news = conn.execute('SELECT * FROM news ORDER BY created_at DESC').fetchall()
    conn.close()
    return news

def create_news(title, content, author='Admin', published=True):
    """Erstellt eine Nachricht"""
    conn = get_db_connection()
    cursor = conn.execute('''
        INSERT INTO news (title, content, author, published)
        VALUES (?, ?, ?, ?)
    ''', (title, content, author, published))
    news_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return news_id

# Clothing Rules-Funktionen
def get_clothing_rules():
    """Holt alle Kleidungsregeln"""
    conn = get_db_connection()
    rules = conn.execute('SELECT * FROM clothing_rules ORDER BY event_type').fetchall()
    conn.close()
    return rules

def create_clothing_rule(event_type, description):
    """Erstellt eine Kleidungsregel"""
    conn = get_db_connection()
    cursor = conn.execute('''
        INSERT INTO clothing_rules (event_type, description)
        VALUES (?, ?)
    ''', (event_type, description))
    rule_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return rule_id

# User-Funktionen für Admin
def get_user_by_username(username):
    """Holt einen Benutzer nach Username"""
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ? AND active = 1', (username,)).fetchone()
    conn.close()
    return user

def create_user(username, password_hash, role='trainer'):
    """Erstellt einen neuen Benutzer"""
    conn = get_db_connection()
    cursor = conn.execute('''
        INSERT INTO users (username, password_hash, role)
        VALUES (?, ?, ?)
    ''', (username, password_hash, role))
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return user_id
