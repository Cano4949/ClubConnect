"""
Admin Blueprint Routes - Verwaltungsfunktionen
"""

from flask import render_template, redirect, url_for, flash, request, jsonify
from app.admin import bp
from app.auth.routes import trainer_required
from app.forms import EventForm, PlayerForm, NewsForm, ClothingRuleForm, BulkInviteForm
from app.models import (
    get_upcoming_events, get_event_by_id, create_event, update_event, delete_event,
    get_all_players, get_player_by_id, create_player, update_player,
    get_player_invites_for_event, bulk_invite_players, update_invite_status,
    get_all_news, create_news, get_clothing_rules, create_clothing_rule
)
from datetime import datetime, date

@bp.route('/')
@trainer_required
def dashboard():
    """Admin-Dashboard"""
    # Statistiken sammeln
    upcoming_events = get_upcoming_events(5)
    all_players = get_all_players()
    recent_news = get_all_news()[:3]
    
    # Event-Statistiken
    total_events = len(get_upcoming_events(100))
    total_players = len(all_players)
    active_players = len([p for p in all_players if p['active']])
    
    stats = {
        'total_events': total_events,
        'total_players': total_players,
        'active_players': active_players,
        'total_news': len(recent_news)
    }
    
    return render_template('admin/dashboard.html',
                         upcoming_events=upcoming_events,
                         recent_news=recent_news,
                         stats=stats)

# Event-Verwaltung
@bp.route('/events')
@trainer_required
def events():
    """Event-Übersicht"""
    events = get_upcoming_events(50)
    return render_template('admin/events.html', events=events)

@bp.route('/events/create', methods=['GET', 'POST'])
@trainer_required
def create_event_route():
    """Neues Event erstellen"""
    form = EventForm()
    
    if form.validate_on_submit():
        event_id = create_event(
            title=form.title.data,
            event_type=form.type.data,
            date=form.date.data.strftime('%Y-%m-%d'),
            time=form.time.data.strftime('%H:%M'),
            location=form.location.data,
            clothing=form.clothing.data,
            description=form.description.data
        )
        
        if event_id:
            flash(f'Event "{form.title.data}" wurde erfolgreich erstellt.', 'success')
            return redirect(url_for('admin.event_detail', event_id=event_id))
        else:
            flash('Fehler beim Erstellen des Events.', 'danger')
    
    return render_template('admin/event_form.html', form=form, title='Neues Event')

@bp.route('/events/<int:event_id>')
@trainer_required
def event_detail(event_id):
    """Event-Details für Admin"""
    event = get_event_by_id(event_id)
    if not event:
        flash('Event nicht gefunden.', 'danger')
        return redirect(url_for('admin.events'))
    
    # Einladungen laden
    invites = get_player_invites_for_event(event_id)
    
    # Statistiken
    stats = {
        'total': len(invites),
        'accepted': len([i for i in invites if i['status'] == 'accepted']),
        'declined': len([i for i in invites if i['status'] == 'declined']),
        'pending': len([i for i in invites if i['status'] == 'pending']),
        'maybe': len([i for i in invites if i['status'] == 'maybe'])
    }
    
    return render_template('admin/event_detail.html', 
                         event=event, 
                         invites=invites, 
                         stats=stats)

