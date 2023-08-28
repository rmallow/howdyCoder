from .action import action
from . import actionFactory as aF


from collections.abc import Iterable
from typing import List


class aggregate(action):
    """
    Aggregates are intended to perform the same action on multiple inputes
    Either combining all the inputs for one action
    Or Performing the action on multiple sets of inputs
    """

    def __init__(self, *args, combined=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.combined: bool = False
        self.lastNumColumns = 0
        self.childActions: List[action] = []

    def createChildren(self):
        numColumns = len(self.feed.data.keys()) + len(self.feed.calcData.keys())
        if numColumns > self.lastNumColumns:
            if self.combined and len(self.aggregateColumns) > 0:
                # so if it's combined and there are already some aggregate columns then just
                # modify whats already there
                self.modifyCombinedActionAggregate()
            self.addNewChildren()
        self.lastNumColumns = numColumns

    def createChildAction(self, doSetupFunc: bool = True):
        config = self.getConfig()
        actionType = config.type_
        factory = aF.actionFactory()
        newAction = factory.create(config, actionType, doSetupFunc=doSetupFunc)
        newAction.feed = self.feed
        return newAction

    def update(self) -> list:
        """
        If the aggregate is a trigger than it will return it's child return values as one list
        If the aggregate is an event then it will just return an empty list that shouldn't be used
        """
        self.createChildren()

        triggerReturnVal = []
        for child in self.childActions:
            # events will return None, but triggers could return something useful
            actionVal = child.update()
            if actionVal is not None:
                if isinstance(actionVal, Iterable) and not isinstance(actionVal, str):
                    triggerReturnVal += actionVal
                else:
                    triggerReturnVal.append(actionVal)

        return triggerReturnVal
