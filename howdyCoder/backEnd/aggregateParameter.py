from .aggregate import aggregate

from ..commonUtil import mpLogging

INPUT_PARAMETER = "inputParameter"
OUTPUT_PARAMETER = "outputParameter"


AGGREGATE_PARAMETER_REQUIRED_LIST = ["aggregateConfig"]


class aggregateParameter(aggregate):
    """
    Aggregate paramater expands off of the parameters and sends those parameters
    to the child actions
    """

    def __init__(self, aggregateConfig, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.aggregateConfig: dict = aggregateConfig

        if (
            INPUT_PARAMETER not in self.aggregateConfig
            or OUTPUT_PARAMETER not in self.aggregateConfig
        ):
            mpLogging.critical(
                "Invalid aggregateConfig supplied for aggregate parameter: " + self.name
            )

        self.childrenCreated = False

    def createChildren(self):
        if not self.childrenCreated:
            self.childrenCreated = True
            newParameters = self.parameters.copy()
            try:
                del newParameters[self.aggregateConfig[INPUT_PARAMETER]]
                for parameter in self.parameters[self.aggregateConfig[INPUT_PARAMETER]]:
                    newAction = self.createChildAction(doSetupFunc=False)
                    newAction.parameters = newParameters.copy()
                    newAction.parameters[
                        self.aggregateConfig[OUTPUT_PARAMETER]
                    ] = parameter
                    newAction.name += "-" + parameter
                    self.childActions.append(newAction)
            except:
                mpLogging.critical(
                    "Critical error creating children action for agg: "
                    + self.name
                    + " input parameter name: "
                    + self.aggregateConfig[INPUT_PARAMETER]
                )
