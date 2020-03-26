import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.conf import settings

from api.libs.api_response import ApiResponse
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
        api_response = ApiResponse()

        try:
            text_data_json = json.loads(text_data)
        except json.JSONDecodeError as e:
            print("json.JSONDecodeError", e)
            api_response.failure("json format is invalid")
            api_response.value(text_data)
            self._send_client_sync(api_response.response)
        else:
            # TODO validate
            # validate(text_data_json)

            op = text_data_json["op"]

            if op == "listen":
                self.sensor_names = text_data_json["v"]

                # Send message to room group
                api_response.success()

                if tick_nos := self.sensor_ticks():
                    self.run_tick()
            elif op == "scan":
                api_response.success()
                api_response.value(
                    # dummy scanned info
                    [{"name": "scaned_sensor_name", "id": "scaned_sensor_id"}]
                )
            elif op == "stop":
                self.stop_tick()
                api_response.success("Worker stopped")
            else:
                api_response.failure("No operation")

            self._send_client_sync(api_response.response)

    def _send_client_sync(self, result):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "send_client", "result": result}
        )

    def send_client(self, event):
        self.send(json.dumps(event["result"]))

    # def send_ws(self):
    def sensor_value(self):
        # TODO: 今はBME280固定
        self._send_client_sync({"BME0": Bme280Handler.main()})

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
