import PySide6.QtGui
from .configWindow import configWindow
from .loggingWindow import loggingWindow
from .statusWindow import statusWindow
from .qtUiFiles import ui_mainWindow
from .mainModel import mainModel
from .modInstallDialog import ModInstallDialog

# import name page for find children to connect signal
from .create.createNamePage import CreateNamePage

from ..core.commonGlobals import Modes

from PySide6 import QtWidgets, QtCore, QtGui


class mainWindow(QtWidgets.QMainWindow):
    runAllSignal = QtCore.Signal()
    endAllSignal = QtCore.Signal()

    def __init__(self, isLocal: bool, parent=None):
        super().__init__(parent)
        # Load UI
        self._ui = ui_mainWindow.Ui_AlgoBuilder()
        self._ui.setupUi(self)

        screen = self.screen()
        self.setMaximumSize(screen.geometry().width(), screen.geometry().height())

        self._main_model = mainModel(isLocal, parent=self)

        # setup signal and slots for output tab
        self._main_model.updateOutputSignal.connect(
            self._ui.outputPage.mainOutputViewModel.receiveData
        )
        self._main_model.updateColumnsSignal.connect(
            self._ui.outputPage.mainOutputViewModel.receiveColumns
        )
        self._ui.outputPage.mainOutputViewModel.addOutputViewSignal.connect(
            self._main_model.messageMainframe
        )

        # Create and connect logging window
        self.loggingWindow = loggingWindow(self)
        self._main_model.updateLoggingSignal.connect(
            self.loggingWindow.loggingModel.receiveData
        )
        self._ui.actionLogging.triggered.connect(self.loggingWindow.show)

        # Create and connect status window
        self.statusWindow = statusWindow(self)
        self._main_model.updateStatusSignal.connect(
            self.statusWindow.statusModel.receiveData
        )
        self._ui.actionStatus.triggered.connect(self.statusWindow.show)

        # Create config window
        self.configWindow = configWindow(self)

        # Set up signal and slots
        # For mysterious reasons this signal slot cannot be deleted for the rest of the UI to work
        # After brief investigation I have no idea why this is the case
        self._ui.actionLoad_Config.triggered.connect(lambda: self.configWindow.show())
        # Spooky, noted to fix in later development

        self._ui.actionStart_All.triggered.connect(self.checkModules)
        self._ui.actionEnd_All.triggered.connect(self.endAllSignal)
        self.runAllSignal.connect(self._main_model.sendCmdStartAll)
        self.endAllSignal.connect(self._main_model.sendCmdEndAll)
        self.configWindow._ui.loadConfigsButton.clicked.connect(self.slotLoadConfigs)
        self._ui.controlPage.new_block_widget.ui.createButton.pressed.connect(
            lambda: self._ui.stackedWidget.setCurrentWidget(self._ui.createPage)
        )

        # the create name page needs to check if the name already exists before letting the user proceed
        # to do this it will send a signal to the main model's algo dict to see if it is there
        # then that will return back if it is in there
        # alternatively, this could of been done with just passing in the algo_dict to the createNamePage
        # but I wanted to avoid that for safety
        w: CreateNamePage
        for w in self.findChildren(CreateNamePage):
            w.doesAlgoNameExist.connect(self._main_model.algo_dict.contains)
            self._main_model.algo_dict.nameExists.connect(w.doesNameExistSlot)
        self._ui.createPage.addAlgo.connect(self._main_model.addAlgo)
        self._ui.createPage.addAlgo.connect(
            lambda: self._ui.stackedWidget.setCurrentWidget(self._ui.controlPage)
        )
        self._ui.controlPage.startAlgo.connect(self.algoStartControlBox)
        self._main_model.algo_dict.dataChanged.connect(
            self._ui.controlPage.compareDataToCurrentWidgets
        )
        self._main_model.algo_dict.dataChanged.connect(
            self._ui.outputPage.mainOutputViewModel.dataChanged
        )
        self._ui.controlPage.algo_dict = self._main_model.algo_dict
        self._ui.outputPage.mainOutputViewModel.algo_dict = self._main_model.algo_dict
        self._ui.stackedWidget.currentChanged.connect(self.pageChanged)
        self._ui.changePageButton.released.connect(
            lambda: self._ui.stackedWidget.setCurrentWidget(
                self._ui.controlPage
                if self._ui.stackedWidget.currentWidget() == self._ui.outputPage
                else self._ui.outputPage
            )
        )

        self._module_install_window = ModInstallDialog(self)
        self._module_install_window.setVisible(False)
        self._module_install_window.accepted.connect(self.moduleCheckAccepted)
        self._main_model.moduleStatusChangedSignal.connect(self.moduleStatusChanged)
        self._module_install_window.installPackagesSignal.connect(
            self._main_model.sendInstallPackagesCommand
        )

        self.show()

    @QtCore.Slot()
    def slotLoadConfigs(self):
        pass

    @QtCore.Slot()
    def pageChanged(self, new_page_index: int):
        cur_page = self._ui.stackedWidget.currentWidget()
        self._ui.changePageButton.setText(
            "Go to Control Page"
            if cur_page == self._ui.outputPage
            else "Go to Output Page"
        )
        self._ui.changePageButton.setHidden(cur_page == self._ui.createPage)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        screen = self.screen().geometry()
        resize = False
        width = self.width()
        height = self.height()

        if self.width() > screen.width():
            resize = True
            width = screen.width()

        if self.height() > screen.height():
            resize = True
            height = screen.height()

        if resize:
            QtCore.QTimer.singleShot(0, lambda: self.resize(width, height))
        else:
            return super().resizeEvent(event)

    @QtCore.Slot()
    def algoStartControlBox(self, code):
        data = self._main_model.algo_dict.getData(code)
        if data is not None:
            if data.mode == Modes.STARTED:
                self._main_model.sendCmdEnd(code)
            else:
                self.checkModules(code)

    @QtCore.Slot()
    def checkModules(self, code=None):
        modules = self._main_model.getModules(code)
        if any(not status for _, status in modules):
            self._module_install_window.updateTable(code, modules)
            self._module_install_window.open()
        else:
            if code:
                self._main_model.sendCmdStart(code)
            else:
                self._main_model.sendCmdStartAll()

    @QtCore.Slot()
    def moduleCheckAccepted(self):
        if self._module_install_window.current_code is not None:
            self._main_model.sendCmdStart(self._module_install_window.current_code)
        else:
            self._main_model.sendCmdStartAll()

    @QtCore.Slot()
    def moduleStatusChanged(self):
        """If the module status has changed and the window is visible, it's because we tried an install"""
        if self._module_install_window.isVisible():
            self._module_install_window.updateTable(
                self._module_install_window.current_code,
                self._main_model.getModules(self._module_install_window.current_code),
            )

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        button_response = QtWidgets.QMessageBox.question(
            self,
            "Are you sure you want to shutdown?",
            "Are you sure you want to shutdown? Shutting down will close this window and the currently running programs.",
        )
        if button_response == QtWidgets.QMessageBox.StandardButton.Yes:
            self._main_model.shutdown()
            event.accept()
        else:
            event.ignore()
