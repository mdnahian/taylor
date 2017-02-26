from flask import (Blueprint, jsonify, request, make_response)
from .model import Twiml
from lib.constants import (API)
from lib.utils import handle_exceptions

blueprint = Blueprint("twiml", __name__, url_prefix="/twimls")


@blueprint.route("", methods=["POST"])
@handle_exceptions
def create():

    twiml = Twiml.create(request.get_json())

    return jsonify(
        status=API.STATUS.SUCCESS,
        twiml=twiml
    ), API.HTTP.OK


@blueprint.route("/<twiml_id>.xml", methods=["GET"])
@handle_exceptions
def get(twiml_id):

    twiml = Twiml.get(twiml_id=twiml_id)
    response = make_response(twiml.xml)
    response.headers["Content-Type"] = "application/xml"
    return response
