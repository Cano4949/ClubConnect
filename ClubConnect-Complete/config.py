import os
from datetime import timedelta

class Config:
    """Basis-Konfiguration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///clubconnect.db'
    CLUB_NAME = os.environ.get('CLUB_NAME') or 'ClubConnect'
    WTF_CSRF_ENABLED = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False  # In Produktion auf True setzen
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)

class DevelopmentConfig(Config):
    """Entwicklungskonfiguration"""
    DEBUG = True
    DATABASE_URL = 'sqlite:///clubconnect_dev.db'

class TestingConfig(Config):
    """Test-Konfiguration"""
    TESTING = True
    WTF_CSRF_ENABLED = False
    DATABASE_URL = 'sqlite:///:memory:'

class ProductionConfig(Config):
    """Produktionskonfiguration"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///clubconnect.db'

class HerokuConfig(ProductionConfig):
    """Heroku-spezifische Konfiguration"""
    pass

class DockerConfig(ProductionConfig):
    """Docker-spezifische Konfiguration"""
    pass

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'heroku': HerokuConfig,
    'docker': DockerConfig,
    'default': DevelopmentConfig
}
