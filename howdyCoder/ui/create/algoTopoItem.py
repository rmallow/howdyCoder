from ..uiConstants import SceneMode
from ..contextMenu import ContextResultType, createAndDisplayMenu
from ...core.dataStructs import ItemSettings

from PySide6 import QtWidgets, QtCore, QtGui

import typing
from dataclasses import dataclass
from enum import Enum, IntEnum, auto
import heapq


DISTANCE_FROM_BOUNDARY = 15
ITEM_MARGIN = 10
ITEM_TEXT_GAP = 16
MAX_TEXT_WIDTH = 150


class VariableDragData(QtCore.QMimeData):
    def __init__(self, text: str) -> None:
        super().__init__()
        self.setText(text)


class ConnectedMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAcceptHoverEvents(True)
        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(
            QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemSendsScenePositionChanges
        )
        self._lines = []

    def addLine(self, line: QtWidgets.QGraphicsLineItem, is_p1: bool):
        self._lines.append((line, is_p1))

    def itemChange(
        self, change: QtWidgets.QGraphicsItem.GraphicsItemChange, value: typing.Any
    ) -> typing.Any:
        if (
            change == QtWidgets.QGraphicsItem.GraphicsItemChange.ItemPositionChange
            and self.scene()
        ):
            self.moveLinesToCenter(value)
        return super().itemChange(change, value)

    def moveLinesToCenter(self, new_pos: QtCore.QPointF):
        x_offset = self.boundingRect().x() + self.boundingRect().width() / 2
        y_offset = self.boundingRect().y() + self.boundingRect().height() / 2

        new_center = QtCore.QPointF(new_pos.x() + x_offset, new_pos.y() + y_offset)

        for line, is_p1 in self._lines:
            p1 = new_center if is_p1 else line.line().p1()
            p2 = line.line().p2() if is_p1 else new_center
            line.setLine(QtCore.QLineF(p1, p2))

    def getCenter(self) -> QtCore.QPointF:
        x_offset = self.boundingRect().x() + self.boundingRect().width() / 2
        y_offset = self.boundingRect().y() + self.boundingRect().height() / 2
        return QtCore.QPointF(self.x() + x_offset, self.y() + y_offset)

    def hideConnectedLines(self):
        for line in self._lines:
            line[0].hide()


class TopoSignalController(QtCore.QObject):
    mouseEnter = QtCore.Signal(str)
    mouseLeft = QtCore.Signal()
    mouseRelease = QtCore.Signal(str)
    contextResult = QtCore.Signal(object)


class ColorRank(IntEnum):
    OVERRIDE = 0
    CURRENT_EDIT = auto()
    SELECTED = auto()
    HOVER = auto()
    BASE = auto()


class ColorRankMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._color_ranking = [None] * len(ColorRank)

    def _changeColor(self, color: QtCore.Qt.GlobalColor | None):
        """Internal use for changing the color, external should add to the color ranking heap"""
        pen = self.pen()
        pen.setColor(color)
        self.setPen(pen)

    def changeColor(
        self,
        color: QtCore.Qt.GlobalColor | None,
        color_rank: ColorRank = ColorRank.BASE,
    ):
        """
        Add to the color ranking then change the color
        For now this is only iterating over 5 ranks so it shouldn't matter
        If this is increased, then consideration should be taken of how this is done so it's not an O(n) operation each time
        where n is the rank but each rank has to be able to be added and removed as seen fit
        """
        self._color_ranking[color_rank.value] = color
        current_color = QtCore.Qt.GlobalColor.black
        try:
            current_color = next(
                color for color in self._color_ranking if color is not None
            )
        except StopIteration as _:
            pass
        self._changeColor(current_color)

    def resetColor(self):
        self._color_ranking = [None] * len(ColorRank)


class AlgoLine(ColorRankMixin, QtWidgets.QGraphicsLineItem):
    pass


