"""
Main Blueprint Routes - Öffentliche Seiten
"""

from flask import render_template, request, jsonify, current_app
from app.main import bp
from app.models import (
    get_upcoming_events, get_event_by_id, get_latest_news, 
    get_clothing_rules, get_player_invites_for_event
)
from app.forms import FilterForm, SearchForm
from datetime import datetime, date

@bp.route('/')
def index():
    """Startseite mit Übersicht"""
    # Kommende Events
    upcoming_events = get_upcoming_events(5)
    
    # Neueste Nachrichten
    latest_news = get_latest_news(3)
    
    return render_template('index.html', 
                         upcoming_events=upcoming_events,
                         latest_news=latest_news)

@bp.route('/calendar')
def calendar():
    """Kalenderansicht aller Events"""
    filter_form = FilterForm()
    
    # Filter-Parameter aus URL
    event_type = request.args.get('event_type', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    
    # Events laden (hier vereinfacht - in echter App würde man filtern)
    events = get_upcoming_events(50)  # Mehr Events für Kalender
    
    # Events für Kalender-JSON formatieren
    calendar_events = []
    for event in events:
        calendar_events.append({
            'id': event['id'],
            'title': event['title'],
            'start': f"{event['date']}T{event['time']}",
            'url': f"/event/{event['id']}",
            'className': f"event-{event['type']}"
        })
    
    return render_template('calendar.html', 
                         filter_form=filter_form,
                         calendar_events=calendar_events)

@bp.route('/event/<int:event_id>')
def event_detail(event_id):
    """Event-Detailseite"""
    event = get_event_by_id(event_id)
    if not event:
        return render_template('errors/404.html'), 404
    
    # Einladungen für dieses Event
    invites = get_player_invites_for_event(event_id)
    
    # Statistiken
    total_invites = len(invites)
    accepted = len([i for i in invites if i['status'] == 'accepted'])
    declined = len([i for i in invites if i['status'] == 'declined'])
    pending = len([i for i in invites if i['status'] == 'pending'])
    
    stats = {
        'total': total_invites,
        'accepted': accepted,
        'declined': declined,
        'pending': pending
    }
    
    return render_template('event_detail.html', 
                         event=event, 
                         invites=invites,
                         stats=stats)

@bp.route('/invites')
def invites():
    """Einladungsübersicht (vereinfacht - normalerweise spieler-spezifisch)"""
    # Hier würde man normalerweise den eingeloggten Spieler verwenden
    # Für Demo-Zwecke zeigen wir alle kommenden Events
    upcoming_events = get_upcoming_events(10)
    
    return render_template('invites.html', events=upcoming_events)

@bp.route('/clothing')
def clothing():
    """Kleidungsregeln"""
    clothing_rules = get_clothing_rules()
    
    # Regeln nach Event-Typ gruppieren
    rules_by_type = {}
    for rule in clothing_rules:
        event_type = rule['event_type']
        if event_type not in rules_by_type:
            rules_by_type[event_type] = []
        rules_by_type[event_type].append(rule)
    
    return render_template('clothing.html', rules_by_type=rules_by_type)

@bp.route('/news')
def news():
    """Vereinsnachrichten"""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # Vereinfachte Paginierung (in echter App würde man LIMIT/OFFSET verwenden)
    all_news = get_latest_news(50)  # Mehr News laden
    
    # Paginierung simulieren
    start = (page - 1) * per_page
    end = start + per_page
    news_items = all_news[start:end]
    
    has_prev = page > 1
    has_next = len(all_news) > end
    
    pagination = {
        'has_prev': has_prev,
        'has_next': has_next,
        'prev_num': page - 1 if has_prev else None,
        'next_num': page + 1 if has_next else None,
        'page': page
    }
    
    return render_template('news.html', 
                         news_items=news_items,
                         pagination=pagination)

@bp.route('/api/events')
def api_events():
    """API-Endpoint für Events (für AJAX-Requests)"""
    events = get_upcoming_events(50)
    
    # Events in JSON-Format konvertieren
    events_json = []
    for event in events:
        events_json.append({
            'id': event['id'],
            'title': event['title'],
            'type': event['type'],
            'date': event['date'],
            'time': event['time'],
            'location': event['location'],
            'clothing': event['clothing'],
            'description': event['description']
        })
    
    return jsonify(events_json)

@bp.route('/search')
def search():
    """Suchfunktion"""
    search_form = SearchForm()
    query = request.args.get('query', '').strip()
    results = []
    
    if query:
        # Vereinfachte Suche in Events (in echter App würde man Volltext-Suche verwenden)
        all_events = get_upcoming_events(100)
        for event in all_events:
            if (query.lower() in event['title'].lower() or 
                (event['description'] and query.lower() in event['description'].lower()) or
                (event['location'] and query.lower() in event['location'].lower())):
                results.append(event)
    
    return render_template('search.html', 
                         search_form=search_form,
                         query=query,
                         results=results)

# Template-Filter
@bp.app_template_filter('datetime')
def datetime_filter(value, format='%d.%m.%Y'):
    """Datum formatieren"""
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            return value
    
    if isinstance(value, date):
        return value.strftime(format)
    return value

@bp.app_template_filter('time')
def time_filter(value, format='%H:%M'):
    """Zeit formatieren"""
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, '%H:%M:%S').time()
        except ValueError:
            try:
                value = datetime.strptime(value, '%H:%M').time()
            except ValueError:
                return value
    
    if hasattr(value, 'strftime'):
        return value.strftime(format)
    return value

@bp.app_template_filter('event_type_name')
def event_type_name_filter(value):
    """Event-Typ in deutschen Namen umwandeln"""
    type_names = {
        'training': 'Training',
        'match': 'Spiel',
        'tournament': 'Turnier',
        'meeting': 'Besprechung',
        'other': 'Sonstiges'
    }
    return type_names.get(value, value)

@bp.app_template_filter('status_name')
def status_name_filter(value):
    """Status in deutschen Namen umwandeln"""
    status_names = {
        'pending': 'Ausstehend',
        'accepted': 'Zugesagt',
        'declined': 'Abgesagt',
        'maybe': 'Vielleicht'
    }
    return status_names.get(value, value)

@bp.app_template_filter('status_class')
def status_class_filter(value):
    """CSS-Klasse für Status"""
    status_classes = {
        'pending': 'warning',
        'accepted': 'success',
        'declined': 'danger',
        'maybe': 'info'
    }
    return status_classes.get(value, 'secondary')
