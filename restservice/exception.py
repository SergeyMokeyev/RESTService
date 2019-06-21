class RESTError(Exception):
    def __init__(self, error, message=None, detail=None):
        self.error = error
        self.message = message
        self.detail = detail
