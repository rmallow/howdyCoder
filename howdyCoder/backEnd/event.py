from . import action as act


class event(act.Action):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self):
        stdout_list, stderr_list = [], []
        for value, stdout_str, stderr_str, index in super().multipleUpdate():
            self.feed.appendCalcData(self.name, index, value)
            stdout_list.append(stdout_str)
            stderr_list.append(stderr_str)
        return stdout_list, stderr_list
