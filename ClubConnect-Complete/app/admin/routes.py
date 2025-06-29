from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app import db
from app.admin import admin
from app.models import Event, Player, News, ClothingRule, Invite, User
from app.forms import EventForm, PlayerForm, NewsForm, ClothingRuleForm, UserForm
from datetime import datetime, date
from sqlalchemy import func

@admin.before_request
@login_required
def require_login():
    """Ensure all admin routes require login."""
    pass

@admin.route('/dashboard')
def dashboard():
    """Admin dashboard with statistics."""
    # Get statistics
    total_events = Event.query.count()
    upcoming_events = Event.query.filter(Event.date >= date.today()).count()
    total_players = Player.query.filter_by(active=True).count()
    total_news = News.query.filter_by(published=True).count()
    
    # Get recent activities
    recent_events = Event.query.order_by(Event.created_at.desc()).limit(5).all()
    recent_players = Player.query.order_by(Player.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         total_events=total_events,
                         upcoming_events=upcoming_events,
                         total_players=total_players,
                         total_news=total_news,
                         recent_events=recent_events,
                         recent_players=recent_players)

# Event Management
@admin.route('/events')
def events():
    """List all events."""
    page = request.args.get('page', 1, type=int)
    pagination = Event.query.order_by(Event.date.desc(), Event.time.desc()).paginate(
        page=page,
        per_page=current_app.config['ITEMS_PER_PAGE'],
        error_out=False
    )
    events = pagination.items
    return render_template('admin/events.html', events=events, pagination=pagination)

@admin.route('/event/new', methods=['GET', 'POST'])
def new_event():
    """Create new event."""
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            description=form.description.data,
            event_type=form.event_type.data,
            date=form.date.data,
            time=form.time.data,
            location=form.location.data,
            max_participants=form.max_participants.data,
            created_by=current_user.id
        )
        db.session.add(event)
        db.session.commit()
        flash('Event wurde erfolgreich erstellt!', 'success')
        return redirect(url_for('admin.events'))
    return render_template('admin/event_form.html', form=form, title='Neues Event')

@admin.route('/event/<int:id>/edit', methods=['GET', 'POST'])
def edit_event(id):
    """Edit existing event."""
    event = Event.query.get_or_404(id)
    form = EventForm(obj=event)
    if form.validate_on_submit():
        event.title = form.title.data
        event.description = form.description.data
        event.event_type = form.event_type.data
        event.date = form.date.data
        event.time = form.time.data
        event.location = form.location.data
        event.max_participants = form.max_participants.data
        db.session.commit()
        flash('Event wurde erfolgreich aktualisiert!', 'success')
        return redirect(url_for('admin.events'))
    return render_template('admin/event_form.html', form=form, title='Event bearbeiten')

@admin.route('/event/<int:id>/delete', methods=['POST'])
def delete_event(id):
    """Delete event."""
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    flash('Event wurde erfolgreich gelöscht!', 'success')
    return redirect(url_for('admin.events'))

@admin.route('/event/<int:id>/invites')
def event_invites(id):
    """Manage invitations for an event."""
    event = Event.query.get_or_404(id)
    
    # Get all players not yet invited
    invited_player_ids = [i.player_id for i in event.invites]
    available_players = Player.query.filter(
        ~Player.id.in_(invited_player_ids),
        Player.active == True
    ).order_by(Player.last_name, Player.first_name).all()
    
    # Get current invitations
    invites = Invite.query.filter_by(event_id=id).join(Player).order_by(
        Invite.status, Player.last_name, Player.first_name
    ).all()
    
    return render_template('admin/event_invites.html', 
                         event=event, 
                         invites=invites,
                         available_players=available_players)

@admin.route('/event/<int:event_id>/invite/<int:player_id>', methods=['POST'])
def send_invite(event_id, player_id):
    """Send invitation to a player."""
    event = Event.query.get_or_404(event_id)
    player = Player.query.get_or_404(player_id)
    
    # Check if invite already exists
    existing = Invite.query.filter_by(event_id=event_id, player_id=player_id).first()
    if existing:
        flash('Einladung existiert bereits!', 'warning')
    else:
        invite = Invite(event_id=event_id, player_id=player_id)
        db.session.add(invite)
        db.session.commit()
        flash(f'Einladung an {player.full_name} wurde versendet!', 'success')
    
    return redirect(url_for('admin.event_invites', id=event_id))

@admin.route('/invite/<int:id>/delete', methods=['POST'])
def delete_invite(id):
    """Delete an invitation."""
    invite = Invite.query.get_or_404(id)
    event_id = invite.event_id
    db.session.delete(invite)
    db.session.commit()
    flash('Einladung wurde gelöscht!', 'success')
    return redirect(url_for('admin.event_invites', id=event_id))

# Player Management
@admin.route('/players')
def players():
    """List all players."""
    page = request.args.get('page', 1, type=int)
    team_filter = request.args.get('team', 'all')
    
    query = Player.query
    if team_filter != 'all':
        query = query.filter_by(team=team_filter)
    
    pagination = query.order_by(Player.last_name, Player.first_name).paginate(
        page=page,
        per_page=current_app.config['ITEMS_PER_PAGE'],
        error_out=False
    )
    players = pagination.items
    
    return render_template('admin/players.html', 
                         players=players, 
                         pagination=pagination,
                         team_filter=team_filter)

