from .action import Action

from ..core.commonGlobals import ActionTypeEnum, ENUM_DISPLAY, ENUM_VALUE
from ..core.dataStructs import STDOutErrData
from ..commonUtil.helpers import findEnumByAttribute

import typing
from enum import IntEnum, auto


class ActionGrouping(IntEnum):
    PRODUCER = 0
    CONSUMER = auto()


class ActionPool:
    """
    Container and caller for all actions of a program
    """

    def __init__(
        self,
        actions: typing.Dict[str, Action],
        topo_levels: typing.List[typing.List[str]] = None,
    ):
        self._all_actions: typing.List[typing.List[Action]] = [
            [] for _ in range(len(ActionGrouping))
        ]
        if topo_levels is None:
            for action in actions.values():
                self.addToActionList(action)
        else:
            # the first level is DS so we can ignore it
            if len(topo_levels) > 1:
                for level in topo_levels[1:]:
                    for name in level:
                        if name in actions:
                            self.addToActionList(actions[name])

    def addToActionList(self, action: Action):
        if action.actionType == ActionTypeEnum.TRIGGER.value:
            self._all_actions[ActionGrouping.CONSUMER.value].append(action)
        else:
            self._all_actions[ActionGrouping.PRODUCER.value].append(action)

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
                action.setup()
