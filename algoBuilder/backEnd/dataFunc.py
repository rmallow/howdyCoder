from .dataBase import dataBase

from ..commonUtil.userFuncCaller import userFuncCaller
from ..core.commonGlobals import PASSBACK_DICT

import typing


class dataFunc(dataBase):
    def __init__(self, *args, getFunc=None, setupFuncs={}, **kwargs):
        super().__init__(*args, **kwargs)

        self.getFunc: userFuncCaller = getFunc
        self.setupFuncs: typing.Dict[str, userFuncCaller] = setupFuncs

        # add the pass back dict so that the func can add data here and continue to use it if so desired
        passback_dict = {}
        self.parameters[PASSBACK_DICT] = passback_dict

        self.loadData()

    def getData(self) -> dict:
        """
        Called by fees to get Data

        @returns: dictList of values
        """
        self.getDataLogging()
        return self.dataModifications(self.getFunc(**self.parameters))

    def loadData(self) -> None:
        """
        Calls the setup func and loads the return of the setup func into the parameters
        """
        for key, userFunc in self.setupFuncs.items():
            self.parameters |= {key: userFunc(**self.parameters)}
