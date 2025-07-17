# Feature Voting App - React Native Frontend

A React Native mobile application for the Feature Voting System that allows users to view, create, and vote on feature requests.

## Features

- **Feature List**: View all features with vote counts and upvote buttons
- **Add Feature**: Create new feature requests with title and description
- **Real-time Voting**: Vote for features with instant feedback
- **Pull-to-Refresh**: Refresh the feature list to get latest data
- **User-friendly UI**: Clean, minimal design with intuitive navigation

## Project Structure

```
frontend/
├── App.js                    # Main app component with navigation
├── components/
│   ├── FeatureList.js       # Feature list screen with voting
│   └── NewFeatureForm.js    # New feature creation form
├── services/
│   └── api.js               # API service using Axios
├── package.json             # Dependencies and scripts
├── app.json                 # Expo configuration
└── babel.config.js          # Babel configuration
```

## Setup Instructions

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Configure API endpoint:**
   Edit `services/api.js` and update the `API_BASE_URL` to point to your backend:
   ```javascript
   const API_BASE_URL = 'http://your-backend-url:5000/api';
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

4. **Run on device/simulator:**
   - iOS: `npm run ios`
   - Android: `npm run android`
   - Web: `npm run web`

## Dependencies

- **React Navigation**: For screen navigation
- **Axios**: For API calls to the backend
- **Expo**: For development and build tools
- **React Native**: Core framework

## API Integration

The app connects to the Flask backend using Axios and provides the following functionality:

- Fetch all features with vote counts
- Create new features
- Vote for features
- Track user votes to prevent duplicate voting

## Usage

1. **View Features**: The main screen shows all feature requests sorted by vote count
2. **Vote**: Tap the vote button to upvote a feature (once per user)
3. **Add Feature**: Tap the "Add" button to create a new feature request
4. **Refresh**: Pull down on the list to refresh data from the server

## Configuration

### Backend URL
Update the API base URL in `services/api.js`:
```javascript
const API_BASE_URL = 'http://localhost:5000/api';
```

### User ID Generation
The app generates a unique user ID for voting. In a production app, this would be replaced with proper user authentication.

## Testing

1. Ensure the backend server is running on `http://localhost:5000`
2. Start the React Native development server
3. Test creating features and voting functionality
4. Verify data persistence between app sessions