from .action import Action

from ..core.commonGlobals import ActionTypeEnum, ENUM_DISPLAY, ENUM_VALUE
from ..core.dataStructs import STDOutErrData
from ..commonUtil.helpers import findEnumByAttribute

import typing


class ActionPool:
    """
    Container and caller for all actions of a program
    """

    def __init__(
        self,
        actions: typing.List[Action],
    ):
        self._all_actions: typing.List[typing.List[Action]] = [
            [] for _ in range(len(ActionTypeEnum))
        ]

        for action in actions:
            self._all_actions[
                getattr(
                    findEnumByAttribute(
                        ActionTypeEnum, ENUM_DISPLAY, action.actionType
                    ),
                    ENUM_VALUE,
                )
            ].append(action)

    def doActions(self) -> None:
        """
        Perform all of the actions in order of priority, and collect their stdout/err output
        """
        data_list = []
        for action_list in self._all_actions:
            for action in action_list:
                out, err = action.update()
                data_list.append(STDOutErrData(out, err, action.name))
        return data_list

    def started(self):
        for action_list in self._all_actions:
            for action in action_list:
                action.just_started = True
