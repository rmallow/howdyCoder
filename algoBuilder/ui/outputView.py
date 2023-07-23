from PySide6 import QtWidgets


class outputView(QtWidgets.QWidget):
    def __init__(self, outputViewModel, parent=None):
        super().__init__(parent)
        self.outputViewModel = outputViewModel

    def setup(self):
        pass
