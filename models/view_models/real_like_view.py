
class RealLikeViewModel:
    
    def __init__(self, response_id, surely_real, maybe_real, indecise, maybe_syn, surely_syn, date):
        self.response_id = response_id
        self.surely_real = surely_real
        self.maybe_real = maybe_real
        self.indecise = indecise
        self.maybe_syn = maybe_syn
        self.surely_syn = surely_syn
        self.date = date


class RealLikeWithImageViewModel:

    def __init__(self, response_id, iris_image_id, image_type, surely_real, maybe_real, indecise, maybe_syn, surely_syn, date):
        self.response_id = response_id
        self.iris_image_id = iris_image_id
        self.image_type = image_type
        self.surely_real = surely_real
        self.maybe_real = maybe_real
        self.indecise = indecise
        self.maybe_syn = maybe_syn
        self.surely_syn = surely_syn
        self.date = date
