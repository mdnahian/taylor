from flask import (Blueprint, jsonify, render_template, request)
from .model import Interview
from lib.constants import (API)
from lib.utils import handle_exceptions

blueprint = Blueprint("interview", __name__, url_prefix="/interviews")


@blueprint.route("", methods=["POST"])
@handle_exceptions
def create():

    # json_interview = {
    #     # 'name': request.form['name'],
    #     'phone': '+16073388347'  #request.form['phone'],
    # }
    interview = Interview.create({})

    return jsonify(
        status=API.STATUS.SUCCESS,
        interview=interview
    ), API.HTTP.OK


@blueprint.route("", methods=["GET"])
@handle_exceptions
def welcome():
    return render_template('index.html')


@blueprint.route("/<interview_id>", methods=["GET"])
@handle_exceptions
def get(interview_id):

    interview = Interview.get(interview_id=interview_id)

    return jsonify(
        status=API.STATUS.SUCCESS,
        interview=interview
    ), API.HTTP.OK


@blueprint.route("/<interview_id>/actions/init_call", methods=["POST"])
@handle_exceptions
def init_call(interview_id):

    interview = Interview.init_call(interview_id=interview_id)

    return jsonify(
        status=API.STATUS.SUCCESS,
        interview=interview
    ), API.HTTP.OK


@blueprint.route("/<interview_id>/actions/fetch_recordings", methods=["POST"])
# @handle_exceptions
def fetch_recordings(interview_id):

    recordings = Interview.fetch_recordings(interview_id=interview_id)

    return jsonify(
        status=API.STATUS.SUCCESS,
        recordings=recordings
    ), API.HTTP.OK


@blueprint.route("/<interview_id>/actions/list_recordings", methods=["POST"])
@handle_exceptions
def list_recordings(interview_id):

    recordings = Interview.list_recordings(interview_id=interview_id)

    return jsonify(
        status=API.STATUS.SUCCESS,
        recordings=recordings
    ), API.HTTP.OK


@blueprint.route("/<interview_id>/actions/analyze", methods=["POST"])
# @handle_exceptions
def analyze(interview_id):

    result = Interview.analyze(interview_id=interview_id)

    return jsonify(
        status=API.STATUS.SUCCESS,
        result=result
    ), API.HTTP.OK


@blueprint.route("/<interview_id>/stats", methods=["GET"])
@handle_exceptions
def stats(interview_id):

    interview = Interview.get(interview_id=interview_id)
    return render_template('.html', interview=interview)
