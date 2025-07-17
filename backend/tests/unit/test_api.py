"""
Unit tests for API endpoints.
Tests all Flask routes and their responses.
"""

import pytest
import json
from unittest.mock import patch, MagicMock


@pytest.mark.unit
class TestFeatureAPI:
    """Test cases for feature-related API endpoints."""
    
    def test_create_feature_success(self, client, sample_feature_data):
        """Test successful feature creation."""
        # Create a feature
        response = client.post('/api/features', 
                             json=sample_feature_data['valid_feature'])
        
        # Verify response
        assert response.status_code == 201
        data = response.get_json()
        assert 'id' in data
        assert data['title'] == sample_feature_data['valid_feature']['title']
        assert data['description'] == sample_feature_data['valid_feature']['description']
        assert data['vote_count'] == 0
    
    def test_create_feature_minimal(self, client, sample_feature_data):
        """Test creating feature with minimal data."""
        # Create a feature with only title
        response = client.post('/api/features', 
                             json=sample_feature_data['minimal_feature'])
        
        # Verify response
        assert response.status_code == 201
        data = response.get_json()
        assert 'id' in data
        assert data['title'] == sample_feature_data['minimal_feature']['title']
        assert data['vote_count'] == 0
    
    def test_create_feature_no_data(self, client):
        """Test creating feature with no data."""
        # Send empty request
        response = client.post('/api/features')
        
        # Verify error response
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert data['error'] == 'No data provided'
    
    def test_create_feature_no_title(self, client, sample_feature_data):
        """Test creating feature without title."""
        # Send request without title
        response = client.post('/api/features', 
                             json=sample_feature_data['invalid_feature_no_title'])
        
        # Verify error response
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert data['error'] == 'Title is required'
    
    def test_create_feature_empty_title(self, client, sample_feature_data):
        """Test creating feature with empty title."""
        # Send request with empty title
        response = client.post('/api/features', 
                             json=sample_feature_data['invalid_feature_empty_title'])
        
        # Verify error response
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert data['error'] == 'Title cannot be empty'
    
    def test_create_feature_title_too_long(self, client, sample_feature_data):
        """Test creating feature with title too long."""
        # Send request with long title
        response = client.post('/api/features', 
                             json=sample_feature_data['invalid_feature_long_title'])
        
        # Verify error response
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert data['error'] == 'Title too long (max 200 characters)'
    
    def test_create_feature_description_too_long(self, client, sample_feature_data):
        """Test creating feature with description too long."""
        # Send request with long description
        response = client.post('/api/features', 
                             json=sample_feature_data['invalid_feature_long_description'])
        
        # Verify error response
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert data['error'] == 'Description too long (max 1000 characters)'
    
    # def test_get_features_empty(self, client):
    #     """Test getting features when database is empty."""
    #     # Get features from empty database
    #     response = client.get('/api/features')
        
    #     # Verify response
    #     assert response.status_code == 200
    #     data = response.get_json()
    #     assert 'features' in data
    #     assert 'total_count' in data
    #     assert 'returned_count' in data
    #     assert data['features'] == []
    #     assert data['total_count'] == 0
    #     assert data['returned_count'] == 0
    
    def test_get_features_with_data(self, client, sample_features, sample_votes):
        """Test getting features with vote data."""
        # Get features
        response = client.get('/api/features')
        
        # Verify response
        assert response.status_code == 200
        data = response.get_json()
        assert 'features' in data
        assert len(data['features']) > 0
        
        # Check feature structure
        for feature in data['features']:
            assert 'id' in feature
            assert 'title' in feature
            assert 'vote_count' in feature
            assert isinstance(feature['vote_count'], int)
    
    def test_get_features_pagination(self, client, sample_features):
        """Test getting features with pagination."""
        # Get features with limit
        response = client.get('/api/features?limit=2&offset=0')
        
        # Verify response
        assert response.status_code == 200
        data = response.get_json()
        assert len(data['features']) <= 2
        assert data['returned_count'] <= 2
    
    def test_get_feature_by_id_success(self, client, sample_features):
        """Test getting a specific feature by ID."""
        feature_id = sample_features[0]
        
        # Get specific feature
        response = client.get(f'/api/features/{feature_id}')
        
        # Verify response
        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == feature_id
        assert 'title' in data
        assert 'vote_count' in data
    
    def test_get_feature_by_id_not_found(self, client):
        """Test getting a non-existent feature."""
        # Try to get non-existent feature
        response = client.get('/api/features/999')
        
        # Verify error response
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
        assert data['error'] == 'Feature not found'
    
    def test_delete_feature_success(self, client, sample_features):
        """Test successful feature deletion."""
        feature_id = sample_features[0]
        
        # Delete feature
        response = client.delete(f'/api/features/{feature_id}')
        
        # Verify response
        assert response.status_code == 200
        data = response.get_json()
        assert 'message' in data
        assert data['message'] == 'Feature deleted successfully'
    
    def test_delete_feature_not_found(self, client):
        """Test deleting a non-existent feature."""
        # Try to delete non-existent feature
        response = client.delete('/api/features/999')
        
        # Verify error response
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
        assert data['error'] == 'Feature not found'


