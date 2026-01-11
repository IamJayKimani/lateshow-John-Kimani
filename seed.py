from app import app
from models import db, Episode, Guest, Appearance
import csv

def seed_database():
    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()
        print("Creating all tables...")
        db.create_all()
        
        print("Seeding episodes...")
        # Read episodes from CSV
        episodes = []
        with open('data/episodes.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                episode = Episode(
                    date=row['date'],
                    number=int(row['number'])
                )
                episodes.append(episode)
        
        db.session.add_all(episodes)
        db.session.commit()
        print(f"Added {len(episodes)} episodes")
        
        print("Seeding guests...")
        guests_data = [
            {"name": "Michael J. Fox", "occupation": "actor"},
            {"name": "Sandra Bernhard", "occupation": "Comedian"},
            {"name": "Tracey Ullman", "occupation": "television actress"},
            {"name": "John Malkovich", "occupation": "actor"},
            {"name": "David Letterman", "occupation": "talk show host"},
            {"name": "Julia Roberts", "occupation": "actress"},
            {"name": "Tom Hanks", "occupation": "actor"},
            {"name": "Madonna", "occupation": "singer"},
            {"name": "Robin Williams", "occupation": "comedian"},
            {"name": "Bill Murray", "occupation": "actor"}
        ]
        
        guests = []
        for guest_data in guests_data:
            guest = Guest(
                name=guest_data['name'],
                occupation=guest_data['occupation']
            )
            guests.append(guest)
        
        db.session.add_all(guests)
        db.session.commit()
        print(f"Added {len(guests)} guests")
        
        print("Seeding appearances...")
        appearances_data = [
            {"rating": 4, "episode_id": 1, "guest_id": 1},
            {"rating": 5, "episode_id": 1, "guest_id": 2},
            {"rating": 3, "episode_id": 2, "guest_id": 3},
            {"rating": 5, "episode_id": 2, "guest_id": 4},
            {"rating": 4, "episode_id": 3, "guest_id": 5},
            {"rating": 5, "episode_id": 3, "guest_id": 6},
            {"rating": 2, "episode_id": 4, "guest_id": 7},
            {"rating": 4, "episode_id": 4, "guest_id": 8},
            {"rating": 5, "episode_id": 5, "guest_id": 9},
            {"rating": 3, "episode_id": 5, "guest_id": 10}
        ]
        
        appearances = []
        for appearance_data in appearances_data:
            appearance = Appearance(
                rating=appearance_data['rating'],
                episode_id=appearance_data['episode_id'],
                guest_id=appearance_data['guest_id']
            )
            appearances.append(appearance)
        
        db.session.add_all(appearances)
        db.session.commit()
        print(f"Added {len(appearances)} appearances")
        
        print("Seeding complete!")

if __name__ == '__main__':
    seed_database()