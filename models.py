from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()

#Tabela użytkoników
class User(UserMixin, db.Model):
    username = db.Column(db.String(20), primary_key=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # flaga oznaczająca konto administratora

    def get_id(self):
        return self.username    
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

#Tabela utworów
class Title(db.Model):
    __tablename__ = 'titles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    version = db.Column(db.String)
    year = db.Column(db.Integer)
    # Możesz dodać np. liczbę głosów
    voices_count = db.Column(db.Integer, default=3)

    # Relacja 1->Wiele z Voice
    voices = db.relationship("Voice", backref="title", cascade="all, delete-orphan")

    #def __repr__(self):
        #return f"<Title {self.name}>"


class Voice(db.Model):
    __tablename__ = 'voices'

    id = db.Column(db.Integer, primary_key=True)
    title_id = db.Column(db.Integer, db.ForeignKey('titles.id'), nullable=False)
    voice_name = db.Column(db.String(64), nullable=False)

    # Relacja 1->Wiele z AudioFile
    audio_files = db.relationship("AudioFile", backref="voice", cascade="all, delete-orphan")

    #def __repr__(self):
        #return f"<Voice {self.voice_name}>"


class AudioFile(db.Model):
    __tablename__ = 'audio_files'

    id = db.Column(db.Integer, primary_key=True)
    voice_id = db.Column(db.Integer, db.ForeignKey('voices.id'), nullable=False)
    file_path = db.Column(db.String(256), nullable=False)

    #def __repr__(self):
    #    return f"<AudioFile path={self.file_path}>"