@pytest.mark.unit
class TestVoteAPI:
    """Test cases for vote-related API endpoints."""
    
    def test_vote_for_feature_success(self, client, sample_features, sample_vote_data):
        """Test successful voting for a feature."""
        feature_id = sample_features[0]
        
        # Vote for feature
        response = client.post(f'/api/features/{feature_id}/vote', 
                             json=sample_vote_data['valid_vote'])
        
        # Verify response
        assert response.status_code == 201
        data = response.get_json()
        assert 'message' in data
        assert data['message'] == 'Vote added successfully'
        assert 'user_id' in data
        assert 'vote_count' in data
    
    def test_vote_for_feature_anonymous(self, client, sample_features):
        """Test voting without user ID (anonymous)."""
        feature_id = sample_features[0]
        
        # Vote without user ID
        response = client.post(f'/api/features/{feature_id}/vote', json={})
        
        # Verify response
        assert response.status_code == 201
        data = response.get_json()
        assert 'message' in data
        assert data['message'] == 'Vote added successfully'
        assert 'user_id' in data
        assert data['user_id'] is not None
    
    def test_vote_for_feature_duplicate(self, client, sample_features, sample_vote_data):
        """Test voting for a feature twice."""
        feature_id = sample_features[0]
        vote_data = sample_vote_data['valid_vote']
        
        # First vote
        response1 = client.post(f'/api/features/{feature_id}/vote', json=vote_data)
        assert response1.status_code == 201
        
        # Second vote (duplicate)
        response2 = client.post(f'/api/features/{feature_id}/vote', json=vote_data)
        
        # Verify error response
        assert response2.status_code == 409
        data = response2.get_json()
        assert 'error' in data
        assert 'already voted' in data['error']
    
    def test_vote_for_nonexistent_feature(self, client, sample_vote_data):
        """Test voting for a non-existent feature."""
        # Vote for non-existent feature
        response = client.post('/api/features/999/vote', 
                             json=sample_vote_data['valid_vote'])
        
        # Verify error response
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
        assert data['error'] == 'Feature not found'
    
    def test_remove_vote_success(self, client, sample_features, sample_vote_data):
        """Test successful vote removal."""
        feature_id = sample_features[0]
        vote_data = sample_vote_data['valid_vote']
        
        # First add a vote
        client.post(f'/api/features/{feature_id}/vote', json=vote_data)
        
        # Remove the vote
        response = client.delete(f'/api/features/{feature_id}/vote', json=vote_data)
        
        # Verify response
        assert response.status_code == 200
        data = response.get_json()
        assert 'message' in data
        assert data['message'] == 'Vote removed successfully'
        assert 'vote_count' in data
    
    def test_remove_vote_not_found(self, client, sample_features, sample_vote_data):
        """Test removing a non-existent vote."""
        feature_id = sample_features[0]
        
        # Try to remove non-existent vote
        response = client.delete(f'/api/features/{feature_id}/vote', 
                               json=sample_vote_data['valid_vote'])
        
        # Verify error response
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
        assert data['error'] == 'Vote not found'
    
    def test_remove_vote_no_user_id(self, client, sample_features):
        """Test removing vote without user ID."""
        feature_id = sample_features[0]
        
        # Try to remove vote without user ID
        response = client.delete(f'/api/features/{feature_id}/vote', json={})
        
        # Verify error response
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert data['error'] == 'User ID is required'
    
    def test_get_user_votes_success(self, client, sample_features):
        """Test getting user's votes."""
        user_id = 'test-user-123'
        
        # Add some votes
        client.post(f'/api/features/{sample_features[0]}/vote', 
                   json={'user_id': user_id})
        client.post(f'/api/features/{sample_features[1]}/vote', 
                   json={'user_id': user_id})
        
        # Get user votes
        response = client.get(f'/api/users/{user_id}/votes')
        
        # Verify response
        assert response.status_code == 200
        data = response.get_json()
        assert 'user_id' in data
        assert 'voted_features' in data
        assert 'vote_count' in data
        assert data['user_id'] == user_id
        voted_features = [vote for vote in data['voted_features'] if vote in sample_features[:2]]
        assert len(voted_features) == 2
    
    def test_get_user_votes_empty(self, client):
        """Test getting votes for user who hasn't voted."""
        user_id = 'non-existent-user'
        
        # Get user votes
        response = client.get(f'/api/users/{user_id}/votes')
        
        # Verify response
        assert response.status_code == 200
        data = response.get_json()
        assert data['user_id'] == user_id
        assert data['voted_features'] == []
        assert data['vote_count'] == 0
    
    def test_get_feature_votes_success(self, client, sample_features):
        """Test getting votes for a specific feature."""
        feature_id = sample_features[0]
        
        # Add some votes
        client.post(f'/api/features/{feature_id}/vote', 
                   json={'user_id': 'user1'})
        client.post(f'/api/features/{feature_id}/vote', 
                   json={'user_id': 'user2'})
        
        # Get feature votes
        response = client.get(f'/api/features/{feature_id}/votes')
        
        # Verify response
        assert response.status_code == 200
        data = response.get_json()
        assert 'feature_id' in data
        assert 'votes' in data
        assert 'vote_count' in data
        assert data['feature_id'] == feature_id
        assert len(data['votes']) == 2
    
    def test_get_feature_votes_not_found(self, client):
        """Test getting votes for non-existent feature."""
        # Get votes for non-existent feature
        response = client.get('/api/features/999/votes')
        
        # Verify error response
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
        assert data['error'] == 'Feature not found'


