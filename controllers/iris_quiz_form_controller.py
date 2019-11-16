from app import db
from models.iris_image import IrisImage
import random
from random import randint

REAL_V = 1
SYN_V = 2


def get_random_images():
    # todo try/catch

    s_images = db.session.query(IrisImage.id, IrisImage.type).filter(IrisImage.type == "synthetic").all()
    r_images = db.session.query(IrisImage.id, IrisImage.type).filter(IrisImage.type == "real").all()

    if (random.choice(REAL_V, SYN_V)) == REAL_V:
        qualified_img_id, qualified_img_id_sp = r_images[randint(0, len(r_images))]
    else:
        qualified_img_id, qualified_img_id_sp = s_images[randint(0, len(s_images))]

    real_img_id, real_img_sp = r_images[randint(0, len(r_images))]
    synthetic_img_id, synthetic_img_sp = s_images[randint(0, len(s_images))]

    images_data = {"qualified_img": {'id': qualified_img_id, 'store_path': qualified_img_id_sp},
                   "real_image": {'id': real_img_id, 'store_path': real_img_sp},
                   "synthetic_image": {'id': synthetic_img_id, 'store_path': synthetic_img_sp}}

    return images_data
