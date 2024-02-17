from .startWizardBasePage import StartWizardBasePage
from .qtUiFiles import ui_modInstallWidget

from PySide6 import QtWidgets, QtCore, QtGui
import typing


INSTALL_TEXT = "--- INSTALLING ---"
ALL_INSTALLED = "--- ALL MODULES FOUND ---"
MISSING_MODULES = "--- SOME MODULES MISSING ---"


class ModInstallWidget(StartWizardBasePage):
    installPackagesSignal = QtCore.Signal(list)

    def __init__(
        self,
        parent: typing.Optional[QtWidgets.QWidget] = None,
        f: QtCore.Qt.WindowFlags = QtCore.Qt.WindowFlags(),
    ):
        super().__init__(parent, f)
        self._ui = ui_modInstallWidget.Ui_ModInstallWidget()
        self._ui.setupUi(self)
        self._table_model = QtGui.QStandardItemModel(self)
        self._table_model.setHorizontalHeaderLabels(
            ["Module", "Status", "Package Name"]
        )
        self._ui.tableView.setModel(self._table_model)
        self._all_installed = True
        self._ui.install_button.released.connect(self.installPressed)

    def reset(self):
        self._ui.install_label.setText("")
        self._table_model.removeRows(0, self._table_model.rowCount())
        self._all_installed = True

    def updateTable(self, modules):
        self.reset()
        # do first loop so all of the uninstalled modules are grouped
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
        self.setOk.emit(self._all_installed)
        self._ui.install_button.setEnabled(not self._all_installed)
        self._ui.install_label.setText(
            ALL_INSTALLED if self._all_installed else MISSING_MODULES
        )

    def installPressed(self):
        self._ui.tableView.setCurrentIndex(self._table_model.index(0, 0))
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

    def startPage(self):
        if self._all_installed:
            self.pageFinished.emit()
        else:
            self.setOk.emit(False)
