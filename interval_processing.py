import asyncio


class IntervalProcessing:
    def __init__(self, interval, callback):
        self._interval = interval
        self._callback = callback
        asyncio.run(self._timer_loop())

    async def _timer_loop(self):
        task_main = asyncio.create_task(self._callback())
        task_loop = asyncio.create_task(self._next())
        await task_main
        await task_loop

    async def _next(self):
        await asyncio.sleep(self._interval)
        await self._timer_loop()


async def main_process():
    print(f"main_proccess start")
    await asyncio.sleep(3)
    print(f"main_proccess end")


if __name__ == '__main__':
    try:
        IntervalProcessing(1, main_process)
    except KeyboardInterrupt:
        print("entered Ctrl C")
