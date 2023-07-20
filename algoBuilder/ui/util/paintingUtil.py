import typing

from PySide2 import QtWidgets, QtCore, QtGui


class Overlay(QtWidgets.QWidget):
    """
    Classes that use an overlay must define overlay paint
    """

    def __init__(
        self,
        parent: typing.Optional[QtWidgets.QWidget] = None,
        f: QtCore.Qt.WindowFlags = QtCore.Qt.WindowFlags(),
    ) -> None:
        super().__init__(parent, f)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        parent = self.parent()
        if parent is not None:
            parent.overlayPaint(event)


class OverlayFactoryFilter(QtCore.QObject):
    def __init__(self, parent: typing.Optional[QtCore.QObject] = None) -> None:
        self._overlay: Overlay = None
        super().__init__(parent)

    def eventFilter(self, watched: QtCore.QObject, event: QtCore.QEvent) -> bool:
        if not watched.isWidgetType():
            return False

        if event.type() == QtCore.QEvent.MouseButtonPress:
            if self._overlay is None:
                self._overlay = Overlay()
            self._overlay.setParent(watched)
            self._overlay.resize(watched.size())
            self._overlay.show()
        elif event.type() == QtCore.QEvent.Resize:
            if self._overlay and self._overlay.parentWidget() == watched:
                self._overlay.resize(watched.size())
        return False
