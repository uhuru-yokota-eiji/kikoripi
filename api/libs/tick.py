from django.conf import settings
from asgiref.sync import async_to_sync
import json
from api.libs.interval_processing import IntervalProcessing


class Tick:

    def __init__(self, channel_layer, nos):
        # self.channels_layers = channels_layers
        self.channel_layer = channel_layer
        self.nos = nos  # NOTICE: 現在未使用。同じTICKを複数利用した場合を想定
        self._value = 0
        self.group_name = settings.CHANNEL_GROUP_NAME
        self.interval_proccess = None

    def start(self, interval):
        self.stop()
        self.interval_proccess = IntervalProcessing(
            interval / 1000, self._sensor_value)
        self.interval_proccess.start()

    def stop(self):
        if type(self.interval_proccess) == IntervalProcessing:
            self.interval_proccess.stop()

    def _sensor_value(self):
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'send_client',
                # NOTICE: no=0で固定。今後複数扱うようであればself.nosを利用する。
                'result':
                {
                    settings.SENSOR_NAME_TICK + "0": self.value
                }
            }
        )

    def send_client(self, event):
        self.send(json.dumps(event['result']))

    @property
    def value(self):
        self._value = 1 if self._value == 0 else 0
        return self._value
