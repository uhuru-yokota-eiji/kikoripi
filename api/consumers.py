import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.conf import settings

from api.libs.bme280_handler import Bme280Handler
from api.libs.tick import Tick


class ApiConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        self.op = ""
        self.sensor_names = []
        self.room_group_name = settings.CHANNEL_GROUP_NAME
        self.interval_proccess = None
        self.tick = None
        super().__init__(*args, **kwargs)

    def connect(self):
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # TODO: close_code が何か調べる
        print("disconnect", close_code)
        self.stop_tick()
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        # TODO: jsonじゃない場合のエラー処理が必要
        text_data_json = json.loads(text_data)

        # TODO validate
        # validate(text_data_json)

        op = text_data_json["op"]
        if op == "listen":
            self.sensor_names = text_data_json["v"]

            # Send message to room group
            self.send_client_sync(text_data_json)

            if tick_nos := self.sensor_ticks():
                self.run_tick()
        elif op == "scan":
            self.send_client_sync({"result": "ok"})
        elif op == "stop":
            self.stop_tick()
        elif op == "debug":  # debug mode for dev
            self.send_client_sync({"v": self.sensor_names})
        else:
            pass

    def send_client_sync(self, result):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "send_client", "result": result}
        )

    def send_client(self, event):
        self.send(json.dumps(event["result"]))

    # def send_ws(self):
    def sensor_value(self):
        # TODO: 今はBME280固定
        self.send_client_sync({"BME0": Bme280Handler.main()})

    def run_tick(self):
        if tick_nos := self.sensor_ticks():
            self.tick = self.tick or Tick(tick_nos[0])
            self.tick.start(self.channel_layer)

    def stop_tick(self):
        if type(self.tick) == Tick:
            self.tick.stop()

    def sensor_ticks(self):
        tick_nos = []
        for sensor_name in self.sensor_names:
            if sensor_name.startswith(settings.SENSOR_NAME_TICK):
                ticks = sensor_name.split(settings.SENSOR_NAME_TICK)
                tick_nos.append(ticks[1])
        return tick_nos
