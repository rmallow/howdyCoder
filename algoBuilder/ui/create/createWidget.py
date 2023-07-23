from .createBasePage import CreateBasePage

# various pages
from .createNamePage import CreateNamePage
from .createAddPage import CreateActionAddPage, CreateDataSourceAddPage
from .createDataSourceTypePage import CreateDataSourceTypePage
from .createDataSourceSettingsPage import CreateDataSourceSettingsPage
from .createParametersPage import (
    CreateDataSourceParametersPage,
    CreateActionParametersPage,
)
from .createConfirmPage import (
    CreateDataSourceConfirmPage,
    CreateActionConfirmPage,
    CreateFinalConfirmPage,
)
from .createActionTypePage import CreateActionTypePage
from .createActionSettingsPage import CreateActionSettingsPage

from ..uiConstants import PageKeys
from ..qtUiFiles import ui_createWidget

from ..util import animations

from ...commonUtil.helpers import createErrorLabel

from PySide6 import QtWidgets, QtCore

from dataclasses import dataclass, fields
import typing


@dataclass
class createWidgetPage:
    name: str
    page: CreateBasePage

    def __iter__(self):
        for field in fields(self):
            yield getattr(self, field.name)


CREATION_WIDGET_PAGES: typing.List[CreateBasePage] = [
    CreateNamePage,
    CreateDataSourceAddPage,
    CreateDataSourceTypePage,
    CreateDataSourceSettingsPage,
    CreateDataSourceParametersPage,
    CreateDataSourceConfirmPage,
    CreateActionAddPage,
    CreateActionTypePage,
    CreateActionSettingsPage,
    CreateActionParametersPage,
    CreateActionConfirmPage,
    CreateFinalConfirmPage,
]


