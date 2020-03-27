from django.conf import settings


class ParseApiParams:
    """apiのクエリパラメータ解析
    """

    MODE_SENSOR = "sensor"
    MODE_WRITE = "write"
    MODE_READ = "read"
    MODE_LISTEN = "listen"

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

    LISTEN_SENSOR_NAMES = [
        settings.SENSOR_NAME_TICK,
    ]

    API_MODE = {
        MODE_SENSOR: {
            "target_key": "ids",
            "sensor_name_list": SENSOR_SENSOR_NAMES,
            "other_keys": [],
        },
        MODE_WRITE: {
            "target_key": "target",
            "sensor_name_list": WRITE_SENSOR_NAMES,
            "other_keys": ["value", "interval"],
        },
        MODE_READ: {
            "target_key": "target",
            "sensor_name_list": READ_SENSOR_NAMES,
            "other_keys": ["type", "sampling"],
        },
        MODE_LISTEN: {
            "target_key": "v",
            "sensor_name_list": LISTEN_SENSOR_NAMES,
            "other_keys": [],
        },
    }

    def __init__(self, params, mode):
        self._params = params
        self._mode = mode
        self._result = {}
        self._parse()

    def _parse(self):
        """_paramsを解析し_result変数に結果保存
        """
        for target in self._targets:
            self._parse_main(target)

    @property
    def _setting_params(self):
        """モードごとに設定されたdictを返す

        Returns:
            dict: API_MODE内の該当するmode
        """
        return self.API_MODE[self._mode]

    @property
    def _targets(self):
        """解析対象のキーを配列で返す
        対象が一つの場合、[]で配列にする

        Returns:
            list: 解析対象のキー名一覧 ex) ["TICK0", "BME0]
        """
        target = self._params.get(self._setting_params["target_key"])
        return target if type(target) == list else [target]

    def _parse_main(self, target_name):
        """sensor名とsensor番号を分離し各sensor名ごとに情報を構造化し_result変数に結果保存

        Args:
            target_name (str): 対象センサー名 ex) BME0, TICK1

        _result変数に、例として以下の形式で保存する
            {
                "BME":[{"no":0, "temperature":26.0,・・・}],
                "TICK":[{"no":1,・・・}],
                ・・・
            }
        """
        sensor_names = self._setting_params["sensor_name_list"]
        for sensor_name in sensor_names:
            if target_name.startswith(sensor_name):
                if self._result.get(sensor_name, 0) == 0:
                    self._result[sensor_name] = []
                try:
                    no = self._parse_no(target_name, sensor_name)
                except ValueError as e:
                    print(f"sensor_name {target_name} is not include no:", e)
                else:
                    sensor_info = self._sensor_info(no, target_name)
                    self._result[sensor_name].append(sensor_info)

    def _sensor_info(self, no, target_name):
        """sensorに関する情報を返す

        Args:
            no (str): sensor番号
            target_name (str): sensor名

        Returns:
            dict: センサー毎の付属情報
            ex)
                {
                    "no": 0,
                    "name": "TICK0",
                    "interval": 1000,
                }
        """
        sensor_info = {"no": no, "name": target_name}
        for key in self._setting_params["other_keys"]:
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

    def _parse_no(self, target_name, sensor_name):
        """target_nameからセンサー番号を返す

        Args:
            target_name (str): ターゲット名 ex) "BME0"
            sensor_name (str): センサー名 ex) "BME"

        Returns:
            int: センサー番号 ex) 0
        """
        if sensor_name == settings.SENSOR_NAME_ADC:
            no = self._parse_adc_no(target_name)
        else:
            no = self._parse_no_main(target_name, sensor_name)
        return no

    def _parse_no_main(self, target_name, sensor_name):
        """センサー番号返すメイン処理
        """
        return int(target_name.replace(sensor_name, ""))

    def _parse_adc_no(self, target_str):
        """
        A(n) Port is Pin (n+14) Port
        ex) A0 Port is Pin 14 Port
        """
        return self._parse_no_main(target_str, "ADC") + 14

    def tick(self, ind):
        return self._result[settings.SENSOR_NAME_TICK][ind]
