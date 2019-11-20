import app
from app import db
from models.iris_image import IrisImage

class IrisImageController:

    def store_image_data(self, width, height, image_type, file_name, store_path):
        iris_image = IrisImage(width=width, height=height, type=image_type, file_name=file_name, store_path=store_path)
        db.session.add(iris_image)
        db.session.commit()
