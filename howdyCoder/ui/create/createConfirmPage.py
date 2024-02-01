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
    DataSourceSettings,
)
from ...core.commonGlobals import ActionTypeEnum, DataSourcesTypeEnum


import typing
from numbers import Number
from functools import singledispatch
import dataclasses

from PySide6 import QtWidgets, QtCore, QtGui

LEFT_MARGIN = 30
MIN_FONT_SIZE = 15
FONT_DECREMENT = 4


def createLayout(parent: QtWidgets.QWidget) -> QtWidgets.QVBoxLayout:
    layout = QtWidgets.QVBoxLayout(parent)
    layout.setContentsMargins(LEFT_MARGIN, 0, 0, 0)
    return layout


def createLabel(text: str, parent: QtWidgets.QWidget) -> QtWidgets.QWidget:
    label = QtWidgets.QLabel(text, parent)
    label.setFont(parent.font())
    return label


def createBasicWidget(parent: QtWidgets.QWidget) -> QtWidgets.QWidget:
    w = QtWidgets.QWidget(parent)
    w.setFont(
        QtGui.QFont(
            parent.font().family(),
            max(parent.font().pointSize() - FONT_DECREMENT, MIN_FONT_SIZE),
        )
    )
    return w


def getCheckOrX(bool_val):
    return qtResourceManager.getResourceByName(
        "icons",
        ("checkmark_green.png" if bool_val else "x_red.png"),
    )


@singledispatch
def createValueLabel(val, name, parent: QtWidgets.QWidget) -> QtWidgets.QWidget:
    return None


@createValueLabel.register(Number)
@createValueLabel.register(str)
def _(val, name, parent: QtWidgets.QWidget) -> QtWidgets.QWidget:
    return createLabel(f"{name}: {val}", parent)


@createValueLabel.register
def _(val: bool, name: str, parent: QtWidgets.QWidget) -> QtWidgets.QWidget:
    w = createBasicWidget(parent)
    layout = QtWidgets.QHBoxLayout(w)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(createLabel(f"{name}: ", parent))
    icon = QtWidgets.QLabel(parent)
    icon.setPixmap(getCheckOrX(val).scaled(15, 15))
    layout.addWidget(icon)
    layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
    w.setLayout(layout)
    return w


@createValueLabel.register
def _(val: list, name: str, parent: QtWidgets.QWidget) -> QtWidgets.QWidget:
    w = createBasicWidget(parent)
    layout = QtWidgets.QVBoxLayout(w)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(createLabel(f"{name}:", parent))
    sub_w = createBasicWidget(w)
    sub_layout = createLayout(sub_w)
    for v in val:
        sub_sub_w = createWidget(v, sub_w)
        if sub_sub_w is None:
            sub_sub_w = createLabel(str(v), sub_w)
        sub_layout.addWidget(sub_sub_w)
    sub_w.setLayout(sub_layout)
    layout.addWidget(sub_w)
    w.setLayout(layout)
    return w


@createValueLabel.register
def _(val: dict, name: str, parent: QtWidgets.QWidget) -> QtWidgets.QWidget:
    w = createBasicWidget(parent)
    layout = QtWidgets.QVBoxLayout(w)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(createLabel(f"{name}:", w))
    sub_w = createBasicWidget(w)
    sub_layout = createLayout(sub_w)
    for k, v in val.items():
        sub_layout.addWidget(createLabel(f"{k}:", sub_w))
        sub_sub_w = createWidget(v, sub_w)
        if sub_sub_w is None:
            sub_sub_w = createLabel(str(v), sub_w)
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
    w = createBasicWidget(parent)
    layout = createLayout(w)
    layout.addWidget(createValueLabel(data_struct.name, "Rename", w))
    layout.addWidget(createValueLabel(data_struct.requires_new, "Requires New", w))
    layout.addWidget(createValueLabel(data_struct.period, "Period", w))
    w.setLayout(layout)
    return w


@createWidget.register
def _(data_struct: Parameter, parent: QtWidgets.QWidget) -> QtWidgets.QWidget:
    w = createBasicWidget(parent)
    layout = createLayout(w)
    layout.addWidget(createLabel(data_struct.name, w))
    inner_w = createBasicWidget(w)
    inner_l = createLayout(inner_w)
    inner_l.addWidget(createValueLabel(data_struct.type_, "Type", w))
    inner_l.addWidget(createValueLabel(data_struct.value, "Value", w))
    inner_w.setLayout(inner_l)
    layout.addWidget(inner_w)
    w.setLayout(layout)
    return w


