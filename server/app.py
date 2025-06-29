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
    position = request.args.get('position')
    county_id = request.args.get('countyId', type=int)
    constituency_id = request.args.get('constituencyId', type=int)
    ward_id = request.args.get('wardId', type=int)

    query = Candidate.query

    if position:
        query = query.filter(Candidate.position == position)

    if position:
        pos = position.lower()
        if pos == 'president':
            # president not filtered
            pass
        elif pos in ['governor', 'senator']:
            if county_id:
                query = query.filter(Candidate.county_id == county_id)
        elif pos == 'mp':
            if constituency_id:
                query = query.filter(Candidate.constituency_id == constituency_id)
        elif pos == 'mca':
            if ward_id:
                query = query.filter(Candidate.ward_id == ward_id)
    else:
        # if no specific position, fallback location filtering
        if ward_id:
            query = query.filter(Candidate.ward_id == ward_id)
        elif constituency_id:
            query = query.filter(Candidate.constituency_id == constituency_id)
        elif county_id:
            query = query.filter(Candidate.county_id == county_id)

    candidates = query.all()
    return jsonify([c.to_dict() for c in candidates]), 200


@app.route('/candidates/grouped', methods=['GET'])
def get_candidates_grouped():
    candidates = Candidate.query.all()
    grouped = defaultdict(list)
    for c in candidates:
        grouped[c.position].append(c.to_dict())
    return jsonify(grouped), 200

@app.route('/constituencies/by_county/<int:county_id>', methods=['GET'])
def get_constituencies_by_county(county_id):
    constituencies = Constituency.query.filter_by(county_id=county_id).all()
    return jsonify([c.to_dict() for c in constituencies]), 200

@app.route('/counties', methods=['GET'])
def get_counties():
    counties = County.query.all()
    return jsonify([c.to_dict() for c in counties])

@app.route('/wards/by_constituency/<int:constituency_id>', methods=['GET'])
def get_wards_by_constituency(constituency_id):
    wards = Ward.query.filter_by(constituency_id=constituency_id).all()
    return jsonify([w.to_dict() for w in wards]), 200

@app.route('/pollingstations/by_ward/<int:ward_id>', methods=['GET'])
def get_pollingstations_by_ward(ward_id):
    stations = PollingStation.query.filter_by(ward_id=ward_id).all()
    return jsonify([s.to_dict() for s in stations]), 200

@app.route('/votes/count', methods=['GET'])
def count_votes():
    results = db.session.query(
        Candidate.id,
        Candidate.name,
        Candidate.position,
        Candidate.party,
        func.count(Vote.id).label('vote_count')
    ).outerjoin(Vote).filter(
        (Vote.spoilt == False) | (Vote.id == None)
    ).group_by(Candidate.id).all()

    return jsonify([
        {
            "candidate_id": r.id,
            "candidate_name": r.name,
            "position": r.position,
            "party": r.party,
            "vote_count": r.vote_count
        }
        for r in results
    ])

@app.route('/vote', methods=['POST'])
def submit_vote():
    data = request.get_json()
    voter_id = data.get('voter_id')
    candidate_ids = data.get('candidate_ids')

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


if __name__ == '__main__':
    app.run(port=5555)
