from .programManager import ProgramManager
from ..core.commonGlobals import ProgramSettings

import copy
import typing

from dataclass_wizard import fromdict


class ScriptManager(ProgramManager):
    def __init__(self):
        super().__init__()
        pass

    def load(self, config: ProgramSettings):
        pass
