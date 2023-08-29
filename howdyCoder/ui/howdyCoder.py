from .mainWindow import MainWindow
from . import tutorialOverlay
from .util import qtResourceManager
import os
from PySide6 import QtWidgets, QtCore, QtGui


"""THIS FILE'S NAME SHOWS UP IN THE MAC MENU BAR DROPDOWN, HENCE THE NAME"""


def start(isLocal: bool):
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QtWidgets.QApplication([])
    app.setWindowIcon(
        QtGui.QIcon(qtResourceManager.getResourceByName("app-icons", "1024.png"))
    )
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