class ConnectedRectItem(ConnectedMixin, ColorRankMixin, QtWidgets.QGraphicsRectItem):
    def __init__(
        self,
        item_settings: ItemSettings,
        signal_controller: TopoSignalController,
        item_name="",
        boundary_left=0,
        boundary_right=1,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.createChildren(item_settings, item_name=item_name)
        self.item_settings: ItemSettings = item_settings
        self._name = item_name if item_name else item_settings.name
        self._signal_controller = signal_controller
        self.mode: SceneMode = SceneMode.TOPO_VIEW
        self.selectable: bool = True

        brush = QtGui.QBrush(QtCore.Qt.GlobalColor.white)
        self.setBrush(brush)

        pen = QtGui.QPen()
        pen.setWidthF(3)
        self.setPen(pen)

        self._boundary_left = boundary_left
        self._boundary_right = boundary_right

    def reset(self):
        self.selectable = True
        self.mode = SceneMode.TOPO_VIEW
        self.show()

    def setSelectable(self, selectable: bool):
        self.selectable = selectable

    def setMode(self, mode: SceneMode):
        self.mode = mode

    def mouseMoveEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent):
        if self.mode == SceneMode.ACTION and self.selectable:
            drag = QtGui.QDrag(event.widget())
            drag_data = VariableDragData(self._name)
            drag.setMimeData(drag_data)
            drag.exec(QtCore.Qt.DropAction.MoveAction)
        elif self.mode != SceneMode.ACTION:
            return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if self.selectable:
            self._signal_controller.mouseRelease.emit(self._name)
            if self.mode != SceneMode.ACTION:
                if event.scenePos().x() < self._boundary_left:
                    self.setX(self._boundary_left + DISTANCE_FROM_BOUNDARY)
                elif event.scenePos().x() > self._boundary_right:
                    self.setX(self._boundary_right - DISTANCE_FROM_BOUNDARY)

    def hoverEnterEvent(self, event: QtWidgets.QGraphicsSceneHoverEvent):
        self._signal_controller.mouseEnter.emit(self._name)
        return super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event: QtWidgets.QGraphicsSceneHoverEvent) -> None:
        self._signal_controller.mouseLeft.emit()
        return super().hoverLeaveEvent(event)

    def createTextItem(self, text: str, x: int, y: int):
        """Adding the parent item to the constructor caused text to not appear, but using setParentItem instead works"""
        item = QtWidgets.QGraphicsTextItem(text)
        item.setDefaultTextColor(QtCore.Qt.GlobalColor.black)
        item.setParentItem(self)
        item.setTextWidth(MAX_TEXT_WIDTH)
        item.setPos(x, y)
        return item

    def createLineItem(self, x: int, y: int):
        item = QtWidgets.QGraphicsRectItem(0, 0, 50, 0)
        item.setParentItem(self)
        item.setPos(x, y)
        return item

    def createChildren(self, item_settings: ItemSettings, item_name=""):
        text_list = [
            item_settings.type_,
            item_name if item_name else item_settings.name,
        ]
        lines = []
        last_y = ITEM_MARGIN
        width = 0
        for x in range(len(text_list)):
            text_item = self.createTextItem(text_list[x], ITEM_MARGIN, last_y)
            last_y += text_item.boundingRect().height()
            width = max(width, text_item.boundingRect().width() + ITEM_MARGIN * 2)
            if x != len(text_list) - 1:
                last_y += ITEM_TEXT_GAP // 2
                line_item = self.createLineItem(0, last_y)
                lines.append(line_item)
                last_y += line_item.boundingRect().height()
                last_y += ITEM_TEXT_GAP // 2
        for line_item in lines:
            line_item.setRect(0, 0, width, 0)
        self.setRect(0, 0, width, last_y + ITEM_MARGIN)

    ITEM_CONTEXT_RESULT_TOPO_TYPES = [
        ContextResultType.COPY,
        ContextResultType.EDIT,
        ContextResultType.REMOVE,
    ]

    ITEM_CONTEXT_RESULT_ACTION_TYPES = [ContextResultType.SELECT]

    def contextMenuEvent(self, event: QtWidgets.QGraphicsSceneContextMenuEvent) -> None:
        if self.selectable:
            event.accept()
            createAndDisplayMenu(
                event.screenPos(),
                self.ITEM_CONTEXT_RESULT_TOPO_TYPES
                if self.mode == SceneMode.TOPO_VIEW
                else self.ITEM_CONTEXT_RESULT_ACTION_TYPES,
                self._signal_controller.contextResult,
                name=self._name,
            )
