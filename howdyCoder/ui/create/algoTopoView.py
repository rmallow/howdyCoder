from ..uiConstants import SceneMode
from .algoTopoItem import ConnectedRectItem, TopoSignalController, ColorRank, AlgoLine

from ..contextMenu import (
    ContextResultType,
    createAndDisplayMenu,
    handleContextResult,
)

from ..qtUiFiles import ui_algoTopoView

from ..tutorialOverlay import AbstractTutorialClass
from ..util import abstractQt

from ...core.dataStructs import (
    ProgramSettings,
    AlgoSettings,
    DataSourceSettings,
    ItemSettings,
    ActionSettings,
)

from ...core.commonGlobals import ActionTypeEnum
from ...core import topoSort

from ...commonUtil.helpers import getDupeName

import typing
import copy
from collections import defaultdict
from enum import IntEnum, auto

from PySide6 import QtWidgets, QtCore, QtGui

COLUMN_SPACING = 250
DISTANCE_BETWEEN = 50


class SceneZIndex(IntEnum):
    BASE = auto()
    LINE = auto()
    ITEM = auto()


class AlgoTopoScene(QtWidgets.QGraphicsScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.signal_controller = TopoSignalController(self)
        self.current_items: typing.Dict[str, ConnectedRectItem] = {}
        self.line_mapping: typing.Dict[
            typing.Tuple[str, str], QtWidgets.QGraphicsLineItem
        ] = {}
        self.current_hover_item = ""
        self.current_selected_item = ""

        self.signal_controller.mouseEnter.connect(self.itemHoverEnter)
        self.signal_controller.mouseLeft.connect(self.itemHoverLeft)
        self.signal_controller.mouseRelease.connect(self.itemSelected)

        self.levels: typing.List[typing.List[str]] = [[]]
        self.outgoing_mapping: topoSort.NodeMapping = defaultdict(list)
        self.incoming_mapping: topoSort.NodeMapping = defaultdict(list)

    def reset(self):
        self.current_items = {}
        self.line_mapping = {}
        self.current_hover_item = ""
        self.current_selected_item = ""
        self.clear()

    def dfs(self, name, direction_container, item_action, line_action):
        item_action(self.current_items[name])
        for other in direction_container[name]:
            line_action(self.line_mapping[(name, other)])
            self.dfs(other, direction_container, item_action, line_action)

    def highlightNodes(
        self, name: str, color: QtCore.Qt.GlobalColor | None, color_rank=ColorRank.BASE
    ):
        action = lambda item: item.changeColor(color, color_rank)
        self.dfs(name, self.outgoing_mapping, action, action)
        self.dfs(name, self.incoming_mapping, action, action)

    def createLine(self, name_p1: str, name_p2: str):
        if name_p1 in self.current_items and name_p2 in self.current_items:
            item_p1 = self.current_items[name_p1]
            item_p2 = self.current_items[name_p2]
            line = AlgoLine(
                item_p1.getCenter().x(),
                item_p1.getCenter().y(),
                item_p2.getCenter().x(),
                item_p2.getCenter().y(),
            )
            self.addItem(line)
            pen = line.pen()
            pen.setWidthF(3)
            line.setPen(pen)
            line.setZValue(SceneZIndex.LINE.value)
            item_p1.addLine(line, True)
            item_p2.addLine(line, False)
            self.line_mapping[(name_p1, name_p2)] = line
            self.line_mapping[(name_p2, name_p1)] = line

    def changeColorHelper(
        self,
        name: str,
        color: QtCore.Qt.GlobalColor | None,
        color_rank: ColorRank = ColorRank.BASE,
    ):
        if name in self.current_items:
            self.current_items[name].changeColor(color, color_rank)

    def itemSelected(self, name):
        self.changeColorHelper(self.current_selected_item, None, ColorRank.SELECTED)
        self.current_selected_item = name
        if self.current_selected_item:
            self.changeColorHelper(
                self.current_selected_item,
                QtCore.Qt.GlobalColor.yellow,
                ColorRank.SELECTED,
            )

    def itemHoverEnter(self, name):
        self.current_hover_item = name
        self.highlightNodes(name, QtCore.Qt.GlobalColor.red, ColorRank.HOVER)

    def itemHoverLeft(self):
        if self.current_hover_item:
            self.highlightNodes(self.current_hover_item, None, ColorRank.HOVER)
        self.current_hover_item = ""

    def setConfig(self, creator_config: ProgramSettings):
        (
            self.levels,
            self.outgoing_mapping,
            self.incoming_mapping,
        ) = topoSort.getTopoSort(creator_config.settings)
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
                    self.signal_controller,
                    item_name=name,
                    boundary_left=x * COLUMN_SPACING,
                    boundary_right=(x + 1) * COLUMN_SPACING - DISTANCE_BETWEEN,
                )
                item.setZValue(SceneZIndex.ITEM.value)
                self.current_items[name] = item
                item.setPos(x * COLUMN_SPACING + DISTANCE_BETWEEN, last_y)
                last_y += item.boundingRect().height() + DISTANCE_BETWEEN
                self.addItem(item)
            max_height = max(max_height, last_y)
        for p1, outgoing_nodes in self.outgoing_mapping.items():
            for node in outgoing_nodes:
                self.createLine(p1, node)

        self.setSceneRect(
            0,
            0,
            (len(self.levels) + 2) * COLUMN_SPACING + DISTANCE_BETWEEN,
            max_height,
        )

    def setMode(self, mode: SceneMode, action_being_edited: str = ""):
        self.itemHoverLeft()
        self.itemSelected("")
        for _, item in self.current_items.items():
            item.setMode(mode)
            item.resetColor()
            item.show()
            item.setSelectable(True)
        for line in self.line_mapping.values():
            line.show()

        if mode == SceneMode.ACTION:

            def hideBoth(item: ConnectedRectItem):
                item.hide()
                item.hideConnectedLines()

            if action_being_edited in self.current_items:
                for outgoing in self.outgoing_mapping[action_being_edited]:
                    self.dfs(outgoing, self.outgoing_mapping, hideBoth, lambda _: None)
                self.changeColorHelper(
                    action_being_edited,
                    QtCore.Qt.GlobalColor.blue,
                    ColorRank.CURRENT_EDIT,
                )
                self.current_items[action_being_edited].setSelectable(False)

            for item in self.current_items.values():
                if (
                    item._name != action_being_edited
                    and item.item_settings.type_ == ActionTypeEnum.TRIGGER.value
                ):
                    hideBoth(item)

    def contextMenuEvent(self, event: QtWidgets.QGraphicsSceneContextMenuEvent) -> None:
        super().contextMenuEvent(event)
        # event could be accepted by an item, iff not we will display a context menu here
        if not event.isAccepted():
            createAndDisplayMenu(
                event.screenPos(),
                [ContextResultType.ADD_ACTION, ContextResultType.ADD_DATA_SOURCE],
                self.signal_controller.contextResult,
            )


