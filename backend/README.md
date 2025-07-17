# Feature Voting System Backend

A Flask-based REST API for managing feature requests and voting.

## Features

- Create and manage feature requests
- Vote for features (upvote only)
- SQLite database with migrations
- CORS enabled for frontend integration
- Comprehensive error handling
- Modular code structure

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python app.py
   ```

3. **Test the API:**
   ```bash
   curl http://localhost:5000/api/health
   ```

## API Endpoints

### Features
- `GET /api/features` - Get all features with vote counts
- `POST /api/features` - Create a new feature
- `GET /api/features/<id>` - Get a specific feature
- `DELETE /api/features/<id>` - Delete a feature

### Votes
- `POST /api/features/<id>/vote` - Vote for a feature
- `DELETE /api/features/<id>/vote` - Remove vote from a feature

### Users
- `GET /api/users/<user_id>/votes` - Get user's votes

### Utility
- `GET /api/health` - Health check
- `GET /api/stats` - Database statistics

## Environment Variables

- `FLASK_HOST` - Host to bind to (default: 0.0.0.0)
- `FLASK_PORT` - Port to run on (default: 5000)
- `FLASK_DEBUG` - Enable debug mode (default: False)
- `SECRET_KEY` - Flask secret key (default: dev key)

## Database

The application uses SQLite with automatic initialization. The database file `feature_voting.db` is created automatically when the app starts.

## Project Structure

```
backend/
├── app.py          # Main Flask application
├── routes.py       # API route definitions
├── models.py       # Database models (Feature, Vote)
├── db.py           # Database setup and utilities
├── requirements.txt # Python dependencies
└── README.md       # This file
```