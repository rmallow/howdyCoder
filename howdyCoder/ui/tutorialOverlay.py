from .util import qtResourceManager
from .util import abstractQt

from abc import abstractmethod, ABC
import typing
import time

from PySide6 import QtWidgets, QtCore, QtGui


class OverlayWidget(QtWidgets.QWidget):
    """Created by Abstract Tutorial Class"""

    def __init__(
        self,
        parent: QtWidgets.QWidget | None = None,
        f: QtCore.Qt.WindowType = QtCore.Qt.WindowType(),
    ) -> None:
        super().__init__(parent, f)
        assert self.parent()  # parent must exist as overlay will match its size
        self._pixmap = None
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.changeParent()

    def changeParent(self):
        if self.parent():
            self.parent().installEventFilter(self)
            self.raise_()

    def eventFilter(self, watched: QtCore.QObject, event: QtCore.QEvent) -> bool:
        if watched == self.parent():
            if event.type() == QtCore.QEvent.Type.Resize:
                self.resize(event.size())
            elif event.type() == QtCore.QEvent.Type.ChildAdded:
                self.raise_()
        return super().eventFilter(watched, event)

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        if self._pixmap is not None:
            assert self._pixmap
            painter = QtGui.QPainter(self)
            painter.drawPixmap(self.rect(), self._pixmap)
            painter.end()
        else:
            return super().paintEvent(event)

    def changePixmap(self, new_pixmap: QtGui.QPixmap):
        self._pixmap = new_pixmap
        self.repaint()


class AbstractTutorialClass(ABC):
    """Used in conjunction with Overlay Widget, manages images for overlay as well as for finding sub widgets"""

    def __init__(self, resource_prefix: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """Make sure the current class is a qt object and that the resource is either intentionally none or has resources"""
        assert isinstance(self, QtCore.QObject)
        assert resource_prefix == "None" or qtResourceManager.getFilesInPrefix(
            resource_prefix, folder="Tutorial"
        )
        self._overlay = OverlayWidget(self)
        self.resource_prefix = resource_prefix
        self._current_index = None

    @abstractmethod
    def getTutorialClasses(self) -> typing.List:
        return []

    def changeOverlayPicture(self, new_pixmap: QtGui.QPixmap) -> None:
        self._overlay.changePixmap(new_pixmap)


class TutorialEventFilter(QtCore.QObject):
    PAUSE_BETWEEN_OVERLAYS = 0.6

    def __init__(
        self,
        top_level_filter_object: AbstractTutorialClass,
        parent: QtCore.QObject | None = None,
    ) -> None:
        super().__init__(parent)
        self._top_level_filter_object: AbstractTutorialClass = top_level_filter_object
        self._last_displayed = set()
        self._current_displayed = set()
        self._objs: typing.List[AbstractTutorialClass] = []
        self._obj_index = 0
        self._resource_index = 0
        self._last_button_press = 0.0
        self._tutorial_started = False

    def getNextValidObjIndex(self):
        while self._obj_index < len(self._objs) and (
            self._objs[self._obj_index].resource_prefix in self._last_displayed
            or not qtResourceManager.getFilesInPrefix(
                self._objs[self._obj_index].resource_prefix, folder="Tutorial"
            )
        ):
            self._obj_index += 1

    def setCurrentOverlayPicture(self):
        self._objs[self._obj_index].changeOverlayPicture(
            qtResourceManager.getResourceByIndex(
                self._objs[self._obj_index].resource_prefix,
                self._resource_index,
                folder="Tutorial",
            )
        )

    def eventFilter(self, watched: QtCore.QObject, event: QtCore.QEvent) -> bool:
        if (
            self._tutorial_started
            and event.type() == QtCore.QEvent.Type.MouseButtonPress
        ):
            # arbitrary pause time
            if time.time() - self._last_button_press > self.PAUSE_BETWEEN_OVERLAYS:
                if self._resource_index < len(
                    qtResourceManager.getFilesInPrefix(
                        self._objs[self._obj_index].resource_prefix, folder="Tutorial"
                    )
                ):
                    self.setCurrentOverlayPicture()
                    self._resource_index += 1
                else:
                    self._objs[self._obj_index].changeOverlayPicture(None)
                    self._obj_index += 1
                    self.getNextValidObjIndex()
                    self._resource_index = 0
                    if self._obj_index < len(self._objs):
                        self.setCurrentOverlayPicture()
                        self._resource_index += 1
                    else:
                        self._obj_index = self._resource_index = 0
                        self._tutorial_started = False
                        self._last_displayed = self._current_displayed
                self._last_button_press = time.time()
                self._top_level_filter_object.repaint()
            return True
        else:
            return super().eventFilter(watched, event)

    @QtCore.Slot()
    def tutorial_started(self):
        self._obj_index = self._resource_index = 0
        self._objs = self._top_level_filter_object.getTutorialClasses()
        self._current_displayed = set(obj.resource_prefix for obj in self._objs)
        if self._last_displayed == self._current_displayed:
            self._last_displayed = set()
        self.getNextValidObjIndex()
        self._tutorial_started = self._obj_index < len(self._objs)
        if self._tutorial_started:
            self._objs[self._obj_index].changeOverlayPicture(
                qtResourceManager.getResourceByIndex(
                    self._objs[self._obj_index].resource_prefix,
                    self._resource_index,
                    folder="Tutorial",
                )
            )
            self._resource_index += 1
            self._last_button_press = time.time()
            self._top_level_filter_object.repaint()
