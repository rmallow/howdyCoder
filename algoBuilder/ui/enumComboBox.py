from ..commonUtil import helpers
from ..core.commonGlobals import ENUM_DISPLAY, ENUM_VALUE, ENUM_HIDE

import typing

from aenum import Enum
from PySide2 import QtWidgets


class EnumComboBox(QtWidgets.QComboBox):
    def __init__(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)
        self._enum: Enum = None

    def setEnum(self, enum: Enum):
        self._enum = enum
        for e in enum:
            if hasattr(e, ENUM_DISPLAY) and hasattr(e, ENUM_VALUE):
                # if there is a hide key then don't add to the combo
                if hasattr(e, ENUM_HIDE) and getattr(e, ENUM_HIDE):
                    continue
                self.addItem(getattr(e, ENUM_DISPLAY), getattr(e, ENUM_VALUE))

    def setItemByEnumValue(self, enum_value: Enum):
        if self._enum is not None and enum_value in self._enum:
            self.setCurrentIndex(self.findData(getattr(enum_value, ENUM_VALUE)))

    def setItemByEnumAttribute(
        self, attribute_name: str, value: typing.Union[str, int]
    ):
        enum_value = helpers.findEnumByAttribute(self._enum, attribute_name, value)
        self.setItemByEnumValue(enum_value)
