import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')

    SQLALCHEMY_DATABASE_FILE = os.environ.get('DATABASE_FILE')\
        or os.path.join(basedir, 'PrayerOfHannah.sqlite')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')\
        or 'sqlite:///' + SQLALCHEMY_DATABASE_FILE

    SQLALCHEMY_TRACK_MODIFICATIONS = False