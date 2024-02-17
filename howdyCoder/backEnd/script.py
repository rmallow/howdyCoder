from .program import Program
from .actionPool import ActionPool
from .actionFactory import actionFactory

from ..core.commonGlobals import ProgramTypes
from ..core.dataStructs import ProgramSettings, ScriptSettings

from .actionPool import ActionPool

import copy
import typing

from dataclass_wizard import fromdict, asdict


class Script(Program):
    def __init__(
        self,
        is_local: bool,
        settings: ProgramSettings,
        *args,
        **kwargs,
    ):
        super().__init__(is_local, settings, *args, **kwargs)
        self.type_ = ProgramTypes.SCRIPT
        self.period = settings.settings.action.period

        # construct sub items
        self.loadSettings(settings)
        self.start()

    def loadSettings(self, settings: ProgramSettings):
        func_replaced_config = copy.deepcopy(asdict(settings))
        self._user_funcs = self.addUserFuncs(func_replaced_config)
        script_settings_with_user_funcs: ScriptSettings = fromdict(
            ProgramSettings, func_replaced_config
        ).settings

        self.action_pool = self.loadActionPool(script_settings_with_user_funcs)

    def loadActionPool(self, script_settings_with_user_funcs: ScriptSettings):
        factory = actionFactory()
        return ActionPool(
            {
                script_settings_with_user_funcs.name: factory.create(
                    script_settings_with_user_funcs.action,
                    script_settings_with_user_funcs.action.type_,
                )
            }
        )

    def update(self):
        self.doActions()
