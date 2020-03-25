from django.conf import settings


class ParseApiParams:
    """apiのクエリパラメータ解析
    """

    SENSOR_SENSOR_NAMES = [
        settings.SENSOR_NAME_TICK,
        settings.SENSOR_NAME_BME,
    ]

    WRITE_SENSOR_NAMES = [
        settings.SENSOR_NAME_TICK,
        settings.SENSOR_NAME_GP,
    ]

    READ_SENSOR_NAMES = [
        settings.SENSOR_NAME_ADC,
    ]

    def __init__(self, params, mode):
        # paramsのtypeはdjango.http.request.QueryDict
        self._params = params
        # write read sensor scan
        self._mode = mode

        self._result = {}
        self._target_sensor_name = ""
        self._ids = []
        self._parse()

    def _parse(self):
        if self._mode == "sensor":
            self.ids = self._params.get("ids")
            for sensor_id in self.ids:
                self._parse_main(sensor_id, self.SENSOR_SENSOR_NAMES)
        elif self._mode == "write":
            self.target = self._params.get("target", "")
            self._parse_main(
                self.target, self.WRITE_SENSOR_NAMES, ["value", "interval"]
            )

        elif self._mode == "read":
            self.target = self._params.get("target", "")
            self._parse_main(self.target, self.READ_SENSOR_NAMES, ["type", "sampling"])
        else:
            pass

    def _parse_main(self, target_sensor_name, sensor_names, input_values=[]):
        """sensor名とsensor番号を分離し値を取得

        Args:
            target_name (str): 対象センサー名
            sensor_names (list): 解析対象のセンサー名一覧
        """
        for sensor_name in sensor_names:
            if target_sensor_name.startswith(sensor_name):
                if self._result.get(sensor_name, 0) == 0:
                    self._result[sensor_name] = []
                try:
                    if sensor_name == settings.SENSOR_NAME_ADC:
                        no = self._parse_adc_no(target_sensor_name)
                    else:
                        no = self._parse_no(target_sensor_name, sensor_name)
                except ValueError as e:
                    print(f"sensor_name {target_sensor_name} is not include no:", e)
                else:
                    sensor_info = self._sensor_info(
                        no, target_sensor_name, input_values
                    )
                    self._result[sensor_name].append(sensor_info)

    def _sensor_info(self, no, target_sensor_name, input_values):
        sensor_info = {"no": no, "name": target_sensor_name}
        for key in input_values:
            val = self._params.get(key, "")
            if val:
                sensor_info[key] = val
        return sensor_info

    def has_bme(self):
        return settings.SENSOR_NAME_BME in self._result

    def has_tick(self):
        return settings.SENSOR_NAME_TICK in self._result

    def has_gp(self):
        return settings.SENSOR_NAME_GP in self._result

    def gp(self, ind):
        return self._result[settings.SENSOR_NAME_GP][ind]

    def bme(self, ind):
        return self._result[settings.SENSOR_NAME_BME][ind]

    def adc(self, ind):
        return self._result[settings.SENSOR_NAME_ADC][ind]

    def _parse_no(self, target_str, sensor_name):
        return int(target_str.replace(sensor_name, ""))

    def _parse_adc_no(self, target_str):
        """
        A(n) Port is Pin (n+14) Port
        ex) A0 Port is Pin 14 Port
        """
        return self._parse_no(target_str, "ADC") + 14

    def tick(self, ind):
        return self._result[settings.SENSOR_NAME_TICK][ind]

    @property
    def target(self):
        return self._target_sensor_name

    @target.setter
    def target(self, target_sensor_name):
        self._target_sensor_name = target_sensor_name

    @property
    def ids(self):
        return self._ids

    @ids.setter
    def ids(self, ids):
        # TODO: ids内の値に関してvalidation追加する
        self._ids = ids
