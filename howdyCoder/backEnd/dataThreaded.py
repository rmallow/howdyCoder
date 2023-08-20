from .dataFunc import dataFunc

from ..commonUtil import mpLogging

import threading
import queue


class dataThreaded(dataFunc):
    """
    Use dataThreaded for continuously calling a dataFunc getData in a seperate thread
    This will pass the results to a queue and retrieve those results in the get datafunc
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.outputQueue = None
        self.getterThread = None
        self.threadStarted = False

    def getData(self) -> dict:
        self.getDataLogging()
        if not self.threadStarted:
            self.outputQueue = queue.Queue()
            self.getterThread = threading.Thread(target=self.getDataThreaded)
            self.getterThread.start()
            self.threadStarted = True

        returnData = None
        n = len(self.outputQueue)
        for _ in range(n):
            rawVal = self.outputQueue.popleft()

            if returnData is None:
                returnData = rawVal
            else:
                for key, val in rawVal.items():
                    if key in returnData:
                        returnData[key] += val
                    else:
                        returnData[key] = val
        return self.dataModifications(returnData)

    def getDataThreaded(self):
        while True:
            # In case of Exceptions just keep trying
            try:
                self.getFunc(**{"outputQueue": self.outputQueue}, **self.parameters)
            except Exception as e:
                mpLogging.error(
                    f"Exception during data thread getter, trying again, exception: {e}"
                )
