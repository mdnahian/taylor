from flask import (Blueprint, jsonify, request)
from .model import Recording
from lib.constants import (API)
from lib.utils import handle_exceptions

blueprint = Blueprint("recording", __name__, url_prefix="/recordings")


@blueprint.route("", methods=["POST"])
@handle_exceptions
def create():

    recording = Recording.create(request.get_json())

    return jsonify(
        status=API.STATUS.SUCCESS,
        recording=recording
    ), API.HTTP.OK


@blueprint.route("/<recording_id>", methods=["GET"])
@handle_exceptions
def get(recording_id):

    recording = Recording.get(recording_id=recording_id)

    return jsonify(
        status=API.STATUS.SUCCESS,
        recording=recording
    ), API.HTTP.OK


@blueprint.route("/<recording_id>/actions/<action>", methods=["POST"])
@handle_exceptions
def action(recording_id, action):

    recording = Recording.action(recording_id=recording_id, action=action)

    return jsonify(
        status=API.STATUS.SUCCESS,
        recording=recording
    ), API.HTTP.OK
