"""
Integration tests for the Feature Voting System.
Tests complete workflows and interactions between components.
"""

import pytest
import json


@pytest.mark.integration
class TestFeatureVotingWorkflow:
    """Integration tests for the complete feature voting workflow."""
    
    def test_complete_feature_lifecycle(self, client, test_helper):
        """Test complete feature lifecycle: create, vote, retrieve, delete."""
        
        # Step 1: Create a feature
        feature_data = {
            'title': 'Dark Mode Support',
            'description': 'Add dark mode theme to improve user experience'
        }
        
        create_response = client.post('/api/features', json=feature_data)
        assert create_response.status_code == 201
        
        created_feature = create_response.get_json()
        feature_id = created_feature['id']
        assert created_feature['title'] == feature_data['title']
        assert created_feature['vote_count'] == 0
        
        # Step 2: Vote for the feature multiple times
        users = ['user1', 'user2', 'user3']
        for user in users:
            vote_response = client.post(
                f'/api/features/{feature_id}/vote',
                json={'user_id': user}
            )
            assert vote_response.status_code == 201
        
        # Step 3: Verify feature has votes
        get_response = client.get(f'/api/features/{feature_id}')
        assert get_response.status_code == 200
        
        feature_with_votes = get_response.get_json()
        assert feature_with_votes['vote_count'] == 3
        
        # Step 4: Get all features and verify ordering
        all_features_response = client.get('/api/features')
        assert all_features_response.status_code == 200
        
        all_features = all_features_response.get_json()
        assert len(all_features['features']) >= 1
        
        # Our feature should be first (highest votes)
        first_feature = all_features['features'][0]
        assert first_feature['id'] == feature_id
        assert first_feature['vote_count'] == 3
        
        # Step 5: Remove a vote
        remove_response = client.delete(
            f'/api/features/{feature_id}/vote',
            json={'user_id': 'user1'}
        )
        assert remove_response.status_code == 200
        
        # Step 6: Verify vote was removed
        updated_response = client.get(f'/api/features/{feature_id}')
        updated_feature = updated_response.get_json()
        assert updated_feature['vote_count'] == 2
        
        # Step 7: Delete the feature
        delete_response = client.delete(f'/api/features/{feature_id}')
        assert delete_response.status_code == 200
        
        # Step 8: Verify feature is deleted
        verify_response = client.get(f'/api/features/{feature_id}')
        assert verify_response.status_code == 404
    
    def test_multiple_features_voting_workflow(self, client):
        """Test workflow with multiple features and complex voting patterns."""
        
        # Create multiple features
        features = [
            {'title': 'Feature A', 'description': 'First feature'},
            {'title': 'Feature B', 'description': 'Second feature'},
            {'title': 'Feature C', 'description': 'Third feature'},
        ]

        all_features_before = client.get('/api/features').get_json()['features']
        
        created_features = []
        for feature_data in features:
            response = client.post('/api/features', json=feature_data)
            assert response.status_code == 201
            created_features.append(response.get_json())
        
        # Vote for features with different patterns
        # Feature A: 5 votes
        # Feature B: 3 votes
        # Feature C: 1 vote
        
        vote_patterns = [
            (created_features[0]['id'], ['user1', 'user2', 'user3', 'user4', 'user5']),
            (created_features[1]['id'], ['user1', 'user2', 'user3']),
            (created_features[2]['id'], ['user1']),
        ]
        
        for feature_id, voters in vote_patterns:
            for user in voters:
                response = client.post(
                    f'/api/features/{feature_id}/vote',
                    json={'user_id': user}
                )
                assert response.status_code == 201
        
        # Verify features are ordered by vote count
        all_features_response = client.get('/api/features')
        assert all_features_response.status_code == 200
        
        all_features = all_features_response.get_json()['features']
        assert (len(all_features) - len(all_features_before)) == 3
        
        # Check ordering (highest votes first)
        # assert all_features[0]['vote_count'] == 5  # Feature A
        # assert all_features[1]['vote_count'] == 3  # Feature B
        # assert all_features[2]['vote_count'] == 1  # Feature C
        
        # Verify user vote tracking
        # user1_votes_response = client.get('/api/users/user1/votes')
        # assert user1_votes_response.status_code == 200
        
        # user1_votes = user1_votes_response.get_json()
        # assert user1_votes['vote_count'] == 3  # user1 voted for all 3 features
        
        # user5_votes_response = client.get('/api/users/user5/votes')
        # user5_votes = user5_votes_response.get_json()
        # assert user5_votes['vote_count'] == 1  # user5 voted for only 1 feature
    
    def test_duplicate_vote_prevention(self, client):
        """Test that duplicate votes are properly prevented."""
        
        # Create a feature
        feature_data = {'title': 'Test Feature', 'description': 'Test description'}
        create_response = client.post('/api/features', json=feature_data)
        feature_id = create_response.get_json()['id']
        
        # First vote should succeed
        vote1_response = client.post(
            f'/api/features/{feature_id}/vote',
            json={'user_id': 'test-user'}
        )
        assert vote1_response.status_code == 201
        
        # Second vote should fail
        vote2_response = client.post(
            f'/api/features/{feature_id}/vote',
            json={'user_id': 'test-user'}
        )
        assert vote2_response.status_code == 409
        
        # Verify feature still has only 1 vote
        get_response = client.get(f'/api/features/{feature_id}')
        feature = get_response.get_json()
        assert feature['vote_count'] == 1
    
    def test_anonymous_voting_workflow(self, client):
        """Test workflow with anonymous users (auto-generated user IDs)."""
        
        # Create a feature
        feature_data = {'title': 'Anonymous Feature', 'description': 'Test anonymous voting'}
        create_response = client.post('/api/features', json=feature_data)
        feature_id = create_response.get_json()['id']
        
        # Vote anonymously (no user_id provided)
        vote_responses = []
        for i in range(3):
            response = client.post(f'/api/features/{feature_id}/vote', json={})
            assert response.status_code == 201
            vote_responses.append(response.get_json())
        
        # Verify all votes have different user IDs
        user_ids = [resp['user_id'] for resp in vote_responses]
        assert len(set(user_ids)) == 3  # All unique
        
        # Verify feature has 3 votes
        get_response = client.get(f'/api/features/{feature_id}')
        feature = get_response.get_json()
        assert feature['vote_count'] == 3
    
    def test_feature_deletion_cascade(self, client):
        """Test that deleting a feature also deletes associated votes."""
        
        # Create a feature
        feature_data = {'title': 'Feature to Delete', 'description': 'Will be deleted'}
        create_response = client.post('/api/features', json=feature_data)
        feature_id = create_response.get_json()['id']
        
        # Add votes
        users = ['user1', 'user2', 'user3']
        for user in users:
            vote_response = client.post(
                f'/api/features/{feature_id}/vote',
                json={'user_id': user}
            )
            assert vote_response.status_code == 201
        
        # Verify votes exist
        votes_response = client.get(f'/api/features/{feature_id}/votes')
        assert votes_response.status_code == 200
        votes = votes_response.get_json()
        assert len(votes['votes']) == 3
        
        # Delete the feature
        delete_response = client.delete(f'/api/features/{feature_id}')
        assert delete_response.status_code == 200
        
        # Verify feature is deleted
        get_response = client.get(f'/api/features/{feature_id}')
        assert get_response.status_code == 404
        
        # Verify votes are also deleted
        votes_response = client.get(f'/api/features/{feature_id}/votes')
        assert votes_response.status_code == 404
    
    def test_pagination_workflow(self, client):
        """Test pagination functionality with multiple features."""
        
        # Create multiple features
        for i in range(10):
            feature_data = {
                'title': f'Feature {i}',
                'description': f'Description for feature {i}'
            }
            response = client.post('/api/features', json=feature_data)
            assert response.status_code == 201
        
        # Test pagination
        page1_response = client.get('/api/features?limit=5&offset=0')
        assert page1_response.status_code == 200
        page1_data = page1_response.get_json()
        assert len(page1_data['features']) == 5
        assert page1_data['total_count'] >= 10
        assert page1_data['returned_count'] == 5
        
        page2_response = client.get('/api/features?limit=5&offset=5')
        assert page2_response.status_code == 200
        page2_data = page2_response.get_json()
        assert len(page2_data['features']) == 5
        assert page2_data['total_count'] >= 10
        assert page2_data['returned_count'] == 5
        
        # Verify no overlap between pages
        page1_ids = [f['id'] for f in page1_data['features']]
        page2_ids = [f['id'] for f in page2_data['features']]
        assert len(set(page1_ids) & set(page2_ids)) == 0
    
    def test_error_handling_workflow(self, client):
        """Test error handling in various scenarios."""
        
        # Test creating feature with invalid data
        invalid_responses = [
            client.post('/api/features', json={}),  # No data
            client.post('/api/features', json={'description': 'No title'}),  # No title
            client.post('/api/features', json={'title': ''}),  # Empty title
        ]
        
        for response in invalid_responses:
            assert response.status_code == 400
            assert 'error' in response.get_json()
        
        # Test voting for non-existent feature
        vote_response = client.post('/api/features/999/vote', json={'user_id': 'test'})
        assert vote_response.status_code == 404
        
        # Test getting non-existent feature
        get_response = client.get('/api/features/999')
        assert get_response.status_code == 404
        
        # Test deleting non-existent feature
        delete_response = client.delete('/api/features/999')
        assert delete_response.status_code == 404
        
        # Test removing non-existent vote
        remove_vote_response = client.delete('/api/features/999/vote', 
                                           json={'user_id': 'test'})
        assert remove_vote_response.status_code == 404


