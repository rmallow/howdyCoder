from .handlerData import handlerData

from .util import wrappers as wrap

from ..commonUtil.userFuncCaller import UserFuncCaller

import typing


class handler:
    """
    handler class, takes message from message router and based on conditions calls ouputFunc

    Attributes:
        code:
            string value of the block the handler is associated with
        calcFunc:
            calculating function for determining to call outputFunc based on messages from router
        period:
            integer period for messages to pull in
        parameters:
            passed in parameters to be used in func calls
        setupFuncs:
            when setup is called adds to parameters for later use
        aggregate:
            bool for if aggregate or not
    """

    def __init__(
        self,
        code,
        calcFunc,
        *args,
        period=1,
        name="defaultHandlerName",
        parameters={},
        setupFuncs={},
        outputFunc=None,
        aggregate=False,
        **kwargs
    ):
        self.code: str = code
        self.calcFunc: UserFuncCaller = calcFunc
        self.period: int = period
        self.name: str = name
        self.parameters: typing.Dict[str, typing.Any] = parameters
        self.setupFuncs: typing.Dict[str, UserFuncCaller] = setupFuncs
        self.outputFunc: UserFuncCaller = outputFunc
        self.aggregate: bool = aggregate
        self.handlerData: handlerData = None
        self.personalData: typing.Dict = {}

    async def updatePriority(self, message):
        # this func will handle priority messages
        pass

    async def update(self, key):
        """
        @brief: called to update by message router to update handler
            when message subscription is hit

        @param: key - messageKey to update parameter on

        calls calcFunc and outputFunc if bool result of calcFunc is true
        parameters passed into funcs is:
            handlerData, parameters, personalData in that order

        TODO: handle passing functions based on arguement names,
            which means to update wrapper
        """
        handlerData = self.handlerData.getPeriod(key, self.period)

        handlerParams = {"handlerData": handlerData, "personalData": self.personalData}
        rawVal = self.calcFunc(**handlerParams, **self.parameters)
        # then unpack the results, personalData return could be None
        # first result should always be boolResult
        boolResult, personalData = wrap.iterableReturnValue(rawVal, 2)

        # append personal data
        if personalData is not None:
            self.personalData[key] = personalData

        # after adjust personal data, call output function
        if boolResult:
            self.outputFunc(**handlerParams, **self.parameters)

    def setup(self):
        """
        Called on handler initialization, this setup function is supplied from the config
        """
        for key, func in self.setupFuncs.items():
            self.parameters |= {key: func(**self.parameters)}
