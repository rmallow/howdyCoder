from ..core import message as msg
from ..core.messageKey import messageKey
from .action import action as act
from .event import event
from .trigger import trigger
from . import feed as feedModule
from . import messageRouter as mRModule

from ..core.configConstants import ActionTypeEnum


class actionPool:
    """
    Container and caller for all actions of a algo, communicates with messageRouter

    Attributes:
        triggers/events:
            main data structures for actionPool, contains all actions split into event/triggers
        code:
            algo code that the actionPool belongs to
        count:
            int number of times update called
    """

    def __init__(
        self,
        actions: list[act],
        code: str,
    ):
        # self.messageRouter: mRModule.messageRouter = messageRouter
        self.code: str = code
        self.events: list[event] = []
        self.triggers: list[trigger] = []
        self.count: int = 0

        for action in actions:
            self.addAction(action)

    def doActions(self) -> None:
        """
        Perform all of the events followed by all of the triggers
        if given handle aggregate actions
        dispatch trigger messages to message router
        """
        for event in self.events:
            event.update()
        for trigger in self.triggers:
            trigger.update()

    def addAction(self, action: act) -> None:
        """Seperate action out into trigger or event list"""
        if action.actionType == ActionTypeEnum.EVENT.display:
            self.events.append(action)
        else:
            self.triggers.append(action)
