from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime


Base = declarative_base()

# ---------------- Location Tables ----------------

class County(Base):
    __tablename__ = 'counties'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    constituencies = relationship('Constituency', back_populates='county')

class Constituency(Base):
    __tablename__ = 'constituencies'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    county_id = Column(Integer, ForeignKey('counties.id'))

    county = relationship('County', back_populates='constituencies')
    wards = relationship('Ward', back_populates='constituency')

class Ward(Base):
    __tablename__ = 'wards'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    constituency_id = Column(Integer, ForeignKey('constituencies.id'))

    constituency = relationship('Constituency', back_populates='wards')
    polling_stations = relationship('PollingStation', back_populates='ward')

class PollingStation(Base):
    __tablename__ = 'polling_stations'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    ward_id = Column(Integer, ForeignKey('wards.id'))

    ward = relationship('Ward', back_populates='polling_stations')
    voters = relationship('Voter', back_populates='polling_station')

# ---------------- User and Voting Tables ----------------

class Voter(Base):
    __tablename__ = 'voters'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    polling_station_id = Column(Integer, ForeignKey('polling_stations.id'))
    has_voted = Column(Boolean, default=False)

    polling_station = relationship('PollingStation', back_populates='voters')
    votes = relationship('Vote', back_populates='voter')

class Candidate(Base):
    __tablename__ = 'candidates'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    party = Column(String)
    position = Column(String)
    ward_id = Column(Integer, ForeignKey('wards.id'), nullable=True)

    votes = relationship('Vote', back_populates='candidate')

class Vote(Base):
    __tablename__ = 'votes'
    id = Column(Integer, primary_key=True)
    voter_id = Column(Integer, ForeignKey('voters.id'))
    candidate_id = Column(Integer, ForeignKey('candidates.id'))
    timestamp = Column(DateTime, default=datetime.utcnow)

    voter = relationship('Voter', back_populates='votes')
    candidate = relationship('Candidate', back_populates='votes')
