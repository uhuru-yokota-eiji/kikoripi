class ApiResponse:

    RESULT_KEY = "result"
    RESULT_VALUE_SUCCESS = "success"
    RESULT_VALUE_ERROR = "error"
    MESSAGE_KEY = "msg"
    MESSAGE_VALUE_SUCCESS = "Success"

    def __init__(self, args={}):
        self._response = {}
        if not args:
            self.set_params(args)

    def set_params(self, kwargs):
        for k, v in kwargs.items():
            self._set_param(k, v)

    def _set_param(self, key, value):
        # TODO: key, valueのvalidation追加
        self._response[key] = value

    def success(self, msg=""):
        if not msg:
            msg = self.MESSAGE_VALUE_SUCCESS

        params = {self.RESULT_KEY: self.RESULT_VALUE_SUCCESS, self.MESSAGE_KEY: msg}
        self.set_params(params)

    def failure(self, msg=""):
        print("call failure")
        if not msg:
            msg = self.RESULT_VALUE_ERROR

        params = {self.RESULT_KEY: self.RESULT_VALUE_ERROR, self.MESSAGE_KEY: msg}
        self.set_params(params)

    @property
    def response(self):
        return self._response
