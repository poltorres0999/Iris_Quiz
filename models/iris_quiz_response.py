from app import db


class IrisQuizResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_quality_value = db.Column(db.Integer, nullable=False)
    real_image_value = db.Column(db.Boolean, nullable=False)
    synthetic_image_value = db.Column(db.Boolean, nullable=False)
    qualified_image_id = db.Column(db.Integer, db.ForeignKey("iris_image.id"), nullable=False)
    real_image_id = db.Column(db.Integer, db.ForeignKey("iris_image.id"), nullable=False)
    synthetic_image_id = db.Column(db.Integer, db.ForeignKey("iris_image.id"), nullable=False)

    qualified_image = db.relationship("IrisImage", foreign_keys=[qualified_image_id])
    real_image = db.relationship("IrisImage", foreign_keys=[real_image_id])
    synthetic_image = db.relationship("IrisImage", foreign_keys=[synthetic_image_id])





