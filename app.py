from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Episode, Guest, Appearance
import os

app = Flask(__name__)
CORS(app)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return '<h1>The Late Show API</h1>'

# GET /episodes
@app.route('/episodes', methods=['GET'])
def get_episodes():
    episodes = Episode.query.all()
    episodes_data = [{
        'id': episode.id,
        'date': episode.date,
        'number': episode.number
    } for episode in episodes]
    
    return jsonify(episodes_data)

# GET /episodes/<int:id>
@app.route('/episodes/<int:id>', methods=['GET'])
def get_episode(id):
    episode = Episode.query.get(id)
    
    if not episode:
        return jsonify({'error': 'Episode not found'}), 404
    
    # Get appearances with guest details
    appearances_data = []
    for appearance in episode.appearances:
        appearances_data.append({
            'id': appearance.id,
            'rating': appearance.rating,
            'episode_id': appearance.episode_id,
            'guest_id': appearance.guest_id,
            'guest': {
                'id': appearance.guest.id,
                'name': appearance.guest.name,
                'occupation': appearance.guest.occupation
            }
        })
    
    episode_data = {
        'id': episode.id,
        'date': episode.date,
        'number': episode.number,
        'appearances': appearances_data
    }
    
    return jsonify(episode_data)

# GET /guests
@app.route('/guests', methods=['GET'])
def get_guests():
    guests = Guest.query.all()
    guests_data = [{
        'id': guest.id,
        'name': guest.name,
        'occupation': guest.occupation
    } for guest in guests]
    
    return jsonify(guests_data)

# POST /appearances
@app.route('/appearances', methods=['POST'])
def create_appearance():
    try:
        data = request.get_json()
        
        # Check if all required fields are present
        if not all(key in data for key in ['rating', 'episode_id', 'guest_id']):
            return jsonify({'errors': ['rating, episode_id, and guest_id are required']}), 400
        
        # Validate rating
        rating = data['rating']
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            return jsonify({'errors': ['rating must be an integer between 1 and 5']}), 400
        
        # Check if episode exists
        episode = Episode.query.get(data['episode_id'])
        if not episode:
            return jsonify({'errors': ['Episode not found']}), 404
        
        # Check if guest exists
        guest = Guest.query.get(data['guest_id'])
        if not guest:
            return jsonify({'errors': ['Guest not found']}), 404
        
        # Create new appearance
        appearance = Appearance(
            rating=data['rating'],
            episode_id=data['episode_id'],
            guest_id=data['guest_id']
        )
        
        db.session.add(appearance)
        db.session.commit()
        
        # Return the created appearance with nested episode and guest data
        appearance_data = {
            'id': appearance.id,
            'rating': appearance.rating,
            'episode_id': appearance.episode_id,
            'guest_id': appearance.guest_id,
            'episode': {
                'id': episode.id,
                'date': episode.date,
                'number': episode.number
            },
            'guest': {
                'id': guest.id,
                'name': guest.name,
                'occupation': guest.occupation
            }
        }
        
        return jsonify(appearance_data), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'errors': [str(e)]}), 400

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(port=5555, debug=True)