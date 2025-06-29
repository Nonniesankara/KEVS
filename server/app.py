#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, County, Constituency, Ward, PollingStation, Voter, Candidate, Vote
from sqlalchemy import func
from flask_cors import CORS
from collections import defaultdict
import os

app = Flask(__name__)

# ---------------- Configuration ----------------

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'instance', 'kevs.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

# ---------------- GET Routes ----------------

@app.route('/candidates', methods=['GET'])
def get_candidates():
    candidates = Candidate.query.all()
    return jsonify([candidate.to_dict() for candidate in candidates])

@app.route('/candidates/grouped', methods=['GET'])
def get_candidates_grouped():
    candidates = Candidate.query.all()
    grouped = defaultdict(list)
    for c in candidates:
        grouped[c.position].append(c.to_dict())
    return jsonify(grouped), 200

@app.route('/constituencies', methods=['GET'])
def get_constituencies():
    constituencies = Constituency.query.all()
    return jsonify([c.to_dict() for c in constituencies])

@app.route('/constituencies/by_county/<int:county_id>', methods=['GET'])
def get_constituencies_by_county(county_id):
    constituencies = Constituency.query.filter_by(county_id=county_id).all()
    return jsonify([c.to_dict() for c in constituencies]), 200

@app.route('/counties', methods=['GET'])
def get_counties():
    counties = County.query.all()
    return jsonify([c.to_dict() for c in counties])

@app.route('/wards', methods=['GET'])
def get_wards():
    wards = Ward.query.all()
    return jsonify([w.to_dict() for w in wards])

@app.route('/wards/by_constituency/<int:constituency_id>', methods=['GET'])
def get_wards_by_constituency(constituency_id):
    wards = Ward.query.filter_by(constituency_id=constituency_id).all()
    return jsonify([w.to_dict() for w in wards]), 200

@app.route('/pollingstations', methods=['GET'])
def get_polling_stations():
    stations = PollingStation.query.all()
    return jsonify([s.to_dict() for s in stations])

@app.route('/pollingstations/by_ward/<int:ward_id>', methods=['GET'])
def get_pollingstations_by_ward(ward_id):
    stations = PollingStation.query.filter_by(ward_id=ward_id).all()
    return jsonify([s.to_dict() for s in stations]), 200

@app.route('/votes', methods=['GET'])
def get_votes():
    votes = Vote.query.all()
    return jsonify([v.to_dict() for v in votes])

@app.route('/votes/count', methods=['GET'])
def count_votes():
    results = db.session.query(
        Candidate.id,
        Candidate.name,
        func.count(Vote.id).label('vote_count')
    ).join(Vote).filter(Vote.spoilt == False).group_by(Candidate.id).all()

    return jsonify([
        {
            "candidate_id": r.id,
            "candidate_name": r.name,
            "vote_count": r.vote_count
        }
        for r in results
    ])

@app.route('/voters', methods=['GET'])
def get_voters():
    voters = Voter.query.all()
    return jsonify([v.to_dict() for v in voters]), 200

# ---------------- PATCH & POST Routes ----------------

@app.route('/votes/<int:id>/spoil', methods=['PATCH'])
def spoil_vote(id):
    vote = Vote.query.get_or_404(id)
    vote.spoilt = True
    db.session.commit()
    return jsonify(vote.to_dict()), 200

@app.route('/vote', methods=['POST'])
def submit_vote():
    data = request.get_json()
    voter_id = data.get('voter_id')
    candidate_ids = data.get('candidate_ids')  # Expecting a list

    if not voter_id or not candidate_ids or not isinstance(candidate_ids, list):
        return jsonify({"error": "voter_id and candidate_ids (list) are required"}), 400

    voter = Voter.query.get(voter_id)
    if not voter:
        return jsonify({"error": "Voter not found"}), 404
    if voter.has_voted:
        return jsonify({"error": "Voter has already voted"}), 403

    for candidate_id in candidate_ids:
        candidate = Candidate.query.get(candidate_id)
        if not candidate:
            return jsonify({"error": f"Candidate with ID {candidate_id} not found"}), 404
        vote = Vote(voter_id=voter_id, candidate_id=candidate_id, spoilt=False)
        db.session.add(vote)

    voter.has_voted = True
    db.session.commit()

    return jsonify({"message": "All votes submitted successfully"}), 201

# ---------------- LOGIN Route ----------------

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    voter = Voter.query.filter_by(username=username).first()

    if voter and voter.password == password:
        return jsonify({
            "voter_id": voter.id,
            "username": voter.username,
            "has_voted": voter.has_voted
        }), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

# ---------------- Run Server ----------------

if __name__ == '__main__':
    app.run(port=5555)
