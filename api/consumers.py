from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from api.libs.interval_processing import IntervalProcessing
from api.libs import bme280


# TODO: Chatという文字は消す
class ChatConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        self.op = ""
        self.sensor_names = []
        self.interval = 1000
        self.room_group_name = 'wss_ws'
        self.interval_proccess = None
        super().__init__(*args, **kwargs)


    def connect(self):
        print("connect")
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # TODO: close_code が何か調べる
        print("disconnect", close_code)
        self.stop_interval_processing()
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        # TODO: jsonじゃない場合のエラー処理が必要
        text_data_json = json.loads(text_data)

        # TODO validate
        # validate(text_data_json)

        op = text_data_json['op']
        if(op == "listen"):
            self.sensor_names = text_data_json['v']
            self.interval = int(text_data_json['interval'])

            # Send message to room group
            self.send_client_sync(text_data_json)

            self.run_interval_processing()
        elif(op == "scan"):
            self.send_client_sync({"result": "ok"})
        elif(op == "stop"):
            # TODO: close_codeが何か調べる
            self.disconnect(close_code=100)
            self.stop_interval_processing()
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
        self.send(json.dumps(event['result']))

    # def send_ws(self):
    def sensor_value(self):
        # TODO: 今はBME280固定
        data = bme280.main()
        self.send_client_sync(
            {
                "BME0": data
            }
        )

    def run_interval_processing(self):
        # send sensor value to ws server
        self.stop_interval_processing()
        self.interval_proccess = IntervalProcessing(
            self.interval / 1000, self.sensor_value)
        self.interval_proccess.start()



    def stop_interval_processing(self):
        if type(self.interval_proccess) == IntervalProcessing:
            self.interval_proccess.stop()
