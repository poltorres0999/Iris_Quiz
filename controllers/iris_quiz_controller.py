import app
from app import db
from forms.forms import IrisQuizForm
from models.iris_image import IrisImage
from models.iris_real_like_response import RealLikeResponse
import random
from random import randint
from datetime import datetime

REAL_V = 1
SYN_V = 2


class IrisQuizController:

    def store_real_syn_response(self, response):
        # TODO: TRY/CATCH
        db.session.add(response)
        db.session.commit()

    def update_real_like(self, image_id, response_value):
        date = datetime.now().isoformat()

        if RealLikeResponse.query.get(image_id) is None:
            db.session.add(RealLikeResponse(iris_image_id=image_id, date=date))

        if response_value == 1:
            db.session.query(RealLikeResponse).filter_by(id=image_id).update({'surely_real': RealLikeResponse.surely_real + 1,
                                                                              'date': date})
        elif response_value == 2:
            db.session.query(RealLikeResponse).filter_by(id=image_id).update({'maybe_real': RealLikeResponse.maybe_real + 1,
                                                                              'date': date})
        elif response_value == 3:
            db.session.query(RealLikeResponse).filter_by(id=image_id).update({'indecise': RealLikeResponse.indecise + 1,
                                                                              'date': date})
        elif response_value == 4:
            db.session.query(RealLikeResponse).filter_by(id=image_id).update({'maybe_syn': RealLikeResponse.maybe_syn + 1,
                                                                              'date': date})
        else:
            db.session.query(RealLikeResponse).filter_by(id=image_id).update({'surely_syn': RealLikeResponse.surely_syn + 1,
                                                                              'date': date})
        db.session.commit()

    def get_random_images(self):
        # todo try/catch

        s_images = db.session.query(IrisImage.id, IrisImage.store_path).filter(IrisImage.type == "synthetic").all()
        r_images = db.session.query(IrisImage.id, IrisImage.store_path).filter(IrisImage.type == "real").all()

        if (random.choice([REAL_V, SYN_V])) == REAL_V:
            qualified_img_id, qualified_img_sp = r_images[randint(0, len(r_images) - 1)]
        else:
            qualified_img_id, qualified_img_sp = s_images[randint(0, len(s_images) - 1)]

        real_img_id, real_img_sp = r_images[randint(0, len(r_images) - 1)]
        synthetic_img_id, synthetic_img_sp = s_images[randint(0, len(s_images) - 1)]

        images_data = {"qualified_img": {'id': qualified_img_id, 'store_path': qualified_img_sp},
                       "real_image": {'id': real_img_id, 'store_path': real_img_sp},
                       "synthetic_image": {'id': synthetic_img_id, 'store_path': synthetic_img_sp}}

        return images_data
