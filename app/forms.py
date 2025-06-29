from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, DateField, TimeField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, Optional
from app.models import User, Player

class LoginForm(FlaskForm):
    """Login form for admin users."""
    username = StringField('Benutzername', validators=[DataRequired()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    remember_me = BooleanField('Angemeldet bleiben')
    submit = SubmitField('Anmelden')

class EventForm(FlaskForm):
    """Form for creating/editing events."""
    title = StringField('Titel', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Beschreibung')
    event_type = SelectField('Event-Typ', 
                           choices=[('training', 'Training'), 
                                   ('game', 'Spiel'), 
                                   ('meeting', 'Meeting'), 
                                   ('tournament', 'Turnier')],
                           validators=[DataRequired()])
    date = DateField('Datum', validators=[DataRequired()])
    time = TimeField('Uhrzeit', validators=[DataRequired()])
    location = StringField('Ort', validators=[Length(max=200)])
    max_participants = IntegerField('Max. Teilnehmer', validators=[Optional()])
    submit = SubmitField('Speichern')

class PlayerForm(FlaskForm):
    """Form for creating/editing players."""
    first_name = StringField('Vorname', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Nachname', validators=[DataRequired(), Length(max=50)])
    email = StringField('E-Mail', validators=[DataRequired(), Email(), Length(max=120)])
    phone = StringField('Telefon', validators=[Length(max=20)])
    position = StringField('Position', validators=[Length(max=50)])
    jersey_number = IntegerField('Trikotnummer', validators=[Optional()])
    birth_date = DateField('Geburtsdatum', validators=[Optional()])
    team = SelectField('Team', 
                      choices=[('A-Team', 'A-Team'), 
                              ('B-Team', 'B-Team'), 
                              ('Jugend', 'Jugend'), 
                              ('Senioren', 'Senioren')],
                      validators=[Optional()])
    active = BooleanField('Aktiv')
    submit = SubmitField('Speichern')
    
    def __init__(self, original_email=None, *args, **kwargs):
        super(PlayerForm, self).__init__(*args, **kwargs)
        self.original_email = original_email
    
    def validate_email(self, email):
        if email.data != self.original_email:
            player = Player.query.filter_by(email=email.data).first()
            if player:
                raise ValidationError('Diese E-Mail-Adresse wird bereits verwendet.')

class NewsForm(FlaskForm):
    """Form for creating/editing news."""
    title = StringField('Titel', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Inhalt', validators=[DataRequired()])
    published = BooleanField('Veröffentlicht')
    submit = SubmitField('Speichern')

class InviteForm(FlaskForm):
    """Form for managing invitations."""
    player_ids = SelectField('Spieler', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Einladungen versenden')

class BulkInviteForm(FlaskForm):
    """Form for bulk invitations."""
    select_all = BooleanField('Alle auswählen')
    team_filter = SelectField('Team-Filter', 
                            choices=[('all', 'Alle Teams'),
                                    ('A-Team', 'A-Team'), 
                                    ('B-Team', 'B-Team'), 
                                    ('Jugend', 'Jugend'), 
                                    ('Senioren', 'Senioren')])
    submit = SubmitField('Ausgewählte einladen')

class ClothingRuleForm(FlaskForm):
    """Form for clothing rules."""
    event_type = SelectField('Event-Typ', 
                           choices=[('training', 'Training'), 
                                   ('game', 'Spiel'), 
                                   ('meeting', 'Meeting'), 
                                   ('tournament', 'Turnier')],
                           validators=[DataRequired()])
    description = TextAreaField('Kleidungsvorschrift', validators=[DataRequired()])
    submit = SubmitField('Speichern')

class UserForm(FlaskForm):
    """Form for creating admin users."""
    username = StringField('Benutzername', validators=[DataRequired(), Length(max=64)])
    email = StringField('E-Mail', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Passwort', validators=[DataRequired()])
    password2 = PasswordField('Passwort wiederholen', 
                            validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Benutzer erstellen')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Dieser Benutzername wird bereits verwendet.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Diese E-Mail-Adresse wird bereits verwendet.')
