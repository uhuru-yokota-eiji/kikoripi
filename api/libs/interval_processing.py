import time
import threading


class IntervalProcessing:
    """定期実行用処理クラス
    _interval間隔での定期実行処理をスレッドに投げ非同期で処理する
    この定期実行処理（_scheduleメソッド）自体をスレッドにより非同期処理する
    """

    def __init__(self, interval, method, args=()):
        self._interval = interval
        self._method = method
        self._args = args
        self._stop = True
        self._thread = threading.Thread(target=self._schedule)

    def _schedule(self):
        """_interval間隔で定期実行をスレッドに投げる
        """
        base_time_sec = time.time()
        while not self._stop:
            t = threading.Thread(target=self._method, args=self._args)
            t.start()
            self._sleep_interval(base_time_sec)

    def _sleep_interval(self, base_time_sec):
        """_interval間隔の誤差を吸収してsleepさせる

        Args:
            base_time_sec (int): 定期実行開始時間
        """
        next_time_sec = (
            (base_time_sec - time.time()) % self._interval
        ) or self._interval
        time.sleep(next_time_sec)

    def start(self):
        """定期実行を開始
        """
        self._stop = False
        self._thread.start()

    def stop(self):
        """定期実行を停止
        """
        self._stop = True

    def interval(self, interval):
        self._interval = interval
