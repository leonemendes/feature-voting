"""
Vote model for the Feature Voting System.
This module contains the Vote class that handles database operations for votes.
"""

from models.database import get_db_connection
import uuid

from typing import Optional, List

class Vote:
    """
    Vote model representing a user's vote for a feature.
    """
    
    def __init__(self, id=None, feature_id=None, user_id=None, created_at=None):
        self.id = id
        self.feature_id = feature_id
        self.user_id = user_id
        self.created_at = created_at
    
    @staticmethod
    def add_vote(feature_id, user_id=None):
        """
        Add a vote for a feature.
        
        Args:
            feature_id (int): The ID of the feature to vote for
            user_id (str): The ID of the user voting (optional, generates UUID if None)
            
        Returns:
            dict: Result dictionary with success status and message
        """
        # Generate a user ID if not provided
        if user_id is None:
            user_id = str(uuid.uuid4())
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Check if feature exists
            cursor.execute('SELECT id FROM features WHERE id = ?', (feature_id,))
            if not cursor.fetchone():
                return {'success': False, 'message': 'Feature not found'}
            
            # Check if user has already voted
            cursor.execute('SELECT id FROM votes WHERE feature_id = ? AND user_id = ?', 
                         (feature_id, user_id))
            if cursor.fetchone():
                return {'success': False, 'message': 'User has already voted for this feature'}
            
            # Add the vote
            cursor.execute('''
                INSERT INTO votes (feature_id, user_id)
                VALUES (?, ?)
            ''', (feature_id, user_id))
            
            conn.commit()
            return {'success': True, 'message': 'Vote added successfully', 'user_id': user_id}
        
        except Exception as e:
            print(f"Error adding vote: {e}")
            return {'success': False, 'message': 'Error adding vote'}
        finally:
            conn.close()
    
    @staticmethod
    def remove_vote(feature_id, user_id):
        """
        Remove a vote for a feature.
        
        Args:
            feature_id (int): The ID of the feature
            user_id (str): The ID of the user
            
        Returns:
            dict: Result dictionary with success status and message
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM votes WHERE feature_id = ? AND user_id = ?', 
                         (feature_id, user_id))
            conn.commit()
            
            if cursor.rowcount > 0:
                return {'success': True, 'message': 'Vote removed successfully'}
            else:
                return {'success': False, 'message': 'Vote not found'}
        
        except Exception as e:
            print(f"Error removing vote: {e}")
            return {'success': False, 'message': 'Error removing vote'}
        finally:
            conn.close()
    
    @staticmethod
    def has_voted(feature_id, user_id):
        """
        Check if user has already voted for a feature.
        
        Args:
            feature_id (int): The ID of the feature
            user_id (str): The ID of the user
            
        Returns:
            bool: True if user has voted, False otherwise
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM votes WHERE feature_id = ? AND user_id = ?', 
                     (feature_id, user_id))
        result = cursor.fetchone()
        conn.close()
        
        return result is not None
    
    @staticmethod
    def get_user_votes(user_id: str) -> List[int]:
        """
        Get all votes by a specific user.
        
        Args:
            user_id (str): The ID of the user
            
        Returns:
            list: List of feature IDs the user has voted for
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT feature_id FROM votes WHERE user_id = ?', (user_id,))
        votes = cursor.fetchall()
        conn.close()
        
        return [vote['feature_id'] for vote in votes]     

    @staticmethod
    def get_vote_count(feature_id):
        """
        Get the vote count for a specific feature.
        
        Args:
            feature_id (int): The ID of the feature
            
        Returns:
            int: Number of votes for the feature
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) as count FROM votes WHERE feature_id = ?', (feature_id,))
        result = cursor.fetchone()
        conn.close()
        
        return result['count']
    
    @staticmethod
    def get_votes_by_feature(feature_id):
        """
        Get all votes for a specific feature.
        
        Args:
            feature_id (int): The ID of the feature
            
        Returns:
            list: List of dictionaries containing vote data
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM votes WHERE feature_id = ?', (feature_id,))
        votes = cursor.fetchall()
        conn.close()
        
        return [dict(vote) for vote in votes]