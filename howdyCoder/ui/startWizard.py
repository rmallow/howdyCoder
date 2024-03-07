from .qtUiFiles import ui_startWizard
from .startWizardBasePage import StartWizardBasePage

from .util import qtResourceManager, nonNativeQMessageBox

from .uiConstants import LaunchSequenceSteps

import typing

from PySide6 import QtWidgets, QtCore, QtGui


class StartWizard(QtWidgets.QDialog):

    LOAD_FILE_LABEL = (
        ("<html><head/><body><p>All checks passed.</p><p><span>" + "\U0001F4C2")
        + " </span>Loading Files...<span>"
        + "\U0001F4C4"
        + " </span></p></body></html>"
    )

    LAUNCH_SEQUENCE_LABEL = (
        ("<html><head/><body><p>All checks passed.</p><p><span>" + "\U0001F680")
        + " </span>Launching Program...   <span>"
        + "\U0001F680"
        + " </span></p></body></html>"
    )

    STATUS_TEXTS = [
        "Parameter Check",
        "File Check",
        "Module Check",
        "Loading Files",
        "LAUNCH SEQUENCE INITIATED",
    ]

    setLaunchStep = QtCore.Signal(LaunchSequenceSteps)

    OK_TEXT = "Ok"
    OVERRIDE_TEXT = "Override"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setModal(True)
        self.ui = ui_startWizard.Ui_StartWizard()
        self.ui.setupUi(self)
        self.ui.launch_label.setText(self.LAUNCH_SEQUENCE_LABEL)
        self.ui.load_file_label.setText(self.LOAD_FILE_LABEL)
        self.ui.ok_button.setText(self.OK_TEXT)

        self._page_order: typing.List[StartWizardBasePage] = [
            self.ui.parameter_check_widget,
            self.ui.file_check_widget,
            self.ui.module_install_widget,
            self.ui.load_file_widget,
            self.ui.launch_widget,
        ]

        for p in self._page_order:
            if isinstance(p, StartWizardBasePage):
                p.setOk.connect(self.setOk)
                p.pageFinished.connect(self.okPressed)
        self._page_index = 0

        self.current_code = ""
        self.ui.ok_button.released.connect(self.okPressed)
        self.ui.page_status_list_widget.setStyleSheet("background-color: #3b4045")
        self.hide()

        """Sanity tests"""
        assert len(self.STATUS_TEXTS) == len(
            self._page_order
        ), "Must have status for each page"
        assert len(LaunchSequenceSteps) == len(
            self._page_order
        ), "Must have page for each launch step"

    @QtCore.Slot()
    def setOk(self, ok_button_value):
        self.ui.ok_button.setText(
            self.OK_TEXT if ok_button_value else self.OVERRIDE_TEXT
        )

    def nextPage(self):
        if self._page_index < len(self._page_order):
            self._page_index += 1
            self.startCurrentPage()

    def okPressed(self):
        if self._page_index < len(self._page_order):
            if self.ui.ok_button.text() == self.OK_TEXT:
                self.ui.page_status_list_widget.item(self._page_index).setIcon(
                    qtResourceManager.getResourceByName(
                        qtResourceManager.ICONS_PREFIX,
                        qtResourceManager.GREEN_CHECKMARK,
                    )
                )
            else:
                message_box = nonNativeQMessageBox.NonNativeQMessageBox(self)
                message_box.setText("Override Warning")
                info_text = "Are you sure want to override? This could cause crashes or unintended consequences when running.\n"
                message_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                message_box.setInformativeText(info_text)
                message_box.setStandardButtons(
                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
                )
                message_box.setDefaultButton(QtWidgets.QMessageBox.No)
                message_box.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
                if message_box.exec() == QtWidgets.QMessageBox.Yes:
                    self.ui.page_status_list_widget.item(self._page_index).setIcon(
                        QtGui.QIcon(
                            self.style().standardPixmap(
                                self.style().StandardPixmap.SP_MessageBoxWarning
                            )
                        )
                    )
                else:
                    return
            self.nextPage()

    def startWizard(self, code: str):
        self.current_code = code
        self._page_index = 0
        self.ui.page_status_list_widget.clear()
        self.ui.ok_button.show()
        self.startCurrentPage()
        self.show()

    def startCurrentPage(self):
        self.ui.ok_button.setText(self.OK_TEXT)
        self.ui.ok_button.setEnabled(False)
        if self._page_index >= LaunchSequenceSteps.LOAD_FILES.value:
            self.ui.ok_button.hide()
        self.ui.page_status_list_widget.addItem(
            QtWidgets.QListWidgetItem(
                QtGui.QIcon(
                    self.style().standardPixmap(
                        QtWidgets.QStyle.StandardPixmap.SP_ToolBarHorizontalExtensionButton
                    )
                ),
                self.STATUS_TEXTS[self._page_index],
                listview=self.ui.page_status_list_widget,
            )
        )
        self.ui.stacked_widget.setCurrentWidget(self._page_order[self._page_index])
        try:
            self.ui.stacked_widget.currentWidget().startPage()
        except AttributeError:
            pass
        self.setLaunchStep.emit(LaunchSequenceSteps(self._page_index))

    @QtCore.Slot()
    def receiveLaunchSequenceResponse(self, response_value: typing.Any) -> None:
        self.ui.ok_button.setEnabled(True)
        if self._page_index >= LaunchSequenceSteps.LOAD_FILES.value:
            self.nextPage()
        else:
            try:
                self.ui.stacked_widget.currentWidget().updateValues(response_value)
            except AttributeError:
                pass
