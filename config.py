import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cartify_secret_key_2024_secure'
    # Default to MySQL database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://cartify:cartify123@localhost:3306/cartify_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Email configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'sthitiprakalpitarath@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # Pagination
    PRODUCTS_PER_PAGE = 12
    ORDERS_PER_PAGE = 10
    
    # File uploads
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Admin configuration
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or 'admin@cartify.com'
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'mysql+pymysql://cartify:cartify123@localhost:3306/cartify_db'

class MySQLDevelopmentConfig(Config):
    """Development configuration using MySQL database"""
    DEBUG = True
    # Format: mysql+pymysql://username:password@host:port/database_name
    # For MySQL setup, use: mysql+pymysql://cartify:cartify123@localhost:3306/cartify_db
    # (after running mysql_setup.bat)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'mysql+pymysql://cartify:cartify123@localhost:3306/cartify_db'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://cartify:cartify123@localhost:3306/cartify_db'

class MySQLProductionConfig(Config):
    """Production configuration using MySQL database"""
    DEBUG = False
    # Format: mysql+pymysql://username:password@host:port/database_name
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:Deba1234@localhost:3306/cartify_db'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'mysql_development': MySQLDevelopmentConfig,
    'production': ProductionConfig,
    'mysql_production': MySQLProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

