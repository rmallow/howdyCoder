from .newBlockWidget import NewBlockWidget
from .algoStatusWidget import AlgoStatusWidget
from .algoData import AlgoDict, AlgoWidgetData
from .tutorialOverlay import AbstractTutorialClass
from .inputBox import InputBox
from .inputWindow import InputWindow

from .util import abstractQt

from .qtUiFiles import ui_controlWidget

from ..core.configConstants import (
    DATA_SOURCES,
    TYPE,
    DataSourcesTypeEnum,
    ENUM_DISPLAY,
    INPUT_TYPE,
)
from ..core.commonGlobals import Modes, InputData

from PySide6 import QtWidgets, QtCore, QtGui

import typing
import math


class EmtpyBox(QtWidgets.QWidget):
    """Filler for the empty spots"""

    def __init__(
        self,
        color: QtGui.QColor,
        add_empty_label=False,
        parent: typing.Optional[QtWidgets.QWidget] = None,
        f: QtCore.Qt.WindowFlags = QtCore.Qt.WindowFlags(),
    ) -> None:
        super().__init__(parent, f)
        if add_empty_label:
            layout = QtWidgets.QVBoxLayout(self)
            layout.addWidget(QtWidgets.QLabel("No Algos Currently"))
        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Window, color)
        # color looked dumb, but if needed add these lines back in
        # self.setAutoFillBackground(True)
        # self.setPalette(pal)


class ControlWidget(
    AbstractTutorialClass,
    QtWidgets.QWidget,
    metaclass=abstractQt.getAbstactQtResolver(QtWidgets.QWidget, AbstractTutorialClass),
):
    TUTORIAL_RESOURCE_PREFIX = "None"

    startAlgo = QtCore.Signal(str)
    shutdownAlgo = QtCore.Signal(str)
    exportData = QtCore.Signal(str)
    inputEntered = QtCore.Signal(InputData)

    def __new__(self, *args, **kwargs):
        abstractQt.handleAbstractMethods(self)
        return super().__new__(self, *args, **kwargs)

    def __init__(
        self,
        parent: typing.Optional[QtWidgets.QWidget] = None,
        f: QtCore.Qt.WindowFlags = QtCore.Qt.WindowFlags(),
    ) -> None:
        super().__init__(self.TUTORIAL_RESOURCE_PREFIX, parent, f)

        self.ui = ui_controlWidget.Ui_ControlWidget()
        self.ui.setupUi(self)

        self.grid_layout = QtWidgets.QGridLayout(self.ui.mainWidget)
        self.new_block_widget = NewBlockWidget(self.ui.mainWidget)
        self.current_width = 2

        self.ui.mainWidget.setLayout(self.grid_layout)

        """This is the main model's algo dict class set by the main window"""
        self.algo_dict: AlgoDict = None
        """This is a mapping of uid's to status widgets"""
        self._algo_widgets: typing.Dict[int, AlgoStatusWidget] = {}
        """Mapping of uid's to input windows"""
        self._algo_input_windows: typing.Dict[int, InputWindow] = {}
        """Do it once before anyhting is in there to position create new button right"""
        self.addWidgets()

    def clear(self):
        while self.grid_layout.count():
            w: QtWidgets.QWidget = self.grid_layout.takeAt(0).widget()
            if isinstance(w, EmtpyBox):
                w.deleteLater()

    def addWidgets(self):
        self.clear()
        self.current_width = max(2, int(math.log2(max(len(self._algo_widgets), 1)) + 1))
        for i, w in enumerate(self._algo_widgets.values()):
            self.grid_layout.addWidget(
                w, i // self.current_width, i % self.current_width
            )
        for i in range(len(self._algo_widgets), self.current_width**2 - 1):
            self.grid_layout.addWidget(
                EmtpyBox(
                    QtGui.QColor(
                        QtCore.Qt.GlobalColor.black
                        if i % 2 == 1
                        else QtCore.Qt.GlobalColor.gray
                    ),
                    add_empty_label=i == 0,
                    parent=self,
                ),
                i // self.current_width,
                i % self.current_width,
            )
        self.grid_layout.addWidget(
            self.new_block_widget, self.current_width - 1, self.current_width - 1
        )

    @QtCore.Slot()
    def compareDataToCurrentWidgets(self):
        """Check if any algos were removed and then check if any were added"""
        if self.algo_dict is not None:
            missing_ids, to_remove_ids = self.algo_dict.compareIds(self._algo_widgets)
            for m in missing_ids:
                data: AlgoWidgetData = self.algo_dict.getDataById(m)
                w = AlgoStatusWidget(data)
                w.ui.start_button.released.connect(
                    lambda: self.startAlgo.emit(data.name)
                )
                w.ui.export_button.released.connect(
                    lambda: self.exportData.emit(data.name)
                )
                w.ui.remove_button.released.connect(lambda: self.removeWidget(m))
                w.ui.input_button.released.connect(lambda: self.createInputWindow(m))
                self._algo_widgets[m] = w
            for r in to_remove_ids:
                self.removeWidget(r, refresh=False)
            self.addWidgets()

    @QtCore.Slot()
    def removeWidget(self, uid: int, refresh=True) -> None:
        if uid in self._algo_widgets:
            if self._algo_widgets[uid].data.mode == Modes.STOPPED:
                self.shutdownAlgo.emit(self._algo_widgets[uid].data.name)
            else:
                self._algo_widgets[uid].deleteLater()
                del self._algo_widgets[uid]
                if refresh:
                    self.addWidgets()

    def getTutorialClasses(self) -> typing.List:
        return (
            [self]
            + (
                next(iter(self._algo_widgets.values())).getTutorialClasses()
                if self._algo_widgets
                else []
            )
            + self.new_block_widget.getTutorialClasses()
        )

    @QtCore.Slot()
    def createInputWindow(self, uid: int):
        if uid not in self._algo_input_windows:
            inputs = []
            if uid in self._algo_widgets and (data := self.algo_dict.getDataById(uid)):
                for key, data_source in data.config[DATA_SOURCES].items():
                    if data_source.get(TYPE, "") == getattr(
                        DataSourcesTypeEnum.INPUT, ENUM_DISPLAY
                    ):
                        w = InputBox(key, data_source[INPUT_TYPE])
                        w.inputEntered.connect(
                            lambda input_data: self.inputPassThrough(
                                input_data, data.name
                            )
                        )
                        inputs.append(w)
            if inputs:
                self._algo_input_windows[uid] = InputWindow(inputs, data.name, self)
        if uid in self._algo_input_windows:
            self._algo_input_windows[uid].show()

    @QtCore.Slot()
    def inputPassThrough(self, input_data: InputData, code: str):
        input_data.code = code
        self.inputEntered.emit(input_data)
