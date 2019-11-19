import app
from app import db
from models.iris_image import IrisImage

class IrisImageController:

    def store_quiz_response(self, iris_image):
        db.session.add(iris_image)
        db.session.commit()
