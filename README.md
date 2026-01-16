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
  },
  {
    "id": 2,
    "date": "1/12/99",
    "number": 2
  }
]
```

### GET /episodes/:id
Returns details of a specific episode including its appearances.

**Parameters:**
- `id` (integer) - Episode ID

**Response (Success):**
```json
{
  "id": 1,
  "date": "1/11/99",
  "number": 1,
  "appearances": [
    {
      "id": 1,
      "rating": 4,
      "episode_id": 1,
      "guest_id": 1,
      "guest": {
        "id": 1,
        "name": "Michael J. Fox",
        "occupation": "actor"
      }
    }
  ]
}
```

**Response (Not Found):**
```json
{
  "error": "Episode not found"
}
```

### GET /guests
Returns a list of all guests.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Michael J. Fox",
    "occupation": "actor"
  },
  {
    "id": 2,
    "name": "Sandra Bernhard",
    "occupation": "Comedian"
  }
]
```

### POST /appearances
Creates a new appearance.

**Request Body:**
```json
{
  "rating": 5,
  "episode_id": 100,
  "guest_id": 123
}
```

**Response (Success):**
```json
{
  "id": 162,
  "rating": 5,
  "guest_id": 3,
  "episode_id": 2,
  "episode": {
    "date": "1/12/99",
    "id": 2,
    "number": 2
  },
  "guest": {
    "id": 3,
    "name": "Tracey Ullman",
    "occupation": "television actress"
  }
}
```

**Response (Validation Error):**
```json
{
  "errors": ["validation errors"]
}
```

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd lateshow-firstname-lastname
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```bash
   flask db upgrade
   python seed.py
   ```

5. Run the application:
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5555`.

## Testing

Import the provided Postman collection (`challenge-4-lateshow.postman_collection.json`) into Postman to test the endpoints.

## Technologies Used

- Flask
- SQLAlchemy
- Flask-Migrate
- Flask-CORS
- SQLite
