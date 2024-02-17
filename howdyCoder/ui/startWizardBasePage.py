from PySide6 import QtWidgets, QtCore


class StartWizardBasePage(QtWidgets.QWidget):
    pageFinished = QtCore.Signal()
    setOk = QtCore.Signal(bool)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def startPage(self):
        pass
