class BaseConfig(object):

    VERSION = "0.1.0"
    TRAP_BAD_REQUEST_ERRORS = True


class DevelopmentConfig(BaseConfig):

    DEBUG = True
