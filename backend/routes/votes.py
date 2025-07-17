"""
Vote routes for the Feature Voting System.
This module defines the REST API endpoints for managing votes.
"""

from flask import Blueprint, request, jsonify
from models.vote import Vote
from models.feature import Feature
import uuid

votes_bp = Blueprint('votes', __name__)

@votes_bp.route('/api/features/<int:feature_id>/vote', methods=['POST'])
def vote_for_feature(feature_id):
    """
    Vote for a feature.
    
    Args:
        feature_id (int): The ID of the feature to vote for
        
    Expected JSON payload (optional):
    {
        "user_id": "User identifier (optional, will generate UUID if not provided)"
    }
    
    Returns:
        JSON response with success/error message
    """
    try:
        # Get user ID from request body or generate one
        data = request.get_json() or {}
        user_id = data.get('user_id')
        
        # If no user_id provided, generate one
        if not user_id:
            user_id = str(uuid.uuid4())
        
        # Add vote
        result = Vote.add_vote(feature_id, user_id)
        
        if result['success']:
            # Get updated vote count
            vote_count = Vote.get_vote_count(feature_id)
            
            return jsonify({
                'message': result['message'],
                'user_id': result['user_id'],
                'vote_count': vote_count
            }), 201
        else:
            # Determine appropriate HTTP status code
            if result['message'] == 'Feature not found':
                status_code = 404
            elif result['message'] == 'User has already voted for this feature':
                status_code = 409  # Conflict
            else:
                status_code = 400  # Bad request
            
            return jsonify({'error': result['message']}), status_code
            
    except Exception as e:
        print(f"Error voting for feature: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@votes_bp.route('/api/features/<int:feature_id>/vote', methods=['DELETE'])
def remove_vote_from_feature(feature_id):
    """
    Remove a vote from a feature.
    
    Args:
        feature_id (int): The ID of the feature to remove vote from
        
    Expected JSON payload:
    {
        "user_id": "User identifier (required)"
    }
    
    Returns:
        JSON response with success/error message
    """
    try:
        # Get user ID from request body
        data = request.get_json()
        
        if not data or not data.get('user_id'):
            return jsonify({'error': 'User ID is required'}), 400
        
        user_id = data['user_id']
        
        # Remove vote
        result = Vote.remove_vote(feature_id, user_id)
        
        if result['success']:
            # Get updated vote count
            vote_count = Vote.get_vote_count(feature_id)
            
            return jsonify({
                'message': result['message'],
                'vote_count': vote_count
            }), 200
        else:
            return jsonify({'error': result['message']}), 404
            
    except Exception as e:
        print(f"Error removing vote: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@votes_bp.route('/api/users/<user_id>/votes', methods=['GET'])
def get_user_votes(user_id):
    """
    Get all votes by a specific user.
    
    Args:
        user_id (str): The ID of the user
        
    Returns:
        JSON response with list of feature IDs the user has voted for
    """
    try:
        # Get user votes
        voted_features = Vote.get_user_votes(user_id)
        
        return jsonify({
            'user_id': user_id,
            'voted_features': voted_features,
            'vote_count': len(voted_features)
        }), 200
        
    except Exception as e:
        print(f"Error getting user votes: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@votes_bp.route('/api/features/<int:feature_id>/votes', methods=['GET'])
def get_feature_votes(feature_id):
    """
    Get all votes for a specific feature.
    
    Args:
        feature_id (int): The ID of the feature
        
    Returns:
        JSON response with list of votes for the feature
    """
    try:
        # Check if feature exists
        feature = Feature.get_by_id(feature_id)
        if not feature:
            return jsonify({'error': 'Feature not found'}), 404
        
        votes = Vote.get_votes_by_feature(feature_id)
        return jsonify({
            'feature_id': feature_id,
            'votes': votes,
            'vote_count': len(votes)
        }), 200
        
    except Exception as e:
        print(f"Error getting feature votes: {e}")
        return jsonify({'error': 'Internal server error'}), 500