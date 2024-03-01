from sqlalchemy import NullPool

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 20
    SQLALCHEMY_POOL_TIMEOUT = 10
    SQLALCHEMY_POOL_RECYCLE = 3600
    SQLALCHEMY_POOL_CLASS = NullPool

class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = 'Sm9obasdasdasdasdasdasddiBTY2asdasda'
    SQLALCHEMY_DATABASE_URI = f"sqlite:////tmp/foo.db"

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'Sm9obiBTY2hy_b2asdasdasdasd0ga2-lja3M_gYXNz'
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:2222@localhost:5432/TestingProject"