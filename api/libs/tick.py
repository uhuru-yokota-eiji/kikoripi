from django.conf import settings
from asgiref.sync import async_to_sync
import json
from api.libs.interval_processing import IntervalProcessing
from api.models import TickInterval
import time
import threading


class Tick:

    DEFAULT_INTERVAL = 1000

    def __init__(self, channel_layer, nos):
        # self.channels_layers = channels_layers
        self.channel_layer = channel_layer
        self.nos = nos  # NOTICE: 現在未使用。同じTICKを複数利用した場合を想定
        self._value = 0
        self.interval = self.DEFAULT_INTERVAL
        self.group_name = settings.CHANNEL_GROUP_NAME
        self.interval_proccess = None
        self.is_stop = True

    def start(self):
        self.stop()
        self.interval_proccess = IntervalProcessing(
            self._interval / 1000, self._send_sensor_value)
        self.interval_proccess.start()
        self.is_stop = False
        self._update_interval()

    def stop(self):
        if type(self.interval_proccess) == IntervalProcessing:
            self.interval_proccess.stop()
            self.is_stop = True

    def _send_sensor_value(self):
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'send_client',
                'result':
                {
                    # NOTICE: no=0で固定。今後複数扱うようであればself.nosを利用する。
                    settings.SENSOR_NAME_TICK + "0": self._sensor_value,
                    "timestamp":time.time()
                }
            }
        )

    def send_client(self, event):
        self.send(json.dumps(event['result']))

    def _update_interval(self):
        _thread = threading.Thread(target=self._update_interval_run)
        _thread.start()

    def _update_interval_run(self):
        while not self.is_stop:
            time.sleep(1)
            if(self._interval_saved and (self.interval != self._interval_saved)):
                self.set_interval = self._interval_saved
                self.start()
                break

    @property
    def _sensor_value(self):
        self._value = 1 if self._value == 0 else 0
        return self._value

    @property
    def _interval(self):
        self.interval = self._interval_saved or self.interval
        return self.interval

    @property
    def _interval_saved(self):
        if(t := TickInterval.objects.all().first()):
            return t.interval
        else:
            return None

    @_interval.setter
    def _interval(self, interval):
        if(interval):
            self.interval = interval
