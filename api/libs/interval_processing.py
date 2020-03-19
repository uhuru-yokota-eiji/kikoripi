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
            next_time_sec = ((base_time_sec - time.time()) % self._interval) or self._interval
            time.sleep(next_time_sec)

    def start(self):
        self._stop = False
        self._thread.start()

    def stop(self):
        self._stop = True


def worker(args):
    # print(args)
    print(f"start worker {time.time()}")
    time.sleep(3)
    print(f"end worker {time.time()}")


if __name__ == '__main__':
    # schedule(3, worker, (0,))
    t = IntervalProcessing(1, worker, (0,))
    t.start()
    print("start thread")
    time.sleep(10)
    print("call stop")
    t.stop()
