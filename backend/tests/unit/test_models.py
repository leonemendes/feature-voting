"""
Unit tests for database models.
Tests the Feature and Vote models independently.
"""

import pytest
from models.feature import Feature
from models.vote import Vote
from models.database import get_db_connection


@pytest.mark.unit
class TestFeatureModel:
    """Test cases for the Feature model."""
    
    def test_feature_creation(self, app):
        """Test creating a new feature."""
        with app.app_context():
            # Create a new feature
            feature = Feature(
                title="Test Feature",
                description="This is a test feature"
            )
            
            # Verify initial state
            assert feature.title == "Test Feature"
            assert feature.description == "This is a test feature"
            assert feature.id is None
            
            # Save the feature
            result = feature.save()
            
            # Verify save was successful
            assert result is True
            assert feature.id is not None
            assert isinstance(feature.id, int)
    
    def test_feature_creation_minimal(self, app):
        """Test creating a feature with minimal data."""
        with app.app_context():
            # Create a feature with only title
            feature = Feature(title="Minimal Feature")
            
            # Save the feature
            result = feature.save()
            
            # Verify save was successful
            assert result is True
            assert feature.id is not None
            assert feature.title == "Minimal Feature"
            assert feature.description is None
    
    def test_feature_update(self, app):
        """Test updating an existing feature."""
        with app.app_context():
            # Create and save a feature
            feature = Feature(
                title="Original Title",
                description="Original description"
            )
            feature.save()
            original_id = feature.id
            
            # Update the feature
            feature.title = "Updated Title"
            feature.description = "Updated description"
            result = feature.save()
            
            # Verify update was successful
            assert result is True
            assert feature.id == original_id
            assert feature.title == "Updated Title"
            assert feature.description == "Updated description"
    
    def test_get_by_id(self, app):
        """Test retrieving a feature by ID."""
        with app.app_context():
            # Create and save a feature
            original_feature = Feature(
                title="Test Feature",
                description="Test description"
            )
            original_feature.save()
            feature_id = original_feature.id
            
            # Retrieve the feature
            retrieved_feature = Feature.get_by_id(feature_id)
            
            # Verify retrieval
            assert retrieved_feature is not None
            assert retrieved_feature.id == feature_id
            assert retrieved_feature.title == "Test Feature"
            assert retrieved_feature.description == "Test description"
    
    def test_get_by_id_not_found(self, app):
        """Test retrieving a non-existent feature."""
        with app.app_context():
            # Try to retrieve a non-existent feature
            feature = Feature.get_by_id(999)
            
            # Verify it returns None
            assert feature is None
    
    def test_get_all_with_votes(self, app, sample_features, sample_votes):
        """Test retrieving all features with vote counts."""
        with app.app_context():
            # Get all features with votes
            features = Feature.get_all_with_votes()
            
            # Verify we got features
            assert len(features) > 0
            
            # Check that features have vote counts
            for feature in features:
                assert 'vote_count' in feature
                assert isinstance(feature['vote_count'], int)
                assert feature['vote_count'] >= 0
            
            # Verify features are sorted by vote count (descending)
            vote_counts = [f['vote_count'] for f in features]
            assert vote_counts == sorted(vote_counts, reverse=True)
    
    def test_delete_feature(self, app):
        """Test deleting a feature."""
        with app.app_context():
            # Create and save a feature
            feature = Feature(title="Feature to Delete")
            feature.save()
            feature_id = feature.id
            
            # Delete the feature
            result = Feature.delete(feature_id)
            
            # Verify deletion
            assert result is True
            
            # Verify feature is gone
            deleted_feature = Feature.get_by_id(feature_id)
            assert deleted_feature is None
    
    def test_delete_feature_not_found(self, app):
        """Test deleting a non-existent feature."""
        with app.app_context():
            # Try to delete a non-existent feature
            result = Feature.delete(999)
            
            # Verify it returns False
            assert result is False
    
    def test_delete_feature_with_votes(self, app, db_connection):
        """Test deleting a feature that has votes."""
        with app.app_context():
            # Create a feature
            feature = Feature(title="Feature with Votes")
            feature.save()
            feature_id = feature.id
            
            # Add a vote
            Vote.add_vote(feature_id, "test-user")
            
            # Delete the feature
            result = Feature.delete(feature_id)
            
            # Verify deletion
            assert result is True
            
            # Verify feature is gone
            deleted_feature = Feature.get_by_id(feature_id)
            assert deleted_feature is None
            
            # Verify votes are also gone
            cursor = db_connection.cursor()
            cursor.execute('SELECT COUNT(*) FROM votes WHERE feature_id = ?', (feature_id,))
            vote_count = cursor.fetchone()[0]
            assert vote_count == 0
    
    def test_to_dict(self, app):
        """Test converting feature to dictionary."""
        with app.app_context():
            # Create and save a feature
            feature = Feature(
                title="Test Feature",
                description="Test description"
            )
            feature.save()
            
            # Convert to dictionary
            feature_dict = feature.to_dict()
            
            # Verify dictionary structure
            assert isinstance(feature_dict, dict)
            assert 'id' in feature_dict
            assert 'title' in feature_dict
            assert 'description' in feature_dict
            assert 'created_at' in feature_dict
            assert 'updated_at' in feature_dict
            
            # Verify values
            assert feature_dict['id'] == feature.id
            assert feature_dict['title'] == "Test Feature"
            assert feature_dict['description'] == "Test description"

    def test_get_all_with_votes_empty(self, app):
        """Test retrieving features when database is empty."""
        with app.app_context():
            # Get all features from empty database
            features = Feature.get_all_with_votes()
            for feature in features:
                Feature.delete(feature['id'])

            features = Feature.get_all_with_votes()
            
            # Verify empty list
            assert features == []

