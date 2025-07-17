import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'data', 'features.db')
    CORS_ORIGINS = ['http://localhost:3000', 'exp://localhost:19000']