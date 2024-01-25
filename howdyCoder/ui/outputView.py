from .tutorialOverlay import AbstractTutorialClass

from .util import abstractQt
from .util.qtUtil import StayOnTopInFocus

from PySide6 import QtWidgets


class outputView(
    AbstractTutorialClass,
    StayOnTopInFocus,
    QtWidgets.QWidget,
    metaclass=abstractQt.getAbstactQtResolver(QtWidgets.QWidget, AbstractTutorialClass),
):
    def __new__(self, *args, **kwargs):
        abstractQt.handleAbstractMethods(self)
        return super().__new__(self, *args, **kwargs)

    def __init__(self, outputViewModel, resource_prefix: str, parent=None):
        super().__init__(resource_prefix, parent)
        self.outputViewModel = outputViewModel

    def setup(self):
        pass
