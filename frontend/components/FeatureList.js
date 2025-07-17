/**
 * FeatureList Component
 * Displays a list of features with vote counts and upvote buttons
 */

import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  FlatList,
  TouchableOpacity,
  StyleSheet,
  Alert,
  RefreshControl,
} from 'react-native';
import { featuresApi, votesApi, getCurrentUserId } from '../services/api';

const FeatureList = ({ navigation }) => {
  const [features, setFeatures] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [userVotes, setUserVotes] = useState([]);

  // Load features when component mounts
  useEffect(() => {
    loadFeatures();
    loadUserVotes();
  }, []);

  /**
   * Load all features from the API
   */
  const loadFeatures = async () => {
    try {
      setLoading(true);
      const featuresData = await featuresApi.getAll();
      setFeatures(featuresData);
    } catch (error) {
      Alert.alert('Error', 'Failed to load features. Please try again.');
      console.error('Error loading features:', error);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Load user's votes to show which features they've voted for
   */
  const loadUserVotes = async () => {
    try {
      const votesData = await votesApi.getUserVotes();
      setUserVotes(votesData.voted_features || []);
    } catch (error) {
      console.error('Error loading user votes:', error);
      // Don't show alert for this as it's not critical
    }
  };

  /**
   * Handle pull-to-refresh
   */
  const onRefresh = async () => {
    setRefreshing(true);
    await loadFeatures();
    await loadUserVotes();
    setRefreshing(false);
  };

  /**
   * Handle voting for a feature
   * @param {number} featureId - ID of the feature to vote for
   */
  const handleVote = async (featureId) => {
    try {
      // Check if user has already voted
      if (userVotes.includes(featureId)) {
        Alert.alert('Already Voted', 'You have already voted for this feature.');
        return;
      }

      // Add vote
      await votesApi.addVote(featureId);
      
      // Update local state
      setUserVotes([...userVotes, featureId]);
      
      // Refresh features to get updated vote counts
      await loadFeatures();
      
      Alert.alert('Success', 'Your vote has been added!');
    } catch (error) {
      let errorMessage = 'Failed to vote. Please try again.';
      
      // Handle specific error messages
      if (error.response?.data?.error) {
        errorMessage = error.response.data.error;
      }
      
      Alert.alert('Error', errorMessage);
      console.error('Error voting:', error);
    }
  };

  /**
   * Navigate to the add feature screen
   */
  const navigateToAddFeature = () => {
    navigation.navigate('AddFeature');
  };

  /**
   * Render individual feature item
   */
  const renderFeatureItem = ({ item }) => {
    const hasVoted = userVotes.includes(item.id);
    
    return (
      <View style={styles.featureItem}>
        <View style={styles.featureContent}>
          <Text style={styles.featureTitle}>{item.title}</Text>
          {item.description ? (
            <Text style={styles.featureDescription}>{item.description}</Text>
          ) : null}
          <Text style={styles.voteCount}>
            {item.vote_count} {item.vote_count === 1 ? 'vote' : 'votes'}
          </Text>
        </View>
        <TouchableOpacity
          style={[
            styles.voteButton,
            hasVoted && styles.voteButtonDisabled
          ]}
          onPress={() => handleVote(item.id)}
          disabled={hasVoted}
        >
          <Text style={[
            styles.voteButtonText,
            hasVoted && styles.voteButtonTextDisabled
          ]}>
            {hasVoted ? '✓ Voted' : '👍 Vote'}
          </Text>
        </TouchableOpacity>
      </View>
    );
  };

  /**
   * Render empty state
   */
  const renderEmptyState = () => (
    <View style={styles.emptyState}>
      <Text style={styles.emptyStateText}>No features yet!</Text>
      <Text style={styles.emptyStateSubtext}>
        Be the first to suggest a feature.
      </Text>
      <TouchableOpacity
        style={styles.addButton}
        onPress={navigateToAddFeature}
      >
        <Text style={styles.addButtonText}>Add Feature</Text>
      </TouchableOpacity>
    </View>
  );

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Feature Requests</Text>
        <TouchableOpacity
          style={styles.addButton}
          onPress={navigateToAddFeature}
        >
          <Text style={styles.addButtonText}>+ Add</Text>
        </TouchableOpacity>
      </View>

      <FlatList
        data={features}
        renderItem={renderFeatureItem}
        keyExtractor={(item) => item.id.toString()}
        contentContainerStyle={features.length === 0 ? styles.emptyContainer : null}
        ListEmptyComponent={!loading ? renderEmptyState : null}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={onRefresh}
            colors={['#007AFF']}
          />
        }
        style={styles.list}
      />

      {loading && features.length === 0 && (
        <View style={styles.loadingContainer}>
          <Text style={styles.loadingText}>Loading features...</Text>
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 12,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
  },
  addButton: {
    backgroundColor: '#007AFF',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 8,
  },
  addButtonText: {
    color: '#fff',
    fontWeight: '600',
    fontSize: 14,
  },
  list: {
    flex: 1,
  },
  featureItem: {
    backgroundColor: '#fff',
    marginHorizontal: 16,
    marginVertical: 8,
    padding: 16,
    borderRadius: 8,
    flexDirection: 'row',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  },
  featureContent: {
    flex: 1,
    marginRight: 12,
  },
  featureTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 4,
  },
  featureDescription: {
    fontSize: 14,
    color: '#666',
    marginBottom: 8,
  },
  voteCount: {
    fontSize: 12,
    color: '#999',
    fontWeight: '500',
  },
  voteButton: {
    backgroundColor: '#007AFF',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 6,
    minWidth: 70,
    alignItems: 'center',
  },
  voteButtonDisabled: {
    backgroundColor: '#e0e0e0',
  },
  voteButtonText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: '600',
  },
  voteButtonTextDisabled: {
    color: '#999',
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  emptyState: {
    alignItems: 'center',
    paddingHorizontal: 32,
  },
  emptyStateText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#666',
    marginBottom: 8,
  },
  emptyStateSubtext: {
    fontSize: 14,
    color: '#999',
    textAlign: 'center',
    marginBottom: 24,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    fontSize: 16,
    color: '#666',
  },
});

export default FeatureList;