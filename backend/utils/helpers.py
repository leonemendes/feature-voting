import uuid
from datetime import datetime

def generate_user_id():
    """Generate a unique user ID."""
    return str(uuid.uuid4())

def format_timestamp(timestamp):
    """Format timestamp for display."""
    if isinstance(timestamp, str):
        return timestamp
    return timestamp.strftime('%Y-%m-%d %H:%M:%S') if timestamp else None

def validate_feature_data(data):
    """Validate feature creation data."""
    if not data:
        return False, "No data provided"
    
    if not data.get('title') or not data.get('title').strip():
        return False, "Title is required"
    
    if len(data.get('title', '')) > 200:
        return False, "Title too long (max 200 characters)"
    
    if len(data.get('description', '')) > 1000:
        return False, "Description too long (max 1000 characters)"
    
    return True, "Valid"