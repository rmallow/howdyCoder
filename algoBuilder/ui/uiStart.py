from .mainWindow import mainWindow
import os
from PySide2 import QtWidgets, QtCore


def start(isLocal: bool):
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QtWidgets.QApplication([])
    path = os.path.abspath(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "res", "base_style.qss"
        )
    )
    with open(path) as f:
        app.setStyleSheet(f.read())
    mainWindow(isLocal)

    app.exec_()
