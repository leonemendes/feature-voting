"""
Test configuration and fixtures for the Feature Voting System.
This module provides pytest fixtures and setup for testing the Flask backend.
"""

import pytest
import os
import tempfile
import sqlite3
from app import create_app
from models.database import init_db, get_db_connection


@pytest.fixture
def app():
    """
    Create and configure a test Flask app instance.
    
    Returns:
        Flask: Test Flask application instance
    """
    # Create a temporary database file
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    
    # Override the database path for testing
    original_db_path = os.environ.get('DATABASE_PATH')
    os.environ['DATABASE_PATH'] = db_path
    
    # Create the Flask app
    app = create_app()
    app.config.update({
        'TESTING': True,
        'DATABASE_PATH': db_path,
        'WTF_CSRF_ENABLED': False,
    })
    
    # Initialize the test database
    with app.app_context():
        init_db()
    
    yield app
    
    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)
    
    # Restore original database path
    if original_db_path:
        os.environ['DATABASE_PATH'] = original_db_path
    elif 'DATABASE_PATH' in os.environ:
        del os.environ['DATABASE_PATH']


@pytest.fixture
def client(app):
    """
    Create a test client for the Flask app.
    
    Args:
        app: Flask application instance
        
    Returns:
        FlaskClient: Test client for making HTTP requests
    """
    return app.test_client()


@pytest.fixture
def runner(app):
    """
    Create a test runner for the Flask app.
    
    Args:
        app: Flask application instance
        
    Returns:
        FlaskCliRunner: Test runner for CLI commands
    """
    return app.test_cli_runner()


@pytest.fixture
def db_connection(app):
    """
    Provide a database connection for testing.
    
    Args:
        app: Flask application instance
        
    Returns:
        sqlite3.Connection: Database connection
    """
    with app.app_context():
        conn = get_db_connection()
        yield conn
        conn.close()


@pytest.fixture
def sample_features(db_connection):
    """
    Create sample features for testing.
    
    Args:
        db_connection: Database connection
        
    Returns:
        list: List of created feature IDs
    """
    cursor = db_connection.cursor()
    
    # Insert sample features
    features = [
        ('Dark Mode', 'Add dark mode theme to the application'),
        ('User Authentication', 'Implement user login and registration'),
        ('Search Functionality', 'Add search feature for better navigation'),
        ('Mobile App', 'Create a mobile version of the application'),
        ('API Documentation', 'Provide comprehensive API documentation'),
    ]
    
    feature_ids = []
    for title, description in features:
        cursor.execute(
            'INSERT INTO features (title, description) VALUES (?, ?)',
            (title, description)
        )
        feature_ids.append(cursor.lastrowid)
    
    db_connection.commit()
    return feature_ids


@pytest.fixture
def sample_votes(db_connection, sample_features):
    """
    Create sample votes for testing.
    
    Args:
        db_connection: Database connection
        sample_features: List of feature IDs
        
    Returns:
        list: List of created vote data
    """
    cursor = db_connection.cursor()
    
    # Create sample votes
    votes = [
        (sample_features[0], 'user1'),  # Dark Mode - 1 vote
        (sample_features[1], 'user1'),  # User Authentication - 2 votes
        (sample_features[1], 'user2'),
        (sample_features[2], 'user1'),  # Search Functionality - 3 votes
        (sample_features[2], 'user2'),
        (sample_features[2], 'user3'),
    ]
    
    for feature_id, user_id in votes:
        cursor.execute(
            'INSERT INTO votes (feature_id, user_id) VALUES (?, ?)',
            (feature_id, user_id)
        )
    
    db_connection.commit()
    return votes


@pytest.fixture
def auth_headers():
    """
    Provide authentication headers for testing.
    
    Returns:
        dict: Headers for authenticated requests
    """
    return {
        'Content-Type': 'application/json',
        'X-User-ID': 'test-user-123'
    }


@pytest.fixture
def sample_feature_data():
    """
    Provide sample feature data for testing.
    
    Returns:
        dict: Sample feature data
    """
    return {
        'valid_feature': {
            'title': 'Test Feature',
            'description': 'This is a test feature for unit testing'
        },
        'minimal_feature': {
            'title': 'Minimal Feature'
        },
        'invalid_feature_no_title': {
            'description': 'Feature without title'
        },
        'invalid_feature_empty_title': {
            'title': '',
            'description': 'Feature with empty title'
        },
        'invalid_feature_long_title': {
            'title': 'A' * 201,  # Too long
            'description': 'Feature with very long title'
        },
        'invalid_feature_long_description': {
            'title': 'Valid Title',
            'description': 'B' * 1001  # Too long
        }
    }


@pytest.fixture
def sample_vote_data():
    """
    Provide sample vote data for testing.
    
    Returns:
        dict: Sample vote data
    """
    return {
        'valid_vote': {
            'user_id': 'test-user-456'
        },
        'anonymous_vote': {},
        'invalid_vote_empty_user': {
            'user_id': ''
        }
    }


class TestHelper:
    """
    Helper class for common testing operations.
    """
    
    @staticmethod
    def create_feature(client, feature_data):
        """
        Helper method to create a feature via API.
        
        Args:
            client: Test client
            feature_data: Feature data dictionary
            
        Returns:
            Response: API response
        """
        return client.post('/api/features', json=feature_data)
    
    @staticmethod
    def get_features(client):
        """
        Helper method to get all features via API.
        
        Args:
            client: Test client
            
        Returns:
            Response: API response
        """
        return client.get('/api/features')
    
    @staticmethod
    def vote_for_feature(client, feature_id, user_id=None):
        """
        Helper method to vote for a feature via API.
        
        Args:
            client: Test client
            feature_id: Feature ID to vote for
            user_id: User ID (optional)
            
        Returns:
            Response: API response
        """
        data = {'user_id': user_id} if user_id else {}
        return client.post(f'/api/features/{feature_id}/vote', json=data)
    
    @staticmethod
    def get_db_stats(db_connection):
        """
        Helper method to get database statistics.
        
        Args:
            db_connection: Database connection
            
        Returns:
            dict: Database statistics
        """
        cursor = db_connection.cursor()
        
        # Get feature count
        cursor.execute('SELECT COUNT(*) FROM features')
        feature_count = cursor.fetchone()[0]
        
        # Get vote count
        cursor.execute('SELECT COUNT(*) FROM votes')
        vote_count = cursor.fetchone()[0]
        
        return {
            'feature_count': feature_count,
            'vote_count': vote_count
        }


@pytest.fixture
def test_helper():
    """
    Provide the TestHelper class for testing.
    
    Returns:
        TestHelper: Helper class instance
    """
    return TestHelper()