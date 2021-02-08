import os


"""Flask configuration"""

TESTING = True
DEBUG = True
FLASK_ENV = 'development'
SECRET_KEY = os.urandom(32)
SQLALCHEMY_DATABASE_URI = 'sqlite:///database'
SQLALCHEMY_TRACK_MODIFICATIONS = False
