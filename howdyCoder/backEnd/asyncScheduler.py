from ..commonUtil import mpLogging

import asyncio
import inspect
from typing import Callable, Any


class asyncScheduler:
    def __init__(self, lockBool=False):
        self.loop = None
        self.tasks = []

    # this function is useful for multiprocessing
    # only pass in objects that have a start() that is awaitable
    def initAndStart(self, objects):
        self.init()
        try:
            for obj in objects:
                self.addTask(obj.start())
        except TypeError:
            self.addTask(objects.start())
        self.start()

    def init(self):
        self.loop = asyncio.new_event_loop()

    def start(self):
        if self.loop is None:
            self.loop = asyncio.new_event_loop()
        self.loop.run_until_complete(asyncio.wait(self.tasks))

    def end(self):
        self.loop.close()

    def addTask(self, func: Callable, name: str = None):
        if inspect.iscoroutine(func):
            self.tasks.append(self.loop.create_task(func, name=name))
        else:
            mpLogging.warning("non coroutine function passed")

    def addTaskArgs(self, func: Callable, args: list[Any], name: str = None):
        self.tasks.append(self.loop.create_task(func(args)))
