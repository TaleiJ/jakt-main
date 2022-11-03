from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    contactNum = db.Column(db.Integer, index=True, unique=True, nullable=False)
    address = db.Column(db.String(100), index=True, nullable=False)

    comments = db.relationship('Comment', backref='user')
    event = db.relationship('Event', backref='user')


class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(500))
    image = db.Column(db.String(400))
    venue = db.Column(db.String(100))
    # double check time and date
    date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    genre = db.Column(db.String(20))
    status = db.Column(db.String(20))
    price = db.Column(db.Integer)
    tickets = db.Column(db.Integer)
    comment = db.relationship('Comment', backref='event')
    #FK's
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return "<Name: {}>",format(self.name)


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default = datetime.now())
    #FK's
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))

    def __repr(self):
        return "Comment: {}".format(self.text)

class Purchased(db.Model):
    __tablename__ = 'purchased'
    id = db.Column(db.Integer, primary_key = True)
    event = db.Column(db.String(500))
    image = db.Column(db.String(400))
    purchased_on = db.Column(db.DateTime, default = datetime.now())
    ticket_number = db.Column(db.Integer)
    #FK's
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
