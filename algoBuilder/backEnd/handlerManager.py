from .handler import handler


"""
manages all handlers and issues update commands
gets update lists and corresponding source codes for updates from message Router

"""


class handlerManager:
    def __init__(self, sharedData):
        self.sharedData = sharedData
        self.messageSubscriptions = {}
        self.aggregateMessageSubscriptions = {}

        self.handlers = {}

    # wrapper for UI to use
    def loadItem(self, configDict):
        self.loadHandlers(configDict)

    def loadHandlers(self, configDict):
        for code, config in configDict.items():
            if code in self.handlers:
                print("Handler code already exists: " + code)
            h = self._loadHandler(code, config)
            h.handlerData = self.sharedData
            self.handlers[code] = h

    def _addSubscriptions(self, subscriptions, val):
        for subscription in subscriptions:
            subscription = subscription.lower()
            # we need to check if it's an aggregate message subscription as we have to handle
            # those type of message subsciptions different than direct ones
            if "*" in subscription:
                lst = self.aggregateMessageSubscriptions.get(subscription, [])
                lst.append(val)
                self.aggregateMessageSubscriptions[subscription] = lst
            else:
                lst = self.messageSubscriptions.get(subscription, [])
                lst.append(val)
                self.messageSubscriptions[subscription] = lst

    def _loadHandler(self, code, config):
        subscriptions = config["subscriptions"]

        config["config"] = config
        if "params" in config:
            config["params"]["subscriptions"] = subscriptions

        h = handler(code, **config)
        h.setup()
        self._addSubscriptions(subscriptions, h)
        return h

    def clear(self):
        self.handlers = None