@bp.route('/events/<int:event_id>/edit', methods=['GET', 'POST'])
@trainer_required
def edit_event(event_id):
    """Event bearbeiten"""
    event = get_event_by_id(event_id)
    if not event:
        flash('Event nicht gefunden.', 'danger')
        return redirect(url_for('admin.events'))
    
    form = EventForm()
    
    if form.validate_on_submit():
        update_event(
            event_id=event_id,
            title=form.title.data,
            event_type=form.type.data,
            date=form.date.data.strftime('%Y-%m-%d'),
            time=form.time.data.strftime('%H:%M'),
            location=form.location.data,
            clothing=form.clothing.data,
            description=form.description.data
        )
        
        flash(f'Event "{form.title.data}" wurde aktualisiert.', 'success')
        return redirect(url_for('admin.event_detail', event_id=event_id))
    
    # Formular mit Event-Daten vorausfüllen
    if request.method == 'GET':
        form.title.data = event['title']
        form.type.data = event['type']
        form.date.data = datetime.strptime(event['date'], '%Y-%m-%d').date()
        form.time.data = datetime.strptime(event['time'], '%H:%M').time()
        form.location.data = event['location']
        form.clothing.data = event['clothing']
        form.description.data = event['description']
    
    return render_template('admin/event_form.html', 
                         form=form, 
                         title='Event bearbeiten',
                         event=event)

@bp.route('/events/<int:event_id>/delete', methods=['POST'])
@trainer_required
def delete_event_route(event_id):
    """Event löschen"""
    event = get_event_by_id(event_id)
    if not event:
        flash('Event nicht gefunden.', 'danger')
        return redirect(url_for('admin.events'))
    
    delete_event(event_id)
    flash(f'Event "{event["title"]}" wurde gelöscht.', 'success')
    return redirect(url_for('admin.events'))

@bp.route('/events/<int:event_id>/invites')
@trainer_required
def manage_invites(event_id):
    """Einladungen verwalten"""
    event = get_event_by_id(event_id)
    if not event:
        flash('Event nicht gefunden.', 'danger')
        return redirect(url_for('admin.events'))
    
    invites = get_player_invites_for_event(event_id)
    all_players = get_all_players()
    
    # Spieler ohne Einladung finden
    invited_player_ids = [invite['player_id'] for invite in invites]
    uninvited_players = [p for p in all_players if p['id'] not in invited_player_ids]
    
    return render_template('admin/manage_invites.html',
                         event=event,
                         invites=invites,
                         uninvited_players=uninvited_players)

@bp.route('/events/<int:event_id>/invite', methods=['POST'])
@trainer_required
def invite_players(event_id):
    """Spieler zu Event einladen"""
    event = get_event_by_id(event_id)
    if not event:
        flash('Event nicht gefunden.', 'danger')
        return redirect(url_for('admin.events'))
    
    player_ids = request.form.getlist('player_ids')
    if not player_ids:
        flash('Keine Spieler ausgewählt.', 'warning')
        return redirect(url_for('admin.manage_invites', event_id=event_id))
    
    # Spieler-IDs in Integers umwandeln
    player_ids = [int(pid) for pid in player_ids]
    
    created_count = bulk_invite_players(event_id, player_ids)
    
    if created_count > 0:
        flash(f'{created_count} Einladungen wurden versendet.', 'success')
    else:
        flash('Keine neuen Einladungen erstellt (möglicherweise bereits vorhanden).', 'info')
    
    return redirect(url_for('admin.manage_invites', event_id=event_id))

# Spieler-Verwaltung
@bp.route('/players')
@trainer_required
def players():
    """Spieler-Übersicht"""
    all_players = get_all_players()
    return render_template('admin/players.html', players=all_players)

@bp.route('/players/create', methods=['GET', 'POST'])
@trainer_required
def create_player_route():
    """Neuen Spieler erstellen"""
    form = PlayerForm()
    
    if form.validate_on_submit():
        player_id = create_player(
            name=form.name.data,
            team=form.team.data,
            email=form.email.data,
            phone=form.phone.data,
            birth_date=form.birth_date.data.strftime('%Y-%m-%d') if form.birth_date.data else None,
            position=form.position.data,
            jersey_number=form.jersey_number.data
        )
        
        if player_id:
            flash(f'Spieler "{form.name.data}" wurde erstellt.', 'success')
            return redirect(url_for('admin.players'))
        else:
            flash('Fehler beim Erstellen des Spielers.', 'danger')
    
    return render_template('admin/player_form.html', form=form, title='Neuer Spieler')

