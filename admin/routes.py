# admin/routes.py
from flask import Blueprint, render_template, flash, redirect, url_for
from forms import AddUserForm, TitleForm, VoiceForm, AudioUploadForm
from models import db, User, Title, Voice, AudioFile
from auth_decorators import admin_required
import os

admin_bp = Blueprint('admin_bp', __name__, template_folder='templates')

#Panel administratora
@admin_bp.route('/')
@admin_required
def admin_index():
    return render_template('admin/index.html')

#Dodawanie nowego utworu
@admin_bp.route('/title/new', methods=['GET', 'POST'])
@admin_required
def new_title():
    form = TitleForm()
    if form.validate_on_submit():
        t = Title(
            name=form.name.data,
            version=form.version.data,
            year=form.year.data,
            voices_count=form.voices_count.data
        )
        db.session.add(t)
        db.session.commit()
        flash("Tytuł dodany pomyślnie!", "success")
        return redirect(url_for('admin_bp.new_voice', title_id=t.id))
    return render_template('admin/new_title.html', form=form)

#Dodawanie głosu
@admin_bp.route('/voice/new/<int:title_id>', methods=['GET','POST'])
@admin_required
def new_voice(title_id):
    form = VoiceForm()
    
    # Pobierz obiekt Title z bazy (lub zgłoś 404, jeśli nie istnieje)
    title_obj = Title.query.get_or_404(title_id)

    if form.validate_on_submit():
        v = Voice(
            title_id=title_id,
            voice_name=form.voice_name.data
        )
        db.session.add(v)
        db.session.commit()
        flash("Głos dodany!", "success")
        return redirect(url_for('admin_bp.upload_audio', voice_id=v.id))
    return render_template('admin/new_voice.html', form=form, title=title_obj)

#Dodanie nagrania
@admin_bp.route('/voice/<int:voice_id>/upload', methods=['GET','POST'])
@admin_required
def upload_audio(voice_id):
    form = AudioUploadForm()
    voice = Voice.query.get_or_404(voice_id)
    if form.validate_on_submit():
        files = form.audio_files.data  # to jest lista w przypadku MultipleFileField
        for f in files:
            # Zapis pliku w katalogu static/audio
            filename = f.filename
            save_path = os.path.join('static', 'audio', filename)
            # Uwaga: w realnej aplikacji stosuj sprawdzanie bezpieczeństwa nazwy
            f.save(save_path)

            # Tworzymy rekord w bazie
            af = AudioFile(
                voice_id=voice_id,
                file_path=os.path.join(filename)  # np. "audio/test.mp3"
            )
            db.session.add(af)

        db.session.commit()
        flash("Pliki audio zostały wgrane! Możesz dodać kolejne.", "success")
        return redirect(url_for('admin_bp.new_title'))
    return render_template('admin/upload_audio.html', form=form, voice=voice)


#Dodawanie użytkowników
@admin_bp.route('/add_user', methods=['GET', 'POST'])
@admin_required
def add_user():

    form = AddUserForm()
    if form.validate_on_submit():
        # Czy jest już ktoś z takim username lub emailem?
        existing_user = User.query.filter(User.username == form.username.data).first()
        if existing_user:
            flash('Użytkownik o nazwie nazwie już istnieje!', 'warning')
            return redirect(url_for('admin_bp.add_user'))

        # Tworzymy nowy obiekt User
        new_user = User(
            username=form.username.data,
            is_admin=form.is_admin.data  # Ustawiamy wg pola formularza
        )
        new_user.set_password(form.password.data)

        # Zapis do bazy
        db.session.add(new_user)
        db.session.commit()

        flash('Użytkownik został dodany pomyślnie!', 'success')
        return redirect(url_for('admin_bp.add_user'))

    return render_template('admin/add_user.html', form=form)