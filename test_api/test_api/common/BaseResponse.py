class BaseResponse:
    def __init__(self, success, message=None, data=None, errors=None):
        self.success = success
        self.message = message
        self.data = data
        self.errors = errors

    @classmethod
    def success_response(cls, data=None, message=None):
        return cls(success=True, data=data, message=message)

    @classmethod
    def error_response(cls, message, errors=None):
        return cls(success=False, message=message, errors=errors)