from app import app
from models import db, County, Constituency, Ward, PollingStation, Voter, Candidate, Vote
import json

with app.app_context():
    print("Clearing old data...")
    Vote.query.delete()
    Candidate.query.delete()
    Voter.query.delete()
    PollingStation.query.delete()
    Ward.query.delete()
    Constituency.query.delete()
    County.query.delete()

    print("Loading seed data...")
    with open('instance/kenya_voting_seed_data.json') as f:
        data = json.load(f)

    print("Seeding counties, constituencies, wards, and polling stations...")
    for c in data['counties']:
        county = County(name=c['name'])
        db.session.add(county)

        for con in c.get('constituencies', []):
            constituency = Constituency(name=con['name'], county=county)
            db.session.add(constituency)

            for w in con.get('wards', []):
                ward = Ward(name=w['name'], constituency=constituency)
                db.session.add(ward)

                for ps in w.get('polling_stations', []):
                    station = PollingStation(name=ps['name'], ward=ward)
                    db.session.add(station)

    db.session.commit()
    print("✅ Done seeding counties, constituencies, wards, and polling stations.")

    print("Seeding candidates...")
    for cand in data['candidates']:
        name = cand['name']
        party = cand['party']
        position = cand['position']

        # Optional location
        ward = cand.get('ward')
        constituency = cand.get('constituency')
        county = cand.get('county')

        candidate = Candidate(
            name=name,
            party=party,
            position=position
        )

        if ward:
            w = Ward.query.filter_by(name=ward).first()
            if w:
                candidate.ward_id = w.id
            else:
                print(f"⚠️ Ward '{ward}' not found for candidate {name}")
        elif constituency:
            con = Constituency.query.filter_by(name=constituency).first()
            if con:
                candidate.constituency_id = con.id
            else:
                print(f"⚠️ Constituency '{constituency}' not found for candidate {name}")
        elif county:
            co = County.query.filter_by(name=county).first()
            if co:
                candidate.county_id = co.id
            else:
                print(f"⚠️ County '{county}' not found for candidate {name}")

        db.session.add(candidate)

    db.session.commit()
    print("✅ Done seeding candidates.")

    print("Seeding voters...")
    voters_data = data.get("voters", [])
    print(f"Found {len(voters_data)} voters in JSON.")

    for v in voters_data:
        username = v["username"]
        password = v["password"]
        ps_name = v.get("polling_station")

        if ps_name:
            polling_station = PollingStation.query.filter_by(name=ps_name).first()
            if polling_station:
                voter = Voter(
                    username=username,
                    password=password,
                    polling_station_id=polling_station.id
                )
                db.session.add(voter)
                print(f"✅ Added voter {username} assigned to polling station '{ps_name}'")
            else:
                print(f"⚠️ Polling station '{ps_name}' not found for voter '{username}'. Skipping this voter.")
        else:
            print(f"⚠️ No polling station provided for voter '{username}'. Skipping this voter.")

    db.session.commit()
    print("✅ Done seeding voters.")
