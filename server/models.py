from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ---------------- Location Tables ----------------

class County(db.Model):
    __tablename__ = 'counties'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    constituencies = db.relationship('Constituency', back_populates='county')

class Constituency(db.Model):
    __tablename__ = 'constituencies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    county_id = db.Column(db.Integer, db.ForeignKey('counties.id'))

    county = db.relationship('County', back_populates='constituencies')
    wards = db.relationship('Ward', back_populates='constituency')

class Ward(db.Model):
    __tablename__ = 'wards'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    constituency_id = db.Column(db.Integer, db.ForeignKey('constituencies.id'))

    constituency = db.relationship('Constituency', back_populates='wards')
    polling_stations = db.relationship('PollingStation', back_populates='ward')

class PollingStation(db.Model):
    __tablename__ = 'polling_stations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ward_id = db.Column(db.Integer, db.ForeignKey('wards.id'))

    ward = db.relationship('Ward', back_populates='polling_stations')
    voters = db.relationship('Voter', back_populates='polling_station')

# ---------------- User and Voting Tables ----------------

class Voter(db.Model):
    __tablename__ = 'voters'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    polling_station_id = db.Column(db.Integer, db.ForeignKey('polling_stations.id'))
    has_voted = db.Column(db.Boolean, default=False)

    polling_station = db.relationship('PollingStation', back_populates='voters')
    votes = db.relationship('Vote', back_populates='voter')

class Candidate(db.Model):
    __tablename__ = 'candidates'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    party = db.Column(db.String)
    position = db.Column(db.String)
    ward_id = db.Column(db.Integer, db.ForeignKey('wards.id'), nullable=True)

    votes = db.relationship('Vote', back_populates='candidate')

class Vote(db.Model):
    __tablename__ = 'votes'
    id = db.Column(db.Integer, primary_key=True)
    voter_id = db.Column(db.Integer, db.ForeignKey('voters.id'))
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    voter = db.relationship('Voter', back_populates='votes')
    candidate = db.relationship('Candidate', back_populates='votes')
