from email.policy import default
from enum import unique
from lib2to3.pgen2 import token
from traceback import print_exception
import uuid
from datetime import datetime
import secrets
from xmlrpc.client import DateTime

#3rd party imports
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_marshmallow import Marshmallow
from sqlalchemy import ForeignKey


# Adding flask security for passwords
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

 
# User Model Creation
class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(50), nullable = True, default = '')
    last_name = db.Column(db.String(50), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default='', unique = True)
    data_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    character = db.relationship('Character', backref="owner", lazy=True)

    def __init__(self, email, first_name='', last_name='', id='', password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.token = self.set_token(24)
        self.email = email
        self.g_auth_verify = g_auth_verify

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def set_token(self, length):
        return secrets.token_hex(length)

    def __repr__(self):
        return f'User {self.email} has been added to the database.'

class Character(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(250), nullable = True)
    comics_appeared = db.Column(db.String(250), nullable = True)
    super_power = db.Column(db.String(50), nullable = True)
    data_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_token = db.Column(db.String(200), db.ForeignKey('user.token'), nullable = False)
    
    def __init__(self, name, description, comics_appeared, super_power, date_created, user_token, id=''):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.comics_appeared = comics_appeared
        self.super_power = super_power
        self.date_created = date_created
        self.user_token = user_token

    def set_id(self):
        return secrets.token_urlsafe()

    def __repr__(self):
        return f"The following Character has been added: {self.name}."

# creation of API Schema via the marshmallow Object
class CharacterSchema(ma.Schema):
    class Meta:
        fields = ['id','name', 'description', 'comics_appeared', 'super_power', 'date_created']

character_schema = CharacterSchema()
characters_schema = CharacterSchema(many=True)