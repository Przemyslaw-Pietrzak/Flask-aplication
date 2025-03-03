from flask import Flask, render_template, url_for, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, fresh_login_required
from wtforms import BooleanField, StringField, PasswordField, SubmitField
from flask_wtf import FlaskForm
from urllib.parse import urlparse, urljoin
from models import User, db, migrate, csrf
from admin.routes import admin_bp
from strefa_ch.routes import strefa_bp
import os


app = Flask(__name__)
app.config.from_pyfile('config.cfg')

db.init_app(app)
migrate.init_app(app, db)
csrf.init_app(app)

basedir = os.path.abspath(os.path.dirname(__file__))

# Rejestracja blueprintów
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(strefa_bp, url_prefix='/strefa')

# Konfiguracja Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # widok, do którego przekierowywujemy nieautoryzowanych użytkowników
login_manager.login_message = 'Proszę zaloguj się: ' # tekst flasha przy logowaniu(od przekierowania)

@login_manager.user_loader
def load_user(username):
    return User.query.get(username)

def is_safe_url(target):    #funkcja sprawdzająca czy nie ostaniemy pzekierowani poza obręb naszej aplikacji, zabezpieczenie przed phisingiem
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
            ref_url.netloc == test_url.netloc

class LoginForm(FlaskForm):
    name = StringField('Nazwa użytkownika')
    password = PasswordField('Hasło')
    remember = BooleanField('Zapamiętaj mnie')


@app.route('/init')
def init():
    db.create_all()

    #Tworzenie nowego admina
    admin = User.query.filter(User.username=='admin').first() 
    if admin == None:
        admin = User(username='admin')
        admin.set_password('haslo')
        admin.is_admin = True
        db.session.add(admin)
        db.session.commit()
    
    return '<h1>Initial configuration done!</h1>'

@app.route("/")
def index():
    return render_template("index.html", active_menu='home')

@app.route('/about')
def about():
    return  render_template('about.html', active_menu='about')

@app.route('/contact')
def contact():
    return  render_template('contact.html', active_menu='contact')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter(User.username == form.name.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)    #następuje zapisanie tego użytkownika w sesji; form remember z formluarza

            next = request.args.get('next') # jak zostaliśmy przekierowani do zalogowania ten kod wróci nas po zalogowaniu do strony którą chcieliśmy odwiedzić przed zalogowaniem
            if next and is_safe_url(next): # odwołanie do zabezpieczenia phishingowego
                return redirect(next)
            else:
                return redirect(url_for('strefa_bp.index'))
        else:
            flash('Nieprawidłowy login lub hasło', 'warning')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('Wylogowano Cię.', 'warning')
    return redirect(url_for('index'))


@app.route('/users')
def users():
    return  render_template('users.html')

if __name__ == "__main__":
    app.run(debug=True)