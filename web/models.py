from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from web import login_manager, app ,db
from flask_login import UserMixin
import json
from time import time


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    joined_day = db.Column(db.DateTime, default=datetime.utcnow)
    forename = db.Column(db.String(20), unique=True, nullable=False)
    surname = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    date = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.date}')"







