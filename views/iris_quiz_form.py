from flask import Flask, render_template, flash, request, Blueprint

from controllers.iris_quiz_controller import IrisQuizController
from forms.forms import IrisQuizForm
from app import app
from app import sess, session
from models.iris_quiz_response import IrisQuizResponse

TITLE = "Iris quiz"
controller = IrisQuizController()


@app.route("/iris_quiz", methods=['GET'])
def process_form_get():
    form = IrisQuizForm()
    images_data = controller.get_random_images()

    session['qualified_image_id'] = images_data['qualified_img']['id']
    session['real_image_id'] = images_data['real_image']['id']
    session['synthetic_image_id'] = images_data['synthetic_image']['id']
    return render_template('iris_quiz_form.html',
                           form=form,
                           qualified_image=images_data['qualified_img'],
                           real_image=images_data['real_image'],
                           syn_image=images_data['synthetic_image'],
                           title=TITLE)


@app.route("/iris_quiz", methods=['POST'])
def process_form_post():
    iris_quiz_form = IrisQuizForm(request.form)
    img_qualification = request.form['qualification']
    real_img_value = request.form['img_1_response']
    syn_img_value = request.form['img_2_response']

    if iris_quiz_form.validate():
        real_img_value, syn_img_value = __process_image_values(real_img_value, syn_img_value)
        response = IrisQuizResponse(image_quality_value=int(img_qualification),
                                    real_image_value=real_img_value,
                                    synthetic_image_value=syn_img_value,
                                    qualified_image_id=int(session['qualified_image_id']),
                                    real_image_id=int(session['real_image_id']),
                                    synthetic_image_id=int(session['synthetic_image_id']))
        controller.store_quiz_response(response)
        return render_template('iris_quiz_succes.html')
    else:
        return render_template('index.html')


def __process_image_values(real_image_value, syn_image_value):
    syn_img_value = True
    real_img_value = True

    if syn_image_value == "real":
        syn_img_value = False
    if real_image_value == "synthetic":
        real_img_value = False

    return real_img_value, syn_img_value
