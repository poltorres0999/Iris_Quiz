from app import app
from controllers.iris_image_controller import IrisImageController

TITLE = "Iris quiz"
controller = IrisImageController()

@app.route("/upload_iris_image", methods=['GET'])
def upload_image_form_get():
    form = ()


@app.route("/upload_iris_image", methods=['POST'])
def upload_image_form_post():
    pass