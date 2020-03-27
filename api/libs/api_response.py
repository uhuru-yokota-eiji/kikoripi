class ApiResponse:

    KEY_RESULT = "result"
    KEY_MESSAGE = "msg"
    KEY_VALUE = "v"
    VALUE_RESULT_SUCCESS = "success"
    VALUE_RESULT_ERROR = "error"
    VALUE_MESSAGE_SUCCESS = "Success"

    def __init__(self, args={}):
        self._response = {}
        if not args:
            self.set_params(args)

    def set_params(self, kwargs):
        """レスポンスとして必要なパラメータをdict型でセットする
        Args:
            kwargs (dict): 返したいパラメータ。ex) {"intervale": 2000}
        """
        for k, v in kwargs.items():
            self._set_param(k, v)

    def _set_param(self, key, value):
        # TODO: key, valueのvalidation追加
        self._response[key] = value

    def success(self, msg=""):
        """処理正常時のレスポンス設定

        Args:
            msg (str, optional): レスポンスのメッセージを設定する. Defaults to "".
        """
        if not msg:
            msg = self.VALUE_MESSAGE_SUCCESS

        params = {self.KEY_RESULT: self.VALUE_RESULT_SUCCESS, self.KEY_MESSAGE: msg}
        self.set_params(params)

    def failure(self, msg=""):
        """処理失敗時のレスポンス設定

        Args:
            msg (str, optional): レスポンスのメッセージを設定する. Defaults to "".
        """
        if not msg:
            msg = self.RESULT_VALUE_ERROR

        params = {self.KEY_RESULT: self.VALUE_RESULT_ERROR, self.KEY_MESSAGE: msg}
        self.set_params(params)

    def value(self, v):
        """固定のvalueキー（KEY_VALUEキー）の値をセットする

        Args:
            v (str or int): センサー値などの値
        """
        self.set_params({self.KEY_VALUE: v})

    @property
    def response(self):
        return self._response
