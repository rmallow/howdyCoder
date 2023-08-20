from .mainWindow import MainWindow
from . import tutorialOverlay
import os
from PySide6 import QtWidgets, QtCore


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
    main = MainWindow(isLocal)
    event_filter = tutorialOverlay.TutorialEventFilter(main)
    main._ui.action_tutorial.triggered.connect(event_filter.tutorial_started)
    app.installEventFilter(event_filter)
    app.exec_()
