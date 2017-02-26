class APIException(Exception):
    """API Exception, which is to be used for all failed responses."""
    def __init__(self, code, msg, details=None):
        self.code = code
        self.msg = msg
        self.details = details

    def __str__(self):
        return repr({"code": self.code, "msg": self.msg, "details": self.details})
