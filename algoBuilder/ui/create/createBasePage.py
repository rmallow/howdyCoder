from ...core.commonGlobals import UI_GROUP
from ..uiConstants import PageKeys
from ...commonUtil import mpLogging

from abc import ABC, abstractmethod
import typing
from enum import Enum

from PySide2 import QtWidgets, QtCore


class CreateBasePageMeta(type(ABC), type(QtWidgets.QWidget)):
    pass


class CreateBasePage(QtWidgets.QWidget, ABC, metaclass=CreateBasePageMeta):
    PAGE_KEY: Enum = None
    EXIT: Enum = None
    EXIT_LABEL: str = ""

    nextPage = QtCore.Signal()
    manualExit = QtCore.Signal(PageKeys)
    enableNext = QtCore.Signal(bool)
    enableBack = QtCore.Signal(bool)

    def __init__(
        self,
        current_config: typing.Dict[str, typing.Any],
        parent: typing.Optional[QtWidgets.QWidget] = None,
        f: QtCore.Qt.WindowFlags = QtCore.Qt.WindowFlags(),
    ) -> None:
        super().__init__(parent, f)
        assert self.PAGE_KEY, "PAGE_KEY not assigned by sub class"
        self.current_config: typing.Dict[str, typing.Any] = current_config
        self.temp_config: typing.Dict[str, typing.Any] = None  # assigned after the fact
        self.config_keys = []
        self.next_enabled = True
        self.back_enabled = True

    def getConfigSection(self) -> typing.Dict[str, typing.Any]:
        curr = self.current_config
        for k in self.config_keys:
            if k not in curr:
                mpLogging.critical(
                    f"Key not found in current config",
                    group=UI_GROUP,
                    description=f"Keys: {self.config_keys}, config: {self.current_config}",
                )
                return {}
            curr = curr[k]
        return curr

    def getTempConfig(self) -> typing.Dict[str, typing.Any]:
        return self.temp_config

    def getTempConfigFirstValue(self):
        return next(iter(self.temp_config.values()))

    def enableCheck(self):
        """Can be used as a slot for changing inputs on each page"""
        self.next_enabled = self.validate()
        self.enableNext.emit(self.next_enabled)

    def validateText(self, text: str) -> bool:
        """Return true if text exists and first letter isn't a number, this doesn't need to be crazy"""
        return text.strip() and not text.strip()[0].isnumeric()

    @abstractmethod
    def validate(self) -> bool:
        """Return true if all the page fields are valid"""
        return False

    @abstractmethod
    def loadPage(self, keys: typing.List[str]) -> None:
        """Pass in settings to load the page"""
        self.config_keys = keys

    @abstractmethod
    def save(self) -> None:
        """Save the page's values into the config or for UI only info into data structures"""
        pass

    @abstractmethod
    def getKeysForNextPage(self) -> typing.Any:
        """
        Get keys for the next page in the sequence. By default pass ahead all of the keys
        """
        return self.config_keys

    @abstractmethod
    def reset(self) -> None:
        """Clear the widget fields and reset it for new entries"""
        return

    def drawingFix(self):
        """
        When a page is changed, the old page is animated to fade out and removed from the layout
        The new page is added in its place and faded in.
        During this process it appears that some parts of the page are not drawn correctly.
        For example, if you add data to a model that is displayed by a QTableView, that data won't appear
        correctly until you reszie the window, click elsewhere or hover over the table.
        This appears to happen with classes that inherit from QAbstractScrollArea like QTableView, QPlainTextEdit
        A fix for at least these classes is calling obj.viewport().repaint() in the derived page's drawingFix function
        An overrarching fix could be changing the way the animation function works? but unsure and not investigated
        """
        for child in self.findChildren(QtWidgets.QAbstractScrollArea):
            child.viewport().repaint()