class AlgoTopoView(
    AbstractTutorialClass,
    QtWidgets.QWidget,
    metaclass=abstractQt.getAbstactQtResolver(QtWidgets.QWidget, AbstractTutorialClass),
):
    TUTORIAL_RESOURCE_PREFIX = "None"

    openWizard = QtCore.Signal(ItemSettings)
    addItem = QtCore.Signal(ItemSettings)
    editItem = QtCore.Signal(ItemSettings)
    finished = QtCore.Signal(str)
    # remove by item settings so we know if ds or not
    removeItem = QtCore.Signal(ItemSettings)

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

        self.scene = AlgoTopoScene(parent=self)
        self._ui.graphicsView.setScene(self.scene)

        self.scene.signal_controller.contextResult.connect(
            lambda res: handleContextResult(
                self, res, AlgoTopoView.CONTEXT_RESULT_FUNCTIONS
            )
        )

        self.current_settings: ProgramSettings = None

        self._ui.addButton.released.connect(self.displayAddMenu)
        self._ui.removeButton.released.connect(
            lambda: self.removeItemMenu(self.scene.current_selected_item)
        )
        self._ui.editButton.released.connect(
            lambda: self.editItemMenu(self.scene.current_selected_item)
        )
        self._ui.copyButton.released.connect(
            lambda: self.copyItemMenu(self.scene.current_selected_item)
        )
        self._ui.finishButton.released.connect(
            lambda: self.finished.emit(self._ui.nameEdit.text())
        )
        self._ui.nameEdit.textChanged.connect(self.noBlankName)

    def reset(self):
        self.current_settings = None
        self.scene.reset()

    def setConfigFirstTime(self, creator_config: ProgramSettings):
        self._ui.nameEdit.clear()
        self._ui.nameEdit.setText(creator_config.name)
        self.setConfig(creator_config)

    def setConfig(self, creator_config: ProgramSettings):
        self.reset()
        self.current_settings = copy.deepcopy(creator_config)
        self.scene.setConfig(self.current_settings)

    def copyItemMenu(self, name: str) -> str:
        copied_settings = copy.deepcopy(self.scene.current_items[name].item_settings)
        copied_settings.name = getDupeName(
            copied_settings.name,
            self.current_settings.settings.data_sources
            if self.scene.current_items[name].item_settings.isDataSource()
            else self.current_settings.settings.action_list,
        )
        self.addItem.emit(copied_settings)

    def editItemMenu(self, name: str):
        self.editItem.emit(self.scene.current_items[name].item_settings)

    def removeItemMenu(self, name: str):
        self.removeItem.emit(self.scene.current_items[name].item_settings)

    def addActionMenu(self, _):
        self.openWizard.emit(ActionSettings())

    def addDataSourceMenu(self, _):
        self.openWizard.emit(DataSourceSettings())

    def getTutorialClasses(self) -> typing.List:
        return [self]

    @QtCore.Slot()
    def displayAddMenu(self):
        createAndDisplayMenu(
            QtGui.QCursor.pos(),
            [ContextResultType.ADD_ACTION, ContextResultType.ADD_DATA_SOURCE],
            self.scene.signal_controller.contextResult,
        )

    @QtCore.Slot()
    def noBlankName(self) -> str:
        if not self._ui.nameEdit.text():
            self._ui.nameEdit.setText(AlgoSettings.DEFAULT_NAME)

    CONTEXT_RESULT_FUNCTIONS = {
        ContextResultType.COPY: copyItemMenu,
        ContextResultType.EDIT: editItemMenu,
        ContextResultType.REMOVE: removeItemMenu,
        ContextResultType.ADD_ACTION: addActionMenu,
        ContextResultType.ADD_DATA_SOURCE: addDataSourceMenu,
    }