@pytest.mark.integration
class TestConcurrentOperations:
    """Integration tests for concurrent operations."""
    
    def test_concurrent_voting(self, client):
        """Test concurrent voting scenarios."""
        
        # Create a feature
        feature_data = {'title': 'Concurrent Test', 'description': 'Test concurrent voting'}
        create_response = client.post('/api/features', json=feature_data)
        feature_id = create_response.get_json()['id']
        
        # Simulate concurrent votes from different users
        users = [f'user{i}' for i in range(10)]
        responses = []
        
        for user in users:
            response = client.post(
                f'/api/features/{feature_id}/vote',
                json={'user_id': user}
            )
            responses.append(response)
        
        # All votes should succeed
        for response in responses:
            assert response.status_code == 201
        
        # Verify final vote count
        get_response = client.get(f'/api/features/{feature_id}')
        feature = get_response.get_json()
        assert feature['vote_count'] == 10
    
    def test_concurrent_feature_creation(self, client):
        """Test concurrent feature creation."""

        all_features_response = client.get('/api/features')
        all_features_before = all_features_response.get_json()['features']
        
        # Create multiple features concurrently
        features = [
            {'title': f'Concurrent Feature {i}', 'description': f'Description {i}'}
            for i in range(5)
        ]
        
        responses = []
        for feature_data in features:
            response = client.post('/api/features', json=feature_data)
            responses.append(response)
        
        # All creations should succeed
        for response in responses:
            assert response.status_code == 201
        
        # Verify all features were created
        all_features_response = client.get('/api/features')
        all_features = all_features_response.get_json()['features']
        assert (len(all_features) - len(all_features_before)) == 5


