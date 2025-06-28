"""
Auth Blueprint Routes - Authentifizierung
"""

from flask import render_template, redirect, url_for, flash, session, request
from werkzeug.security import check_password_hash, generate_password_hash
from app.auth import bp
from app.forms import LoginForm
from app.models import get_user_by_username, create_user
from functools import wraps

def login_required(f):
    """Decorator für Login-Pflicht"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Bitte melden Sie sich an, um diese Seite zu besuchen.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def trainer_required(f):
    """Decorator für Trainer-Berechtigung"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Bitte melden Sie sich an.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        
        if session.get('user_role') != 'trainer':
            flash('Sie haben keine Berechtigung für diese Seite.', 'danger')
            return redirect(url_for('main.index'))
        
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login-Seite"""
    if 'user_id' in session:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        # Benutzer aus Datenbank laden
        user = get_user_by_username(username)
        
        if user and check_password_hash(user['password_hash'], password):
            # Login erfolgreich
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['user_role'] = user['role']
            session.permanent = form.remember_me.data
            
            flash(f'Willkommen zurück, {username}!', 'success')
            
            # Weiterleitung zur ursprünglich angeforderten Seite
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            
            # Standard-Weiterleitung je nach Rolle
            if user['role'] == 'trainer':
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('main.index'))
        else:
            flash('Ungültiger Benutzername oder Passwort.', 'danger')
    
    return render_template('auth/login.html', form=form)

@bp.route('/logout')
def logout():
    """Benutzer abmelden"""
    username = session.get('username', 'Benutzer')
    session.clear()
    flash(f'Auf Wiedersehen, {username}!', 'info')
    return redirect(url_for('main.index'))

# Hilfsfunktionen für Templates
@bp.app_template_global()
def current_user():
    """Aktueller Benutzer für Templates"""
    if 'user_id' in session:
        return {
            'id': session['user_id'],
            'username': session['username'],
            'role': session.get('user_role', 'user'),
            'is_authenticated': True,
            'is_trainer': session.get('user_role') == 'trainer'
        }
    return {
        'is_authenticated': False,
        'is_trainer': False
    }

# Initialisierung: Standard-Admin-Benutzer erstellen
def init_admin_user():
    """Erstellt Standard-Admin-Benutzer falls nicht vorhanden"""
    try:
        admin_user = get_user_by_username('admin')
        if not admin_user:
            # Standard-Admin erstellen
            password_hash = generate_password_hash('admin123')  # In Produktion ändern!
            create_user('admin', password_hash, 'trainer')
            print("Standard-Admin-Benutzer erstellt: admin/admin123")
    except Exception as e:
        print(f"Fehler beim Erstellen des Admin-Benutzers: {e}")
