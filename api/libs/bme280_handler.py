from ..apps import ApiConfig
import time

if ApiConfig.is_env_raspi():
    import smbus2
    import bme280


class Bme280Handler:
    """bme280モジュールを開発用にオーバーライド
    ・開発環境と実機環境で同じコードで動作させることができる
    ・開発と実機の分岐処理を集約している
    """

    @classmethod
    def main(cls):
        if ApiConfig.is_env_raspi():
            port = 1
            address = 0x76
            bus = smbus2.SMBus(port)
            data = bme280.sample(bus, address)
            return {
                "timestamp": data.timestamp.timestamp(),
                "temperature": data.temperature,
                "pressure": data.pressure,
                "humidity": data.humidity,
            }
        else:
            # dummy data
            return {
                "timestamp": time.time(),
                "temperature": 12.3,
                "pressure": 1234.567,
                "humidity": 45.67,
            }
