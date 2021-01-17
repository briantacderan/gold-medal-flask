from datetime import datetime
from app import db


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), index=True, unique=True)
    code = db.Column(db.String(140), index=True, unique=True)
    population = db.Column(db.Integer, index=True)
    gdp = db.Column(db.Integer, index=True)
    medals = db.Column(db.Integer, index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    golds = db.relationship('Gold', backref='author', lazy='dynamic')
    sports = db.relationship('Sport', backref='author', lazy='dynamic')
    
    def __repr__(self):
        return '<Country {}>'.format(self.name)

    
class Gold(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, index=True)
    city = db.Column(db.String(140), index=True)
    sport = db.Column(db.String(140), index=True)
    discipline = db.Column(db.String(140), index=True)
    name = db.Column(db.String(140), index=True)
    country = db.Column(db.String(140), index=True)
    gender = db.Column(db.String(140), index=True)
    event = db.Column(db.String(140), index=True)
    season = db.Column(db.String(140), index=True)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return '<Gold {}>'.format(self.name)

    
class Sport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), index=True)
    count = db.Column(db.Integer, index=True)
    percent = db.Column(db.Integer, index=True)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return '<Sport {}>'.format(self.name)