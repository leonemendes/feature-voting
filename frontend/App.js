/**
 * Feature Voting App
 * Main App component with navigation between FeatureList and NewFeatureForm
 */

import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { StatusBar } from 'expo-status-bar';
import { StyleSheet, View } from 'react-native';

// Import components
import FeatureList from './components/FeatureList';
import NewFeatureForm from './components/NewFeatureForm';

// Create stack navigator
const Stack = createStackNavigator();

const App = () => {
  return (
    <SafeAreaProvider>
      <NavigationContainer>
        <StatusBar style="dark" />
        <Stack.Navigator
          initialRouteName="FeatureList"
          screenOptions={{
            headerStyle: {
              backgroundColor: '#fff',
              shadowColor: '#000',
              shadowOffset: { width: 0, height: 1 },
              shadowOpacity: 0.1,
              shadowRadius: 2,
              elevation: 2,
            },
            headerTintColor: '#007AFF',
            headerTitleStyle: {
              fontWeight: '600',
              fontSize: 18,
            },
            headerBackTitleVisible: false,
          }}
        >
          <Stack.Screen
            name="FeatureList"
            component={FeatureList}
            options={{
              headerShown: false, // We'll use custom header in FeatureList
            }}
          />
          <Stack.Screen
            name="AddFeature"
            component={NewFeatureForm}
            options={{
              headerShown: false, // We'll use custom header in NewFeatureForm
              presentation: 'modal',
            }}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </SafeAreaProvider>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
});

export default App;