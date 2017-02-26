class API:
    class HTTP:
        OK = 200
        CREATED = 201
        ACCEPTED = 202
        BAD_REQUEST = 400
        UNAUTHORIZED = 401
        NOT_FOUND = 404
        UNPROCESSABLE = 422
        UNEXPECTED = 500

    class STATUS:
        SUCCESS = True
        FAILED = False


class INTERVIEW:
    class STATUS:
        INIT = 1


BASE_URL = "http://5a86b22d.ngrok.io"
