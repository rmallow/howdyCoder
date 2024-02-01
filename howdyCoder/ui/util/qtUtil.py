import typing

from PySide6 import QtWidgets, QtCore, QtGui


def setWordWrapOnButton(button: QtWidgets.QPushButton):
    text = button.text()
    button.setText("")
    label = QtWidgets.QLabel(text, button)
    label.setWordWrap(True)
    layout = QtWidgets.QHBoxLayout(button)
    layout.addWidget(label, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
    button.setLayout(layout)


class CompleterDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent: QtCore.QObject | None = ...) -> None:
        self._completer_strings: typing.List[str] = []
        super().__init__(parent)

    def setCompleterStrings(self, string_list):
        self._completer_strings = string_list

    def createEditor(
        self,
        parent: QtWidgets.QWidget,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex | QtCore.QPersistentModelIndex,
    ) -> QtWidgets.QWidget:
        editor = super().createEditor(parent, option, index)
        setCompleter(editor, self._completer_strings)
        return editor


def setCompleter(editor: QtWidgets.QWidget, completer_strings: typing.List[str]):
    try:
        editor.setCompleter(QtWidgets.QCompleter())
    except:
        return None
    completer = QtWidgets.QCompleter(completer_strings, editor)
    editor.setCompleter(completer)
    return completer


class StayOnTopInFocus:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        QtGui.QGuiApplication.instance().applicationStateChanged.connect(
            self.changeAlwaysOnTop
        )

    def changeAlwaysOnTop(self, state: QtCore.Qt.ApplicationState):
        if not self.isHidden():
            self.setWindowFlag(
                QtCore.Qt.WindowType.WindowStaysOnTopHint,
                state == QtCore.Qt.ApplicationState.ApplicationActive,
            )
            self.show()


class ExpandingLabelWidget(QtWidgets.QWidget):
    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QtWidgets.QHBoxLayout(self)
        self.label = ElidedLabel(text)
        self.button = QtWidgets.QPushButton("+")
        self.button.setToolTipDuration(0)
        self.button.released.connect(self.buttonReleased)
        self.label.updateFinished.connect(self.enableButton)
        self.label.elidedText.connect(self.button.setVisible)
        layout.addWidget(self.button)
        layout.addWidget(self.label)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self._button_enabled = True

    @QtCore.Slot()
    def enableButton(self):
        self._button_enabled = True

    @QtCore.Slot()
    def buttonReleased(self):
        if self._button_enabled:
            self._button_enabled = False
            self.label.toggleExpansion()
            self.button.setText("+" if self.button.text() == "-" else "-")

    def setText(self, text: str):
        self.label.text = text
        self.label.update()


class ElidedLabel(QtWidgets.QLabel):
    updateFinished = QtCore.Signal()
    elidedText = QtCore.Signal(bool)

    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = text
        self._collapsed = self._elide_text = True
        self.min_height_collapsed = None
        self.setWordWrap(True)
        self.setMinimumWidth(500)
        self.setMaximumWidth(500)
        self.setMaximumHeight(1)

    def paintEvent(self, e: QtGui.QPaintEvent) -> None:
        if not self._elide_text:
            self.setText(self.text)
            return super().paintEvent(e)
        self.setText("")
        painter = QtGui.QPainter(self)
        text_document = QtGui.QTextDocument(self.text, self)
        block = text_document.begin()
        lines_drawn = y = max_width = height = 0
        while block.isValid() and lines_drawn < 3:
            if not block.isVisible():
                block = block.next()
                continue
            layout = block.layout()
            rect = text_document.documentLayout().blockBoundingRect(block)
            height = rect.height()
            max_width = max(max_width, rect.width())
            if block.text().strip():
                layout.draw(painter, QtCore.QPoint(0, 0))
                lines_drawn += 1
                y += height + painter.fontMetrics().lineSpacing()
                end_point = layout.position()
            block = block.next()

        if block.isValid():
            painter.drawText(
                QtCore.QPoint(
                    max_width // 2,
                    end_point.y() + height + painter.fontMetrics().lineSpacing(),
                ),
                "...",
            )
        self.elidedText.emit(block.isValid())
        if self.min_height_collapsed is None:
            self.min_height_collapsed = y
            self.setMinimumHeight(self.min_height_collapsed)
            self.setMaximumHeight(self.min_height_collapsed)
        painter.end()

    def animationFinished(self):
        if self._collapsed:
            self._elide_text = True
            self.update()
        self.updateFinished.emit()

    @QtCore.Slot()
    def toggleExpansion(self):
        min_height = max_height = 0
        if self._collapsed:
            self._elide_text = False
            self._collapsed = False
            fm = self.fontMetrics()
            rect = self.rect()
            rect.setHeight(10000)
            min_height = max_height = fm.boundingRect(
                rect, QtCore.Qt.TextFlag.TextWordWrap, self.text
            ).height()
        else:
            self._collapsed = True
            min_height = max_height = self.min_height_collapsed

        self.min_anim = QtCore.QPropertyAnimation(self, b"minimumHeight")
        self.min_anim.setDuration(1000)
        self.min_anim.setStartValue(self.minimumHeight())
        self.min_anim.setEndValue(min_height)

        self.max_anim = QtCore.QPropertyAnimation(self, b"maximumHeight")
        self.max_anim.setDuration(1000)
        self.max_anim.setStartValue(self.maximumHeight())
        self.max_anim.setEndValue(max_height)
        self.group = QtCore.QParallelAnimationGroup()
        self.group.addAnimation(self.min_anim)
        self.group.addAnimation(self.max_anim)
        self.group.start()
        self.group.finished.connect(self.animationFinished)


class WordWrapHeader(QtWidgets.QHeaderView):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setDefaultAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.TextFlag.TextWordWrap
        )

    def sectionSizeFromContents(self, logicalIndex: int) -> QtCore.QSize:
        text = self.model().headerData(
            logicalIndex, self.orientation(), QtCore.Qt.ItemDataRole.DisplayRole
        )
        fM = self.fontMetrics()
        rect = fM.boundingRect(
            QtCore.QRect(0, 0, self.sectionSize(logicalIndex), 5000),
            self.defaultAlignment(),
            text,
        )
        buffer = QtCore.QSize(2, 25)
        together = rect.size() + buffer
        return together
