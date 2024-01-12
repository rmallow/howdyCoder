from PySide6.QtWidgets import QGraphicsSceneContextMenuEvent, QGraphicsSceneHoverEvent
from ...core.dataStructs import ItemSettings

from PySide6 import QtWidgets, QtCore, QtGui

import typing
from dataclasses import dataclass
from enum import Enum


class ContextResultType(Enum):
    REMOVE = "Remove"
    EDIT = "Edit"
    COPY = "Copy"


@dataclass(frozen=True)
class ContextResult:
    type_: ContextResultType = ContextResultType.REMOVE
    name: str = ""


DISTANCE_FROM_BOUNDARY = 15
ITEM_MARGIN = 10
ITEM_TEXT_GAP = 16


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


class TopoSignalController(QtCore.QObject):
    mouseEnter = QtCore.Signal(str)
    mouseLeft = QtCore.Signal()
    mouseRelease = QtCore.Signal(str)
    contextResult = QtCore.Signal(object)


class ConnectedRectItem(ConnectedMixin, QtWidgets.QGraphicsRectItem):
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
        self.create_children(item_settings, item_name=item_name)
        self.item_settings = item_settings
        self._name = item_name if item_name else item_settings.name
        self._signal_controller = signal_controller

        brush = QtGui.QBrush(QtCore.Qt.GlobalColor.white)
        self.setBrush(brush)

        pen = QtGui.QPen()
        pen.setWidthF(3)
        self.setPen(pen)

        self._boundary_left = boundary_left
        self._boundary_right = boundary_right

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self._signal_controller.mouseRelease.emit(self._name)
        if event.scenePos().x() < self._boundary_left:
            self.setX(self._boundary_left + DISTANCE_FROM_BOUNDARY)
        elif event.scenePos().x() > self._boundary_right:
            self.setX(self._boundary_right - DISTANCE_FROM_BOUNDARY)

    def hoverEnterEvent(self, event: QtWidgets.QGraphicsSceneHoverEvent):
        self._signal_controller.mouseEnter.emit(self._name)
        return super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self._signal_controller.mouseLeft.emit()
        return super().hoverLeaveEvent(event)

    def createTextItem(self, text: str, x: int, y: int):
        item = QtWidgets.QGraphicsSimpleTextItem()
        item.setText(text)
        item.setParentItem(self)
        item.setPos(x, y)
        return item

    def createLineItem(self, x: int, y: int):
        item = QtWidgets.QGraphicsRectItem(0, 0, 50, 0)
        item.setParentItem(self)
        item.setPos(x, y)
        return item

    def create_children(self, item_settings: ItemSettings, item_name=""):
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

    def contextMenuEvent(self, event: QGraphicsSceneContextMenuEvent) -> None:
        event.accept()
        menu = QtWidgets.QMenu()
        for context_type_enum in ContextResultType:
            action = menu.addAction(context_type_enum.value)
            context_res = ContextResult(context_type_enum, self._name)
            action.triggered.connect(
                lambda _=None, val=context_res: self._signal_controller.contextResult.emit(
                    val
                )
            )
        menu.exec(event.screenPos())
