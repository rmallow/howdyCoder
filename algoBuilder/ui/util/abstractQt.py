from abc import ABC
from PySide6 import QtWidgets, QtCore
from functools import cache


@cache
def getAbstactQtResolver(base_qt_class: QtCore.QObject, base_abstract_class=ABC):
    class _ShibokenObjectTypeFence(type(base_qt_class)):
        pass

    class _ResolverMeta(
        _ShibokenObjectTypeFence, type(base_abstract_class), type(base_qt_class)
    ):
        pass

    return _ResolverMeta


def handleAbstractMethods(cls):
    if cls.__abstractmethods__:
        s = "s" if len(cls.__abstractmethods__) > 1 else ""
        raise TypeError(
            f"Can't instantiate abstract class {cls.__name__} "
            f'with abstract method{s} {", ".join(cls.__abstractmethods__)}'
        )


# Example Widget, add the __new__ function check the abstract methods
class AbstractWidget(
    QtWidgets.QWidget, metaclass=getAbstactQtResolver(QtWidgets.QWidget)
):
    def __new__(self, *args, **kwargs):
        handleAbstractMethods(self)
        return super().__new__(self, *args, **kwargs)
