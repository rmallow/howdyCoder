from ..core.message import message

from ..core.commonGlobals import DATA_LENGTH, RUNTIME, RECEIVE_TIME

from dataclasses import dataclass
from enum import Enum
import typing

from PySide2 import QtCore


class AlgoStatusEnum(str, Enum):
    STARTED = "Started"
    STOPPED = "Stopped"
    STANDBY = "Standby"


@dataclass
class AlgoData:
    name: str
    config: typing.Dict
    uid: int
    runtime: float = 0.0
    data_count: int = 0
    status: AlgoStatusEnum = AlgoStatusEnum.STANDBY


class AlgoDict(QtCore.QObject):
    nameExists = QtCore.Signal(bool)
    dataChanged = QtCore.Signal()

    def __init__(self, parent: typing.Optional[QtCore.QObject] = None) -> None:
        """Dict for algo data to faciliate safe interaction with data"""
        super().__init__(parent)
        self._algos: typing.Dict[str, AlgoData] = {}
        self._current_id_set: typing.Dict[int, str] = {}
        self._current_uid: int = 0

    def getConfigs(self) -> typing.Dict:
        for key, algo in self._algos.items():
            yield {key: algo.config}

    def getData(self, name: str):
        if name in self._algos:
            return self._algos[name]
        return None

    def getDataById(self, uid: int) -> AlgoData:
        if uid in self._current_id_set and self._current_id_set[uid] in self._algos:
            return self._algos[self._current_id_set[uid]]

    def setData(self, name: str, data: AlgoData):
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
        self._algos[code] = AlgoData(code, algo_config, self._current_uid)
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

    def updateAlgoStatus(self, m: message):
        if m.key.sourceCode in self._algos:
            if DATA_LENGTH in m.details:
                self._algos[m.key.sourceCode].data_count = m.details[DATA_LENGTH]
            if RUNTIME in m.details:
                self._algos[m.key.sourceCode].runtime = m.details[RUNTIME]
            self._algos[m.key.sourceCode].status = (
                AlgoStatusEnum.STARTED
                if RECEIVE_TIME in m.details
                else AlgoStatusEnum.STOPPED
            )
