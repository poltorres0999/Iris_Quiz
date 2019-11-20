from app import db
from datetime import datetime


class RealLikeResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    iris_image_id = db.Column(db.Integer, db.ForeignKey("iris_image.id"), nullable=False)
    surely_real = db.Column(db.Integer, default=0, nullable=False)
    maybe_real = db.Column(db.Integer, default=0, nullable=False)
    indecise = db.Column(db.Integer, default=0, nullable=False)
    maybe_syn = db.Column(db.Integer, default=0, nullable=False)
    surely_syn = db.Column(db.Integer, default=0, nullable=False)
    date = db.Column(db.String(128), nullable=False, default=datetime.now().isoformat())

    iris_image = db.relationship("IrisImage", foreign_keys=[iris_image_id])
