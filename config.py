import os
from datetime import timedelta


class Config:
    """Configuração base para todos os ambientes."""
    
    # Configurações básicas
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Configurações do banco de dados
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Configurações de logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    
    # Configurações de segurança
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    # Configurações de paginação
    ITEMS_PER_PAGE = 20
    MAX_ITEMS_PER_PAGE = 100
    
    # Configurações de cache
    CACHE_TYPE = os.environ.get('CACHE_TYPE', 'simple')
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Configurações de upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = 'uploads'
    
    # Configurações de email (se necessário)
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')


class DevelopmentConfig(Config):
    """Configuração para desenvolvimento."""
    
    DEBUG = True
    TESTING = False
    LOG_LEVEL = 'DEBUG'
    
    # Configurações específicas para desenvolvimento
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///dev.db'
    
    # Configurações de CORS mais permissivas para desenvolvimento
    CORS_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000', 'http://localhost:8080']


class TestingConfig(Config):
    """Configuração para testes."""
    
    TESTING = True
    DEBUG = False
    
    # Usar banco de dados em memória para testes
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # Desabilitar CSRF para testes
    WTF_CSRF_ENABLED = False
    
    # Configurações específicas para testes
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=1)


class ProductionConfig(Config):
    """Configuração para produção."""
    
    DEBUG = False
    TESTING = False
    
    # Configurações de segurança para produção
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    
    # Configurações de banco de dados para produção
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    # Configurações de CORS mais restritivas
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '').split(',')
    
    # Configurações de logging para produção
    LOG_LEVEL = 'WARNING'
    
    # Configurações de cache para produção
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = os.environ.get('REDIS_URL')


class StagingConfig(Config):
    """Configuração para staging."""
    
    DEBUG = False
    TESTING = False
    
    # Configurações similares à produção, mas com mais logs
    LOG_LEVEL = 'INFO'
    
    # Configurações de banco de dados para staging
    SQLALCHEMY_DATABASE_URI = os.environ.get('STAGING_DATABASE_URL')


# Dicionário de configurações
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'staging': StagingConfig,
    'default': DevelopmentConfig
} 