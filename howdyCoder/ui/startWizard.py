from .qtUiFiles import ui_startWizard
from .startWizardBasePage import StartWizardBasePage

from .util import qtResourceManager, nonNativeQMessageBox

import typing

from PySide6 import QtWidgets, QtCore, QtGui


class StartWizard(QtWidgets.QDialog):
    STATUS_TEXTS = ["Parameter Check", "Module Check"]

    finishedWizard = QtCore.Signal()

    OK_TEXT = "Ok"
    OVERRIDE_TEXT = "Override"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setModal(True)
        self.ui = ui_startWizard.Ui_StartWizard()
        self.ui.setupUi(self)
        self.ui.launch_label.setText(
            "<html><head/><body><p>All checks passed.</p><p><span>"
            + "\U0001F680"
            + " </span>Launching Program...   <span>"
            + "\U0001F680"
            + " </span></p></body></html>",
        )
        self.ui.ok_button.setText(self.OK_TEXT)

        self._page_order: typing.List[StartWizardBasePage] = [
            self.ui.parameter_check_widget,
            self.ui.module_install_widget,
        ]
        assert len(self.STATUS_TEXTS) == len(
            self._page_order
        ), "Must have status for each page"
        for p in self._page_order:
            p.setOk.connect(self.setOk)
            p.pageFinished.connect(self.okPressed)
        self._page_index = 0

        self.current_code = ""
        self.ui.ok_button.released.connect(self.okPressed)
        self.ui.page_status_list_widget.setStyleSheet("background-color: #3b4045")
        self.hide()

    @QtCore.Slot()
    def setOk(self, ok_button_value):
        self.ui.ok_button.setText(
            self.OK_TEXT if ok_button_value else self.OVERRIDE_TEXT
        )

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
            self._page_index += 1
            if self._page_index == len(self._page_order):
                self.ui.ok_button.hide()
                self.ui.page_status_list_widget.addItem(
                    QtWidgets.QListWidgetItem(
                        QtGui.QIcon(
                            self.style().standardPixmap(
                                QtWidgets.QStyle.StandardPixmap.SP_ToolBarHorizontalExtensionButton
                            )
                        ),
                        "LAUNCH SEQUENCE INITIATED",
                        listview=self.ui.page_status_list_widget,
                    )
                )
                self.ui.stacked_widget.setCurrentWidget(self.ui.launch_widget)
                self.finishedWizard.emit()
            else:
                self.startCurrentPage()

    def startWizard(self, code: str):
        self.current_code = code
        self._page_index = 0
        self.ui.page_status_list_widget.clear()
        self.ui.ok_button.show()
        self.startCurrentPage()
        self.show()

    def startCurrentPage(self):
        self.ui.ok_button.setText(self.OK_TEXT)
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
        self.ui.stacked_widget.currentWidget().startPage()