@createWidget.register
def _(data_struct: FunctionSettings, parent: QtWidgets.QWidget) -> QtWidgets.QWidget:
    w = createBasicWidget(parent)
    layout = createLayout(w)
    layout.addWidget(createValueLabel(data_struct.name, "Name", w))
    if data_struct.import_statements:
        layout.addWidget(createValueLabel(data_struct.imports, "Imports", w))
    layout.addWidget(createLabel("Code: ", w))
    layout.addWidget(qtUtil.ExpandingLabelWidget(data_struct.code, w))
    w.setLayout(layout)
    return w


@createWidget.register
def _(data_struct: ItemSettings, parent: QtWidgets.QWidget) -> QtWidgets.QWidget:
    w = createBasicWidget(parent)
    layout = createLayout(w)
    if data_struct.sub_type:
        layout.addWidget(createValueLabel(data_struct.sub_type, "Sub Type", w))
    settings_w = createBasicWidget(w)
    settings_l = createLayout(settings_w)
    if (
        data_struct.type_ == ActionTypeEnum.EVENT.value
        or data_struct.type_ == DataSourcesTypeEnum.FUNC.display
    ):
        settings_l.addWidget(
            createValueLabel(data_struct.flatten, "Flatten", settings_w)
        )
    if (
        data_struct.type_ == DataSourcesTypeEnum.FUNC.display
        or data_struct.type_ == ActionTypeEnum.SCRIPT.value
    ):
        settings_l.addWidget(
            createValueLabel(data_struct.single_shot, "Single Shot", settings_w)
        )
        settings_l.addWidget(createValueLabel(data_struct.period, "Period", settings_w))
    if settings_l.count():
        layout.addWidget(createLabel("Settings:", w))
        settings_w.setLayout(settings_l)
        layout.addWidget(settings_w)
    if (
        data_struct.type_ == ActionTypeEnum.EVENT.value
        or data_struct.type_ == ActionTypeEnum.TRIGGER.value
        or data_struct.type_ == DataSourcesTypeEnum.FUNC.display
    ):
        if data_struct.parameters:
            layout.addWidget(
                createValueLabel(list(data_struct.parameters.values()), "Parameters", w)
            )
        if data_struct.setup_functions:
            layout.addWidget(
                createValueLabel(
                    list(data_struct.setup_functions.values()), "Setup Functions", w
                )
            )
    w.setLayout(layout)
    return w


@createWidget.register
def _(data_struct: DataSourceSettings, parent: QtWidgets.QWidget) -> QtWidgets.QWidget:
    field_names = set(f.name for f in dataclasses.fields(ItemSettings))
    w = createWidget(
        ItemSettings(
            **{k: v for k, v in data_struct.__dict__.items() if k in field_names}
        ),
        parent,
    )
    layout = w.layout()
    if data_struct.type_ == DataSourcesTypeEnum.FUNC.display:
        layout.insertWidget(
            0, createValueLabel([data_struct.get_function], "Function", w)
        )
    if data_struct.type_ == DataSourcesTypeEnum.INPUT.display:
        layout.insertWidget(
            0, createValueLabel(data_struct.input_type, "Input Type", w)
        )
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

    if data_struct.type_ == ActionTypeEnum.TRIGGER.value:
        layout.insertWidget(
            0, createValueLabel([data_struct.output_function], "Output Function", w)
        )
    if data_struct.type_ == ActionTypeEnum.EVENT.value or ActionTypeEnum.TRIGGER.value:
        layout.insertWidget(
            0, createValueLabel([data_struct.calc_function], "Calculating Function", w)
        )
    layout.addWidget(createValueLabel(data_struct.input_, "Input", w))
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
        config = self.getConfig()
        self._ui.title_label.setText(f"{config.name} : {config.type_}")
        w = QtWidgets.QWidget(self._ui.scrollArea)
        layout = createLayout(w)
        w.setFont(QtGui.QFont(w.font().family(), 26))
        layout.addWidget(createWidget(config, w))
        w.setLayout(layout)
        self._ui.scrollArea.setWidget(w)

    def save(self) -> None:
        # saving of the temp config to the full config is done via the confirm button
        pass

    def getTutorialClasses(self) -> typing.List:
        return [self]
