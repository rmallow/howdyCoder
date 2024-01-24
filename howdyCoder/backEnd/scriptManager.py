from .programManager import ProgramManager
from .script import Script
from .action import Action
from .actionPool import ActionPool
from .actionFactory import actionFactory

from ..core.dataStructs import ProgramSettings, ScriptSettings

import copy
import typing

from dataclass_wizard import fromdict, asdict


class ScriptManager(ProgramManager):
    def __init__(self):
        super().__init__()

    def load(self, program_settings: ProgramSettings) -> Script:
        func_replaced_config = copy.deepcopy(asdict(program_settings))
        user_funcs = self.addUserFuncs(func_replaced_config)
        script_settings_with_user_funcs: ScriptSettings = fromdict(
            ProgramSettings, func_replaced_config
        ).settings
        script = Script(
            self.loadActionPool(script_settings_with_user_funcs),
            program_settings,
            user_funcs,
        )
        self.programs[script_settings_with_user_funcs.name] = script
        return script

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
