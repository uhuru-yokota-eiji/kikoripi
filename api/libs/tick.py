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
    INSTANCE_RUNNING = None

    def __init__(self, no):
        self.no = str(no)
        self.channel_layer = None
        self._value = 0
        self.interval = self.DEFAULT_INTERVAL
        self.group_name = settings.CHANNEL_GROUP_NAME
        self.interval_proccess = None
        self.is_stop = True

    def start(self, channel_layer):
        """interval(ms) ごとに定期処理する

        Args:
            channel_layer (channels.layers.InMemoryChannelLayer):
                websocket通信を管理するchannelのlayer
        """
        self.channel_layer = channel_layer

        self.stop()
        self.interval_proccess = IntervalProcessing(
            self._interval / 1000, self._send_sensor_value
        )
        self.interval_proccess.start()

        # NOTICE: globals()[self.__class__.__name__]は自身のクラス名
        globals()[self.__class__.__name__].INSTANCE_RUNNING = self

        self.is_stop = False

    def stop(self):
        """定期処理を停止する
        """
        if type(self.interval_proccess) == IntervalProcessing:
            self.interval_proccess.stop()
            self.is_stop = True

    def _send_sensor_value(self):
        """定期処理の中身。値をクライアントに送信する。
        """
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                "type": "send_client",
                "result": {self.sensor_name: self._sensor_value_ws},
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

        TickInterval.update_interval(_interval_ms)

        self = cls.INSTANCE_RUNNING
        if self and self._is_run():
            self.interval_proccess.interval(self._interval / 1000)

    def _is_run(self):
        """定期処理が稼働中か判定

        Returns:
            bool: 稼働中ならTrue
        """
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
            json["msg"]: 任意のメッセージ
            json["id"]: wss用識別子  #TODO 現在はとりいそぎsensor_name
        """

        value = {"msg": "Use listen interface for WebSocket", "id": self.sensor_name}
        return value

    @property
    def _interval(self):
        """intervalの値の取得
        保存済みがあればそれを優先し、無ければインスタンス変数を参照する

        Returns:
            int: interval(s)
        """
        self.interval = self._interval_saved or self.interval
        return self.interval

    @property
    def _interval_saved(self):
        """保存済みintervalを返す

        Returns:
            int or None: 保存済みinterval(ms)
        """
        t = TickInterval.objects.all().first()
        return t.interval if t else None

    @_interval.setter
    def _interval(self, interval):
        """intervalのsetter

        Args:
            interval (int): interval(ms)
        """
        if interval > 0:
            self.interval = interval
        else:
            print(f"interval value {interval} is invalid")
