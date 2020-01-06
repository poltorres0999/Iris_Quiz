import csv
import json
import os
import time
import glob

from flask import render_template, request, Response, send_file
from flask_login import login_required

from app import app
from app import session
from controllers.real_like_controller import RealLikeController
from controllers.real_syn_controller import RealSynController
from models.view_models.real_like_view import RealLikeWithImageViewModel
from models.view_models.real_syn_view import RealSynView

real_like_controller = RealLikeController()
real_syn_controller = RealSynController()
TITLE = "Iris quiz responses"
real_like_columns = ["Response ID", "Image ID", "Image type", "Surely real", "Maybe real", "Indecise", "Maybe synthetic", "Surely synthetic", "Date"]
real_syn_columns = ["Response ID", "Real image ID", "Synthetic Image ID", "Real Image Response", "Syn image response", "Date"]


@app.route('/quiz_responses')
@login_required
def show_response_table():

    if request.args.get("current_table") is None:
        current_table = "real_like_table"
    else:
        current_table = request.args.get("current_table")

    if "data_timeout" not in session:
        json_real_like_data, json_real_syn_data = __load_response_data()
        __store_session_data(real_like_data=json_real_like_data, real_syn_data=json_real_syn_data)
    else:
        if time.time() - session["data_timeout"] > 30:
            json_real_like_data, json_real_syn_data = __load_response_data()
            __store_session_data(real_like_data=json_real_like_data, real_syn_data=json_real_syn_data)
        else:
            json_real_like_data = session['real_like_data']
            json_real_syn_data = session['real_syn_data']

    return render_template('iris_responses.html',
                           real_like_columns=real_like_columns,
                           real_like_data=json_real_like_data,
                           real_syn_data=json_real_syn_data,
                           real_syn_columns=real_syn_columns,
                           current_table=current_table,
                           title=TITLE)


@app.route('/quiz_responses/download/<response_type>/<format>')
@login_required
def download_quiz_responses(response_type, format):
    __clean_tmp_csv()
    if response_type == "image_quality":
        data = __load_image_quality_responses()
    elif response_type == "real_syn":
        data = __load_real_syn_responses()

    if format == "json":
        formatted_data = json.dumps({f"{response_type}": [ob.__dict__ for ob in data]})
        return Response(
            formatted_data,
            mimetype="application/json",
            headers={"Content-disposition": f"attachment; filename=quiz_{response_type}_responses.{format}"})

    elif format == "csv":
        if response_type == "image_quality":
            headers = real_like_columns
        elif response_type == "real_syn":
            headers = real_syn_columns
        file_path = __responses_to_csv(data, headers)

        return send_file(file_path, as_attachment=True,
                         attachment_filename=f"quiz_{response_type}_responses.{format}",
                         mimetype="text/csv")


def __load_response_data():
    real_like_data = __load_image_quality_responses()
    real_syn_data = __load_real_syn_responses()
    json_real_like_data = json.dumps({"data": [ob.__dict__ for ob in real_like_data]})
    json_real_syn_data = json.dumps({"data": [ob.__dict__ for ob in real_syn_data]})

    return json_real_like_data, json_real_syn_data


def __load_image_quality_responses():
    real_like_responses = real_like_controller.get_all_responses_with_image()
    real_like_view_data = __real_like_view_model(real_like_responses)

    return real_like_view_data


def __load_real_syn_responses():
    real_syn_responses = real_syn_controller.get_all_responses()
    real_syn_view_data = __real_syn_view_mode(real_syn_responses)

    return real_syn_view_data


def __store_session_data(real_like_data, real_syn_data):
    session['real_like_data'] = real_like_data
    session['real_syn_data'] = real_syn_data
    session['data_timeout'] = time.time()


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


def __responses_to_csv(responses, headers):
    temp_file_path = f"{app.config['TMP_CSV']}/{time.time()}.csv"
    with open(temp_file_path, 'w', newline='') as csvfile:
        response_writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        response_writer.writerow(headers)
        for response in responses:
            response_writer.writerow([value for attr, value in response.__dict__.items()])

    return temp_file_path


def __clean_tmp_csv():
    file_pahts = glob.glob(f"{app.config['TMP_CSV']}/*.csv")
    if len(file_pahts) > 0:
        for file in file_pahts:
            creation_time = float(os.path.splitext(os.path.basename(file))[0])
            if time.time() - creation_time > int(app.config["FILE_TIMEOUT"]):
                os.remove(file)


