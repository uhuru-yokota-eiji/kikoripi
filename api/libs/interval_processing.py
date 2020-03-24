import time
import threading


class IntervalProcessing:
    def __init__(self, interval, method, args=()):
        self._interval = interval
        self._method = method
        self._args = args
        self._stop = True
        self._thread = threading.Thread(target=self._schedule)

    def _schedule(self):
        base_time_sec = time.time()
        next_time_sec = 0
        while not self._stop:
            _thread = threading.Thread(target=self._method, args=self._args)
            _thread.start()
            next_time_sec = (
                (base_time_sec - time.time()) % self._interval
            ) or self._interval
            time.sleep(next_time_sec)

    def start(self):
        self._stop = False
        self._thread.start()

    def stop(self):
        self._stop = True

    def interval(self, interval):
        """ intervalの更新
        :interval (sec)
        """
        self._interval = interval
