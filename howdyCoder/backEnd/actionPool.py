from .action import Action

from ..core.commonGlobals import ActionTypeEnum, ENUM_DISPLAY, ENUM_VALUE
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
        self._all_actions = [[] for _ in range(len(ActionTypeEnum))]

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
        Perform all of the actions in order of priority
        """
        for action_list in self._all_actions:
            for a in action_list:
                a.update()
