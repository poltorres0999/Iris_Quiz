from app import db


class IrisImage(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    width = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(20), nullable=False)
    file_name = db.Column(db.String(128), nullable=False)
    store_path = db.Column(db.String(128), nullable=False)
    """
    TODO
    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, w):
        if w < 0: raise ValueError("Width must have a positive value")

    @property
    def height(self):
        return self._width

    @height.setter
    def height(self, h):
        if h < 0: raise ValueError("Width must have a positive value")
    """

