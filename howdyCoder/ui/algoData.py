from ..core.message import message

from ..core.commonGlobals import Modes, AlgoStatusData, AlgoSettings

from dataclasses import dataclass
import typing

from PySide6 import QtCore


@dataclass
class AlgoWidgetData:
    name: str
    config: AlgoSettings
    uid: int
    runtime: float = 0.0
    data_count: int = 0
    mode: Modes = Modes.STANDBY


class AlgoDict(QtCore.QObject):
    nameExists = QtCore.Signal(bool)
    dataChanged = QtCore.Signal()

    def __init__(self, parent: typing.Optional[QtCore.QObject] = None) -> None:
        """Dict for algo data to faciliate safe interaction with data"""
        super().__init__(parent)
        self._algos: typing.Dict[str, AlgoWidgetData] = {}
        self._current_id_set: typing.Dict[int, str] = {}
        self._current_uid: int = 0

    def getConfigs(self) -> typing.List[AlgoSettings]:
        for _, algo in self._algos.items():
            yield algo.config

    def getData(self, name: str):
        if name in self._algos:
            return self._algos[name]
        return None

    def getDataById(self, uid: int) -> AlgoWidgetData:
        if uid in self._current_id_set and self._current_id_set[uid] in self._algos:
            return self._algos[self._current_id_set[uid]]

    def setData(self, name: str, data: AlgoWidgetData):
        self._algos[name] = data
        self.dataChanged.emit()

    @QtCore.Slot()
    def contains(self, name):
        self.nameExists.emit(name in self._algos)
        return name in self._algos

    def remove(self, name: str):
        if name in self._algos:
            del self._current_id_set[self._algos[name].uid]
            del self._algos[name]
            self.dataChanged.emit()

    @QtCore.Slot()
    def addAlgo(self, code: str, algo_config: typing.Dict):
        self.remove(code)  # shouldn't already exist, but for safety
        self._algos[code] = AlgoWidgetData(code, algo_config, self._current_uid)
        self._current_id_set[self._current_uid] = code
        self._current_uid += 1
        self.dataChanged.emit()

    def compareIds(
        self, other: typing.Dict[int, typing.Any]
    ) -> typing.List[typing.List[int]]:
        """Determines what ids are not in the passed in set and what ids are in the other set but not in our set"""
        return [
            [my_id for my_id in self._current_id_set.keys() if my_id not in other],
            [o_id for o_id in other.keys() if o_id not in self._current_id_set],
        ]

    def updateAlgoStatus(self, code: str, data: AlgoStatusData):
        if code in self._algos:
            self._algos[code].data_count = data.data_length
            self._algos[code].runtime = data.runtime
            self._algos[code].mode = data.mode
