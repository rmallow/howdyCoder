from .action import Action
from ..core import message as msg
from ..commonUtil import userFuncCaller
from ..core.dataStructs import ActionSettings

import typing
from collections.abc import Iterable


class trigger(Action):
    def __init__(self, action_settings: ActionSettings, *args, **kwargs):
        self.output_func: userFuncCaller = action_settings.output_function
        super().__init__(action_settings, *args, **kwargs)

    def update(self):
        stdout_list, stderr_list = [], []
        for value, stdout_str, stderr_str, _ in super().multipleUpdate():
            if value:
                self.output_func(**self.parameters)
            stdout_list.append(stdout_str)
            stderr_list.append(stderr_str)
        return stdout_list, stderr_list

    def processRawTriggerValue(self, rawTriggerValue: typing.Any) -> list[msg.message]:
        """
        Take the unknown return type of a trigger and return a list of messages

        NOT CURRENTLY USED AND WOULD ONLY BE USED ONCE MOVING BACK TO HANDLERS
        """
        messagesToSendList = []
        if rawTriggerValue is not None:
            # if raw trigger is an iterable but not a string, iterate through
            if isinstance(rawTriggerValue, Iterable) and not isinstance(
                rawTriggerValue, str
            ):
                for rawMessage in rawTriggerValue:
                    sentMessage = None
                    if isinstance(rawMessage, msg.message):
                        # rawMessage are already message class messages so just adjust key and name
                        sentMessage = rawMessage
                    else:
                        # if not create the message here based of the raw value
                        if rawMessage is None:
                            continue
                        sentMessage = msg.message(
                            msg.MessageType.NORMAL,
                            rawMessage,
                        )
                    sentMessage.name = self.name
                    messagesToSendList.append(sentMessage)
            else:
                sentMessage = None
                if isinstance(rawTriggerValue, msg.message):
                    # rawMessage are already message class messages
                    sentMessage = rawTriggerValue

                else:
                    # raw value was neither message nor iterable so just send the raw value
                    sentMessage = msg.message(
                        msg.MessageType.NORMAL,
                        rawTriggerValue,
                    )
                    sentMessage.name = self.name
                sentMessage.name = self.name
                messagesToSendList.append(sentMessage)
        return messagesToSendList
