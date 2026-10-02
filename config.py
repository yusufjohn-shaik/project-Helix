import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Secret key for Flask sessions
    SECRET_KEY = os.getenv("SECRET_KEY", "default-helix-secret-key-change-me")
    
    # PostgreSQL Database Credentials
    DB_USER = os.getenv("DB_USER", "helix_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "helix123")
    DB_NAME = os.getenv("DB_NAME", "helix")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", 5432))
    
    # Folder path where uploaded documents/files will be saved
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", os.path.join(os.path.dirname(__file__), "static", "uploads"))
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 16 * 1024 * 1024))  # 16MB file limit
