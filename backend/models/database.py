"""
Database setup and migration utilities for the Feature Voting System.
This module handles SQLite database initialization and schema management.
"""

import sqlite3
import os
from config import Config

# Database configuration
DATABASE_NAME = 'feature_voting.db'
DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', DATABASE_NAME)

def get_db_connection():
    """
    Create and return a database connection with row factory for dict-like access.
    
    Returns:
        sqlite3.Connection: Database connection object
    """
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # This enables dict-like access to rows
    return conn

def init_db():
    """
    Initialize the database with required tables.
    This function creates the features and votes tables if they don't exist.
    """
    # Ensure data directory exists
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create features table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS features (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create votes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feature_id INTEGER NOT NULL,
            user_id TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (feature_id) REFERENCES features (id) ON DELETE CASCADE,
            UNIQUE(feature_id, user_id)
        )
    ''')
    
    # Create indexes for better performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_votes_feature_id ON votes(feature_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_votes_user_id ON votes(user_id)')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def migrate_database():
    """
    Run database migrations if needed.
    This function can be extended to handle schema updates.
    """
    # For now, we'll just ensure the database is initialized
    init_db()
    print("Database migrations completed!")

def reset_database():
    """
    Reset the database by dropping all tables and recreating them.
    WARNING: This will delete all data!
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Drop tables if they exist
    cursor.execute('DROP TABLE IF EXISTS votes')
    cursor.execute('DROP TABLE IF EXISTS features')
    
    conn.commit()
    conn.close()
    
    # Recreate tables
    init_db()
    print("Database reset completed!")

def get_database_stats():
    """
    Get basic statistics about the database.
    
    Returns:
        dict: Dictionary containing database statistics
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get feature count
    cursor.execute('SELECT COUNT(*) as count FROM features')
    feature_count = cursor.fetchone()['count']
    
    # Get vote count
    cursor.execute('SELECT COUNT(*) as count FROM votes')
    vote_count = cursor.fetchone()['count']
    
    # Get most voted feature
    cursor.execute('''
        SELECT f.title, COUNT(v.id) as vote_count
        FROM features f
        LEFT JOIN votes v ON f.id = v.feature_id
        GROUP BY f.id
        ORDER BY vote_count DESC
        LIMIT 1
    ''')
    top_feature = cursor.fetchone()
    
    conn.close()
    
    return {
        'total_features': feature_count,
        'total_votes': vote_count,
        'top_feature': dict(top_feature) if top_feature else None
    }

if __name__ == '__main__':
    # Initialize database when run directly
    init_db()