from app import db
from models.iris_real_like_response import RealLikeResponse
from models.iris_image import IrisImage

SYN_VAL = 'synthetic'
REAL_VAL = 'real'


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

    def get_response(self, image_id):
        return db.session.query(RealLikeResponse).filter_by(iris_image_id=image_id)

    def get_all_responses(self):
        return db.session.query(RealLikeResponse).all()

    def get_responses_sum(self):
        responses_sum = [0 for i in range(5)]
        responses = self.get_all_responses()
        for response in responses:
            response_values = self.__get_response_values(response)
            responses_sum = [responses_sum[i]+response_values[i] for i in range(len(response_values))]

        return responses_sum

    def get_responses_sum_divided(self):
        real_responses = [0 for i in range(5)]
        syn_responses = [0 for i in range(5)]
        total_responses = [0 for i in range(5)]
        responses = db.session.query(RealLikeResponse)\
            .join(IrisImage, IrisImage.id == RealLikeResponse.iris_image_id ).all()

        for response in responses:
            response_values = self.__get_response_values(response)
            total_responses = [total_responses[i]+response_values[i] for i in range(len(response_values))]

            if response.iris_image.type == SYN_VAL:
                syn_responses = [syn_responses[i]+response_values[i] for i in range(len(response_values))]
            else:
                real_responses = [real_responses[i]+response_values[i] for i in range(len(response_values))]

        return total_responses, syn_responses, real_responses

    def get_all_responses_with_image(self):
        return db.session.query(RealLikeResponse).join(IrisImage, IrisImage.id == RealLikeResponse.iris_image_id).all()

    def __get_response_values(self, response):
        response_sum = total_responses = [0 for i in range(5)]

        response_sum[0] = response.surely_real
        response_sum[1] = response.maybe_real
        response_sum[2] = response.indecise
        response_sum[3] = response.maybe_syn
        response_sum[4] = response.surely_syn

        return response_sum











