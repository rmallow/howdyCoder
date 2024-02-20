from ..core.dataStructs import DataSourceSettings, FunctionSettings
from .dataBase import dataBase

from ..commonUtil.userFuncCaller import UserFuncCaller
from ..core.commonGlobals import PASSBACK_DICT, EditorType

import typing


class dataFunc(dataBase):
    def __init__(self, data_source_settings: DataSourceSettings, *args, **kwargs):
        super().__init__(data_source_settings, *args, **kwargs)

        self.getFunc: UserFuncCaller = data_source_settings.get_function.user_function
        self.setup_funcs: typing.Dict[str, FunctionSettings] = {
            v.name: v.value
            for v in data_source_settings.parameters.values()
            if v.type_ == EditorType.FUNC.display
        }
        self._internal_setup_functions = (
            data_source_settings.get_function.internal_setup_functions
        )

        # add the pass back dict so that the func can add data here and continue to use it if so desired
        passback_dict = {}
        self.parameters[PASSBACK_DICT] = passback_dict

    def getData(self) -> dict:
        """
        Called by fees to get Data

        @returns: dictList of values
        """
        self.getDataLogging()
        vals, _1, _2 = self.getFunc(**self.parameters)
        return self.dataModifications(vals)

    def loadData(self) -> None:
        """
        Calls the setup func and loads the return of the setup func into the parameters
        """
        for key, function_settings in self.setup_funcs.items():
            self.parameters |= {
                key: function_settings.user_function(**self.parameters)[0]
            }

        for func_name, parm_name in self._internal_setup_functions.items():
            self.parameters |= {
                parm_name: self.getFunc.callFunc(func_name, **self.parameters)[0]
            }
