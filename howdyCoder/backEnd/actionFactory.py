from .action import action
from .event import event
from .trigger import trigger
from .aggregateData import aggregateData
from .aggregateDataParameter import aggregateDataParameter
from .aggregateParameter import aggregateParameter

from ..core.configConstants import ActionTypeEnum

_ACTION_FACTORY_TYPES = {
    ActionTypeEnum.EVENT.display: event,
    ActionTypeEnum.TRIGGER.display: trigger,
    "aggregatedata": aggregateData,
    "aggregatedataparameter": aggregateDataParameter,
    "aggregateparameter": aggregateParameter,
}


class actionFactory:
    """
    This class is intended to seperate the creation of actions into it's own module
    No action of type "action" will be made as that is a virtual class
    Note the creator type is not necessarily an actionType, as creatorType could be aggregate
    but action type could be event or trigger
    """

    def create(
        self, config: dict, creatorType: str, doSetupFunc: bool = True
    ) -> action:
        """
        Based on a creator type, creates an action using the given config

        Args:
            config:
                dict to use to create new action
            creatorType:
                type of action to create
            doSetupFunc:
                option bool if the setup funcs need to be done again
                some copied actions dont need to rerun setup funcs
        """
        actionCreator = self._getCreator(creatorType)
        actionObj = actionCreator(config)
        if doSetupFunc:
            actionObj.setup()
        return actionObj

    def validType(self, creatorType: str) -> bool:
        """Determine if the creator type is a valid action type"""
        return creatorType.lower() in _ACTION_FACTORY_TYPES

    def _getCreator(self, creatorType: str):
        """Get the action creator for the action type"""
        if creatorType.lower() in _ACTION_FACTORY_TYPES:
            return _ACTION_FACTORY_TYPES[creatorType.lower()]
        else:
            return None
