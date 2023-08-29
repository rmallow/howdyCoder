from ..qtUiFiles.ui_creatorTypeSelector import Ui_CreatorTypeSelector
from ...core.commonGlobals import ProgramTypes

import typing

from PySide6 import QtWidgets, QtCore


class CreatorTypeWindow(QtWidgets.QDialog):
    DEFAULT_LABEL = "Select the type of program to create."

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
        self.setModal(True)

    def reset(self):
        self._ui.program_type_view.selectionModel().reset()
        self._ui.program_type_description.setText(self.DEFAULT_LABEL)

    def getTypeSelected(self):
        if res := self._ui.program_type_view.selectedItems():
            return res[0].text()
