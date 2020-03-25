import json
import time

from asgiref.sync import async_to_sync
from django.conf import settings

from api.libs.interval_processing import IntervalProcessing
from api.models import TickInterval


class Tick:

    DEFAULT_INTERVAL = 1000
    # 実行中のインスタンスをクラスメソッドからアクセスできるように保存
    # 同時に１インスタンスのみ実行する想定
    running_instance = None

    def __init__(self, no):
        self.no = no
        self.channel_layer = None
        self._value = 0
        self.interval = self.DEFAULT_INTERVAL
        self.group_name = settings.CHANNEL_GROUP_NAME
        self.interval_proccess = None
        self.is_stop = True

    def start(self, channel_layer):
        self.channel_layer = channel_layer

        self.stop()
        self.interval_proccess = IntervalProcessing(
            self._interval / 1000, self._send_sensor_value
        )
        self.interval_proccess.start()

        # NOTICE: globals()[self.__class__.__name__]は自身のクラス名
        globals()[self.__class__.__name__].running_instance = self

        self.is_stop = False

    def stop(self):
        if type(self.interval_proccess) == IntervalProcessing:
            self.interval_proccess.stop()
            self.is_stop = True

    def _send_sensor_value(self):
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                "type": "send_client",
                "result": {
                    self.sensor_name: self._sensor_value_ws,
                    "timestamp": time.time(),
                },
            },
        )

    @property
    def sensor_name(self):
        return settings.SENSOR_NAME_TICK + self.no

    def send_client(self, event):
        self.send(json.dumps(event["result"]))

    @classmethod
    def update_interval(cls, _interval_ms):
        """intervalの更新
        Args:
            _interval_ms (int): msec
        """

        self = cls.running_instance

        self._update_stored_interval(_interval_ms)

        if self._is_run():
            self.interval_proccess.interval(self._interval / 1000)

    def _update_stored_interval(self, interval):
        """保存しているintervalの更新
        """
        t = TickInterval.objects.all().first()
        if t:
            t.interval = interval
            t.save()
        else:
            TickInterval.objects.create(interval=interval)

    def _is_run(self):
        return type(self.interval_proccess) == IntervalProcessing

    @property
    def _sensor_value_ws(self):
        """websocket通信時のセンサー値
        Returns:
            int: 1 or 0 を繰り返す
        """
        self._value = 1 if self._value == 0 else 0
        return self._value

    @property
    def sensor_value(self):
        """/sensor apiで取得時のセンサー値
        Returns:
            json["msg"]: 固定メッセージ
            json["id"]: wss用識別子  #TODO 現在はとりいそぎsensor_name
        """

        value = {"msg": "Use listen interface for WebSocket", "id": self.sensor_name}
        return value

    @property
    def _interval(self):
        self.interval = self._interval_saved or self.interval
        return self.interval

    @property
    def _interval_saved(self):
        t = TickInterval.objects.all().first()
        if t:
            return t.interval
        else:
            return None

    @_interval.setter
    def _interval(self, interval):
        if interval > 0:
            self.interval = interval
        else:
            print(f"interval value {interval} is invalid")
