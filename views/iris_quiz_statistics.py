from flask import render_template
from flask_paginate import Pagination, get_page_args
from app import app
from controllers.real_like_controller import RealLikeController
from controllers.real_syn_controller import RealSynController

real_like_controller = RealLikeController()
real_syn_controller = RealSynController()


@app.route("/quiz_statistics", methods=['GET'])
def show_statistics():
    total_bar_data, syn_bar_data, real_bar_data, bar_labels = __responses_bar_chart_metadata()
    syn_dou_data, syn_dou_labels = __syn_dou_chart_metadata()
    real_dou_data, real_dou_labels = __real_dou_chart_metadata()

    total_bar_colors = ["#9eb2f0", "#a1d9e6", "#efc9c5", "#f3d7d7", "#f5ecdd"]
    syn_bar_colors = ["#aaaaaa", "#d2d0d1", "#e8e6e7", "#e1cecd", "#d6a6a3"]
    real_bar_colors = ["#3985e0", "#5090de", "#4da8e4", "#7fc0eb", "#c2ddef"]
    total_bar_label = "Overall image quality of Real and Synthetic images"
    syn_bar_label = "Overall image quality of Synthetic images"
    real_bar_label = "Overall image quality of Real images"
    bar_label = "Numer of responses"

    syn_dou_colors = ["#ebdbd9", "#99CCFF"]
    syn_dou_label = "Synthetic image response"
    real_dou_colors = ["#0080FF", "#d88764"]
    real_dou_label = "Real image response"

    return render_template('quiz_statistics.html', tota_bar_data=total_bar_data, bar_labels=bar_labels,
                           real_bar_data=real_bar_data, syn_bar_data=syn_bar_data, syn_bar_label=syn_bar_label,
                           total_bar_colors=total_bar_colors, syn_bar_colors=syn_bar_colors,
                           real_bar_colors=real_bar_colors, bar_label=bar_label, total_bar_label=total_bar_label,
                           real_bar_label=real_bar_label, syn_dou_colors=syn_dou_colors, syn_dou_label=syn_dou_label,
                           real_dou_colors=real_dou_colors, real_dou_label=real_dou_label, syn_dou_data=syn_dou_data,
                           syn_dou_labels=syn_dou_labels, real_dou_data=real_dou_data, real_dou_labels=real_dou_labels)


def __responses_bar_chart_metadata():
    total_bar, syn_bar_data, real_bar_data = real_like_controller.get_responses_sum_divided()
    bar_labels = ["Surely real", "Maybe Real", "Indecise", "Maybe synthetic", "Surely synthetic"]

    return total_bar, syn_bar_data, real_bar_data, bar_labels


def __syn_dou_chart_metadata():
    syn_wrong_dou_data = real_syn_controller.count_wrong_real_responses()
    syn_correct_dou_data = real_syn_controller.count_correct_real_responses()
    syn_dou_labels = ["Synthetic image voted as synthetic", "Synthetic images voted as real"]

    return [syn_correct_dou_data, syn_wrong_dou_data], syn_dou_labels


def __real_dou_chart_metadata():
    real_wrong_dou_data = real_syn_controller.count_wrong_syn_responses()
    real_correct_dou_data = real_syn_controller.count_correct_syn_responses()
    real_dou_labels = ["Real image voted as real", "Real images voted as synthetic"]

    return [real_correct_dou_data, real_wrong_dou_data], real_dou_labels

