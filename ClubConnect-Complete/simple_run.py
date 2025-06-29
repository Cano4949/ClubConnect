from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf.csrf import CSRFProtect
from datetime import datetime, timedelta
import sqlite3
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
csrf = CSRFProtect(app)

# Datenbank initialisieren
def init_db():
    conn = sqlite3.connect('clubconnect.db')
    c = conn.cursor()
    
    # Events Tabelle
    c.execute('''CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        location TEXT,
        event_type TEXT DEFAULT 'training'
    )''')
    
    # Players Tabelle
    c.execute('''CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT,
        phone TEXT,
        position TEXT
    )''')
    
    # News Tabelle
    c.execute('''CREATE TABLE IF NOT EXISTS news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT,
        date TEXT NOT NULL
    )''')
    
    # Beispieldaten einfügen
    c.execute("SELECT COUNT(*) FROM events")
    if c.fetchone()[0] == 0:
        events = [
            ('Wöchentliches Training', 'Reguläres Training für alle Spieler', '2025-06-26', '18:00', 'Sportplatz Hauptstraße', 'training'),
            ('Spiel gegen FC Beispielstadt', 'Auswärtsspiel', '2025-06-28', '15:00', 'Auswärtsstadion', 'game'),
            ('Vereinsversammlung', 'Monatliche Vereinsversammlung', '2025-07-02', '19:30', 'Vereinsheim', 'meeting'),
            ('Sommerturnier', 'Jährliches Sommerturnier', '2025-07-15', '10:00', 'Sportplatz Hauptstraße', 'tournament'),
            ('Training Jugend', 'Training für Jugendmannschaft', '2025-06-27', '16:00', 'Sportplatz Hauptstraße', 'training')
        ]
        c.executemany("INSERT INTO events (title, description, date, time, location, event_type) VALUES (?, ?, ?, ?, ?, ?)", events)
    
    c.execute("SELECT COUNT(*) FROM players")
    if c.fetchone()[0] == 0:
        players = [
            ('Max Mustermann', 'max@example.com', '0123456789', 'Stürmer'),
            ('Anna Schmidt', 'anna@example.com', '0123456790', 'Mittelfeld'),
            ('Tom Weber', 'tom@example.com', '0123456791', 'Verteidiger'),
            ('Lisa Müller', 'lisa@example.com', '0123456792', 'Torwart'),
            ('Jan Fischer', 'jan@example.com', '0123456793', 'Mittelfeld')
        ]
        c.executemany("INSERT INTO players (name, email, phone, position) VALUES (?, ?, ?, ?)", players)
    
    c.execute("SELECT COUNT(*) FROM news")
    if c.fetchone()[0] == 0:
        news = [
            ('Willkommen bei ClubConnect!', 'Das neue Vereinsmanagement-System ist online.', '2025-06-25'),
            ('Saisonstart 2025', 'Die neue Saison beginnt am 1. Juli 2025.', '2025-06-24'),
            ('Turnier-Anmeldung', 'Anmeldung für das Sommerturnier ist geöffnet.', '2025-06-23')
        ]
        c.executemany("INSERT INTO news (title, content, date) VALUES (?, ?, ?)", news)
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('clubconnect.db')
    c = conn.cursor()
    
    # Kommende Events
    c.execute("SELECT * FROM events ORDER BY date LIMIT 5")
    events = c.fetchall()
    
    # Neueste News
    c.execute("SELECT * FROM news ORDER BY date DESC LIMIT 3")
    news = c.fetchall()
    
    conn.close()
    
    return render_template('index.html', events=events, news=news)

@app.route('/calendar')
def calendar():
    conn = sqlite3.connect('clubconnect.db')
    c = conn.cursor()
    c.execute("SELECT * FROM events ORDER BY date")
    events = c.fetchall()
    conn.close()
    
    return render_template('calendar.html', events=events)

@app.route('/admin')
def admin():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('clubconnect.db')
    c = conn.cursor()
    
    # Statistiken
    c.execute("SELECT COUNT(*) FROM events")
    event_count = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM players")
    player_count = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM news")
    news_count = c.fetchone()[0]
    
    conn.close()
    
    stats = {
        'events': event_count,
        'players': player_count,
        'news': news_count
    }
    
    return render_template('admin/dashboard.html', stats=stats)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == 'admin' and password == 'admin123':
            session['user'] = username
            flash('Erfolgreich angemeldet!', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Ungültige Anmeldedaten!', 'error')
    
    return render_template('auth/login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Erfolgreich abgemeldet!', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    print("🚀 ClubConnect startet...")
    print("📍 URL: http://localhost:5000")
    print("🔑 Login: admin / admin123")
    print("⏹️  Stoppen mit Ctrl+C")
    app.run(host='0.0.0.0', port=5000, debug=True)
