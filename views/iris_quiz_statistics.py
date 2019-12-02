from flask import render_template

from app import app
from controllers.real_like_controller import RealLikeController
from controllers.real_syn_controller import RealSynController

real_like_controller = RealLikeController()
real_syn_controller = RealSynController()


@app.route("/quiz_statistics", methods=['GET'])
def show_statistics():
    bar_data, bar_labels, bar_max = __responses_bar_chart_metadata()
    syn_dou_data, syn_dou_labels = __syn_dou_chart_metadata()
    real_dou_data, real_dou_labels = __real_dou_chart_metadata()

    bar_colors = ["#aaaaaa", "#d2d0d1", "#e8e6e7", "#e1cecd", "#d6a6a3"]
    bar_label = "Numer of responses"
    bar_foot_label = "Overall image quality of real and synthetic images"

    syn_dou_colors = ["#ebdbd9", "#99CCFF"]
    syn_dou_label = "Synthetic image response"
    real_dou_colors = ["#0080FF", "#d88764"]
    real_dou_label = "Real image response"

    return render_template('quiz_statistics.html', bar_data=bar_data, bar_labels=bar_labels, bar_max=bar_max,
                           bar_colors=bar_colors, bar_label=bar_label, bar_foot_label=bar_foot_label,
                           syn_dou_colors=syn_dou_colors, syn_dou_label=syn_dou_label, real_dou_colors=real_dou_colors,
                           real_dou_label=real_dou_label, syn_dou_data=syn_dou_data, syn_dou_labels=syn_dou_labels,
                           real_dou_data=real_dou_data, real_dou_labels=real_dou_labels)


def __responses_bar_chart_metadata():
    bar_data = real_like_controller.get_all_real_like_responses_sum()
    bar_max = max(bar_data)
    bar_labels = ["Surely real", "Maybe Real", "Indecise", "Maybe synthetic", "Surely synthetic"]

    return bar_data, bar_labels, bar_max


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
