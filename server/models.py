from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ---------------- Location Tables ----------------

class County(db.Model):
    __tablename__ = 'counties'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    constituencies = db.relationship('Constituency', back_populates='county')
    candidates = db.relationship('Candidate', back_populates='county')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Constituency(db.Model):
    __tablename__ = 'constituencies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    county_id = db.Column(db.Integer, db.ForeignKey('counties.id'), nullable=False)

    county = db.relationship('County', back_populates='constituencies')
    wards = db.relationship('Ward', back_populates='constituency')
    candidates = db.relationship('Candidate', back_populates='constituency')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "county_id": self.county_id
        }

class Ward(db.Model):
    __tablename__ = 'wards'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    constituency_id = db.Column(db.Integer, db.ForeignKey('constituencies.id'), nullable=False)

    constituency = db.relationship('Constituency', back_populates='wards')
    polling_stations = db.relationship('PollingStation', back_populates='ward')
    candidates = db.relationship('Candidate', back_populates='ward')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "constituency_id": self.constituency_id
        }

class PollingStation(db.Model):
    __tablename__ = 'polling_stations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ward_id = db.Column(db.Integer, db.ForeignKey('wards.id'), nullable=False)

    ward = db.relationship('Ward', back_populates='polling_stations')
    voters = db.relationship('Voter', back_populates='polling_station')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "ward_id": self.ward_id
        }

# ---------------- User and Voting Tables ----------------

class Voter(db.Model):
    __tablename__ = 'voters'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    polling_station_id = db.Column(db.Integer, db.ForeignKey('polling_stations.id'), nullable=False)
    has_voted = db.Column(db.Boolean, default=False)

    polling_station = db.relationship('PollingStation', back_populates='voters')
    votes = db.relationship('Vote', back_populates='voter')

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "polling_station_id": self.polling_station_id,
            "has_voted": self.has_voted
        }

# ---------------- Candidate Table (with dynamic region support) ----------------

class Candidate(db.Model):
    __tablename__ = 'candidates'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    party = db.Column(db.String, nullable=False)
    position = db.Column(db.String, nullable=False)

    # Optional regional ties depending on position
    ward_id = db.Column(db.Integer, db.ForeignKey('wards.id'), nullable=True)
    constituency_id = db.Column(db.Integer, db.ForeignKey('constituencies.id'), nullable=True)
    county_id = db.Column(db.Integer, db.ForeignKey('counties.id'), nullable=True)

    ward = db.relationship('Ward', back_populates='candidates')
    constituency = db.relationship('Constituency', back_populates='candidates')
    county = db.relationship('County', back_populates='candidates')

    votes = db.relationship('Vote', back_populates='candidate')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "party": self.party,
            "position": self.position,
            "ward_id": self.ward_id,
            "constituency_id": self.constituency_id,
            "county_id": self.county_id
        }

# ---------------- Vote Table ----------------

class Vote(db.Model):
    __tablename__ = 'votes'
    id = db.Column(db.Integer, primary_key=True)
    voter_id = db.Column(db.Integer, db.ForeignKey('voters.id'), nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    spoilt = db.Column(db.Boolean, default=False, nullable=False)

    voter = db.relationship('Voter', back_populates='votes')
    candidate = db.relationship('Candidate', back_populates='votes')

    def to_dict(self):
        return {
            "id": self.id,
            "voter_id": self.voter_id,
            "candidate_id": self.candidate_id,
            "timestamp": self.timestamp,
            "spoilt": self.spoilt
        }
