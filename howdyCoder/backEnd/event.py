from . import action as act
from . import constants as con

from ..commonUtil import mpLogging


class event(act.action):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self):
        for value, index in super().update():
            self.feed.appendCalcData(self.name, index, value)
