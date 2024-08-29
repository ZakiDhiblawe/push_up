from . import db
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
    __tablename__ = 'users'  # Ensure table name matches the SQL schema

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(200), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    reset_token = db.Column(db.String(100), nullable=True)
    profile_picture = db.Column(
        db.String(200), nullable=True, default='default.jpg')
    workouts = db.relationship('Workout', backref='author', lazy=True)

    def date_today(self):
        return datetime.utcnow().date()


class Workout(db.Model):
    __tablename__ = 'workouts'  # Ensure table name matches the SQL schema

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pushups = db.Column(db.Integer, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    comment = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
