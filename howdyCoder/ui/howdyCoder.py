from .mainWindow import MainWindow
from . import tutorialOverlay
from .util import qtResourceManager
import os
from PySide6 import QtWidgets, QtCore, QtGui
from qt_material import apply_stylesheet


"""THIS FILE'S NAME SHOWS UP IN THE MAC MENU BAR DROPDOWN, HENCE THE NAME"""


def start(isLocal: bool):
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    QtGui.QGuiApplication.setDesktopSettingsAware(False)
    app = QtWidgets.QApplication([])
    app.setWindowIcon(
        QtGui.QIcon(qtResourceManager.getResourceByName("app-icons", "1024.png"))
    )

    main = MainWindow(isLocal)
    path = os.path.abspath(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "res", "howdy_style.qss"
        )
    )
    apply_stylesheet(app, theme="dark_lightgreen.xml", css_file=path)

    event_filter = tutorialOverlay.TutorialEventFilter(main)
    main._ui.action_tutorial.triggered.connect(event_filter.tutorial_started)
    app.installEventFilter(event_filter)
    app.exec_()
