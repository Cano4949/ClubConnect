"""
ClubConnect WTForms Formulare
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, TimeField, PasswordField, BooleanField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, Optional, Length, NumberRange
from wtforms.widgets import TextArea

class LoginForm(FlaskForm):
    """Login-Formular für Trainer"""
    username = StringField('Benutzername', validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Passwort', validators=[DataRequired()])
    remember_me = BooleanField('Angemeldet bleiben')
    submit = SubmitField('Anmelden')

class EventForm(FlaskForm):
    """Formular für Event-Erstellung und -Bearbeitung"""
    title = StringField('Titel', validators=[DataRequired(), Length(max=200)])
    type = SelectField('Typ', choices=[
        ('training', 'Training'),
        ('match', 'Spiel'),
        ('tournament', 'Turnier'),
        ('meeting', 'Besprechung'),
        ('other', 'Sonstiges')
    ], validators=[DataRequired()])
    date = DateField('Datum', validators=[DataRequired()])
    time = TimeField('Uhrzeit', validators=[DataRequired()])
    location = StringField('Ort', validators=[Optional(), Length(max=200)])
    clothing = SelectField('Kleidung', choices=[
        ('', 'Keine Angabe'),
        ('training', 'Trainingskleidung'),
        ('match', 'Spielkleidung'),
        ('formal', 'Formelle Kleidung'),
        ('casual', 'Freizeitkleidung')
    ], validators=[Optional()])
    description = TextAreaField('Beschreibung', validators=[Optional(), Length(max=1000)])
    submit = SubmitField('Speichern')

class PlayerForm(FlaskForm):
    """Formular für Spieler-Erstellung und -Bearbeitung"""
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    team = StringField('Team/Mannschaft', validators=[Optional(), Length(max=50)])
    email = StringField('E-Mail', validators=[Optional(), Email(), Length(max=100)])
    phone = StringField('Telefon', validators=[Optional(), Length(max=20)])
    birth_date = DateField('Geburtsdatum', validators=[Optional()])
    position = SelectField('Position', choices=[
        ('', 'Keine Angabe'),
        ('goalkeeper', 'Torwart'),
        ('defender', 'Verteidiger'),
        ('midfielder', 'Mittelfeldspieler'),
        ('forward', 'Stürmer'),
        ('other', 'Sonstiges')
    ], validators=[Optional()])
    jersey_number = IntegerField('Trikotnummer', validators=[Optional(), NumberRange(min=1, max=99)])
    active = BooleanField('Aktiv', default=True)
    submit = SubmitField('Speichern')

class InviteForm(FlaskForm):
    """Formular für Einladungsstatus-Update"""
    status = SelectField('Status', choices=[
        ('pending', 'Ausstehend'),
        ('accepted', 'Zugesagt'),
        ('declined', 'Abgesagt'),
        ('maybe', 'Vielleicht')
    ], validators=[DataRequired()])
    notes = TextAreaField('Notizen', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Status aktualisieren')

class BulkInviteForm(FlaskForm):
    """Formular für Massen-Einladungen"""
    player_ids = SelectField('Spieler auswählen', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Einladungen senden')

class NewsForm(FlaskForm):
    """Formular für Nachrichten-Erstellung und -Bearbeitung"""
    title = StringField('Titel', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Inhalt', validators=[DataRequired(), Length(max=5000)], widget=TextArea())
    author = StringField('Autor', validators=[Optional(), Length(max=100)], default='Admin')
    published = BooleanField('Veröffentlicht', default=True)
    submit = SubmitField('Speichern')

class ClothingRuleForm(FlaskForm):
    """Formular für Kleidungsregeln"""
    event_type = SelectField('Event-Typ', choices=[
        ('training', 'Training'),
        ('match', 'Spiel'),
        ('tournament', 'Turnier'),
        ('meeting', 'Besprechung'),
        ('other', 'Sonstiges')
    ], validators=[DataRequired()])
    description = TextAreaField('Beschreibung', validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField('Speichern')

class SearchForm(FlaskForm):
    """Suchformular"""
    query = StringField('Suche', validators=[Optional(), Length(max=100)])
    submit = SubmitField('Suchen')

class FilterForm(FlaskForm):
    """Filter-Formular für Events"""
    event_type = SelectField('Typ', choices=[
        ('', 'Alle'),
        ('training', 'Training'),
        ('match', 'Spiel'),
        ('tournament', 'Turnier'),
        ('meeting', 'Besprechung'),
        ('other', 'Sonstiges')
    ], validators=[Optional()])
    date_from = DateField('Von Datum', validators=[Optional()])
    date_to = DateField('Bis Datum', validators=[Optional()])
    submit = SubmitField('Filtern')
