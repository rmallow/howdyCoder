from .aggregateData import aggregateData
from ..core.configConstants import INPUT


class aggregateDataParameter(aggregateData):
    """
    Aggregate param data expands off of the parameters and looks
    for column names based on the parameters
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self):
        # should this be INPUT_PARAMETER? revisit when aggregates are added back
        self.input = self.parameters.get(INPUT, [])
        super().update()
