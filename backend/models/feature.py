"""
Feature model for the Feature Voting System.
This module contains the Feature class that handles database operations for features.
"""

from models.database import get_db_connection
from datetime import datetime

class Feature:
    """
    Feature model representing a feature request that can be voted on.
    """
    
    def __init__(self, id=None, title=None, description=None, created_at=None, updated_at=None):
        self.id = id
        self.title = title
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at
    
    def save(self):
        """
        Save the feature to the database.
        Creates a new feature if id is None, otherwise updates existing feature.
        
        Returns:
            bool: True if save was successful, False otherwise
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            if self.id is None:
                # Create new feature
                cursor.execute('''
                    INSERT INTO features (title, description)
                    VALUES (?, ?)
                ''', (self.title, self.description))
                self.id = cursor.lastrowid
            else:
                # Update existing feature
                cursor.execute('''
                    UPDATE features 
                    SET title = ?, description = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (self.title, self.description, self.id))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error saving feature: {e}")
            return False
        finally:
            conn.close()
    
    @staticmethod
    def get_all_with_votes():
        """
        Get all features with their vote counts, ordered by vote count (descending).
        
        Returns:
            list: List of dictionaries containing feature data and vote counts
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                f.id,
                f.title,
                f.description,
                f.created_at,
                f.updated_at,
                COUNT(v.id) as vote_count
            FROM features f
            LEFT JOIN votes v ON f.id = v.feature_id
            GROUP BY f.id
            ORDER BY vote_count DESC, f.created_at DESC
        ''')
        
        features = cursor.fetchall()
        conn.close()
        
        return [dict(feature) for feature in features]
    
    @staticmethod
    def get_by_id(feature_id):
        """
        Get a feature by its ID.
        
        Args:
            feature_id (int): The ID of the feature to retrieve
            
        Returns:
            Feature: Feature object if found, None otherwise
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM features WHERE id = ?', (feature_id,))
        feature_data = cursor.fetchone()
        conn.close()
        
        if feature_data:
            return Feature(
                id=feature_data['id'],
                title=feature_data['title'],
                description=feature_data['description'],
                created_at=feature_data['created_at'],
                updated_at=feature_data['updated_at']
            )
        return None
    
    @staticmethod
    def delete(feature_id):
        """
        Delete a feature and all its votes.
        
        Args:
            feature_id (int): The ID of the feature to delete
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Delete associated votes first (cascading delete)
            cursor.execute('DELETE FROM votes WHERE feature_id = ?', (feature_id,))
            # Delete the feature
            cursor.execute('DELETE FROM features WHERE id = ?', (feature_id,))
            
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting feature: {e}")
            return False
        finally:
            conn.close()
    
    def to_dict(self):
        """
        Convert the feature to a dictionary for JSON serialization.
        
        Returns:
            dict: Feature data as dictionary
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }