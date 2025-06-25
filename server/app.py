#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db  
from models import County, Constituency, Ward, PollingStation, Voter, Candidate, Vote

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kevs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

#------all the get requests for the ui layout----------

#route for getting all the candidates 
@app.route('/candidates', methods=['GET'])
def get_candidates():
    candidates = Candidate.query.all()
    return jsonify([candidate.to_dict() for candidate in candidates])

#getting all the constituencies
@app.route('/constituencies', methods=['GET'])
def get_constituencies():
    constituencies=Constituency.query.all()
    return jsonify([constituency.to_dict() for constituency in constituencies])

#getting all the counties
@app.route('/counties', methods=['GET'])
def get_counties():
    counties=County.query.all()
    return jsonify([county.to_dict() for county in counties ])

#getting all the polling stations
@app.route('/pollingstations', methods=['GET'])
def get_polling_stations():
    polling_stations=PollingStation.query.all()
    return jsonify([polling_station.to_dict() for polling_station in polling_stations])

#getting all the votes(maybe we can use this to count the total no, of votes + determaining spoilt votes)
@app.route('/votes', methods=['GET'])
def get_votes():
    votes= Vote.query.all()
    return jsonify([vote.to_dict() for vote in votes])

@app.route('/wards', methods=['GET'])
def get_wards():
    wards=Ward.query.all()
    return jsonify([ward.to_dict() for ward in wards])

#--------------------------------------------------------------
# route for changing the status of a vote
@app.route('/votes/<int:id>/spoil', methods=['PATCH'])
def spoil_vote(id):
    vote = Vote.query.get_or_404(id)
    vote.spoilt = True
    db.session.commit()
    return jsonify(vote.to_dict()), 200

#route for voting
@app.route('/vote', methods=['POST'])
def submit_vote():
    data = request.get_json()

    voter_id = data.get('voter_id')
    candidate_id = data.get('candidate_id')

    if not voter_id or not candidate_id:
        return jsonify({"error": "voter_id and candidate_id are required"}), 400

    voter = Voter.query.get(voter_id)
    if not voter:
        return jsonify({"error": "Voter not found"}), 404
    if voter.has_voted:
        return jsonify({"error": "Voter has already voted"}), 403

    candidate = Candidate.query.get(candidate_id)
    if not candidate:
        return jsonify({"error": "Candidate not found"}), 404

    vote = Vote(voter_id=voter_id, candidate_id=candidate_id, spoilt=False)
    voter.has_voted = True 

    db.session.add(vote)
    db.session.commit()

    return jsonify(vote.to_dict()), 201

#route for counting votes to be displayed on by indivitual candidates.
from flask import jsonify
from sqlalchemy import func

@app.route('/votes/count', methods=['GET'])
def count_votes():
    results = db.session.query(
        Candidate.id,
        Candidate.name,
        func.count(Vote.id).label('vote_count')
    ).join(Vote).filter(Vote.spoilt == False).group_by(Candidate.id).all()

    data = [
        {
            "candidate_id": r.id,
            "candidate_name": r.name,
            "vote_count": r.vote_count
        }
        for r in results
    ]

    return jsonify(data), 200



if __name__ == '__main__':
    app.run(port=5555)