from .createBasePage import CreateBasePage

from ..qtUiFiles import ui_createDataSourceConfirmPage
from ..uiConstants import PageKeys
from ..util import qtResourceManager, qtUtil

from ...core.dataStructs import (
    ItemSettings,
    InputSettings,
    Parameter,
    FunctionSettings,
    ActionSettings,
)
from ...core.commonGlobals import ActionTypeEnum, DataSourcesTypeEnum


import typing
from functools import singledispatch
import dataclasses

from PySide6 import QtWidgets, QtCore

LEFT_MARGIN = 10


def createLayout(parent: QtWidgets.QWidget) -> QtWidgets.QVBoxLayout:
    layout = QtWidgets.QVBoxLayout(parent)
    layout.setContentsMargins(LEFT_MARGIN, 0, 0, 0)
    return layout


def getCheckOrX(bool_val):
    return qtResourceManager.getResourceByName(
        "icons",
        ("checkmark_green.png" if bool_val else "x_red.png"),
    )


@singledispatch
def createValueLabel(val, name, parent: QtWidgets.QWidget) -> QtWidgets.QWidget:
    return None


@createValueLabel.register(int)
@createValueLabel.register(str)
def _(val, name, parent: QtWidgets.QWidget) -> QtWidgets.QWidget:
    return QtWidgets.QLabel(f"{name}: {val}", parent)


@createValueLabel.register
def _(val: bool, name: str, parent: QtWidgets.QWidget) -> QtWidgets.QWidget:
    w = QtWidgets.QWidget(parent)
    layout = QtWidgets.QHBoxLayout(w)
    layout.addWidget(QtWidgets.QLabel(f"{name}:", parent))
    icon = QtWidgets.QLabel(parent)
    icon.setPixmap(getCheckOrX(val).scaled(20, 20))
    layout.addWidget(icon)
    w.setLayout(layout)
    return w


@createValueLabel.register
def _(val: list, name: str, parent: QtWidgets.QWidget) -> QtWidgets.QWidget:
    w = QtWidgets.QWidget(parent)
    layout = QtWidgets.QVBoxLayout(w)
    layout.addWidget(QtWidgets.QLabel(f"{name}:", parent))
    sub_w = QtWidgets.QWidget(w)
    sub_layout = createLayout(sub_w)
    for v in val:
        sub_sub_w = createWidget(v, sub_w)
        if sub_sub_w is None:
            sub_sub_w = QtWidgets.QLabel(str(v), sub_w)
        sub_layout.addWidget(sub_sub_w)
    sub_w.setLayout(sub_layout)
    layout.addWidget(sub_w)
    w.setLayout(layout)
    return w


@singledispatch
def createWidget(data_struct, parent: QtWidgets.QWidget) -> QtWidgets.QWidget:
    return None


@createWidget.register
def _(data_struct: InputSettings, parent: QtWidgets.QWidget) -> QtWidgets.QWidget:
    w = QtWidgets.QWidget(parent)
    layout = createLayout(w)
    layout.addWidget(createValueLabel(data_struct.name, "Name", w))
    layout.addWidget(createValueLabel(data_struct.requires_new, "Requires New", w))
    layout.addWidget(createValueLabel(data_struct.period, "Period", w))
    w.setLayout(layout)
    return w


@createWidget.register
def _(data_struct: Parameter, parent: QtWidgets.QWidget) -> QtWidgets.QWidget:
    w = QtWidgets.QWidget(parent)
    layout = createLayout(w)
    layout.addWidget(createValueLabel(data_struct.name, "Name", w))
    layout.addWidget(createValueLabel(data_struct.type_, "Type", w))
    layout.addWidget(createValueLabel(data_struct.value, "Value", w))
    w.setLayout(layout)
    return w


