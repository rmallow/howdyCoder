from . import action as act


class event(act.Action):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self):
        for value, index in super().update():
            self.feed.appendCalcData(self.name, index, value)
