from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, MultipleFileField, SelectField
from wtforms.validators import DataRequired, Length, Optional, NumberRange

class AddUserForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[
        DataRequired(message='Nazwa użytkownika '),
        Length(min=3, max=50, message='Nazwa użytkownika musi mieć od 3 do 50 znaków.')
    ])
    password = PasswordField('Hasło', validators=[
        DataRequired(message='Hasło '),
        Length(min=6, message='Hasło musi mieć co najmniej 6 znaków.')
    ])
    is_admin = BooleanField('Czy nadać uprawnienia administratora?')
    submit = SubmitField('Dodaj użytkownika')


class TitleForm(FlaskForm):
    name = StringField("Nazwa utworu", validators=[DataRequired()])
    version = SelectField("Wersja",choices=['ver.1', 'ver.2', 'ver.3', 'ver.4'])
    year = IntegerField("Rok produkcji", validators=[DataRequired(), NumberRange(min=2017)])
    voices_count = IntegerField('Ilość głosów', validators=[DataRequired(), NumberRange(min=1)])

class VoiceForm(FlaskForm):
    voice_name = SelectField("Głos",choices=['Sopran', 'Alt', 'Tenor'])

class AudioUploadForm(FlaskForm):
    # Pole do wgrywania jednego pliku
    # audio_file = FileField("Plik audio", validators=[Optional()])
    
    # Albo wiele plików
    audio_files = MultipleFileField("Pliki audio", validators=[Optional()])