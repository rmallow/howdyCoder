from .qtUiFiles import ui_modInstallDialog

from PySide6 import QtWidgets, QtCore, QtGui
import typing


INSTALL_TEXT = "--- INSTALLING ---"
ALL_INSTALLED = "--- ALL MODULES FOUND ---"
MISSING_MODULES = "--- SOME MODULES MISSING ---"


class ModInstallDialog(QtWidgets.QDialog):
    installPackagesSignal = QtCore.Signal(list)

    def __init__(
        self,
        parent: typing.Optional[QtWidgets.QWidget] = None,
        f: QtCore.Qt.WindowFlags = QtCore.Qt.WindowFlags(),
    ):
        super().__init__(parent, f)
        self._ui = ui_modInstallDialog.Ui_ModInstallDialog()
        self._ui.setupUi(self)
        self._table_model = QtGui.QStandardItemModel(self)
        self._ui.tableView.setModel(self._table_model)
        self.current_code = None
        self._all_installed = True
        self._ui.ok_button.released.connect(self.okPressed)
        self._ui.cancel_button.released.connect(self.reject)
        self._ui.install_button.released.connect(self.installPressed)

    def updateTable(self, code, modules):
        self._ui.install_label.setText("")
        self._table_model.clear()
        self.current_code = code
        # do first loop so all of the uninstalled modules are grouped
        self._all_installed = True
        for status_type in [False, True]:
            for name, status in modules:
                if status == status_type:
                    self._all_installed = self._all_installed and status
                    name_item = QtGui.QStandardItem(name)
                    name_item.setEditable(False)
                    status_item = QtGui.QStandardItem(
                        "Installed" if status else "Not Installed"
                    )
                    status_item.setBackground(
                        QtGui.QBrush(QtCore.Qt.green if status else QtCore.Qt.red)
                    )
                    status_item.setForeground(QtGui.QBrush(QtCore.Qt.white))
                    status_item.setEditable(False)
                    package_item = QtGui.QStandardItem(name if not status else "")
                    package_item.setEditable(not status)
                    self._table_model.appendRow([name_item, status_item, package_item])
        self._ui.ok_button.setText("Ok" if self._all_installed else "Override")
        self._ui.install_button.setEnabled(not self._all_installed)
        self._ui.install_label.setText(
            ALL_INSTALLED if self._all_installed else MISSING_MODULES
        )

    def okPressed(self):
        if (
            self._all_installed
            or QtWidgets.QMessageBox.warning(
                self,
                "Override Warning",
                "Are you sure want to override and not install all modules? This could cause crashes or unintended consequences when running.",
                QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Ok,
            )
            == QtWidgets.QMessageBox.Ok
        ):
            self.accept()

    def installPressed(self):
        self._ui.install_button.setEnabled(False)
        self._ui.install_label.setText(INSTALL_TEXT)
        packages = []
        for row in range(self._table_model.rowCount()):
            # only the uninstalled modules have a third column this is editable
            if self._table_model.item(row, 2).isEditable() and self._table_model.item(
                row, 2
            ).data(QtCore.Qt.DisplayRole):
                packages.append(
                    self._table_model.item(row, 2).data(QtCore.Qt.DisplayRole)
                )
        self.installPackagesSignal.emit(packages)
