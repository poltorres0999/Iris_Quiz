import app
from app import db
from models.iris_image import IrisImage

class IrisImageController:

    def store_image_data(self, iris_image):
        db.session.add(iris_image)
        db.session.commit()
