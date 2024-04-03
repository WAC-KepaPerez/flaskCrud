# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import datetime
db = SQLAlchemy()

class Workouts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    reps = db.Column(db.Integer)
    description = db.Column(db.String(45))
    completed = db.Column(db.Boolean, default=False)
    created= db.Column(db.DateTime, default=datetime.datetime.now)
    slug = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45),unique=True)
    created= db.Column(db.DateTime, default=datetime.datetime.now)
    password = db.Column(db.String(45))

# You can define more model classes here if needed
