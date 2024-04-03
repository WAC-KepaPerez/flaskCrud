# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Workouts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    reps = db.Column(db.Integer)
    description = db.Column(db.String(45))
    completed = db.Column(db.Boolean, default=False)

# You can define more model classes here if needed
