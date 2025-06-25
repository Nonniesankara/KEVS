#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
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

#route for getting a candidate by their id (Read)

# route for creating a voter (create)

#route for changing the value of the spoilt column in vote to be spoilt (PATCH)  


#route for counting votes to be displayed on by indivitual candidates.


if __name__ == '__main__':
    app.run(port=5555)