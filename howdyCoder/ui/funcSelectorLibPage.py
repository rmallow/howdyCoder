from .funcSelectorPageBase import FuncSelectorPageBase
from .qtUiFiles import ui_funcSelectorLibPage


from ..core import librarySingleton
from ..core.libraryBase import Library
from ..core.dataStructs import FunctionSettings

import ast
import typing

from PySide6 import QtWidgets, QtCore, QtGui

CODE_ROLE = QtCore.Qt.UserRole + 1
SETTINGS_ROLE = CODE_ROLE + 1


class FuncSelectorLibPage(FuncSelectorPageBase):
    """
    Widget for selecting a function from a library
    """

    TUTORIAL_RESOURCE_PREFIX = "FuncSelectorLibrary"

    def __init__(
        self,
        parent: typing.Optional[QtWidgets.QWidget] = None,
        f: QtCore.Qt.WindowFlags = QtCore.Qt.WindowFlags(),
    ) -> None:
        super().__init__(self.TUTORIAL_RESOURCE_PREFIX, parent, f)
        self._ui = ui_funcSelectorLibPage.Ui_FuncSelectorLibPage()
        self._ui.setupUi(self)

        # setup model
        self._lib_model = QtGui.QStandardItemModel(self._ui.libView)
        self._lib_search_model = QtCore.QSortFilterProxyModel(self._ui.libView)
        self._lib_search_model.setSourceModel(self._lib_model)
        self._lib_search_model.setRecursiveFilteringEnabled(True)
        self._lib_search_model.setFilterCaseSensitivity(
            QtCore.Qt.CaseSensitivity.CaseInsensitive
        )
        self._ui.search_edit.textChanged.connect(self.filterChanged)

        self._ui.libView.setModel(self._lib_search_model)
        self._lib_search_model.rowsInserted.connect(self.alwaysExpand)
        self._ungrouped_item = QtGui.QStandardItem("Ungrouped")
        self._lib_model.appendRow(self._ungrouped_item)

        # connect signal and slots
        self._ui.libraryButton.pressed.connect(self.loadLibrary)
        self._ui.libView.clicked.connect(self.libItemSelected)
        self._ui.selectButton.pressed.connect(self.validateFunction)

        self._selectedIndex: QtCore.QModelIndex = None

    @QtCore.Slot()
    def filterChanged(self, text: str) -> None:
        self._lib_search_model.setFilterFixedString(text)

    @QtCore.Slot()
    def alwaysExpand(self, parent: QtCore.QModelIndex, first: int, last: int) -> None:
        # Keep the function tree view always expanded
        self._ui.libView.expandRecursively(parent)

    @QtCore.Slot()
    def loadLibrary(self) -> None:
        """
        Create a file selection dialog and load the library from the selected file

        The file must be a valid python library or an AFL
        If it is a python library it will try to parse the module into an AST
        After that it will create a root item with the path and name of the library
        the valid library funcs in the module will then be appended as children of the library item

        If it is an AFL, it was parse the yml config and directly populate the library
        Functions will have their own imports instead of all imports being for all functions
        There is compilation checking but this shouldn't be an issue unless the files are hand modified
        """
        file_dlg_return = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Select an algo library",
            ".",
            "Algo Function Library Files (*.afl);;Python Library Files (*.py)",
        )
        # the file name with full path is the first of the returned tuple
        if file_dlg_return is not None and len(file_dlg_return) > 0:
            file_path = file_dlg_return[0]
            lib = librarySingleton.loadLibrary(file_path)
            if lib is not None:
                self.addLibray(lib)

    def addFuncItem(
        self,
        lib_item: QtGui.QStandardItem,
        function_item_name: str,
        function_settings: FunctionSettings,
    ) -> None:
        """
        Using the function node create the function item
        """
        function_item = QtGui.QStandardItem(function_item_name)
        function_item.setData(function_settings.code, CODE_ROLE)
        function_item.setData(function_settings, SETTINGS_ROLE)
        lib_item.appendRow(function_item)

    @QtCore.Slot()
    def libItemSelected(self, index: QtCore.QModelIndex) -> None:
        """
        If the index is a leaf then function into the text edit
        """
        if index is not None and index.isValid():
            # check if this index is a leaf
            func_description = "Select a function"
            if not index.model().hasChildren(index):
                self._selectedIndex = index
                func_description = index.data(CODE_ROLE)
            self._ui.funcDescription.document().setPlainText(func_description)

    @QtCore.Slot()
    def validateFunction(self) -> None:
        """
        Make sure a valid selected index has been selected
        """
        if self._selectedIndex is not None and self._selectedIndex.isValid():
            if self._selectedIndex.parent().isValid():
                if not self._selectedIndex.model().hasChildren(self._selectedIndex):
                    self.funcSelected.emit(self._selectedIndex.data(SETTINGS_ROLE))
                    return
        self._ui.funcDescription.document().setPlainText("Not a valid function!!!")

    def addLibray(self, library: Library):
        """Find the correct group and add the library to that group"""
        if library is not None:
            # first determine if the library has a group
            group_item = self._ungrouped_item
            if library.group != "":
                group_list = self._lib_model.findItems(library.group)
                if len(group_list) > 0:
                    group_item = group_list[0]
                else:
                    # new group so add it to the model
                    group_item = QtGui.QStandardItem(library.group)
                    self._lib_model.appendRow(group_item)

            # we have the group now get the functions out of the library
            lib_item = QtGui.QStandardItem(library.name)
            for key, func in library.functions.items():
                self.addFuncItem(lib_item, key, func)

            # finally add the functions to the group
            group_item.appendRow(lib_item)

    def updateData(self) -> None:
        """When the window is called to be shown, (func selector will call this)
        clear the lib model and replace it with what is in the library singleton,
        this is in case somewhere a library has been loaded since last time this func selector was shown
        """
        self._lib_model.clear()
        self._lib_model.appendRow(self._ungrouped_item)
        libraries = librarySingleton.getLibraries()
        for lib in libraries:
            self.addLibray(lib)
        self._ui.funcDescription.clear()
        self._selectedIndex = None
