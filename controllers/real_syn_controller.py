from app import db
from models.iris_real_syn_response import RealSynResponse

REAL_V = 1
SYN_V = 2


class RealSynController:

    def store_real_syn_response(self, real_image_id, syn_image_id, real_image_response, syn_image_response, date):
        real_syn_response = RealSynResponse(real_image_id=real_image_id,
                                            syn_image_id=syn_image_id,
                                            real_image_response=real_image_response,
                                            syn_image_response=syn_image_response,
                                            date=date)

        db.session.add(real_syn_response)
        db.session.commit()

    def get_all_responses(self):
        return db.session.query(RealSynResponse).all()

    def get_correct_syn_responses(self):
        return db.session.query(RealSynResponse).filter_by(syn_image_response='synthetic')

    def get_correct_real_responses(self):
        return db.session.query(RealSynResponse).filter_bt(real_image_response='real')

    def get_wrong_syn_responses(self):
        return db.session.query(RealSynResponse).filter_by(syn_image_response='real')

    def get_wrong_real_responses(self):
        return db.session.query(RealSynResponse).filter_bt(real_image_response='synthetic')

    def count_correct_syn_responses(self):
        return RealSynResponse.query.filter_by(syn_image_response='synthetic').count()

    def count_wrong_syn_responses(self):
        return RealSynResponse.query.filter_by(syn_image_response='real').count()

    def count_correct_real_responses(self):
        return RealSynResponse.query.filter_by(real_image_response='real').count()

    def count_wrong_real_responses(self):
        return RealSynResponse.query.filter_by(real_image_response='synthetic').count()





