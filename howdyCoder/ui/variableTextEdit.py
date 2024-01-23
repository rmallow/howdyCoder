import typing

from PySide6 import QtCore, QtGui, QtWidgets

from enum import IntEnum, auto

from ..libraries.textMerger import STARTING_BRACE, ENDING_BRACE, isVarText

OBJECT_REPLACEMENT_CHARACTER = "\uFFFC"


class Property(IntEnum):
    TEXT_DATA = QtGui.QTextFormat.Property.UserProperty + 1


class ObjectTypes(IntEnum):
    VARIABLE_TEXT_OBJECT = QtGui.QTextFormat.ObjectTypes.UserObject + 1


class VariableDragData(QtCore.QMimeData):
    def __init__(self, text: str) -> None:
        super().__init__()
        self.setText(text)


class VariableTextObject(QtGui.QPyTextObject):
    def intrinsicSize(
        self, doc: QtGui.QTextDocument, posInDocument: int, format_: QtGui.QTextFormat
    ) -> QtCore.QSizeF:
        fm = QtGui.QFontMetricsF(doc.defaultFont())
        return fm.size(
            QtCore.Qt.TextFlag.TextSingleLine,
            format_.property(Property.TEXT_DATA.value),
        )

    def drawObject(
        self,
        painter: QtGui.QPainter,
        rect: QtCore.QRectF | QtCore.QRect,
        doc: QtGui.QTextDocument,
        posInDocument: int,
        format_: QtGui.QTextFormat,
    ) -> None:
        pen = painter.pen()
        pen.setColor(QtCore.Qt.GlobalColor.red)
        painter.setPen(pen)
        painter.drawText(
            rect,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignBottom,
            format_.property(Property.TEXT_DATA.value),
        )


class VariableTextEdit(QtWidgets.QTextEdit):
    insertedBlock = QtCore.Signal(str)
    removedBlocks = QtCore.Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.interface = VariableTextObject()
        self.document().documentLayout().registerHandler(
            ObjectTypes.VARIABLE_TEXT_OBJECT.value, self.interface
        )

        self.document().contentsChange.connect(self.checkChanges)

    def insertFromMimeData(self, source: QtCore.QMimeData) -> None:
        if isinstance(source, VariableDragData):
            self.insertTextBlock(source.text())
        else:
            super().insertFromMimeData(source)

    @QtCore.Slot()
    def insertTextBlock(self, text: str):
        format_ = QtGui.QTextCharFormat()
        format_.setObjectType(ObjectTypes.VARIABLE_TEXT_OBJECT.value)
        format_.setProperty(Property.TEXT_DATA.value, text)
        cursor = self.textCursor()
        cursor.insertText(OBJECT_REPLACEMENT_CHARACTER, format_)
        self.insertedBlock.emit(text)
        self.setTextCursor(cursor)

    @QtCore.Slot()
    def checkChanges(self, pos: int, removed: int, added: int):
        if removed > 0:
            self.undo()
            cursor = self.textCursor()
            cursor.setPosition(pos)
            for _ in range(removed):
                cursor.movePosition(
                    QtGui.QTextCursor.MoveOperation.NextCharacter,
                    QtGui.QTextCursor.MoveMode.KeepAnchor,
                )
                text = cursor.selectedText()
                cursor.clearSelection()
                if text == OBJECT_REPLACEMENT_CHARACTER:
                    self.removedBlocks.emit(
                        cursor.charFormat().property(Property.TEXT_DATA)
                    )
            self.redo()

    def getVariableText(self) -> typing.List:
        cursor = self.textCursor()
        cursor.movePosition(
            QtGui.QTextCursor.MoveOperation.Start, QtGui.QTextCursor.MoveMode.MoveAnchor
        )
        current_string = []
        res = []
        while cursor.movePosition(
            QtGui.QTextCursor.MoveOperation.NextCharacter,
            QtGui.QTextCursor.MoveMode.KeepAnchor,
        ):
            char = cursor.selectedText()
            cursor.clearSelection()
            if char == OBJECT_REPLACEMENT_CHARACTER:
                if current_string:
                    res.append("".join(current_string))
                res.append(
                    STARTING_BRACE
                    + cursor.charFormat().property(Property.TEXT_DATA)
                    + ENDING_BRACE
                )
                current_string = []
            else:
                current_string.append(char)
        if current_string:
            res.append("".join(current_string))
        return res

    def setTextFromList(
        self, variable_text_list: typing.List[str], current_items: typing.Dict
    ) -> None:
        for text in variable_text_list:
            if (
                isVarText(text)
                and text[len(STARTING_BRACE) : -len(ENDING_BRACE)] in current_items
                and current_items[
                    text[len(STARTING_BRACE) : -len(ENDING_BRACE)]
                ].isVisible()
            ):
                self._ui.drag_edit.insertTextBlock(
                    text[len(STARTING_BRACE) : -len(ENDING_BRACE)]
                )
            else:
                cursor = self._ui.drag_edit.textCursor()
                cursor.movePosition(
                    QtGui.QTextCursor.MoveOperation.End,
                    QtGui.QTextCursor.MoveMode.MoveAnchor,
                )
                cursor.insertText(text)
