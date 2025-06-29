from flask import render_template, request, current_app
from app.main import main
from app.models import Event, Player, News, ClothingRule, Invite
from datetime import datetime, date
from sqlalchemy import and_

@main.route('/')
@main.route('/index')
def index():
    """Home page with upcoming events and latest news."""
    # Get upcoming events
    upcoming_events = Event.query.filter(
        Event.date >= date.today()
    ).order_by(Event.date, Event.time).limit(5).all()
    
    # Get latest news
    latest_news = News.query.filter_by(published=True).order_by(
        News.created_at.desc()
    ).limit(3).all()
    
    return render_template('index.html', 
                         events=upcoming_events, 
                         news=latest_news)

@main.route('/calendar')
def calendar():
    """Calendar view of all events."""
    # Get filter parameters
    event_type = request.args.get('type', 'all')
    month = request.args.get('month', datetime.now().month, type=int)
    year = request.args.get('year', datetime.now().year, type=int)
    
    # Build query
    query = Event.query
    
    if event_type != 'all':
        query = query.filter_by(event_type=event_type)
    
    # Filter by month and year
    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)
    
    query = query.filter(
        and_(Event.date >= start_date, Event.date < end_date)
    )
    
    events = query.order_by(Event.date, Event.time).all()
    
    return render_template('calendar.html', 
                         events=events,
                         current_month=month,
                         current_year=year,
                         event_type=event_type)

@main.route('/event/<int:id>')
def event_detail(id):
    """Event detail page."""
    event = Event.query.get_or_404(id)
    
    # Get invitations with player details
    invites = Invite.query.filter_by(event_id=id).join(Player).all()
    
    # Get clothing rules for this event type
    clothing_rule = ClothingRule.query.filter_by(event_type=event.event_type).first()
    
    return render_template('event_detail.html', 
                         event=event, 
                         invites=invites,
                         clothing_rule=clothing_rule)

@main.route('/players')
def players():
    """Public player list."""
    team_filter = request.args.get('team', 'all')
    
    query = Player.query.filter_by(active=True)
    
    if team_filter != 'all':
        query = query.filter_by(team=team_filter)
    
    players = query.order_by(Player.last_name, Player.first_name).all()
    
    return render_template('players.html', 
                         players=players,
                         team_filter=team_filter)

@main.route('/player/<int:id>')
def player_detail(id):
    """Player detail page."""
    player = Player.query.get_or_404(id)
    
    # Get player's upcoming events
    upcoming_invites = Invite.query.join(Event).filter(
        Invite.player_id == id,
        Event.date >= date.today()
    ).order_by(Event.date, Event.time).all()
    
    return render_template('player_detail.html', 
                         player=player,
                         upcoming_invites=upcoming_invites)

@main.route('/news')
def news():
    """News page with pagination."""
    page = request.args.get('page', 1, type=int)
    
    pagination = News.query.filter_by(published=True).order_by(
        News.created_at.desc()
    ).paginate(
        page=page,
        per_page=current_app.config['ITEMS_PER_PAGE'],
        error_out=False
    )
    
    news_items = pagination.items
    
    return render_template('news.html', 
                         news=news_items,
                         pagination=pagination)

@main.route('/news/<int:id>')
def news_detail(id):
    """News detail page."""
    news_item = News.query.get_or_404(id)
    
    # Get related news
    related_news = News.query.filter(
        News.id != id,
        News.published == True
    ).order_by(News.created_at.desc()).limit(3).all()
    
    return render_template('news_detail.html', 
                         news=news_item,
                         related_news=related_news)

@main.route('/clothing-rules')
def clothing_rules():
    """Display clothing rules for different event types."""
    rules = ClothingRule.query.all()
    return render_template('clothing_rules.html', rules=rules)

@main.route('/about')
def about():
    """About page."""
    return render_template('about.html')

@main.route('/contact')
def contact():
    """Contact page."""
    return render_template('contact.html')
