/**
 * API service for the Feature Voting System
 * Handles all HTTP requests to the Flask backend using Axios
 */

import axios from 'axios';

// Configure the base URL for the API
// Change this to your backend server URL
const API_BASE_URL = 'http://localhost:5000/api';

// Create an Axios instance with default configuration
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000, // 10 second timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for logging (optional)
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('API Response Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

/**
 * Generate a unique user ID for voting
 * In a real app, this would be tied to user authentication
 */
const generateUserId = () => {
  return 'user_' + Math.random().toString(36).substr(2, 9);
};

// Store user ID in memory (in a real app, use AsyncStorage)
let currentUserId = generateUserId();

/**
 * Get the current user ID
 */
export const getCurrentUserId = () => currentUserId;

/**
 * API functions for features
 */
export const featuresApi = {
  /**
   * Get all features with vote counts
   * @returns {Promise} Promise that resolves to features array
   */
  getAll: async () => {
    try {
      const response = await api.get('/features');
      return response.data.features || response.data;
    } catch (error) {
      console.error('Error fetching features:', error);
      throw error;
    }
  },

  /**
   * Create a new feature
   * @param {Object} feature - Feature object with title and description
   * @returns {Promise} Promise that resolves to created feature
   */
  create: async (feature) => {
    try {
      const response = await api.post('/features', feature);
      return response.data;
    } catch (error) {
      console.error('Error creating feature:', error);
      throw error;
    }
  },

  /**
   * Get a specific feature by ID
   * @param {number} id - Feature ID
   * @returns {Promise} Promise that resolves to feature object
   */
  getById: async (id) => {
    try {
      const response = await api.get(`/features/${id}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching feature:', error);
      throw error;
    }
  },

  /**
   * Delete a feature
   * @param {number} id - Feature ID
   * @returns {Promise} Promise that resolves to success message
   */
  delete: async (id) => {
    try {
      const response = await api.delete(`/features/${id}`);
      return response.data;
    } catch (error) {
      console.error('Error deleting feature:', error);
      throw error;
    }
  },
};

/**
 * API functions for votes
 */
export const votesApi = {
  /**
   * Vote for a feature
   * @param {number} featureId - Feature ID to vote for
   * @returns {Promise} Promise that resolves to vote result
   */
  addVote: async (featureId) => {
    try {
      const response = await api.post(`/features/${featureId}/vote`, {
        user_id: currentUserId,
      });
      return response.data;
    } catch (error) {
      console.error('Error adding vote:', error);
      throw error;
    }
  },

  /**
   * Remove vote from a feature
   * @param {number} featureId - Feature ID to remove vote from
   * @returns {Promise} Promise that resolves to removal result
   */
  removeVote: async (featureId) => {
    try {
      const response = await api.delete(`/features/${featureId}/vote`, {
        data: { user_id: currentUserId },
      });
      return response.data;
    } catch (error) {
      console.error('Error removing vote:', error);
      throw error;
    }
  },

  /**
   * Get user's votes
   * @returns {Promise} Promise that resolves to user's voted features
   */
  getUserVotes: async () => {
    try {
      const response = await api.get(`/users/${currentUserId}/votes`);
      return response.data;
    } catch (error) {
      console.error('Error fetching user votes:', error);
      throw error;
    }
  },
};

/**
 * API functions for health checks and stats
 */
export const utilsApi = {
  /**
   * Health check endpoint
   * @returns {Promise} Promise that resolves to health status
   */
  healthCheck: async () => {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      console.error('Error checking health:', error);
      throw error;
    }
  },

  /**
   * Get database statistics
   * @returns {Promise} Promise that resolves to database stats
   */
  getStats: async () => {
    try {
      const response = await api.get('/stats');
      return response.data;
    } catch (error) {
      console.error('Error fetching stats:', error);
      throw error;
    }
  },
};

export default api;