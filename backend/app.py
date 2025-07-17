"""
Main Flask application for the Feature Voting System.
This module initializes the Flask app, configures CORS, and sets up the API routes.
"""

from flask import Flask, jsonify
from flask_cors import CORS
from routes.features import features_bp
from routes.votes import votes_bp
from models.database import init_db, get_db_connection
import os

def create_app():
    """
    Create and configure the Flask application.
    
    Returns:
        Flask: Configured Flask application instance
    """
    # Create Flask app
    app = Flask(__name__)
    
    # App configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Enable CORS for all routes (allows frontend to make requests)
    CORS(app, origins=[
        "http://localhost:3000",    # React development server
        "http://localhost:19006",   # Expo web
        "exp://localhost:19000",    # Expo mobile
        "http://127.0.0.1:3000",
        "http://127.0.0.1:19006"
    ])
    
    # Initialize database
    init_db()
    
    # Register API blueprints
    app.register_blueprint(features_bp)
    app.register_blueprint(votes_bp)
    
    # Root endpoint
    @app.route('/')
    def index():
        """
        Root endpoint that provides API information.
        
        Returns:
            JSON response with API information and available endpoints
        """
        return jsonify({
            'message': 'Feature Voting System API',
            'version': '1.0.0',
            'endpoints': {
                'features': {
                    'GET /api/features': 'Get all features with vote counts',
                    'POST /api/features': 'Create a new feature',
                    'GET /api/features/<id>': 'Get a specific feature',
                    'DELETE /api/features/<id>': 'Delete a feature'
                },
                'votes': {
                    'POST /api/features/<id>/vote': 'Vote for a feature',
                    'DELETE /api/features/<id>/vote': 'Remove vote from a feature'
                },
                'users': {
                    'GET /api/users/<user_id>/votes': 'Get user\'s votes'
                },
                'health': {
                    'GET /api/health': 'Health check endpoint'
                },
                'stats': {
                    'GET /api/stats': 'Get database statistics'
                }
            }
        })
    
    # App health check endpoint
    @app.route('/api/health')
    def get_health():
        """
        Get health check endpoint.

        Returns:
            JSON response with health check
        """
        return jsonify({
            'status': 'healthy',
            'message': 'Health check endpoint.',
            'version': '1.0.0'
        }), 200
    
    # Database stats endpoint
    @app.route('/api/stats')
    def get_stats():
        """
        Get database statistics.
        
        Returns:
            JSON response with database statistics
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Get feature count
            cursor.execute('SELECT COUNT(*) as count FROM features')
            feature_count = cursor.fetchone()['count']
            
            # Get vote count
            cursor.execute('SELECT COUNT(*) as count FROM votes')
            vote_count = cursor.fetchone()['count']
            
            conn.close()
            
            stats = {
                'total_features': feature_count,
                'total_votes': vote_count
            }
            return jsonify(stats), 200
        except Exception as e:
            print(f"Error getting stats: {e}")
            return jsonify({'error': 'Failed to get statistics'}), 500
    
    # Global error handlers
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors globally."""
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        """Handle 405 errors globally."""
        return jsonify({'error': 'Method not allowed'}), 405
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors globally."""
        return jsonify({'error': 'Internal server error'}), 500
    
    # Handle JSON parsing errors
    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 errors globally."""
        return jsonify({'error': 'Bad request - Invalid JSON'}), 400
    
    return app

def run_app():
    """
    Run the Flask application.
    This function is used when the script is run directly.
    """
    app = create_app()
    
    # Get configuration from environment variables
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"Starting Feature Voting API on {host}:{port}")
    print(f"Debug mode: {debug}")
    print("Available endpoints:")
    print("  GET  /                     - API information")
    print("  GET  /api/health           - Health check")
    print("  GET  /api/stats            - Database statistics")
    print("  GET  /api/features         - Get all features")
    print("  POST /api/features         - Create new feature")
    print("  GET  /api/features/<id>    - Get specific feature")
    print("  POST /api/features/<id>/vote - Vote for feature")
    print("  DELETE /api/features/<id>/vote - Remove vote")
    print("  GET  /api/users/<id>/votes - Get user votes")
    
    app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    run_app()