from ..core import message as msg
from .asyncScheduler import asyncScheduler
from . import handler
from . import handlerData
import fnmatch

from .util.commandProcessor import commandProcessor

from ..commonUtil import mpLogging
from ..core.commonGlobals import ROUTER_GROUP

import queue
from collections.abc import Iterable


class messageRouter(commandProcessor):
    """
    This class works as an intermediate between the blocks and the handlers
    The message router accepts new messages from triggers and sends
    those messages out to all handlers that are subscribed to that message
    """

    def __init__(
        self,
        messageSubscriptions: dict[str, handler.handler],
        aggregateMessageSubscriptions: dict[str, handler.handler],
        hD: handlerData,
        queue,
    ):
        # initalize command processor
        super().__init__()

        self.end = False
        self.messageQueue = queue
        self.messageSubscriptions: dict[str, handler.handler] = messageSubscriptions
        self.aggregateMessageSubscriptions: dict[
            str, handler.handler
        ] = aggregateMessageSubscriptions
        self.handlerUpdateDict = {}
        self.handlerData: handlerData = hD

        self.blocksToClear = set()

        self.addCmdFunc(msg.CommandType.CLEAR, messageRouter.cmdClear)

        self.loop = asyncScheduler()

    def initAndStartLoop(self, isLocal):
        mpLogging.info("Starting Message Roouter", group=ROUTER_GROUP)
        self.loop.init()
        self.loop.addTask(self.mainLoop(), name="Router Main Loop")
        self.loop.start()

    async def mainLoop(self):
        # main process loop for message router
        while not self.end:
            try:
                # pylint: disable=no-member
                message = await self.messageQueue.coro_get(timeout=2)
            except queue.Empty:
                continue
            else:
                if message is not None:
                    # determine if message is a command
                    if isinstance(message, msg.message):
                        # just one message, check what type
                        if message.isCommand():
                            # calls processorCommand func
                            self.processCommand(message.content, details=message)
                        elif message.isPriority():
                            # immediately broadcast a priority message
                            self.broadcastPriority(message)
                        else:
                            mpLogging.warning(
                                "Unexpected message type",
                                description="Message: " + str(message),
                                group=ROUTER_GROUP,
                            )
                    elif isinstance(message, Iterable):
                        for singleMessage in message:
                            if (
                                isinstance(singleMessage, msg.message)
                                and singleMessage.isNormal()
                            ):
                                self.broadcast(singleMessage)
                            else:
                                mpLogging.warning(
                                    "Unexpected value in message router message list",
                                    dsecription="Message: " + str(singleMessage),
                                    group=ROUTER_GROUP,
                                )
                    else:
                        mpLogging.warning(
                            "Unexpected value in router",
                            description="Message: " + str(message),
                            group=ROUTER_GROUP,
                        )

    # send to message subscriptions priority
    def broadcastPriority(self, message):
        self.handlerData.insert(message)
        handlerList = self.findMessageSubscription(message)
        for handlerToUpdate in handlerList:
            self.loop.addTaskArgs(handlerToUpdate.updatePriority, message)

    # send to message subscriptions
    def broadcast(self, message):
        self.handlerData.insert(message)
        handlerList = self.findMessageSubscription(message)
        updateSet = self.handlerUpdateDict.get(message.key, set())
        updateSet.update(handlerList)

    def receive(self, message):
        # pylint: disable=no-member
        self.messageQueue.put(message)

    def findMessageSubscription(self, message: msg.message) -> list[handler.handler]:
        """
        @brief: Using message subscriptions find a handler that is subscribed to the message

        @parm: message - message that we are checking subscriptions on
        @return: list of handlers that are subscribed to the message
        """
        # first check the direct message subscriptions
        handlerList = self.messageSubscriptions.get(message.name, [])

        # next check if any of them match an aggregate subscription
        for (
            aggSubscription,
            subHandlerList,
        ) in self.aggregateMessageSubscriptions.items():
            if fnmatch.fnmatch(message.name, aggSubscription):
                handlerList.extend(subHandlerList)
        return handlerList

    def cmdStart(self, command, details=None):
        """
        @brief: called from command processor super class when Start command is received
            signals the start of messages for this key
            clears data for code if it's been marked to clear

        @param: command - command being executed
        @param: details - rest of message command came on
        """
        if details.key.sourceCode in self.blocksToClear:
            self.handlerData.clearCode(details.key.sourceCode)
            self.blocksToClear.remove(details.key.sourceCode)
        if details.key not in self.handlerUpdateDict:
            self.handlerUpdateDict[details.key] = set()
        else:
            mpLogging.warning(
                "start cmd on existing update list",
                description="Message details: " + str(details),
                group=ROUTER_GROUP,
            )

    def cmdEnd(self, command, details=None):
        """
        @brief: called from command processor super class when End command is received
            signals the end of messages for this key

        @param: command - command being executed
        @param: details - rest of message command came on
        """
        updateSet = self.handlerUpdateDict.pop(details.key, set())
        for handlerToUpdate in updateSet:
            self.loop.addTaskArgs(handlerToUpdate.update, details.key)

    def cmdShutdown(self, command, details=None):
        """
        @brief: called from command processor super class when Shutdown command is received

        @param: command - command being executed
        @param: details - rest of message command came on
        """
        self.end = True

    def cmdClear(self, command, details=None):
        """
        @brief: called from command processor super class when Clear command is received
            Adds code to set, this code will be cleared when start is called for same code

        @param: command - command being executed
        @param: details - rest of message command came on
        """
        self.blocksToClear.add(details.key.sourceCode)
