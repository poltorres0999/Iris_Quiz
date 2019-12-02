from app import db
from models.iris_real_like_response import RealLikeResponse

REAL_V = 1
SYN_V = 2


class RealLikeController:

    def update_real_like(self, image_id, response_value, date):
        if RealLikeResponse.query.get(image_id) is None:
            db.session.add(RealLikeResponse(iris_image_id=image_id, date=date))
        if response_value == 1:
            db.session.query(RealLikeResponse).filter_by(iris_image_id=image_id).update(
                {'surely_real': RealLikeResponse.surely_real + 1,
                 'date': date})
        elif response_value == 2:
            db.session.query(RealLikeResponse).filter_by(iris_image_id=image_id).update(
                {'maybe_real': RealLikeResponse.maybe_real + 1,
                 'date': date})
        elif response_value == 3:
            db.session.query(RealLikeResponse).filter_by(iris_image_id=image_id).update(
                {'indecise': RealLikeResponse.indecise + 1,
                 'date': date})
        elif response_value == 4:
            db.session.query(RealLikeResponse).filter_by(iris_image_id=image_id).update(
                {'maybe_syn': RealLikeResponse.maybe_syn + 1,
                 'date': date})
        else:
            db.session.query(RealLikeResponse).filter_by(iris_image_id=image_id).update(
                {'surely_syn': RealLikeResponse.surely_syn + 1,
                 'date': date})
        db.session.commit()

    def get_real_like_response(self, image_id):
        return db.session.query(RealLikeResponse).filter_by(iris_image_id=image_id)

    def get_all_real_like_responses(self):
        return db.session.query(RealLikeResponse).all()

    def get_all_real_like_responses_sum(self):
        responses_sum = [0 for i in range(5)]
        responses = self.get_all_real_like_responses()
        for response in responses:
            responses_sum[0] += response.surely_real
            responses_sum[1] += response.maybe_real
            responses_sum[2] += response.indecise
            responses_sum[3] += response.maybe_syn
            responses_sum[4] += response.surely_syn

        return responses_sum




