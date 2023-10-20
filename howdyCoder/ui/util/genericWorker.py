from PySide6 import QtCore


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
