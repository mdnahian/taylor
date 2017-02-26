from flask import (Flask, jsonify)
from logging import (DEBUG, Formatter, INFO)
from logging.handlers import RotatingFileHandler
import os
from lib.constants import (API)
from lib.utils import (AlchemyEncoder)
from interview.controller import blueprint as interview
from recording.controller import blueprint as recording
from twiml.controller import blueprint as twiml

__all__ = ['create_app']

DEFAULT_BLUEPRINTS = [
    interview,
    recording,
    twiml
]


def create_app(config='Development'):
    """Creates a Flask app with all custom configurations."""
    app = Flask(__name__)
    app.json_encoder = AlchemyEncoder

    configure_app(app, config)
    configure_blueprints(app, DEFAULT_BLUEPRINTS)
    configure_extensions(app)
    configure_logging(app)
    configure_error_handlers(app)

    return app


def configure_app(app, config):
    """Sample configuration in config.py"""
    app.config.from_object('config.%sConfig' % config)


def configure_extensions(app):
    """Configure all extensions"""


def configure_blueprints(app, blueprints):
    """Configure blueprints from controllers."""
    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def configure_logging(app):
    """Configure loggin to file(info)."""

    log_file = os.path.join(app.config.get('LOG_FOLDER', '/tmp'), 'tranzip.log')
    info_file_handler = RotatingFileHandler(log_file, backupCount=10)
    info_file_handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'))

    if app.debug or app.testing:
        app.logger.setLevel(DEBUG)
        info_file_handler.setLevel(DEBUG)
    else:
        app.logger.setLevel(INFO)
        info_file_handler.setLevel(INFO)

    app.logger.addHandler(info_file_handler)


def configure_error_handlers(app):
    """Configure error handling."""
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify(
            status=API.STATUS.FAILED,
        ), API.HTTP.UNAUTHORIZED

    @app.errorhandler(403)
    def forbidden_page(error):
        return jsonify(
            status=API.STATUS.FAILED,
        ), API.HTTP.FORBIDDEN

    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify(
            status=API.STATUS.FAILED,
        ), API.HTTP.NOT_FOUND

    # @app.errorhandler(500)
    # def server_error_page(error):
    #     return jsonify(
    #         status=API.STATUS.FAILED,
    #     ), API.HTTP.UNEXPECTED
