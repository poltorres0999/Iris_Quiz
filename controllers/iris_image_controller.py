
import app
from app import db
from models.iris_image import IrisImage
from random import randint, choice

REAL_V = 1
SYN_V = 2

class IrisImageController:

    def store_image_data(self, width, height, image_type, file_name, store_path):
        iris_image = IrisImage(width=width, height=height, type=image_type, file_name=file_name, store_path=store_path)
        db.session.add(iris_image)
        db.session.commit()

    def get_random_images(self):
        # todo try/catch

        s_images = db.session.query(IrisImage.id, IrisImage.store_path).filter(IrisImage.type == "synthetic").all()
        r_images = db.session.query(IrisImage.id, IrisImage.store_path).filter(IrisImage.type == "real").all()

        if (choice([REAL_V, SYN_V])) == REAL_V:
            qualified_img_id, qualified_img_sp = r_images[randint(0, len(r_images) - 1)]
        else:
            qualified_img_id, qualified_img_sp = s_images[randint(0, len(s_images) - 1)]

        real_img_id, real_img_sp = r_images[randint(0, len(r_images) - 1)]
        synthetic_img_id, synthetic_img_sp = s_images[randint(0, len(s_images) - 1)]

        images_data = {"qualified_img": {'id': qualified_img_id, 'store_path': qualified_img_sp},
                       "real_image": {'id': real_img_id, 'store_path': real_img_sp},
                       "synthetic_image": {'id': synthetic_img_id, 'store_path': synthetic_img_sp}}

        return images_data
