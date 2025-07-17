# Project: feature-voting

## Primary Language

Python

## Description

A Feature Voting System where users can:

- Post features
- Upvote existing features

## Requirements

- Backend API in Python (Flask)
- SQLite database
- React Native frontend for iOS and Android
- Use modular structure
- Provide a README with run instructions

## Backend Structure

The Flask backend is organized with a modular structure:

```
backend/
├── app.py              # Main Flask application
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── models/
│   ├── __init__.py
│   ├── database.py     # Database setup and utilities
│   ├── feature.py      # Feature model
│   └── vote.py         # Vote model
├── routes/
│   ├── __init__.py
│   ├── features.py     # Feature API endpoints
│   └── votes.py        # Vote API endpoints
├── utils/
│   ├── __init__.py
│   └── helpers.py      # Helper functions
└── data/
    └── feature_voting.db  # SQLite database (auto-created)
```

## Quick Start

### Setup (First Time)
```bash
./setup.sh
```

### Run Both Servers
```bash
./run.sh
```

## Development Commands

### Backend
```bash
cd backend
source venv/bin/activate
python app.py
```

### Frontend
```bash
cd frontend
npm start
```

### API Endpoints
- `POST /api/features` - Create new feature
- `GET /api/features` - Get all features with vote counts
- `GET /api/features/<id>` - Get specific feature
- `POST /api/features/<id>/vote` - Vote for feature
- `DELETE /api/features/<id>/vote` - Remove vote
- `GET /api/users/<user_id>/votes` - Get user's votes
- `GET /api/health` - Health check
- `GET /api/stats` - Database statistics

## Frontend Structure

The React Native frontend is organized as follows:

```
frontend/
├── App.js                    # Main app with navigation
├── components/
│   ├── FeatureList.js       # Feature list screen with voting
│   └── NewFeatureForm.js    # New feature creation form
├── services/
│   └── api.js               # API service using Axios
├── package.json             # Dependencies and scripts
├── app.json                 # Expo configuration
└── README.md                # Frontend setup instructions
```

### Manual Setup
If you prefer to set up manually:

**Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip wheel setuptools
pip install -r requirements.txt
python -c "from models.database import init_db; init_db()"
```

**Frontend:**
```bash
cd frontend
npm install
```

## Testing

The backend includes comprehensive unit and integration tests using pytest:

### Run Tests
```bash
cd backend
pip install -r requirements.txt
pytest
```

### Test Coverage
```bash
pytest --cov=. --cov-report=html
```

### Test Structure
```
tests/
├── conftest.py           # Test configuration and fixtures
├── unit/
│   ├── test_models.py   # Database model tests
│   └── test_api.py      # API endpoint tests
└── integration/
    └── test_full_workflow.py  # Full workflow tests
```

## Additional Instructions

- Every time I give you a prompt, append it to prompts.txt in the root folder:
  - The full prompt I sent
  - A short summary of your response
