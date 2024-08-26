from . import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True)
    name = db.Column(db.String(200))
    password = db.Column(db.String(200))
    reset_token = db.Column(db.String(100), nullable=True)
    profile_picture = db.Column(db.String(200), nullable=True, default='default.jpg')  # New field
    workouts = db.relationship('Workout', backref='author', lazy=True)

    def date_today(self):
        return datetime.utcnow().date()

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pushups = db.Column(db.Integer, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    comment = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