class CreateWidget(QtWidgets.QWidget):
    addAlgo = QtCore.Signal(dict)

    def __init__(
        self,
        parent: typing.Optional[QtWidgets.QWidget] = None,
        f: QtCore.Qt.WindowFlags = QtCore.Qt.WindowFlags(),
    ) -> None:
        super().__init__(parent, f)

        # Load UI file
        self._ui = ui_createWidget.Ui_CreateWidget()
        self._ui.setupUi(self)
        self.current_config = {}
        self.temp_config = {}

        self._createWidgetBoxLayout = QtWidgets.QVBoxLayout(self._ui.createWidgetBox)
        self._createWidgetBoxLayout.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))
        self._ui.createWidgetBox.setLayout(self._createWidgetBoxLayout)

        self._create_widgets_list: typing.List[createWidgetPage] = []

        self._current_exit_page: PageKeys = PageKeys.NO_PAGE

        self.loadCreationWidgets()
        self.loadProgressSteps()
        self.loadCurrentPage()

        # don't want clicking through till animation is over so we disable button on press
        for _, page in self._create_widgets_list:
            page.nextPage.connect(self.nextPressed)
            page.enableNext.connect(self._ui.nextButton.setEnabled)
            page.enableBack.connect(self._ui.backButton.setEnabled)
            page.manualExit.connect(self.exitPressed)
        self._ui.nextButton.released.connect(self.nextPressed)
        self._ui.backButton.released.connect(self.backPressed)
        self._ui.exitButton.released.connect(self.exitPressed)

    def loadCreationWidgets(self) -> None:
        """
        Based on the mapping provided use the factory functions to create and load into the list
        """
        assert len(set(v.PAGE_KEY for v in CREATION_WIDGET_PAGES)) == len(
            CREATION_WIDGET_PAGES
        ), "Duplicate Creation Widget Page Keys"
        for widget_class in CREATION_WIDGET_PAGES:
            p = createWidgetPage(
                widget_class.PAGE_KEY.value, widget_class(self.current_config, self)
            )
            p.page.temp_config = self.temp_config
            self._create_widgets_list.append(p)
        self._current_index: int = 0

        for _, w in self._create_widgets_list:
            w.hide()

    def loadProgressSteps(self) -> None:
        """
        Use the keys provided to create the progress steps widget
        """
        steps = [page.PAGE_KEY.value for page in CREATION_WIDGET_PAGES]
        self._ui.progressSteps.setSteps(steps)

    def loadCurrentPage(self) -> None:
        """
        Clear out any widgets and set the layout to the current page
        """
        for _ in range(0, self._createWidgetBoxLayout.count()):
            self._createWidgetBoxLayout.takeAt(0).hide()
        self._createWidgetBoxLayout.addWidget(
            self._create_widgets_list[self._current_index].page
        )
        self._create_widgets_list[self._current_index].page.show()
        self._ui.backButton.setEnabled(
            self._current_index != 0
            and self._create_widgets_list[self._current_index].page.back_enabled
        )
        self._ui.nextButton.setEnabled(
            self._create_widgets_list[self._current_index].page.next_enabled
        )

    def changePage(self, newIndex: int):
        """Change the page to the given page with an animation, save the current page and check its validity"""
        if newIndex >= 0 and newIndex < len(self._create_widgets_list):
            # disable both the buttons, at the end of the animation they'll be reenabled
            self._ui.nextButton.setEnabled(False)
            self._ui.backButton.setEnabled(False)
            self._ui.exitButton.setEnabled(False)
            currentPage = self._create_widgets_list[self._current_index].page
            if valid_page := currentPage.validate():
                currentPage.save()
            # Get keys from the page before the page we are loading and put it in the page we are loading
            if newIndex > 0:
                keys = self._create_widgets_list[newIndex - 1].page.getKeysForNextPage()
                self._create_widgets_list[newIndex].page.loadPage(keys)
            animations.fadeStart(
                self._ui.createWidgetBox,
                self._create_widgets_list[self._current_index].page,
                self._create_widgets_list[newIndex].page,
                self._createWidgetBoxLayout,
                finishedSlot=lambda: self.animationFinished(newIndex),
            )
            self._ui.progressSteps.setCompletedStep(
                self._current_index,
                valid_page,
            )
            self._ui.progressSteps.goTo(newIndex)
            self._current_index = newIndex

    def nextPressed(self):
        """Go forward a page, if it's the last page then check for any error and save config"""
        if self._current_index == len(self._create_widgets_list) - 1:
            # The main window will change from the create widget to control
            self.addAlgo.emit(self.current_config)
            self.reset()
        else:
            self.changePage(self._current_index + 1)
            self._ui.nextButton.setText(
                "Finish"
                if self._current_index == len(self._create_widgets_list) - 1
                else "Next"
            )
            self._ui.backButton.setText(
                "Start Over"
                if self._current_index == len(self._create_widgets_list) - 1
                else "Back"
            )

    def backPressed(self):
        """Go back a page"""
        if self._current_index == len(self._create_widgets_list) - 1:
            # The back button/start over button was hit on the last page
            # rest all the pages
            message_box = QtWidgets.QMessageBox(self)
            message_box.setText("Are you sure you want to start over?")
            message_box.setInformativeText("The algo you've made will be deleted.")
            message_box.setStandardButtons(
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )
            message_box.setDefaultButton(QtWidgets.QMessageBox.No)
            message_box.setWindowModality(
                QtCore.Qt.WindowModality.ApplicationModal
            )  # redundancy for macOS
            if message_box.exec_() == QtWidgets.QMessageBox.No:
                return
            self.reset()
        else:
            self.changePage(self._current_index - 1)
        self._ui.nextButton.setText("Next")
        self._ui.backButton.setText("Back")

    def animationFinished(self, newIndex: int):
        """
        after widget animation is done, enable button and update widget
        """
        self._ui.backButton.setEnabled(
            self._create_widgets_list[newIndex].page.back_enabled
        )
        self._ui.nextButton.setEnabled(
            self._create_widgets_list[newIndex].page.next_enabled
        )
        self._ui.exitButton.setEnabled(True)
        if self._create_widgets_list[newIndex].page.EXIT_LABEL:
            self._ui.exitButton.setText(
                self._create_widgets_list[newIndex].page.EXIT_LABEL
            )
        if self._create_widgets_list[newIndex].page.EXIT:
            self._current_exit_page = self._create_widgets_list[newIndex].page.EXIT
        self._create_widgets_list[newIndex].page.update()
        self._create_widgets_list[newIndex].page.drawingFix()
        self._ui.scrollArea.viewport().update()

    @QtCore.Slot()
    def resetPages(self, reset_to_index: int) -> None:
        """
        From the current index to the given index, reset those pages by calling CreateBasePage::reset
        Using min, max in range here as reset_to_index could be before or after current index
        """
        for x in range(
            min(self._current_index, reset_to_index),
            max(self._current_index, reset_to_index) + 1,
        ):
            self._create_widgets_list[x].page.reset()

    def reset(self):
        self.resetPages(0)
        self.changePage(0)
        self._ui.progressSteps.reset()
        self.current_config.clear()
        self.temp_config.clear()

    def exitPressed(self, exit_page=None):
        if exit_page is None:
            exit_page = self._current_exit_page
        if exit_page is PageKeys.NO_PAGE:
            self.reset()
            self.addAlgo.emit({})
        else:
            index = None
            for i, v in enumerate(CREATION_WIDGET_PAGES):
                if v.PAGE_KEY is exit_page:
                    index = i
            if index is not None:
                self.resetPages(index)
                self.changePage(index)
