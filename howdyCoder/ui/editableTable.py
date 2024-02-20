from .funcSelector import FuncSelector
from .pathSelector import PathSelector
from .selectorWidget import SelectorWidget

from .util.abstractQt import getAbstactQtResolver, handleAbstractMethods
from .util import qtUtil
from .util.helperData import (
    HelperData,
    PathWithHelperData,
    FunctionSettingsWithHelperData,
)

from ..commonUtil import helpers

from ..core import parameterSingleton
from ..core.commonGlobals import (
    ENUM_DISPLAY,
    ENUM_TYPE,
    ENUM_EDITOR_VALUES,
    ENUM_ENABLED,
    EditorType,
    PathType,
)
import typing
from abc import abstractmethod

from aenum import Enum

from PySide6 import QtCore, QtWidgets

SELECTOR_TYPES = set(
    [EditorType.FUNC.display, EditorType.FOLDER.display, EditorType.FILE.display]
)

PERSISTENT_EDITORS = SELECTOR_TYPES | set(
    [EditorType.GLOBAL_PARAMETER.display, EditorType.KEY.display]
)


def getEditor(
    editor_type: EditorType,
    parent: QtWidgets.QWidget,
    combo_editor_values: typing.List[str] = None,
    combo_hide_values: typing.Set[str] = None,
    func_selector: FuncSelector = None,
    folder_selector: PathSelector = None,
    file_selector: PathSelector = None,
    index: QtCore.QModelIndex = None,
):
    editor = None
    if editor_type == EditorType.STRING or editor_type == EditorType.ANY:
        editor = QtWidgets.QLineEdit(parent)
    elif (
        editor_type == EditorType.COMBO
        or editor_type == EditorType.KEY
        or editor_type == EditorType.GLOBAL_PARAMETER
    ):
        editor = QtWidgets.QComboBox(parent)
        editor.setAutoFillBackground(True)
        combo_values = combo_editor_values
        for comboValue in combo_values:
            if comboValue not in combo_hide_values:
                editor.addItem(comboValue)
        if editor_type == EditorType.KEY or editor_type == EditorType.GLOBAL_PARAMETER:
            if editor_type == EditorType.KEY:
                combo_values = parameterSingleton.getKeys()
            else:
                combo_values = parameterSingleton.getNonKeys()
            for combo_value in combo_values:
                if combo_value.name not in combo_hide_values:
                    editor.addItem(combo_value.name, userData=combo_value)

    elif editor_type == EditorType.INTEGER:
        editor = QtWidgets.QSpinBox(parent)
        editor.setRange(-999999, 999999)
    elif editor_type == EditorType.DECIMAL:
        editor = QtWidgets.QDoubleSpinBox(parent)
        editor.setDecimals(8)
        editor.setRange(-999999, 999999)
    elif editor_type.display in SELECTOR_TYPES and (
        index is None or index in index.model().selector_indexes
    ):
        if editor_type == EditorType.FUNC:
            editor = SelectorWidget(
                index, func_selector, parent, "Parameter Setup Func"
            )
        elif editor_type == EditorType.FOLDER:
            editor = SelectorWidget(index, folder_selector, parent)
        else:
            editor = SelectorWidget(index, file_selector, parent)
        editor.changeExpandingLabelMinWidth(1)
    return editor


class EditableTableDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent: typing.Optional[QtCore.QObject] = None) -> None:
        self._completer_strings: typing.List[str] = []
        super().__init__(parent)

    def setCompleterStrings(self, string_list):
        self._completer_strings = string_list

    def createEditor(
        self,
        parent: QtWidgets.QWidget,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex,
    ) -> QtWidgets.QWidget:
        """
        Create an editor by getting the editor type from the model
        """
        enumKey = index.model().getEnumKey(index)
        editor_type = index.model().getEditorType(index)
        combo_hide_values = set()
        # this is only set in some parameter tables
        if editor_type == EditorType.STRING or editor_type == EditorType.ANY:
            editor = super().createEditor(parent, option, index)
            qtUtil.setCompleter(editor, self._completer_strings)
        else:
            try:
                combo_hide_values = index.model().combo_hide_values
            except AttributeError as _:
                pass
            editor = getEditor(
                editor_type,
                parent,
                combo_editor_values=(
                    getattr(enumKey, ENUM_EDITOR_VALUES, [])
                    if enumKey is not None
                    else []
                ),
                combo_hide_values=combo_hide_values,
                func_selector=index.model().func_selector,
                folder_selector=index.model().folder_selector,
                file_selector=index.model().file_selector,
                index=index,
            )
            if editor_type.display in SELECTOR_TYPES:
                index.model().selector_widgets[index] = editor
        return editor

    def setModelData(
        self,
        editor: QtWidgets.QWidget,
        model: QtCore.QAbstractItemModel,
        index: QtCore.QModelIndex,
    ) -> None:
        """
        Set the model data by getting the editor type from the table
        """
        editorType = index.model().getEditorType(index)
        if (
            editorType == EditorType.STRING
            or editorType == EditorType.ANY
            or editorType == EditorType.INTEGER
            or editorType == EditorType.DECIMAL
        ):
            return super().setModelData(editor, model, index)
        elif editorType == EditorType.COMBO:
            currentText = editor.currentText()
            model.setData(index, currentText)


