"""
Application models
"""

from src import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.BLOB)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('photos', lazy=True))

    def __repr__(self):
        return '<Photo %r>' % self.id
