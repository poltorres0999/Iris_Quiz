import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = True
    #### Data base configuration ####
    DB_USERNAME = "postgres"
    DB_PASSWORD = "admin"
    DB_NAME = "iris_local_db"
    DB_HOST = "localhost"
    DB_PORT = 5432
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Iris images path
    SYNTHETIC_IMG_STORE_PATH = f"static/synthetic_images"
    REAL_IMG_STORE_PATH = f"static/real_images"
    # SECRET KEY (dev)
    SECRET_KEY = 'd4e566364f0c3a89d349b00a425c2ac1b7723eb451df4bdc'
    SESSION_TYPE = 'filesystem'
