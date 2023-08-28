from ..tutorialOverlay import AbstractTutorialClass
from ..util import abstractQt
from ...core.commonGlobals import UI_GROUP, ItemSettings, AlgoSettings, GROUP_SET
from ..uiConstants import PageKeys
from ...commonUtil import mpLogging

from abc import abstractmethod
import typing
from enum import Enum

from PySide6 import QtWidgets, QtCore


class CreateBasePage(
    AbstractTutorialClass,
    QtWidgets.QWidget,
    metaclass=abstractQt.getAbstactQtResolver(QtWidgets.QWidget, AbstractTutorialClass),
):
    PAGE_KEY: Enum = None
    EXIT: Enum = None
    EXIT_LABEL: str = ""
    GROUP = ""

    nextPage = QtCore.Signal()
    manualExit = QtCore.Signal(PageKeys)
    enableNext = QtCore.Signal(bool)
    enableBack = QtCore.Signal(bool)

    def __init__(
        self,
        current_config: AlgoSettings,
        resource_prefix: str,
        parent: typing.Optional[QtWidgets.QWidget] = None,
        f: QtCore.Qt.WindowFlags = QtCore.Qt.WindowFlags(),
    ) -> None:
        super().__init__(resource_prefix, parent, f)
        assert self.PAGE_KEY, "PAGE_KEY not assigned by sub class"
        assert (
            self.GROUP and self.GROUP in GROUP_SET
        ), "GROUP not correctly assigned by sub class"
        self.current_config: AlgoSettings = current_config
        self.temp_config: ItemSettings = None  # assigned after the fact
        self.next_enabled = True
        self.back_enabled = True

    def __new__(self, *args, **kwargs):
        abstractQt.handleAbstractMethods(self)
        return super().__new__(self, *args, **kwargs)

    def getConfig(self) -> AlgoSettings:
        return self.current_config

    def getTempConfig(self) -> ItemSettings:
        return self.temp_config

    def getConfigGroup(self):
        return self.getConfig().getGroupDict(self.GROUP)

    def enableCheck(self):
        """Can be used as a slot for changing inputs on each page"""
        self.next_enabled = self.validate()
        self.enableNext.emit(self.next_enabled)

    def validateText(self, text: str) -> bool:
        """Return true if text exists and first letter isn't a number, this doesn't need to be crazy"""
        return text.strip() and not text.strip()[0].isnumeric()

    @abstractmethod
    def loadPage(self):
        pass

    @abstractmethod
    def validate(self) -> bool:
        """Return true if all the page fields are valid"""
        return False

    @abstractmethod
    def save(self) -> None:
        """Save the page's values into the config or for UI only info into data structures"""
        pass

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
