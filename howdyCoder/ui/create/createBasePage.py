from .algoTopoView import AlgoTopoScene

from ...core.dataStructs import ProgramSettings, ItemSettings
from ..tutorialOverlay import AbstractTutorialClass
from ..util import abstractQt, qtResourceManager
from ..uiConstants import PageKeys, CreateWizardItemType

from dataclasses import dataclass, field
from abc import abstractmethod
import typing
from enum import Enum

from PySide6 import QtWidgets, QtCore


class ItemValidity(Enum):
    VALID = "Valid"
    INVALID = "Invalid"
    WARNING = "Warning"

    def getEnum(valid: bool):
        if valid:
            return ItemValidity.VALID
        else:
            return ItemValidity.INVALID


@dataclass
class HelperData:
    suggested_parameters: typing.List[str] = field(default_factory=list)

    def clear(self):
        self.__init__()


class CreateBasePage(
    AbstractTutorialClass,
    QtWidgets.QWidget,
    metaclass=abstractQt.getAbstactQtResolver(QtWidgets.QWidget, AbstractTutorialClass),
):
    PAGE_KEY: Enum = None

    nextPage = QtCore.Signal()
    manualExit = QtCore.Signal(PageKeys)
    enableBack = QtCore.Signal(bool)
    setSkipPages = QtCore.Signal(list)

    def __init__(
        self,
        current_config: ItemSettings,
        resource_prefix: str,
        parent: typing.Optional[QtWidgets.QWidget] = None,
        f: QtCore.Qt.WindowFlags = QtCore.Qt.WindowFlags(),
    ) -> None:
        super().__init__(resource_prefix, parent, f)
        assert self.PAGE_KEY, "PAGE_KEY not assigned by sub class"
        self.current_config: ItemSettings = current_config
        """
        These variables are assigned after init and can't be used in a constructor, in the future this could be changed
        if all subclasses were to takes *args and/or **kwargs as they should
        """
        self.helper_data: HelperData = None  # assigned after the fact
        self.creator_type: CreateWizardItemType = None  # assigned after the fact
        self.program_settings: ProgramSettings = None  # assigned after the fact
        self.scene: AlgoTopoScene = None  # assigned after the fact
        self.back_enabled = True
        self.next_enabled = True
        self.suggested_validity = ItemValidity.VALID

    def __new__(self, *args, **kwargs):
        abstractQt.handleAbstractMethods(self)
        return super().__new__(self, *args, **kwargs)

    def getConfig(self) -> ItemSettings:
        return self.current_config

    def getProgramSettings(self) -> ProgramSettings:
        return self.program_settings

    def getHelperData(self):
        return self.helper_data if self.helper_data is not None else HelperData()

    def populateParameters(self):
        pass

    def validateText(self, text: str) -> bool:
        """Return true if text exists and first letter isn't a number, this doesn't need to be crazy"""
        return bool(text.strip() and not text.strip()[0].isnumeric())

    @abstractmethod
    def loadPage(self):
        pass

    def validate(self) -> typing.Dict[QtWidgets.QWidget | str, ItemValidity]:
        """Return a mapping of widget to a result of validation for said widget"""
        return {}

    @abstractmethod
    def save(self) -> None:
        """Save the page's values into the config or for UI only info into data structures"""
        pass

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

    def addToSuggestedListWidget(
        self,
        list_widget: QtWidgets.QListWidget,
        current: typing.Set[str],
        suggested: typing.List[str],
    ):
        all_found = True

        def getIcon(name):
            nonlocal all_found
            if name not in current:
                all_found = False
            return qtResourceManager.getResourceByName(
                "icons",
                ("checkmark_green.png" if name in current else "x_red.png"),
            )

        list_widget.clear()
        added = set()
        for name in suggested:
            if name not in added:
                list_widget.addItem(QtWidgets.QListWidgetItem(getIcon(name), name))
                added.add(name)
        self.suggested_validity = (
            ItemValidity.VALID if all_found else ItemValidity.WARNING
        )
