import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.conf import settings

from api.libs.api_response import ApiResponse
from api.libs.parse_api_params import ParseApiParams
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
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # TODO: close_code が何か調べる
        print("disconnect", close_code)
        self.stop_tick()
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
        else:
            # TODO validate
            # validate(text_data_json)
            op = text_data_json["op"]
            if op == "listen":
                self.sensor_names = text_data_json["v"]
                api_response.success()

                parse = ParseApiParams(text_data_json, mode="listen")
                # NOTICE: 配列の最初固定。複数対応は必要なときに実施する
                if parse.tick(0):
                    self.run_tick(0)
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

    def run_tick(self, no):
        self.tick = self.tick or Tick(no)
        self.tick.start(self.channel_layer)

    def stop_tick(self):
        if type(self.tick) == Tick:
            self.tick.stop()