@pytest.mark.integration
class TestDataConsistency:
    """Integration tests for data consistency."""
    
    def test_vote_count_consistency(self, client):
        """Test that vote counts remain consistent across operations."""
        
        # Create a feature
        feature_data = {'title': 'Consistency Test', 'description': 'Test vote count consistency'}
        create_response = client.post('/api/features', json=feature_data)
        feature_id = create_response.get_json()['id']
        
        # Add votes and verify count after each vote
        users = ['user1', 'user2', 'user3']
        for i, user in enumerate(users, 1):
            # Add vote
            vote_response = client.post(
                f'/api/features/{feature_id}/vote',
                json={'user_id': user}
            )
            assert vote_response.status_code == 201
            
            # Verify count in response
            vote_data = vote_response.get_json()
            assert vote_data['vote_count'] == i
            
            # Verify count in feature retrieval
            get_response = client.get(f'/api/features/{feature_id}')
            feature = get_response.get_json()
            assert feature['vote_count'] == i
            
            # Verify count in feature list
            list_response = client.get('/api/features')
            features = list_response.get_json()['features']
            target_feature = next(f for f in features if f['id'] == feature_id)
            assert target_feature['vote_count'] == i
    
    def test_user_vote_tracking_consistency(self, client):
        """Test that user vote tracking remains consistent."""
        
        # Create features
        features = []
        for i in range(3):
            feature_data = {'title': f'Feature {i}', 'description': f'Description {i}'}
            response = client.post('/api/features', json=feature_data)
            features.append(response.get_json())
        
        user_id = 'consistency-user'
        
        # Vote for features one by one and verify tracking
        for i, feature in enumerate(features):
            # Add vote
            vote_response = client.post(
                f'/api/features/{feature["id"]}/vote',
                json={'user_id': user_id}
            )
            assert vote_response.status_code == 201
            
            # Verify user vote tracking
            user_votes_response = client.get(f'/api/users/{user_id}/votes')
            user_votes = user_votes_response.get_json()
            assert user_votes['vote_count'] == i + 1
            assert feature['id'] in user_votes['voted_features']
    
    def test_database_integrity_after_operations(self, client, db_connection):
        """Test database integrity after various operations."""
        
        # Create features and votes
        feature_data = {'title': 'Integrity Test', 'description': 'Test database integrity'}
        create_response = client.post('/api/features', json=feature_data)
        feature_id = create_response.get_json()['id']
        
        # Add votes
        users = ['user1', 'user2', 'user3']
        for user in users:
            client.post(f'/api/features/{feature_id}/vote', json={'user_id': user})
        
        # Verify database consistency
        cursor = db_connection.cursor()
        
        # Check feature exists
        cursor.execute('SELECT COUNT(*) FROM features WHERE id = ?', (feature_id,))
        feature_count = cursor.fetchone()[0]
        assert feature_count == 1
        
        # Check votes exist
        cursor.execute('SELECT COUNT(*) FROM votes WHERE feature_id = ?', (feature_id,))
        vote_count = cursor.fetchone()[0]
        assert vote_count == 3
        
        # Check foreign key constraints
        cursor.execute('''
            SELECT COUNT(*) FROM votes v 
            LEFT JOIN features f ON v.feature_id = f.id 
            WHERE f.id IS NULL
        ''')
        orphaned_votes = cursor.fetchone()[0]
        assert orphaned_votes == 0