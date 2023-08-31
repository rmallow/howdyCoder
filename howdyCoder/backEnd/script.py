from .program import Program
from ..core.commonGlobals import ProgramTypes
from ..core.dataStructs import ProgramSettings
from ..commonUtil.userFuncCaller import UserFuncCaller

from .actionPool import ActionPool

import typing


class Script(Program):
    def __init__(
        self,
        action_pool: ActionPool,
        program_settings: ProgramSettings,
        user_funcs: typing.List[UserFuncCaller],
    ):
        super().__init__(program_settings, user_funcs)
        self.type_ = ProgramTypes.SCRIPT
        self.period = program_settings.settings.action.period
        self.action_pool = action_pool

    def update(self):
        self.action_pool.doActions()
