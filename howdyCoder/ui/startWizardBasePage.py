from PySide6 import QtWidgets, QtCore


class StartWizardBasePage(QtWidgets.QWidget):
    pageFinished = QtCore.Signal()
    setOk = QtCore.Signal(bool)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def startPage(self):
        pass

    @QtCore.Slot()
    def updateValues(self, *args, **kwargs):
        """Pages will use this for interfacing with the main model, which will process the info for them"""
        pass
