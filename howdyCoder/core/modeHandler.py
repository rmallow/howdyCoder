from .dataStructs import Modes

from abc import ABC, abstractmethod


class ModeHandler(ABC):
    def __init__(self, *args, **kwargs):
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
        assert new_mode != self._mode, "Tried to change mode to current mode"
        old_mode = self._mode
        self._mode = new_mode
        self.MODE_FUNC_MAP[self._mode](self, old_mode)

    def getMode(self) -> Modes:
        return self._mode

    MODE_FUNC_MAP = {
        Modes.STANDBY: onStandby,
        Modes.RUNNING: onRunning,
        Modes.FINISHED: onFinished,
        Modes.STOPPED: onStopped,
    }


assert all(m in ModeHandler.MODE_FUNC_MAP for m in Modes), "Missing Mode Handlers"
