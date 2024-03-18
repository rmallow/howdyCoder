from .dataStructs import Modes
from ..commonUtil.multiBase import multiBase

from abc import ABC, abstractmethod


class ModeHandler(multiBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._mode_func_map = {
            Modes.STANDBY: self.onStandby,
            Modes.RUNNING: self.onRunning,
            Modes.FINISHED: self.onFinished,
            Modes.STOPPED: self.onStopped,
        }
        assert all(m in self._mode_func_map for m in Modes), "Missing Mode Handlers"
        self._mode = Modes.STANDBY

    def onStandby(self, old_mode: Modes) -> None:
        pass

    def onRunning(self, old_mode: Modes) -> None:
        pass

    def onFinished(self, old_mode: Modes) -> None:
        pass

    def onStopped(self, old_mode: Modes) -> None:
        pass

    def changeMode(self, new_mode: Modes):
        old_mode = self._mode
        self._mode = new_mode
        self._mode_func_map[self._mode](old_mode)

    def getMode(self) -> Modes:
        return self._mode