class EditableTableModel(
    QtCore.QAbstractTableModel,
    metaclass=getAbstactQtResolver(QtCore.QAbstractTableModel),
):
    """
    Base class for Editable Tables, standardizes modifying values in tables

    Main input is the enum that defines how the table operates and looks
    Attribtures for enum is as follows:
        value - ordering of columns/rows in table
        display - string display value for header
        type - used for delegates, the type of value like str, int, func, see EditorType enum
        editorValues - used by delegate for to populate the editor values, list
        enabled - enabled or disabled
    """

    openPersistentEditor = QtCore.Signal(QtCore.QModelIndex)
    closePersistentEditor = QtCore.Signal(QtCore.QModelIndex)

    def __init__(
        self,
        enum: Enum,
        parent: typing.Optional[QtCore.QObject] = None,
        combo_hide_values=None,
    ) -> None:
        self.enum = enum
        # these are special fields that interact with each other
        # so check ahead of time if they are there
        self.typeEnum = None
        self.valueEnum = None
        if hasattr(self.enum, "TYPE"):
            self.typeEnum = self.enum.TYPE
        if hasattr(self.enum, "VALUE"):
            self.valueEnum = self.enum.VALUE
        self.values = []

        # used for selecting functions
        self.selector_indexes = set()
        self.func_selector = FuncSelector()
        self.folder_selector = PathSelector(PathType.FOLDER)
        self.file_selector = PathSelector(PathType.FILE)
        self.selector_widgets = {}
        self.func_selector.itemSelected.connect(self.itemSelected)
        self.folder_selector.itemSelected.connect(self.itemSelected)
        self.file_selector.itemSelected.connect(self.itemSelected)

        self.combo_hide_values = set(combo_hide_values) if combo_hide_values else set()

        super().__init__(parent=parent)

    def __new__(self, *args, **kwargs):
        handleAbstractMethods(self)
        return super().__new__(self, *args, **kwargs)

    @abstractmethod
    def rowCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        return super().rowCount(parent)

    @abstractmethod
    def columnCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        return super().columnCount(parent)

    @abstractmethod
    def getEnumKey(self, index: QtCore.QModelIndex) -> typing.Any:
        return None

    @abstractmethod
    def getValueKey(self, index: QtCore.QModelIndex) -> int:
        return None

    @abstractmethod
    def getIndex(self, enumKey: typing.Any, valueKey: int) -> QtCore.QModelIndex:
        return None

    @QtCore.Slot()
    def itemSelected(self, settings: HelperData) -> None:
        """When a function is selected update the value with the func and also populate the description"""
        if settings.index is not None and settings.index in self.selector_widgets:
            selectorWidget = self.selector_widgets[settings.index]
            valueKey = self.getValueKey(settings.index)
            if valueKey is not None:
                label = ""
                if isinstance(settings, FunctionSettingsWithHelperData):
                    self.values[valueKey][self.valueEnum] = settings
                    label = settings.function_settings.name
                    selectorWidget.data = settings.function_settings
                elif isinstance(settings, PathWithHelperData):
                    self.values[valueKey][self.valueEnum] = settings.path
                    label = settings.path

                selectorWidget._ui.selectionLabel.setText(label)
                self.dataChanged.emit(
                    settings.index, settings.index, [QtCore.Qt.DisplayRole]
                )

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlags:
        flags = super().flags(index)
        enumKey = self.getEnumKey(index)
        if enumKey is not None and hasattr(enumKey, ENUM_ENABLED) and enumKey.enabled:
            flags = QtCore.Qt.ItemIsEditable | flags
        return flags

    @QtCore.Slot()
    def appendValue(self, value: typing.Dict[str, str] = None):
        """Add a new entry to table, default to empty dict"""
        if value is None:
            value = {}
        self.beginInsertFunc(QtCore.QModelIndex(), len(self.values), len(self.values))
        self.values.append(value)
        self.endInsertFunc()

    @QtCore.Slot()
    def removeValue(self, index):
        if index.isValid():
            valueKey = self.getValueKey(index)
            if valueKey < len(self.values):
                self.beginRemoveFunc(QtCore.QModelIndex(), valueKey, valueKey)
                del self.values[valueKey]
                self.endRemoveFunc()

    def data(
        self, index: QtCore.QModelIndex, role: int = QtCore.Qt.DisplayRole
    ) -> typing.Any:
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return self.getValueIndex(index)
        return None

    def setData(
        self,
        index: QtCore.QModelIndex,
        value: typing.Any,
        role: int = QtCore.Qt.DisplayRole,
    ) -> bool:
        """
        set the data at the given index to value

        If this is  a type item and the value item is not none then clear out description
        and either open or close based on if the type is func or not
        """
        if role == QtCore.Qt.EditRole or role == QtCore.Qt.DisplayRole:
            enumKey = self.getEnumKey(index)
            valueKey = self.getValueKey(index)
            old_val = None
            if valueKey < len(self.values) and enumKey in self.values[valueKey]:
                old_val = self.values[valueKey][enumKey]
            ret_val = self.safeSetValue(valueKey, enumKey, value)
            if (
                enumKey is not None
                and valueKey is not None
                and self.typeEnum is not None
                and self.valueEnum is not None
            ):
                if enumKey == self.typeEnum:
                    funcIndex = self.getIndex(self.valueEnum, valueKey)
                    # if the value was func, then we need to open the func editor
                    if value in SELECTOR_TYPES:
                        if value != old_val and (old_val in SELECTOR_TYPES):
                            self.closePersistentEditor.emit(funcIndex)
                        if value in SELECTOR_TYPES:
                            self.selector_indexes.add(funcIndex)
                        self.openPersistentEditor.emit(funcIndex)
                    else:
                        if funcIndex in self.selector_indexes:
                            self.selector_indexes.remove(funcIndex)
                        self.closePersistentEditor.emit(funcIndex)
                    if value != old_val:
                        self.safeSetValue(valueKey, self.valueEnum, None)
            self.dataChanged.emit(index, index, [QtCore.Qt.DisplayRole])
            return ret_val
        return super().setData(index, value, role)

    def safeSetValue(
        self, valueKey: int, enumKey: typing.Any, value: typing.Any
    ) -> bool:
        if valueKey is not None and valueKey < len(self.values) and enumKey is not None:
            self.values[valueKey][enumKey] = value
            return True
        return False

    def getValueIndex(self, index: QtCore.QModelIndex):
        """Get the value from the QModelIndex"""
        enumKey = self.getEnumKey(index)
        valueKey = self.getValueKey(index)
        return self.getValue(valueKey, enumKey)

    def getValue(self, valueKey: int, enumKey: typing.Any):
        """Based on a given value key and enum key get the value"""
        if (
            valueKey is not None
            and valueKey < len(self.values)
            and enumKey is not None
            and enumKey in self.values[valueKey]
        ):
            return self.values[valueKey][enumKey]
        else:
            return None

    def getEditorType(self, index: QtCore.QModelIndex) -> EditorType:
        """
        Get the editor type for a given index, first get the enumKey, if it is also the value enumKey
        Then look if the type item is also set, if so get the editor type from there
        Otherwise find the editor type off the enum
        """
        enumKey = index.model().getEnumKey(index)
        editorType = None
        if (
            enumKey is not None
            and index.model().valueEnum is not None
            and index.model().valueEnum == enumKey
        ):
            if index.model().typeEnum is not None:
                valueKey = index.model().getValueKey(index)
                if valueKey is not None:
                    editorTypeStr = index.model().getValue(
                        valueKey, index.model().typeEnum
                    )
                    editorType = helpers.findEnumByAttribute(
                        EditorType, ENUM_DISPLAY, editorTypeStr
                    )

        if editorType is None and hasattr(enumKey, ENUM_TYPE):
            editorType = enumKey.type
        return editorType

    @QtCore.Slot()
    def clear(self):
        self.beginResetModel()
        self.values.clear()
        self.endResetModel()

    def setValues(self, values):
        self.beginResetModel()
        self.values = values
        self.endResetModel()


