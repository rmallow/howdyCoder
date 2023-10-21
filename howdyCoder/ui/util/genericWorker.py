from PySide6 import QtCore
from dataclasses import dataclass


def createThreadAndWorker(function, finished_slot, *args, **kwargs):
    thread = QtCore.QThread()
    worker = GenericWorker(function, *args, **kwargs)
    worker.moveToThread(thread)
    thread.started.connect(worker.run)
    worker.finished.connect(finished_slot)
    worker.finished.connect(thread.quit)
    worker.finished.connect(worker.deleteLater)
    thread.finished.connect(thread.deleteLater)
    thread.start()
    return thread, worker


@dataclass
class RunnableReturn:
    id_: int
    value: object


class GenericRunnableSignals(QtCore.QObject):
    finished = QtCore.Signal(RunnableReturn)


class GenericRunnable(QtCore.QRunnable):
    def __init__(self, id_: int, function, *args, **kwargs) -> None:
        super().__init__()
        self._id_ = id_
        self._function = function
        self._args = args
        self._kwargs = kwargs

        self.signals = GenericRunnableSignals()

    def run(self):
        res = RunnableReturn(self._id_, None)
        try:
            res.value = self._function(*self._args, **self._kwargs)
        except Exception:
            pass
        self.signals.finished.emit(res)


class GenericWorker(QtCore.QObject):
    finished = QtCore.Signal(object)

    def __init__(
        self, function, *args, parent: QtCore.QObject | None = None, **kwargs
    ) -> None:
        super().__init__(parent)
        self.function = function
        self.args = args
        self.kwargs = kwargs

    @QtCore.Slot()
    def run(self):
        res = None
        try:
            res = self.function(*self.args, **self.kwargs)
        except Exception:
            pass
        self.finished.emit(res)
