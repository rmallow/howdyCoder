from .algoTopoItem import (
    ConnectedRectItem,
    TopoSignalController,
    ContextResultType,
    ContextResult,
)
from ..qtUiFiles import ui_algoTopoView

from ..tutorialOverlay import AbstractTutorialClass
from ..util import abstractQt

from ...core.dataStructs import ProgramSettings, AlgoSettings, DataSourceSettings

from PySide6 import QtWidgets, QtCore, QtGui

from dataclass_wizard import asdict
import typing
import copy
from collections import defaultdict
from enum import IntEnum, auto

COLUMN_SPACING = 250
DISTANCE_BETWEEN = 50


class SceneZIndex(IntEnum):
    BASE = auto()
    LINE = auto()
    ITEM = auto()


class AlgoTopoView(
    AbstractTutorialClass,
    QtWidgets.QWidget,
    metaclass=abstractQt.getAbstactQtResolver(QtWidgets.QWidget, AbstractTutorialClass),
):
    TUTORIAL_RESOURCE_PREFIX = "None"

    def __new__(self, *args, **kwargs):
        abstractQt.handleAbstractMethods(self)
        return super().__new__(self, *args, **kwargs)

    def __init__(
        self,
        parent: typing.Optional[QtWidgets.QWidget] = None,
        f: QtCore.Qt.WindowFlags = QtCore.Qt.WindowFlags(),
    ) -> None:
        super().__init__(self.TUTORIAL_RESOURCE_PREFIX, parent, f)

        # Load UI file
        self._ui = ui_algoTopoView.Ui_AlgoTopoView()
        self._ui.setupUi(self)

        self.current_items: typing.Dict[str, ConnectedRectItem] = {}
        self.line_mapping: typing.Dict[
            typing.Tuple[str, str], QtWidgets.QGraphicsLineItem
        ] = {}

        self._signal_controller = TopoSignalController(self)
        self._signal_controller.mouseEnter.connect(self.itemHoverEnter)
        self._signal_controller.mouseLeft.connect(self.itemHoverLeft)
        self._signal_controller.mouseRelease.connect(self.itemSelected)
        self._signal_controller.contextResult.connect(self.contextResult)
        self._current_hover_item = ""
        self._current_selected_item = ""

    def changeColorHelper(self, name, color):
        if name in self.current_items:
            pen = self.current_items[name].pen()
            pen.setColor(color)
            self.current_items[name].setPen(pen)

    def itemSelected(self, name):
        self.changeColorHelper(self._current_selected_item, QtCore.Qt.GlobalColor.black)
        self._current_selected_item = name
        self.changeColorHelper(
            self._current_selected_item, QtCore.Qt.GlobalColor.yellow
        )

    def getTopoSort(self, algo_config: AlgoSettings):
        self.levels = [[]]
        for key, data_source in algo_config.data_sources.items():
            for output in data_source.output:
                self.levels[0].append(f"{key}-{output}")
        self.outgoing_mapping = defaultdict(list)
        self.incoming_mapping = defaultdict(list)
        incoming_count = defaultdict(int)
        for key, action in algo_config.action_list.items():
            incoming_count[key] = len(action.input_)
            for name in action.input_.keys():
                self.outgoing_mapping[name].append(key)
                self.incoming_mapping[key].append(name)

        while self.levels[-1]:
            self.levels.append([])
            for n in self.levels[-2]:
                for other in self.outgoing_mapping[n]:
                    incoming_count[other] -= 1
                    if incoming_count[other] == 0:
                        self.levels[-1].append(other)
                        del incoming_count[other]
        del self.levels[-1]

    def highlightNodes(self, name: str, color: QtCore.Qt.GlobalColor):
        pen = self.current_items[name].pen()
        pen.setColor(color)

        def dfsOut(name, pen):
            if name != self._current_selected_item:
                self.current_items[name].setPen(pen)
            for outgoing in self.outgoing_mapping[name]:
                self.line_mapping[(name, outgoing)].setPen(pen)
                dfsOut(outgoing, pen)

        def dfsIn(name, pen):
            if name != self._current_selected_item:
                self.current_items[name].setPen(pen)
            for incoming in self.incoming_mapping[name]:
                self.line_mapping[(incoming, name)].setPen(pen)
                dfsIn(incoming, pen)

        dfsIn(name, pen)
        dfsOut(name, pen)

    def itemHoverEnter(self, name):
        self._current_hover_item = name
        self.highlightNodes(name, QtCore.Qt.GlobalColor.red)

    def itemHoverLeft(self):
        if self._current_hover_item:
            self.highlightNodes(self._current_hover_item, QtCore.Qt.GlobalColor.black)

    def createLine(self, name_p1: str, name_p2: str):
        if name_p1 in self.current_items and name_p2 in self.current_items:
            item_p1 = self.current_items[name_p1]
            item_p2 = self.current_items[name_p2]
            line = self._scene.addLine(
                item_p1.getCenter().x(),
                item_p1.getCenter().y(),
                item_p2.getCenter().x(),
                item_p2.getCenter().y(),
            )
            pen = QtGui.QPen()
            pen.setWidthF(3)
            line.setPen(pen)
            line.setZValue(SceneZIndex.LINE.value)
            item_p1.addLine(line, True)
            item_p2.addLine(line, False)
            self.line_mapping[(name_p1, name_p2)] = line

    def setConfig(self, creator_config: ProgramSettings):
        self._scene = QtWidgets.QGraphicsScene()
        self.current_settings = copy.deepcopy(creator_config)
        self.getTopoSort(creator_config.settings)
        self.current_items = {}
        max_height = 0
        for x in range(len(self.levels)):
            last_y = DISTANCE_BETWEEN
            for name in self.levels[x]:
                settings = None
                if x == 0:
                    ds_name = name.split("-")[0]
                    settings = creator_config.settings.data_sources[ds_name]
                else:
                    settings = creator_config.settings.action_list[name]

                item = ConnectedRectItem(
                    settings,
                    self._signal_controller,
                    item_name=name,
                    boundary_left=x * COLUMN_SPACING,
                    boundary_right=(x + 1) * COLUMN_SPACING - DISTANCE_BETWEEN,
                )
                item.setZValue(SceneZIndex.ITEM.value)
                self.current_items[name] = item
                item.setPos(x * COLUMN_SPACING + DISTANCE_BETWEEN, last_y)
                last_y += item.boundingRect().height() + DISTANCE_BETWEEN
                self._scene.addItem(item)
            max_height = max(max_height, last_y)
        for p1, outgoing_nodes in self.outgoing_mapping.items():
            for node in outgoing_nodes:
                self.createLine(p1, node)

        self._scene.setSceneRect(
            0,
            0,
            (len(self.levels) + 2) * COLUMN_SPACING + DISTANCE_BETWEEN,
            max_height,
        )
        self._ui.graphicsView.setScene(self._scene)

    def copyItem(self, name):
        is_ds = isinstance(self.current_items[name].item_settings, DataSourceSettings)
        copied_settings = copy.deepcopy(self.current_items[name].item_settings)
        if is_ds:
            name = copied_settings.name
        x = 1
        while f"{name}_copy_{x}" in (
            self.current_settings.settings.data_sources
            if is_ds
            else self.current_settings.settings.action_list
        ):
            x += 1
        new_name = f"{name}_copy_{x}"
        copied_settings.name = new_name
        (
            self.current_settings.settings.data_sources
            if is_ds
            else self.current_settings.settings.action_list
        )[new_name] = copied_settings
        self.setConfig(self.current_settings)

    def editItem(self, name):
        pass

    def removeItem(self, name):
        pass

    CONTEXT_RESULT_FUNCTIONS = {
        ContextResultType.COPY: copyItem,
        ContextResultType.EDIT: editItem,
        ContextResultType.REMOVE: removeItem,
    }

    def contextResult(self, context_result: ContextResult):
        if context_result.type_ in AlgoTopoView.CONTEXT_RESULT_FUNCTIONS:
            AlgoTopoView.CONTEXT_RESULT_FUNCTIONS[context_result.type_](
                self, context_result.name
            )
        else:
            assert False, "Invalid context result type"

    def getTutorialClasses(self) -> typing.List:
        return [self]
