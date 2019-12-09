from flask import render_template, request
from flask_paginate import Pagination, get_page_args
from app import app
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

    r_l_page, per_page_r_l, offset_r_l = get_page_args(page_parameter='real_like_table',
                                           per_page_parameter='per_page_real_like')

    if request.args.get("current_table") is None:
        current_table = "real_like_table"
    else:
        current_table = request.args.get("current_table")

    real_like_responses = real_like_controller.get_all_responses_with_image()
    total_real_like_responses = len(real_like_responses)
    real_like_view_data = real_like_view_model(real_like_responses)
    real_like_page = __get_page(real_like_view_data, offset=offset_r_l, num_elements=per_page_r_l)
    real_like_pagination = Pagination(page=r_l_page, per_page_parameter="per_page_real_like", page_parameter='real_like_table',
                                      per_page=per_page_r_l, total=total_real_like_responses,
                                      css_framework='bootstrap4')

    r_s_page, per_page_r_s, offset_r_s = get_page_args(page_parameter='real_syn_table', per_page_parameter='per_page_real_syn')

    real_syn_responses = real_syn_controller.get_all_responses()
    total_real_syn_responses = len(real_syn_responses)
    real_syn_view_data = __real_syn_view_mode(real_syn_responses)
    real_syn_page = __get_page(real_syn_view_data, offset=offset_r_s, num_elements=per_page_r_s)
    real_syn_pagination = Pagination(page=5, page_parameter='real_syn_table', per_page_parameter="per_page_real_syn",
                                     per_page=per_page_r_s, total=total_real_syn_responses,
                                     css_framework='bootstrap4')

    return render_template('iris_responses.html', real_like_columns=real_like_columns, real_like_page=real_like_page,
                           real_like_pagination=real_like_pagination, real_syn_columns=real_syn_columns,
                           real_syn_page=real_syn_page, real_syn_pagination=real_syn_pagination,
                           real_like_current_page=r_l_page, real_syn_current_page=r_s_page,
                           current_table=current_table)


def __get_page(data, offset=0, num_elements=10):
    return data[offset: offset + num_elements]


def real_like_view_model(real_like_data):
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
