from PySide6.QtGui import QResizeEvent
from ..qtUiFiles.ui_creatorTypeSelector import Ui_CreatorTypeSelector
from ...core.commonGlobals import ProgramTypes

import typing

from PySide6 import QtWidgets, QtCore

TYPE_TO_DESCRIPTION_LABEL = {
    ProgramTypes.ALGO.value: "Create an algo.\n\nString together algorithm elements.\nFor when the AI can't generate everything needed in one script.\nThe create wizard will guide you through the steps of creating the algorithm elements.",
    ProgramTypes.SCRIPT.value: "Create a script.\n\nExecute a single AI generated function.\nBest for quick operations.",
}


class CreatorTypeWidget(QtWidgets.QWidget):
    DEFAULT_LABEL = "Select the type of program to create."

    selectionFinished = QtCore.Signal()

    def __init__(
        self,
        parent: typing.Optional[QtWidgets.QWidget] = None,
        f: QtCore.Qt.WindowFlags = QtCore.Qt.WindowFlags(),
    ) -> None:
        super().__init__(parent, f)
        self._ui = Ui_CreatorTypeSelector()
        self._ui.setupUi(self)
        for e in ProgramTypes:
            if e != ProgramTypes.PROGRAM:
                self._ui.program_type_view.addItem(e.value)
        # cheeky
        self.OkEnabled = lambda b: self._ui.button_box.button(
            QtWidgets.QDialogButtonBox.StandardButton.Ok
        ).setEnabled(b)
        self._ui.program_type_view.selectionModel().selectionChanged.connect(
            self.typeSelected
        )
        self.OkEnabled(False)
        self._ui.button_box.accepted.connect(self.selectionFinished)

    def reset(self):
        self._ui.program_type_view.selectionModel().reset()
        self._ui.program_type_description.setText(self.DEFAULT_LABEL)

    def getTypeSelected(self):
        if res := self._ui.program_type_view.selectedItems():
            return res[0].text()

    def typeSelected(self, selection: QtCore.QItemSelection, _):
        if selection.indexes() and selection.indexes()[0].isValid():
            self.OkEnabled(True)
            self._ui.program_type_description.setText(
                TYPE_TO_DESCRIPTION_LABEL.get(
                    selection.indexes()[0].data(QtCore.Qt.ItemDataRole.DisplayRole)
                )
            )
        else:
            self.OkEnabled(False)
            self._ui.typeDescription.setText(self.DEFAULT_LABEL)
