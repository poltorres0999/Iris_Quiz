from app import app
from controllers.iris_image_controller import IrisImageController

TITLE = "Iris quiz"
controller = IrisImageController()

@app.route("/upload_iris_image", methods=['GET'])
def process_form_get():
    form = ()


@app.route("/upload_iris_image", methods=['POST'])
def process_form_get():
    pass