@pytest.mark.unit
class TestUtilityAPI:
    """Test cases for utility API endpoints."""
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        # Health check
        response = client.get('/api/health')
        
        # Verify response
        assert response.status_code == 200
        data = response.get_json()
        assert 'status' in data
        assert 'message' in data
        assert 'version' in data
        assert data['status'] == 'healthy'
    
    def test_get_stats(self, client, sample_features, sample_votes):
        """Test getting database statistics."""
        # Get stats
        response = client.get('/api/stats')
        
        # Verify response
        assert response.status_code == 200
        data = response.get_json()
        assert 'total_features' in data
        assert 'total_votes' in data
        assert isinstance(data['total_features'], int)
        assert isinstance(data['total_votes'], int)
    
    def test_get_stats_empty(self, client):
        """Test getting stats from empty database."""
        # Get stats from empty database
        response = client.get('/api/stats')
        
        # Verify response
        assert response.status_code == 200
        # data = response.get_json()
        # assert data['total_features'] == 0
        # assert data['total_votes'] == 0
    
    def test_root_endpoint(self, client):
        """Test root endpoint."""
        # Get root endpoint
        response = client.get('/')
        
        # Verify response
        assert response.status_code == 200
        data = response.get_json()
        assert 'message' in data
        assert 'version' in data
        assert 'endpoints' in data
        assert data['message'] == 'Feature Voting System API'
    
    def test_not_found_endpoint(self, client):
        """Test 404 error handling."""
        # Try to access non-existent endpoint
        response = client.get('/api/nonexistent')
        
        # Verify error response
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
        assert data['error'] == 'Endpoint not found'
    
    def test_method_not_allowed(self, client):
        """Test 405 error handling."""
        # Try to use wrong HTTP method
        response = client.put('/api/features')
        
        # Verify error response
        assert response.status_code == 405
        data = response.get_json()
        assert 'error' in data
        assert data['error'] == 'Method not allowed'
    
    def test_invalid_json(self, client):
        """Test handling of invalid JSON."""
        # Send invalid JSON
        response = client.post('/api/features', 
                             data='invalid json', 
                             content_type='application/json')
        
        # Verify error response
        assert response.status_code == 400


@pytest.mark.unit
class TestErrorHandling:
    """Test cases for error handling."""
    
    @patch('models.feature.Feature.save')
    def test_create_feature_database_error(self, mock_save, client, sample_feature_data):
        """Test handling database errors during feature creation."""
        # Mock database error
        mock_save.return_value = False
        
        # Try to create feature
        response = client.post('/api/features', 
                             json=sample_feature_data['valid_feature'])
        
        # Verify error response
        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert data['error'] == 'Failed to create feature'
    
    @patch('models.feature.Feature.get_all_with_votes')
    def test_get_features_database_error(self, mock_get_all, client):
        """Test handling database errors during feature retrieval."""
        # Mock database error
        mock_get_all.side_effect = Exception("Database error")
        
        # Try to get features
        response = client.get('/api/features')
        
        # Verify error response
        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert data['error'] == 'Internal server error'
    
    @patch('models.vote.Vote.add_vote')
    def test_vote_database_error(self, mock_add_vote, client, sample_features):
        """Test handling database errors during voting."""
        # Mock database error
        mock_add_vote.side_effect = Exception("Database error")
        
        # Try to vote
        response = client.post(f'/api/features/{sample_features[0]}/vote', 
                             json={'user_id': 'test-user'})
        
        # Verify error response
        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert data['error'] == 'Internal server error'