@bp.route('/players/<int:player_id>/edit', methods=['GET', 'POST'])
@trainer_required
def edit_player(player_id):
    """Spieler bearbeiten"""
    player = get_player_by_id(player_id)
    if not player:
        flash('Spieler nicht gefunden.', 'danger')
        return redirect(url_for('admin.players'))
    
    form = PlayerForm()
    
    if form.validate_on_submit():
        update_player(
            player_id=player_id,
            name=form.name.data,
            team=form.team.data,
            email=form.email.data,
            phone=form.phone.data,
            birth_date=form.birth_date.data.strftime('%Y-%m-%d') if form.birth_date.data else None,
            position=form.position.data,
            jersey_number=form.jersey_number.data,
            active=form.active.data
        )
        
        flash(f'Spieler "{form.name.data}" wurde aktualisiert.', 'success')
        return redirect(url_for('admin.players'))
    
    # Formular vorausfüllen
    if request.method == 'GET':
        form.name.data = player['name']
        form.team.data = player['team']
        form.email.data = player['email']
        form.phone.data = player['phone']
        if player['birth_date']:
            form.birth_date.data = datetime.strptime(player['birth_date'], '%Y-%m-%d').date()
        form.position.data = player['position']
        form.jersey_number.data = player['jersey_number']
        form.active.data = bool(player['active'])
    
    return render_template('admin/player_form.html', 
                         form=form, 
                         title='Spieler bearbeiten',
                         player=player)

# News-Verwaltung
@bp.route('/news')
@trainer_required
def news_admin():
    """News-Verwaltung"""
    all_news = get_all_news()
    return render_template('admin/news.html', news_items=all_news)

@bp.route('/news/create', methods=['GET', 'POST'])
@trainer_required
def create_news_route():
    """Neue Nachricht erstellen"""
    form = NewsForm()
    
    if form.validate_on_submit():
        news_id = create_news(
            title=form.title.data,
            content=form.content.data,
            author=form.author.data or 'Admin',
            published=form.published.data
        )
        
        if news_id:
            flash(f'Nachricht "{form.title.data}" wurde erstellt.', 'success')
            return redirect(url_for('admin.news_admin'))
        else:
            flash('Fehler beim Erstellen der Nachricht.', 'danger')
    
    return render_template('admin/news_form.html', form=form, title='Neue Nachricht')

# Kleidungsregeln-Verwaltung
@bp.route('/clothing')
@trainer_required
def clothing_admin():
    """Kleidungsregeln-Verwaltung"""
    rules = get_clothing_rules()
    return render_template('admin/clothing.html', rules=rules)

@bp.route('/clothing/create', methods=['GET', 'POST'])
@trainer_required
def create_clothing_rule():
    """Neue Kleidungsregel erstellen"""
    form = ClothingRuleForm()
    
    if form.validate_on_submit():
        rule_id = create_clothing_rule(
            event_type=form.event_type.data,
            description=form.description.data
        )
        
        if rule_id:
            flash('Kleidungsregel wurde erstellt.', 'success')
            return redirect(url_for('admin.clothing_admin'))
        else:
            flash('Fehler beim Erstellen der Kleidungsregel.', 'danger')
    
    return render_template('admin/clothing_form.html', form=form, title='Neue Kleidungsregel')

# API-Endpoints für AJAX
@bp.route('/api/invite-status', methods=['POST'])
@trainer_required
def update_invite_status_api():
    """API-Endpoint zum Aktualisieren des Einladungsstatus"""
    data = request.get_json()
    
    if not data or 'player_id' not in data or 'event_id' not in data or 'status' not in data:
        return jsonify({'error': 'Fehlende Parameter'}), 400
    
    try:
        update_invite_status(
            player_id=data['player_id'],
            event_id=data['event_id'],
            status=data['status'],
            notes=data.get('notes', '')
        )
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
