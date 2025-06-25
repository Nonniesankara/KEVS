from app import app, db
from models import County, Constituency, Ward, PollingStation, Voter, Candidate, Vote
from faker import Faker
import random

fake = Faker()

def seed_data():
    with app.app_context():
        # Clear existing data
        Vote.query.delete()
        Candidate.query.delete()
        Voter.query.delete()
        PollingStation.query.delete()
        Ward.query.delete()
        Constituency.query.delete()
        County.query.delete()

        db.session.commit()

        # --- Counties ---
        counties = []
        for _ in range(10):
            county = County(name=fake.city())
            db.session.add(county)
            counties.append(county)

        db.session.commit()

        # --- Constituencies ---
        constituencies = []
        for _ in range(10):
            county = random.choice(counties)
            constituency = Constituency(name=fake.city_suffix(), county=county)
            db.session.add(constituency)
            constituencies.append(constituency)

        db.session.commit()

        # ---Wards ---
        wards = []
        for _ in range(10):
            constituency = random.choice(constituencies)
            ward = Ward(name=fake.street_name(), constituency=constituency)
            db.session.add(ward)
            wards.append(ward)

        db.session.commit()

        # ---Polling Stations ---
        stations = []
        for _ in range(10):
            ward = random.choice(wards)
            station = PollingStation(name=fake.company(), ward=ward)
            db.session.add(station)
            stations.append(station)

        db.session.commit()

        # ---Voters ---
        voters = []
        for _ in range(10):
            station = random.choice(stations)
            voter = Voter(username=fake.unique.user_name(), polling_station=station)
            db.session.add(voter)
            voters.append(voter)

        db.session.commit()

        # ---Candidates ---
        candidates = []
        for _ in range(10):
            ward = random.choice(wards)
            candidate = Candidate(
                name=fake.name(),
                party=fake.company_suffix(),
                position=random.choice(["MCA", "MP", "Senator"]),
                ward_id=ward.id
            )
            db.session.add(candidate)
            candidates.append(candidate)

        db.session.commit()

        # ---Votes ---
        for _ in range(10):
            voter = random.choice(voters)
            candidate = random.choice(candidates)
            vote = Vote(voter=voter, candidate=candidate)
            db.session.add(vote)

        db.session.commit()
        print("Seeding complete!")

if __name__ == '__main__':
    seed_data()