@pytest.mark.unit
class TestVoteModel:
    """Test cases for the Vote model."""
    
    def test_add_vote(self, app, sample_features):
        """Test adding a vote for a feature."""
        with app.app_context():
            feature_id = sample_features[0]
            user_id = "test-user-123"
            
            # Add a vote
            result = Vote.add_vote(feature_id, user_id)
            
            # Verify vote was added
            assert result['success'] is True
            assert result['message'] == 'Vote added successfully'
            assert result['user_id'] == user_id
    
    def test_add_vote_auto_user_id(self, app, sample_features):
        """Test adding a vote with auto-generated user ID."""
        with app.app_context():
            feature_id = sample_features[0]
            
            # Add a vote without user ID
            result = Vote.add_vote(feature_id)
            
            # Verify vote was added
            assert result['success'] is True
            assert result['message'] == 'Vote added successfully'
            assert 'user_id' in result
            assert result['user_id'] is not None
    
    def test_add_vote_duplicate(self, app, sample_features):
        """Test adding a duplicate vote."""
        with app.app_context():
            feature_id = sample_features[0]
            user_id = "test-user-123"
            
            # Add first vote
            result1 = Vote.add_vote(feature_id, user_id)
            assert result1['success'] is True
            
            # Try to add duplicate vote
            result2 = Vote.add_vote(feature_id, user_id)
            
            # Verify duplicate was rejected
            assert result2['success'] is False
            assert result2['message'] == 'User has already voted for this feature'
    
    def test_add_vote_nonexistent_feature(self, app):
        """Test adding a vote for a non-existent feature."""
        with app.app_context():
            # Try to vote for non-existent feature
            result = Vote.add_vote(999, "test-user")
            
            # Verify vote was rejected
            assert result['success'] is False
            assert result['message'] == 'Feature not found'
    
    def test_remove_vote(self, app, sample_features):
        """Test removing a vote."""
        with app.app_context():
            feature_id = sample_features[0]
            user_id = "test-user-123"
            
            # Add a vote first
            Vote.add_vote(feature_id, user_id)
            
            # Remove the vote
            result = Vote.remove_vote(feature_id, user_id)
            
            # Verify vote was removed
            assert result['success'] is True
            assert result['message'] == 'Vote removed successfully'
    
    def test_remove_vote_not_found(self, app, sample_features):
        """Test removing a non-existent vote."""
        with app.app_context():
            feature_id = sample_features[0]
            user_id = "test-user-123"
            
            # Try to remove non-existent vote
            result = Vote.remove_vote(feature_id, user_id)
            
            # Verify removal failed
            assert result['success'] is False
            assert result['message'] == 'Vote not found'
    
    def test_has_voted(self, app, sample_features):
        """Test checking if user has voted."""
        with app.app_context():
            feature_id = sample_features[0]
            user_id = "test-user-123"
            
            # Initially user hasn't voted
            assert Vote.has_voted(feature_id, user_id) is False
            
            # Add a vote
            Vote.add_vote(feature_id, user_id)
            
            # Now user has voted
            assert Vote.has_voted(feature_id, user_id) is True
    
    def test_get_user_votes(self, app, sample_features):
        """Test getting all votes by a user."""
        with app.app_context():
            user_id = "test-user-123"
            
            # Add votes for multiple features
            Vote.add_vote(sample_features[0], user_id)
            Vote.add_vote(sample_features[1], user_id)
            
            # Get user votes
            user_votes = Vote.get_user_votes(user_id)

            user_votes = [vote for vote in user_votes if vote in sample_features[:2]]
            
            # Verify user votes
            assert len(user_votes) == 2
            assert sample_features[0] in user_votes
            assert sample_features[1] in user_votes
    
    def test_get_user_votes_empty(self, app):
        """Test getting votes for user who hasn't voted."""
        with app.app_context():
            # Get votes for non-existent user
            user_votes = Vote.get_user_votes("non-existent-user")
            
            # Verify empty list
            assert user_votes == []
    
    def test_get_vote_count(self, app, sample_features):
        """Test getting vote count for a feature."""
        with app.app_context():
            feature_id = sample_features[0]
            
            # Initially no votes
            assert Vote.get_vote_count(feature_id) == 0
            
            # Add some votes
            Vote.add_vote(feature_id, "user1")
            Vote.add_vote(feature_id, "user2")
            Vote.add_vote(feature_id, "user3")
            
            # Check vote count
            assert Vote.get_vote_count(feature_id) == 3
    
    def test_get_votes_by_feature(self, app, sample_features):
        """Test getting all votes for a feature."""
        with app.app_context():
            feature_id = sample_features[0]
            
            # Add some votes
            Vote.add_vote(feature_id, "user1")
            Vote.add_vote(feature_id, "user2")
            
            # Get votes for feature
            votes = Vote.get_votes_by_feature(feature_id)
            
            # Verify votes
            assert len(votes) == 2
            
            # Check vote structure
            for vote in votes:
                assert 'id' in vote
                assert 'feature_id' in vote
                assert 'user_id' in vote
                assert 'created_at' in vote
                assert vote['feature_id'] == feature_id
    
    def test_get_votes_by_feature_empty(self, app, sample_features):
        """Test getting votes for feature with no votes."""
        with app.app_context():
            feature_id = sample_features[0]
            
            # Get votes for feature with no votes
            votes = Vote.get_votes_by_feature(feature_id)
            
            # Verify empty list
            assert votes == []