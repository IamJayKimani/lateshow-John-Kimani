# The Late Show API

A Flask API for managing episodes, guests, and appearances for "The Late Show" television program.

## Features

- RESTful API with JSON responses
- SQLite database with SQLAlchemy ORM
- Full CRUD operations for episodes, guests, and appearances
- Data validation and error handling
- CORS enabled for cross-origin requests

## Models

### Episode
- `id` (Integer, Primary Key)
- `date` (String) - Date of the episode
- `number` (Integer) - Episode number (unique)

### Guest
- `id` (Integer, Primary Key)
- `name` (String) - Name of the guest
- `occupation` (String) - Occupation of the guest

### Appearance
- `id` (Integer, Primary Key)
- `rating` (Integer) - Rating between 1-5
- `episode_id` (Integer, Foreign Key) - Reference to Episode
- `guest_id` (Integer, Foreign Key) - Reference to Guest

## Relationships

- An `Episode` has many `Guest`s through `Appearance`
- A `Guest` has many `Episode`s through `Appearance`
- An `Appearance` belongs to both an `Episode` and a `Guest`

## Validations

- `Appearance.rating` must be an integer between 1 and 5 (inclusive)

## API Endpoints

### GET /episodes
Returns a list of all episodes.

**Response:**
```json
[
  {
    "id": 1,
    "date": "1/11/99",
    "number": 1
  }
]