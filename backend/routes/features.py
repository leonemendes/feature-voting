"""
Feature routes for the Feature Voting System.
This module defines the REST API endpoints for managing features.
"""

from flask import Blueprint, request, jsonify
from models.feature import Feature
from models.vote import Vote

features_bp = Blueprint('features', __name__)

@features_bp.route('/api/features', methods=['POST'])
def create_feature():
    """
    Create a new feature.
    
    Expected JSON payload:
    {
        "title": "Feature title (required)",
        "description": "Feature description (optional)"
    }
    
    Returns:
        JSON response with created feature data or error message
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        if not data.get('title'):
            return jsonify({'error': 'Title is required'}), 400
        
        if not data.get('title').strip():
            return jsonify({'error': 'Title cannot be empty'}), 400
        
        # Validate title length
        if len(data.get('title', '')) > 200:
            return jsonify({'error': 'Title too long (max 200 characters)'}), 400
        
        # Validate description length
        if len(data.get('description', '')) > 1000:
            return jsonify({'error': 'Description too long (max 1000 characters)'}), 400
        
        # Create new feature
        feature = Feature(
            title=data['title'].strip(),
            description=data.get('description', '').strip()
        )
        
        # Save to database
        if feature.save():
            # Return the created feature with vote count
            return jsonify({
                'id': feature.id,
                'title': feature.title,
                'description': feature.description,
                'created_at': feature.created_at,
                'updated_at': feature.updated_at,
                'vote_count': 0
            }), 201
        else:
            return jsonify({'error': 'Failed to create feature'}), 500
            
    except Exception as e:
        print(f"Error creating feature: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@features_bp.route('/api/features', methods=['GET'])
def get_features():
    """
    Get all features with their vote counts.
    
    Query parameters:
    - limit: Maximum number of features to return (optional)
    - offset: Number of features to skip (optional)
    
    Returns:
        JSON response with list of features and their vote counts
    """
    try:
        # Get query parameters
        limit = request.args.get('limit', type=int)
        offset = request.args.get('offset', type=int, default=0)
        
        # Get all features with vote counts
        features = Feature.get_all_with_votes()
        
        # Apply pagination if limit is specified
        if limit:
            features = features[offset:offset + limit]
        
        # Return features
        return jsonify({
            'features': features,
            'total_count': len(Feature.get_all_with_votes()),
            'returned_count': len(features)
        }), 200
        
    except Exception as e:
        print(f"Error getting features: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@features_bp.route('/api/features/<int:feature_id>', methods=['GET'])
def get_feature(feature_id):
    """
    Get a specific feature by ID.
    
    Args:
        feature_id (int): The ID of the feature to retrieve
        
    Returns:
        JSON response with feature data or error message
    """
    try:
        # Get feature by ID
        feature = Feature.get_by_id(feature_id)
        
        if not feature:
            return jsonify({'error': 'Feature not found'}), 404
        
        # Get vote count for this feature
        vote_count = Vote.get_vote_count(feature_id)
        
        # Return feature with vote count
        feature_data = feature.to_dict()
        feature_data['vote_count'] = vote_count
        
        return jsonify(feature_data), 200
        
    except Exception as e:
        print(f"Error getting feature: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@features_bp.route('/api/features/<int:feature_id>', methods=['DELETE'])
def delete_feature(feature_id):
    """
    Delete a feature and all its votes.
    
    Args:
        feature_id (int): The ID of the feature to delete
        
    Returns:
        JSON response with success/error message
    """
    try:
        # Check if feature exists
        feature = Feature.get_by_id(feature_id)
        if not feature:
            return jsonify({'error': 'Feature not found'}), 404
        
        # Delete feature
        if Feature.delete(feature_id):
            return jsonify({'message': 'Feature deleted successfully'}), 200
        else:
            return jsonify({'error': 'Failed to delete feature'}), 500
            
    except Exception as e:
        print(f"Error deleting feature: {e}")
        return jsonify({'error': 'Internal server error'}), 500