@admin.route('/player/new', methods=['GET', 'POST'])
def new_player():
    """Create new player."""
    form = PlayerForm()
    if form.validate_on_submit():
        player = Player(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            phone=form.phone.data,
            position=form.position.data,
            jersey_number=form.jersey_number.data,
            birth_date=form.birth_date.data,
            team=form.team.data,
            active=form.active.data
        )
        db.session.add(player)
        db.session.commit()
        flash('Spieler wurde erfolgreich erstellt!', 'success')
        return redirect(url_for('admin.players'))
    return render_template('admin/player_form.html', form=form, title='Neuer Spieler')

@admin.route('/player/<int:id>/edit', methods=['GET', 'POST'])
def edit_player(id):
    """Edit existing player."""
    player = Player.query.get_or_404(id)
    form = PlayerForm(obj=player, original_email=player.email)
    if form.validate_on_submit():
        player.first_name = form.first_name.data
        player.last_name = form.last_name.data
        player.email = form.email.data
        player.phone = form.phone.data
        player.position = form.position.data
        player.jersey_number = form.jersey_number.data
        player.birth_date = form.birth_date.data
        player.team = form.team.data
        player.active = form.active.data
        db.session.commit()
        flash('Spieler wurde erfolgreich aktualisiert!', 'success')
        return redirect(url_for('admin.players'))
    return render_template('admin/player_form.html', form=form, title='Spieler bearbeiten')

@admin.route('/player/<int:id>/delete', methods=['POST'])
def delete_player(id):
    """Delete player."""
    player = Player.query.get_or_404(id)
    db.session.delete(player)
    db.session.commit()
    flash('Spieler wurde erfolgreich gelöscht!', 'success')
    return redirect(url_for('admin.players'))

# News Management
@admin.route('/news')
def news():
    """List all news."""
    page = request.args.get('page', 1, type=int)
    pagination = News.query.order_by(News.created_at.desc()).paginate(
        page=page,
        per_page=current_app.config['ITEMS_PER_PAGE'],
        error_out=False
    )
    news_items = pagination.items
    return render_template('admin/news.html', news=news_items, pagination=pagination)

@admin.route('/news/new', methods=['GET', 'POST'])
def new_news():
    """Create new news article."""
    form = NewsForm()
    if form.validate_on_submit():
        news = News(
            title=form.title.data,
            content=form.content.data,
            published=form.published.data,
            author_id=current_user.id
        )
        db.session.add(news)
        db.session.commit()
        flash('Nachricht wurde erfolgreich erstellt!', 'success')
        return redirect(url_for('admin.news'))
    return render_template('admin/news_form.html', form=form, title='Neue Nachricht')

@admin.route('/news/<int:id>/edit', methods=['GET', 'POST'])
def edit_news(id):
    """Edit existing news article."""
    news_item = News.query.get_or_404(id)
    form = NewsForm(obj=news_item)
    if form.validate_on_submit():
        news_item.title = form.title.data
        news_item.content = form.content.data
        news_item.published = form.published.data
        news_item.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Nachricht wurde erfolgreich aktualisiert!', 'success')
        return redirect(url_for('admin.news'))
    return render_template('admin/news_form.html', form=form, title='Nachricht bearbeiten')

@admin.route('/news/<int:id>/delete', methods=['POST'])
def delete_news(id):
    """Delete news article."""
    news_item = News.query.get_or_404(id)
    db.session.delete(news_item)
    db.session.commit()
    flash('Nachricht wurde erfolgreich gelöscht!', 'success')
    return redirect(url_for('admin.news'))

# Clothing Rules Management
@admin.route('/clothing-rules')
def clothing_rules():
    """List all clothing rules."""
    rules = ClothingRule.query.all()
    return render_template('admin/clothing_rules.html', rules=rules)

@admin.route('/clothing-rule/new', methods=['GET', 'POST'])
def new_clothing_rule():
    """Create new clothing rule."""
    form = ClothingRuleForm()
    if form.validate_on_submit():
        rule = ClothingRule(
            event_type=form.event_type.data,
            description=form.description.data
        )
        db.session.add(rule)
        db.session.commit()
        flash('Kleidungsregel wurde erfolgreich erstellt!', 'success')
        return redirect(url_for('admin.clothing_rules'))
    return render_template('admin/clothing_rule_form.html', form=form, title='Neue Kleidungsregel')

@admin.route('/clothing-rule/<int:id>/edit', methods=['GET', 'POST'])
def edit_clothing_rule(id):
    """Edit existing clothing rule."""
    rule = ClothingRule.query.get_or_404(id)
    form = ClothingRuleForm(obj=rule)
    if form.validate_on_submit():
        rule.event_type = form.event_type.data
        rule.description = form.description.data
        rule.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Kleidungsregel wurde erfolgreich aktualisiert!', 'success')
        return redirect(url_for('admin.clothing_rules'))
    return render_template('admin/clothing_rule_form.html', form=form, title='Kleidungsregel bearbeiten')

@admin.route('/clothing-rule/<int:id>/delete', methods=['POST'])
def delete_clothing_rule(id):
    """Delete clothing rule."""
    rule = ClothingRule.query.get_or_404(id)
    db.session.delete(rule)
    db.session.commit()
    flash('Kleidungsregel wurde erfolgreich gelöscht!', 'success')
    return redirect(url_for('admin.clothing_rules'))

# User Management
@admin.route('/users')
def users():
    """List all admin users."""
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)

@admin.route('/user/new', methods=['GET', 'POST'])
def new_user():
    """Create new admin user."""
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Benutzer wurde erfolgreich erstellt!', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/user_form.html', form=form, title='Neuer Benutzer')
