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
    Container and caller for all actions of a block, communicates with messageRouter

    Attributes:
        triggers/events:
            main data structures for actionPool, contains all actions split into event/triggers
        messageRouter:
            where the output from triggers are sent to
        code:
            block code that the actionPool belongs to
        count:
            int number of times update called
    """

    # TODO: Either remove or reimplement message router / handlers
    """
    def __init__(
        self,
        actions: list[act],
        messageRouter: mRModule.messageRouter,
        code: str,
    ):
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
        # TODO: Either remove or reimplement message router / handlers
        """
        if len(self.triggers) > 0:
            # tell message router tha triggers are going to start sending messages
            startKey = messageKey(self.code, self.count)
            startCmd = msg.message(
                msg.MessageType.COMMAND, msg.CommandType.START, key=startKey
            )
            self.messageRouter.receive(startCmd)

            #
            #   various checks done on how to handle values/messages returned from trigger funcs
            #
            sentMessageList = []
            for trigger in self.triggers:
                rawMessageList = trigger.update()
                if rawMessageList:
                    for sentMessage in rawMessageList:
                        sentMessage.key = startKey
                        if sentMessage.name is None:
                            sentMessage.name = trigger.name

                        if sentMessage.isPriority():
                            self.messageRouter.receive(sentMessage)
                        else:
                            sentMessageList.append(sentMessage)

            # send all the non priority messages, if there are any
            if len(sentMessageList) > 0:
                self.messageRouter.receive(sentMessageList)
            #
            #   End of trigger func updating and sending to message router
            #
            # tell message router tha triggers are going to done sending messages
            # handlers should now be told to process this block of messages

            endKey = messageKey(self.code, self.count)
            endCmd = msg.message(
                msg.MessageType.COMMAND, msg.CommandType.END, key=endKey
            )
            self.messageRouter.receive(endCmd)
            self.count += 1
        """

    def addAction(self, action: act) -> None:
        """Seperate action out into trigger or event list"""
        if action.actionType == ActionTypeEnum.EVENT.display:
            self.events.append(action)
        else:
            self.triggers.append(action)
