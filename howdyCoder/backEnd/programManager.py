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
            if c is not None:
                user_funcs.append(userFuncCaller.UserFuncCaller(**c))
                c[k] = user_funcs[-1]

        configLoader.dfsConfigDict(
            config, lambda k: k == USER_FUNC, assignUserFuncCaller
        )
        return user_funcs
