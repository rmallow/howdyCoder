from .createBasePage import CreateBasePage
from .actionListCreator import ActionListCreator
from .actionUIConstant import ActionEnum

import typing

from PySide2 import QtWidgets


class CreateActionListPage(CreateBasePage):
    def __init__(self, parent: typing.Optional[QtWidgets.QWidget] = None):
        super().__init__(parent=parent)
        self._mainLayout = QtWidgets.QVBoxLayout(self)

        self._ui = ActionListCreator(self)
        self._mainLayout.addWidget(self._ui)
        self.setLayout(self._mainLayout)

    def validate(self) -> bool:
        """Check if the name is entered and valid"""
        return self._ui.validate()

    def getConfig(self) -> typing.Dict[str, typing.Any]:
        """Return the configuration for that page"""
        return self._ui.getConfig()

    def update(self) -> None:
        self._ui.update()
        return super().update()

    def loadPage(self, settings) -> None:
        """Clear out current datasources and take in the data sources from the previos page"""
        self._ui.feedModel.clearDataSources()
        if settings is not None:
            for key, setting in settings.items():
                for output in setting.output:
                    colDict = {}
                    colDict[ActionEnum.NAME] = output
                    colDict[ActionEnum.PERIOD] = setting.period
                    colDict[ActionEnum.TYPE] = setting.source_type.display
                    colDict[ActionEnum.INPUT] = key
                    self._ui.feedModel.appendDataSource(colDict)
