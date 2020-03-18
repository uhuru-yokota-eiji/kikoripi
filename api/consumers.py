from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from api.libs import interval_processing
from api.libs.interval_processing import IntervalProcessing


class ChatConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        print("__init__", args)
        self.op = ""
        self.sensor_names = []
        self.interval = 1000
        self.room_group_name = 'wss_ws'
        self.interval_proccess = None
        super().__init__(*args, **kwargs)


    def connect(self):
        print("connect")
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        # self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        print("disconnect", close_code)
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        # TODO: jsonじゃない場合のエラー処理が必要
        text_data_json = json.loads(text_data)

        op = text_data_json['op']
        if(op == "listen"):
            self.sensor_names = text_data_json['v']
            self.interval = int(text_data_json['interval'])

            # Send message to room group
            self.send_client_sync(text_data_json)

            # send sensor value to ws server
            self.interval_proccess = IntervalProcessing(self.interval/1000, self.sensor_value)
            self.interval_proccess.start()
        elif(op == "scan"):
            self.send_client_sync({"result": "ok"})
        elif(op == "stop"):
            # TODO: close_codeが何か調べる
            self.disconnect(close_code=100)
            self.interval_proccess.stop()
        elif(op == "debug"):  # debug mode for dev
            self.send_client_sync(
                {"v": self.sensor_names, "interval": self.interval})
        else:
            pass

    def send_client_sync(self, result):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'send_client',
                'result': result
            }
        )

    def send_client(self, event):
        self.send(json.dumps({
            'result': event['result']
        }))

    # def send_ws(self):
    def sensor_value(self):
        # data = bme280.main()
        data = 123
        self.send_client_sync(
            {
                "result": {
                    "BME0": data  # NOTICE: とりいそぎ固定
                }
            }
        )

