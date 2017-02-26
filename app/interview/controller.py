from flask import (Blueprint, jsonify, request)
from .model import Interview
from lib.constants import (API)
from lib.utils import handle_exceptions

blueprint = Blueprint("interview", __name__, url_prefix="/interviews")


@blueprint.route("", methods=["POST"])
@handle_exceptions
def create():

    interview = Interview.create(request.get_json())

    return jsonify(
        status=API.STATUS.SUCCESS,
        interview=interview
    ), API.HTTP.OK


@blueprint.route("/<interview_id>", methods=["GET"])
@handle_exceptions
def get(interview_id):

    interview = Interview.get(interview_id=interview_id)

    return jsonify(
        status=API.STATUS.SUCCESS,
        interview=interview
    ), API.HTTP.OK


@blueprint.route("/<interview_id>/actions/<action>", methods=["POST"])
# @handle_exceptions
def action(interview_id, action):

    interview = Interview.action(interview_id=interview_id, action=action)

    return jsonify(
        status=API.STATUS.SUCCESS,
        interview=interview
    ), API.HTTP.OK
