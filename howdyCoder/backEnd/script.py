from .program import Program
from ..core.commonGlobals import ProgramTypes


class Script(Program):
    def __init__(self):
        super().__init__(self)
        self.type_ = ProgramTypes.ALGO
