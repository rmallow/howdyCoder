from ..core.dataStructs import USER_FUNC
from .program import Program

from ..commonUtil import userFuncCaller
from ..commonUtil import configLoader

from ..core.dataStructs import SETUP_FUNCS

from abc import ABC, abstractmethod
import copy
import typing


class ProgramManager(ABC):
    def __init__(self):
        self.programs: typing.Dict[str, Program] = {}

    @abstractmethod
    def load(self, config: typing.Dict[str, typing.Any]) -> Program:
        pass

    def getProgram(self, code: str) -> Program:
        return self.programs[code]

    def addUserFuncs(self, config: typing.Dict[str, typing.Any]):
        user_funcs = []

        def assignUserFuncCaller(c, k, v):
            nonlocal user_funcs
            if v is not None:
                user_funcs.append(userFuncCaller.UserFuncCaller(**v))
                c[k][USER_FUNC] = user_funcs[-1]

        def handleSetupFuncs(c, k, v):
            for f_name, f_value in v.items():
                assignUserFuncCaller(v, f_name, f_value)

        configLoader.dfsConfigDict(
            config,
            lambda k: k.lower().endswith("function"),
            assignUserFuncCaller,
        )

        configLoader.dfsConfigDict(config, lambda k: k == SETUP_FUNCS, handleSetupFuncs)
        return user_funcs