class EditableTableModelAddRows(EditableTableModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # determine functions based on the orientation of the table
        self.beginInsertFunc = self.beginInsertRows
        self.endInsertFunc = self.endInsertRows
        self.beginRemoveFunc = self.beginRemoveRows
        self.endRemoveFunc = self.endRemoveRows

    def rowCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        return len(self.values)

    def columnCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        return len(self.enum)

    def getEnumKey(self, index: QtCore.QModelIndex) -> typing.Any:
        if index.isValid():
            return self.enum(index.column())
        else:
            return None

    def getValueKey(self, index: QtCore.QModelIndex) -> int:
        if index.isValid():
            return index.row()
        else:
            return None

    def getIndex(self, enumKey: typing.Any, valueKey: int) -> QtCore.QModelIndex:
        return self.index(valueKey, enumKey.value)

    def headerData(
        self,
        section: int,
        orientation: QtCore.Qt.Orientation,
        role: int = QtCore.Qt.DisplayRole,
    ) -> typing.Any:
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Vertical:
                return section
            else:
                return self.enum(section).display

        return super().headerData(section, orientation, role=role)


class EditableTableModelAddColumn(EditableTableModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.beginInsertFunc = self.beginInsertColumns
        self.endInsertFunc = self.endInsertColumns
        self.beginRemoveFunc = self.beginRemoveRows
        self.endRemoveFunc = self.endRemoveRows

    def rowCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        return len(self.enum)

    def columnCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        return len(self.values)

    def getEnumKey(self, index: QtCore.QModelIndex) -> typing.Any:
        if index.isValid():
            return self.enum(index.row())
        else:
            return None

    def getValueKey(self, index: QtCore.QModelIndex) -> int:
        if index.isValid():
            return index.column()
        else:
            return None

    def getIndex(self, enumKey: typing.Any, valueKey: int) -> QtCore.QModelIndex:
        return self.index(enumKey, valueKey)

    def headerData(
        self,
        section: int,
        orientation: QtCore.Qt.Orientation,
        role: int = QtCore.Qt.DisplayRole,
    ) -> typing.Any:
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Vertical:
                return self.enum(section).display
            else:
                return section

        return super().headerData(section, orientation, role=role)


class EditableTableView(QtWidgets.QTableView):
    def __init__(
        self,
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self.setItemDelegate(EditableTableDelegate(parent))
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def setModel(self, model: QtCore.QAbstractItemModel) -> None:
        """
        If the model we're looking at is EditableTableModel than connect some signal and slots
        (It probably is an EditableTableModel or subclass)
        """
        if isinstance(model, EditableTableModel):
            model.openPersistentEditor.connect(
                lambda index: self.callPersistentEditorAndResize(
                    self.openPersistentEditor, index
                )
            )
            model.closePersistentEditor.connect(
                lambda index: self.callPersistentEditorAndResize(
                    self.closePersistentEditor, index
                )
            )
        return super().setModel(model)

    def callPersistentEditorAndResize(
        self, persitentFunc, index: QtCore.QModelIndex
    ) -> None:
        """
        called when model asks to open persitent editor.
        Resize the contents of that index by row/col to fit editor
        """
        persitentFunc(index)
        self.resizeRowToContents(index.row())
        self.resizeColumnToContents(index.column())

    def getSelected(self) -> QtCore.QModelIndex:
        indexes = self.selectionModel().selectedIndexes()
        selected = QtCore.QModelIndex()
        if len(indexes) > 0:
            selected = indexes[0]
        return selected

    def drawingFix(self):
        """See create page notes on drawing fix for why"""
        for child in self.findChildren(QtWidgets.QAbstractScrollArea):
            child.viewport().repaint()


class PartialReadOnlyList(QtCore.QStringListModel):
    def __init__(
        self,
        parent: typing.Optional[QtCore.QObject] = None,
    ) -> None:
        super().__init__(parent)
        self._readOnlyRows = 0

    def setReadOnlyNum(self, num_rows: int) -> None:
        self._readOnlyRows = num_rows

    def getReadOnlyNum(self) -> int:
        return self._readOnlyRows

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlags:
        flags = super().flags(index)
        if index.row() < self._readOnlyRows:
            flags &= ~QtCore.Qt.ItemFlag.ItemIsEditable
        return flags
