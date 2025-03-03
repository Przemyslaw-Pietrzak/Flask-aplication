from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from models import Title, Voice, AudioFile
from app import db

strefa_bp = Blueprint('strefa_bp', __name__, template_folder='templates')

@strefa_bp.route('/')
@login_required
def index():
    # Prosty widok główny
    return render_template('strefa/index.html', active_menu='home')


@strefa_bp.route('/voice/<voice_name>')
@login_required
def voice_list(voice_name):
    """
    Wyświetla listę utworów (Title), które mają dany Voice (voice_name).
    """
    # Znajdziesz wszystkie recordy Voice, gdzie voice_name = voice_name
    voices = Voice.query.filter_by(voice_name=voice_name).all()
    # w `voice_list.html` wyświetlisz tytuły (voice.title)
    return render_template('strefa/voice_list.html', voice_name=voice_name, voices=voices)


@strefa_bp.route('/voice/<voice_name>/title/<int:title_id>')
@login_required
def audio_files(voice_name, title_id):
    """
    Wyświetla wszystkie pliki audio dla konkretnego tytułu i głosu.
    """
    voice_name = voice_name
    voice = Voice.query.filter_by(voice_name=voice_name, title_id=title_id).first_or_404()
    files = voice.audio_files  # relacja
    return render_template('strefa/audio_files.html', voice=voice, files=files, voice_name=voice_name)