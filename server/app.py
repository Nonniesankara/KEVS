#!/usr/bin/env python3

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db  
from models import County, Constituency, Ward, PollingStation, Voter, Candidate, Vote

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kevs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
# route for creating a voter (create)


#route for getting all the candidates  (Read)
@app.route('/candidates', methods=['GET'])
def get_candidates():
    candidates=Candidate.query.all()
    candidate_dict=[candidate.to_dict() for candidate in candidates] 




#route for getting a candidate by their id (Read)



#route for changing the value of the spoilt column in vote to be spoilt (PATCH)  


#route for counting votes to be displayed on by indivitual candidates.


if __name__ == '__main__':
    app.run(port=5555)