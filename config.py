import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = True
    #### Data base configuration ####
    DB_USERNAME = "postgres"
    DB_PASSWORD = "admin"
    DB_NAME = "iris_dev_db"
    DB_HOST = "localhost"
    DB_PORT = 5432
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Upload images configuration
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    SYNTHETIC_IMG_STORE_PATH = "static/synthetic_images"
    REAL_IMG_STORE_PATH = "static/real_images"
    # Temporal files
    TMP_CSV = "tmp/csv"
    FILE_TIMEOUT = 60
    # SECRET KEY (dev)
    SECRET_KEY = "d4e566364f0c3a89d349b00a425c2ac1b7723eb451df4bdc"
    SESSION_TYPE = "filesystem"
