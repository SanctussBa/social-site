import os


"""Flask configuration"""

TESTING = True
DEBUG = True
FLASK_ENV = 'development'
SECRET_KEY = os.urandom(32)
SQLALCHEMY_DATABASE_URI = 'sqlite:///database'
SQLALCHEMY_TRACK_MODIFICATIONS = False

CKEDITOR_SERVE_LOCAL = True
CKEDITOR_HEIGHT = 200

# To prevent users from uploading very big files
MAX_CONTENT_LENGTH = 800 * 1000