@createWidget.register
def _(data_struct: FunctionSettings, parent: QtWidgets.QWidget) -> QtWidgets.QWidget:
    w = QtWidgets.QWidget(parent)
    layout = createLayout(w)
    layout.addWidget(createValueLabel(data_struct.name, "Name", w))
    if data_struct.import_statements:
        layout.addWidget(createValueLabel(data_struct.import_statements, "Imports", w))
    layout.addWidget(QtWidgets.QLabel("Code: ", w))
    layout.addWidget(qtUtil.ExpandingLabelWidget(data_struct.code, w))
    w.setLayout(layout)
    return w


@createWidget.register
def _(data_struct: ItemSettings, parent: QtWidgets.QWidget) -> QtWidgets.QWidget:
    w = QtWidgets.QWidget(parent)
    layout = createLayout(w)
    layout.addWidget(createValueLabel(data_struct.name, "Name", w))
    layout.addWidget(createValueLabel(data_struct.type_, "Type", w))
    if data_struct.sub_type:
        layout.addWidget(createValueLabel(data_struct.sub_type, "Sub Type", w))
    if (
        data_struct.type_ == ActionTypeEnum.EVENT.value
        or data_struct.type_ == DataSourcesTypeEnum.FUNC.display
    ):
        layout.addWidget(createValueLabel(data_struct.flatten, "Flatten", w))
    if (
        data_struct.type_ == DataSourcesTypeEnum.FUNC.display
        or data_struct.type_ == ActionTypeEnum.SCRIPT.value
    ):
        layout.addWidget(createValueLabel(data_struct.single_shot, "Single Shot", w))
        layout.addWidget(createValueLabel(data_struct.period, "Period", w))
    if (
        data_struct.type_ == ActionTypeEnum.EVENT.value
        or data_struct.type_ == ActionTypeEnum.TRIGGER.value
        or data_struct.type_ == DataSourcesTypeEnum.FUNC.display
    ):
        for param in data_struct.parameters.values():
            layout.addWidget(createWidget(param))
        for setup_functions in data_struct.setup_functions.values():
            layout.addWidget(createWidget(setup_functions))
    w.setLayout(layout)
    return w


@createWidget.register
def _(data_struct: ActionSettings, parent: QtWidgets.QWidget) -> QtWidgets.QWidget:
    field_names = set(f.name for f in dataclasses.fields(ItemSettings))
    w = createWidget(
        ItemSettings(
            **{k: v for k, v in data_struct.__dict__.items() if k in field_names}
        ),
        parent,
    )
    layout = w.layout()
    if data_struct.type_ == ActionTypeEnum.EVENT.value or ActionTypeEnum.TRIGGER.value:
        layout.addWidget(createWidget(data_struct.calc_function))
    if data_struct.type_ == ActionTypeEnum.TRIGGER.value:
        layout.addWidget(createWidget(data_struct.output_function))
    layout.addWidget(createValueLabel(list(data_struct.input_.values()), "Input", w))
    return w


class CreateConfirmPage(CreateBasePage):
    PAGE_KEY = PageKeys.CONFRIM
    TUTORIAL_RESOURCE_PREFIX = "CreateConfirm"

    def __init__(
        self,
        current_config: ItemSettings,
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(current_config, self.TUTORIAL_RESOURCE_PREFIX, parent=parent)

        self._ui = ui_createDataSourceConfirmPage.Ui_CreateDataSourceConfirmPage()
        self._ui.setupUi(self)

    def getConfigForView(self):
        pass

    def loadPage(self) -> None:
        """
        We want the confirm page to only show the section we've been working on.
        """
        super().loadPage()
        w = QtWidgets.QWidget(self._ui.scrollArea)
        layout = createLayout(w)
        layout.addWidget(createWidget(self.getConfig(), w))
        w.setLayout(layout)
        self._ui.scrollArea.setWidget(w)

    def save(self) -> None:
        # saving of the temp config to the full config is done via the confirm button
        pass

    def getTutorialClasses(self) -> typing.List:
        return [self]
