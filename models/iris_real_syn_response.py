from app import db
from datetime import datetime

class RealSynResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    real_image_id = db.Column(db.Integer, db.ForeignKey("iris_image.id"), nullable=False)
    syn_image_id = db.Column(db.Integer, db.ForeignKey("iris_image.id"), nullable=False)
    real_image_response = db.Column(db.String(40), nullable=False)
    syn_image_response = db.Column(db.String(40), nullable=False)
    date = db.Column(db.String(128), nullable=False, default=datetime.now().isoformat())

    real_image = db.relationship("IrisImage", foreign_keys=[real_image_id])
    syn_image = db.relationship("IrisImage", foreign_keys=[syn_image_id])