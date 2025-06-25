from app import app, db
from models import Vote

with app.app_context():
    # Find all votes where spoilt is null
    votes_with_null = Vote.query.filter(Vote.spoilt == None).all()

    # Change spoilt to False for each
    for vote in votes_with_null:
        vote.spoilt = False

    db.session.commit()
    print("All null spoilt values updated to False.")
