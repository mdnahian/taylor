from flask import (Blueprint, jsonify, render_template, request, redirect, url_for)
from .model import Interview
from lib.constants import (API, BASE_URL)
from lib.utils import handle_exceptions
import time

blueprint = Blueprint("interview", __name__, url_prefix="/interviews")


@blueprint.route("", methods=["POST"])
@handle_exceptions
def create():

    json_interview = {
        'name': request.form['name']
    }
    interview = Interview.create(json_interview)

    return redirect(url_for('interview.init_call', interview_id=interview.interview_id), code=307)


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
    # return redirect(url_for('interview.stats', interview_id=interview.interview_id))


@blueprint.route("/alexa", methods=["POST"])
# @handle_exceptions
def alexa():
    interview = Interview.alexa(request.get_json())
    return jsonify(
        url=BASE_URL + "/interviews/" + str(interview.interview_id) + "/stats"
    ), API.HTTP.OK


@blueprint.route("/<interview_id>/actions/fetch_recordings", methods=["POST"])
@handle_exceptions
def fetch_recordings(interview_id):

    time.sleep(10)
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
@handle_exceptions
def analyze(interview_id):

    result = Interview.analyze(interview_id=interview_id)

    return jsonify(
        status=API.STATUS.SUCCESS,
        result=result
    ), API.HTTP.OK


@blueprint.route("/<interview_id>/stats", methods=["GET"])
@handle_exceptions
def stats(interview_id):

    interview, results, analysis = Interview.get_stats(interview_id=interview_id)
    return render_template('dashboard.html', interview=interview, results=results, analysis=analysis)


@blueprint.route("/<interview_id>/transcripts", methods=["GET"])
@handle_exceptions
def transcripts(interview_id):

    results = Interview.get_transcripts(interview_id=interview_id)
    return render_template('transcript.html', results=results)
