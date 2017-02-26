from flask import (Blueprint, jsonify, render_template, request, make_response)
from .model import Question
from lib.constants import (API)
from lib.utils import handle_exceptions

blueprint = Blueprint("question", __name__, url_prefix="/questions")


@blueprint.route("", methods=["POST"])
@handle_exceptions
def create():

    question = Question.create(request.get_json())

    return jsonify(
        status=API.STATUS.SUCCESS,
        question=question
    ), API.HTTP.OK


@blueprint.route("/<question_id>", methods=["GET"])
@handle_exceptions
def get(question_id):

    question = Question.get(question_id=question_id)

    return jsonify(
        status=API.STATUS.SUCCESS,
        question=question
    ), API.HTTP.OK


@blueprint.route("/<question_id>.xml", methods=["GET", "POST"])
@handle_exceptions
def question_xml(question_id):

    question = Question.get(question_id=question_id)
    last = False
    if question_id == "3":
        last = True
    response = make_response(render_template('twiml.xml', question=question, last=last))
    response.headers["Content-Type"] = "application/xml"
    return response


@blueprint.route("/last.xml", methods=["GET", "POST"])
# @handle_exceptions
def last_xml():
    response = make_response("<?xml version='1.0' encoding='utf-8'?><Response><Say>Thank you!</Say></Response>")
    response.headers["Content-Type"] = "application/xml"
    return response
