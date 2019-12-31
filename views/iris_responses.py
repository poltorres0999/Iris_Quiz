from flask import render_template, request, Response
import json
import time
from app import app
from app import session
from controllers.real_like_controller import RealLikeController
from controllers.real_syn_controller import RealSynController
from models.view_models.real_like_view import RealLikeWithImageViewModel
from models.view_models.real_syn_view import RealSynView

real_like_controller = RealLikeController()
real_syn_controller = RealSynController()


@app.route('/quiz_responses')
def show_response_table():

    real_like_columns = ["Response ID", "Image ID", "Image type", "Surely real", "Maybe real", "Indecise",
                         "Maybe synthetic", "Surely synthetic", "Date"]

    real_syn_columns = ["Response ID", "Real image ID", "Synthetic Image ID", "Real Image Response", "Syn image response",
                        "Date"]

    if request.args.get("current_table") is None:
        current_table = "real_like_table"
    else:
        current_table = request.args.get("current_table")

    if "data_timeout" not in session:
        json_real_like_data, json_real_syn_data = load_response_data()
        session['real_like_data'] = json_real_like_data
        session['real_syn_data'] = json_real_syn_data
        session['data_timeout'] = time.time()
    else:
        if time.time() - session["data_timeout"] > 30:
            json_real_like_data, json_real_syn_data = load_response_data()
            session['real_like_data'] = json_real_like_data
            session['real_syn_data'] = json_real_syn_data
            session['data_timeout'] = time.time()
        else:
            json_real_like_data = session['real_like_data']
            json_real_syn_data = session['real_syn_data']

    return render_template('iris_responses.html',
                           real_like_columns=real_like_columns,
                           real_like_data=json_real_like_data,
                           real_syn_data=json_real_syn_data,
                           real_syn_columns=real_syn_columns,
                           current_table=current_table)


def __get_page(data, offset=0, num_elements=10):
    return data[offset: offset + num_elements]


def load_response_data():
    real_like_responses = real_like_controller.get_all_responses_with_image()
    real_like_view_data = __real_like_view_model(real_like_responses)
    json_real_like_data = json.dumps({"data": [ob.__dict__ for ob in real_like_view_data]})

    real_syn_responses = real_syn_controller.get_all_responses()
    real_syn_view_data = __real_syn_view_mode(real_syn_responses)
    json_real_syn_data = json.dumps({"data": [ob.__dict__ for ob in real_syn_view_data]})

    return json_real_like_data, json_real_syn_data


def __real_like_view_model(real_like_data):
    real_like_responses = []
    for data in real_like_data:
        real_like_responses.append(RealLikeWithImageViewModel(data.id, data.iris_image_id, data.iris_image.type,
                                                              data.surely_real, data.maybe_real, data.indecise,
                                                              data.maybe_syn, data.surely_syn, data.date))
    return real_like_responses


def __real_syn_view_mode(real_syn_data):
    real_syn_responses = []
    for data in real_syn_data:
        real_syn_responses.append(RealSynView(data.id, data.real_image_id, data.syn_image_id, data.real_image_response,
                                              data.syn_image_response, data.date))

    return real_syn_responses
