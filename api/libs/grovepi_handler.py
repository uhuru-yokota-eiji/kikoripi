from ..apps import ApiConfig

if ApiConfig.is_env_raspi():
    import grovepi


class GrovepiHandler:
    """grovepiモジュールを開発用にオーバーライド
    ・開発環境と実機環境で同じコードで動作させることができる
    ・開発と実機の分岐処理を集約している
    """

    DUMMY_ANALOG_DATA = 999.999

    @classmethod
    def pinMode(cls, no, mode):
        if ApiConfig.is_env_raspi():
            grovepi.pinMode(no, mode)

    @classmethod
    def digitalWrite(cls, no, value):
        if ApiConfig.is_env_raspi():
            grovepi.digitalWrite(no, value)

    @classmethod
    def digitalRead(cls, no):
        if ApiConfig.is_env_raspi():
            return grovepi.digitalRead(no)

    @classmethod
    def analogRead(cls, no):
        if ApiConfig.is_env_raspi():
            return grovepi.analogRead(no)
        else:
            return cls.DUMMY_ANALOG_DATA
