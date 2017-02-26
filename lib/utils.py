from decimal import Decimal
from flask import (g, jsonify, request)
from functools import wraps
import json
from sqlalchemy.ext.declarative import DeclarativeMeta
from lib import session
from .exceptions import APIException
from lib.constants import API


def handle_exceptions(func):
    @wraps(func)
    def handler(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except APIException as err:
            session.rollback()
            return jsonify(
                status=API.STATUS.FAILED,
                error={'code': err.code, 'msg': err.msg, 'details': err.details}
            ), API.HTTP.UNPROCESSABLE

        except Exception as err:
            session.rollback()
            return jsonify(
                status=API.STATUS.FAILED,
            ), API.HTTP.UNEXPECTED

    return handler


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            for field in [x for x in vars(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    if isinstance(data, int) or isinstance(data, float) or isinstance(data, Decimal):
                        if isinstance(data, Decimal):
                            fields[field] = float(data)
                        else:
                            fields[field] = data
                    else:
                        json.dumps(data)
                        fields[field] = data
                except TypeError:
                    fields[field] = str(data)
            return fields

        return json.JSONEncoder.default(self, obj)
