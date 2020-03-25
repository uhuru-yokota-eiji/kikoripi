from django.conf import settings


class ParseApiParams:
    """apiのクエリパラメータ解析
    """

    SENSOR_NAMES = [
        settings.SENSOR_NAME_TICK,
        settings.SENSOR_NAME_BME,
        settings.SENSOR_NAME_GP,
    ]

    def __init__(self, params, mode):
        # paramsのtypeはdjango.http.request.QueryDict
        self._params = params
        # write read sensor scan
        self._mode = mode

        self._result = {}
        self._parse_url()

    def _parse_url(self):
        if self._mode == "sensor":
            for param_id in self._params_getlist("ids"):
                # sensor名と番号を分離
                for sensor_name in self.SENSOR_NAMES:
                    if param_id.startswith(sensor_name):
                        if self._result.get(sensor_name, 0) == 0:
                            self._result[sensor_name] = []
                        try:
                            if sensor_name == settings.SENSOR_NAME_ADC:
                                no = self._parse_adc_no(param_id)
                            else:
                                no = self._parse_no(param_id, sensor_name)
                        except ValueError as e:
                            print(f"param_id {param_id} is not include no:", e)
                        else:
                            self._result[sensor_name].append(no)
        elif self._mode == "read":
            pass
        elif self._mode == "write":
            pass
        else:
            pass

    def has_bme(self):
        return settings.SENSOR_NAME_BME in self._result

    def has_tick(self):
        return settings.SENSOR_NAME_TICK in self._result

    def _parse_no(self, target_str, sensor_name):
        return int(target_str.replace(sensor_name, ""))

    def _parse_adc_no(self, target_str):
        """
        A(n) Port is Pin (n+14) Port
        ex) A0 Port is Pin 14 Port
        """
        return int(target_str.replace("ADC", "")) + 14

    def _params_getlist(self, target):
        """複数ある値を取得し配列で返す
        getlistメソッドは django.http.request.QueryDict でないと呼べない

        Args:
            target (str): 取得対象のキー名
        Returns:
            [list]: キー名の値
        """
        return self._params.getlist(target)
