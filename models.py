from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import MetaData

# Naming convention for constraints
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)

class Episode(db.Model):
    __tablename__ = 'episodes'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer, nullable=False, unique=True)
    
    # Relationships
    appearances = db.relationship('Appearance', back_populates='episode', cascade='all, delete-orphan')
    guests = db.relationship('Guest', secondary='appearances', back_populates='episodes')
    
    def to_dict(self, include_appearances=False):
        data = {
            'id': self.id,
            'date': self.date,
            'number': self.number
        }
        
        if include_appearances:
            data['appearances'] = [appearance.to_dict() for appearance in self.appearances]
            
        return data

class Guest(db.Model):
    __tablename__ = 'guests'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    occupation = db.Column(db.String, nullable=False)
    
    # Relationships
    appearances = db.relationship('Appearance', back_populates='guest', cascade='all, delete-orphan')
    episodes = db.relationship('Episode', secondary='appearances', back_populates='guests')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'occupation': self.occupation
        }

class Appearance(db.Model):
    __tablename__ = 'appearances'
    
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    
    # Foreign keys
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable=False)
    
    # Relationships
    episode = db.relationship('Episode', back_populates='appearances')
    guest = db.relationship('Guest', back_populates='appearances')
    
    # Validations
    @validates('rating')
    def validate_rating(self, key, rating):
        if not isinstance(rating, int):
            raise ValueError('Rating must be an integer')
        if rating < 1 or rating > 5:
            raise ValueError('Rating must be between 1 and 5')
        return rating
    
    def to_dict(self):
        return {
            'id': self.id,
            'rating': self.rating,
            'episode_id': self.episode_id,
            'guest_id': self.guest_id,
            'episode': {
                'id': self.episode.id,
                'date': self.episode.date,
                'number': self.episode.number
            } if self.episode else None,
            'guest': {
                'id': self.guest.id,
                'name': self.guest.name,
                'occupation': self.guest.occupation
            } if self.guest else None
        }