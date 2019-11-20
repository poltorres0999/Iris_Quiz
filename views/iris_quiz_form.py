from flask import Flask, render_template, flash, request, Blueprint

from controllers.iris_quiz_controller import IrisQuizController
from forms.forms import IrisQuizForm
from models.iris_real_syn_response import RealSynResponse
from app import app
from app import sess, session


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
        real_syn_response = RealSynResponse(real_image_id=session['real_image_id'],
                                            syn_image_id=session['synthetic_image_id'],
                                            real_image_response=real_img_value,
                                            syn_image_response=syn_img_value)

        controller.store_real_syn_response(real_syn_response)
        controller.update_real_like(image_id=session['qualified_image_id'], response_value=int(img_qualification))
        return render_template('iris_quiz_succes.html')
    else:
        return render_template('index.html')

