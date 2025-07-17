/**
 * NewFeatureForm Component
 * Form to create a new feature request
 */

import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  Alert,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
} from 'react-native';
import { featuresApi } from '../services/api';

const NewFeatureForm = ({ navigation }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);

  /**
   * Validate form inputs
   * @returns {boolean} true if form is valid
   */
  const validateForm = () => {
    if (!title.trim()) {
      Alert.alert('Validation Error', 'Please enter a feature title.');
      return false;
    }

    if (title.trim().length > 200) {
      Alert.alert('Validation Error', 'Title must be less than 200 characters.');
      return false;
    }

    if (description.trim().length > 1000) {
      Alert.alert('Validation Error', 'Description must be less than 1000 characters.');
      return false;
    }

    return true;
  };

  /**
   * Handle form submission
   */
  const handleSubmit = async () => {
    if (!validateForm()) {
      return;
    }

    setLoading(true);

    try {
      const newFeature = {
        title: title.trim(),
        description: description.trim(),
      };

      await featuresApi.create(newFeature);
      
      Alert.alert(
        'Success',
        'Feature request created successfully!',
        [
          {
            text: 'OK',
            onPress: () => {
              // Clear form
              setTitle('');
              setDescription('');
              // Navigate back to features list
              navigation.goBack();
            },
          },
        ]
      );
    } catch (error) {
      let errorMessage = 'Failed to create feature. Please try again.';
      
      // Handle specific error messages from backend
      if (error.response?.data?.error) {
        errorMessage = error.response.data.error;
      }
      
      Alert.alert('Error', errorMessage);
      console.error('Error creating feature:', error);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Handle cancel action
   */
  const handleCancel = () => {
    if (title.trim() || description.trim()) {
      Alert.alert(
        'Discard Changes',
        'Are you sure you want to discard your changes?',
        [
          { text: 'Cancel', style: 'cancel' },
          {
            text: 'Discard',
            style: 'destructive',
            onPress: () => {
              setTitle('');
              setDescription('');
              navigation.goBack();
            },
          },
        ]
      );
    } else {
      navigation.goBack();
    }
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <ScrollView style={styles.scrollView} keyboardShouldPersistTaps="handled">
        <View style={styles.header}>
          <TouchableOpacity
            style={styles.cancelButton}
            onPress={handleCancel}
          >
            <Text style={styles.cancelButtonText}>Cancel</Text>
          </TouchableOpacity>
          <Text style={styles.headerTitle}>New Feature</Text>
          <TouchableOpacity
            style={[
              styles.submitButton,
              loading && styles.submitButtonDisabled
            ]}
            onPress={handleSubmit}
            disabled={loading}
          >
            <Text style={[
              styles.submitButtonText,
              loading && styles.submitButtonTextDisabled
            ]}>
              {loading ? 'Creating...' : 'Create'}
            </Text>
          </TouchableOpacity>
        </View>

        <View style={styles.form}>
          <View style={styles.inputGroup}>
            <Text style={styles.label}>
              Title <Text style={styles.required}>*</Text>
            </Text>
            <TextInput
              style={styles.input}
              value={title}
              onChangeText={setTitle}
              placeholder="Enter feature title"
              placeholderTextColor="#999"
              maxLength={200}
              multiline={false}
              editable={!loading}
            />
            <Text style={styles.characterCount}>
              {title.length}/200
            </Text>
          </View>

          <View style={styles.inputGroup}>
            <Text style={styles.label}>Description</Text>
            <TextInput
              style={[styles.input, styles.textArea]}
              value={description}
              onChangeText={setDescription}
              placeholder="Describe your feature request in detail..."
              placeholderTextColor="#999"
              maxLength={1000}
              multiline={true}
              numberOfLines={6}
              textAlignVertical="top"
              editable={!loading}
            />
            <Text style={styles.characterCount}>
              {description.length}/1000
            </Text>
          </View>

          <View style={styles.helpText}>
            <Text style={styles.helpTextTitle}>Tips for a good feature request:</Text>
            <Text style={styles.helpTextItem}>• Use a clear and descriptive title</Text>
            <Text style={styles.helpTextItem}>• Explain the problem you're trying to solve</Text>
            <Text style={styles.helpTextItem}>• Describe the expected behavior</Text>
            <Text style={styles.helpTextItem}>• Keep it concise but detailed</Text>
          </View>
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  scrollView: {
    flex: 1,
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
  cancelButton: {
    paddingHorizontal: 12,
    paddingVertical: 8,
  },
  cancelButtonText: {
    color: '#007AFF',
    fontSize: 16,
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
  },
  submitButton: {
    backgroundColor: '#007AFF',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 8,
  },
  submitButtonDisabled: {
    backgroundColor: '#e0e0e0',
  },
  submitButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  submitButtonTextDisabled: {
    color: '#999',
  },
  form: {
    padding: 16,
  },
  inputGroup: {
    marginBottom: 24,
  },
  label: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 8,
  },
  required: {
    color: '#FF3B30',
  },
  input: {
    backgroundColor: '#fff',
    borderWidth: 1,
    borderColor: '#e0e0e0',
    borderRadius: 8,
    paddingHorizontal: 16,
    paddingVertical: 12,
    fontSize: 16,
    color: '#333',
    minHeight: 50,
  },
  textArea: {
    minHeight: 120,
    maxHeight: 200,
    textAlignVertical: 'top',
  },
  characterCount: {
    fontSize: 12,
    color: '#999',
    textAlign: 'right',
    marginTop: 4,
  },
  helpText: {
    backgroundColor: '#fff',
    padding: 16,
    borderRadius: 8,
    marginTop: 16,
  },
  helpTextTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#333',
    marginBottom: 8,
  },
  helpTextItem: {
    fontSize: 14,
    color: '#666',
    marginBottom: 4,
    lineHeight: 20,
  },
});

export default NewFeatureForm;