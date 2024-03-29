from ..core.dataStructs import AlgoSettings, ProgramStatusData, Modes
from ..core.message import message

from ..core.dataStructs import ProgramSettings

from collections import defaultdict
from dataclasses import dataclass, field
import typing

from PySide6 import QtCore


@dataclass
class ProgramWidgetData:
    name: str
    config: ProgramSettings
    uid: int
    runtime: float = 0.0
    data_count: int = 0
    mode: Modes = Modes.STANDBY
    logging_count: typing.Dict[int, int] = field(
        default_factory=lambda: defaultdict(int)
    )


class ProgramDict(QtCore.QObject):
    dataChanged = QtCore.Signal()

    def __init__(self, parent: typing.Optional[QtCore.QObject] = None) -> None:
        """Dict for program data to faciliate safe interaction with data"""
        super().__init__(parent)
        self._programs: typing.Dict[str, ProgramWidgetData] = {}
        self._current_id_set: typing.Dict[int, str] = {}
        self._current_uid: int = 0

    def getConfigs(self) -> typing.List[ProgramSettings]:
        for _, algo in self._programs.items():
            yield algo.config

    def getData(self, name: str):
        if name in self._programs:
            return self._programs[name]
        return None

    def getDataById(self, uid: int) -> ProgramWidgetData:
        if uid in self._current_id_set and self._current_id_set[uid] in self._programs:
            return self._programs[self._current_id_set[uid]]

    def setData(self, name: str, data: ProgramWidgetData):
        self._programs[name] = data
        self.dataChanged.emit()

    @QtCore.Slot()
    def contains(self, name):
        return name in self._programs

    def remove(self, name: str):
        if name in self._programs:
            del self._current_id_set[self._programs[name].uid]
            del self._programs[name]
            self.dataChanged.emit()

    @QtCore.Slot()
    def addProgram(self, code: str, program_config: ProgramSettings):
        self.remove(code)  # shouldn't already exist, but for safety
        self._programs[code] = ProgramWidgetData(
            code, program_config, self._current_uid
        )
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

    def updateProgramStatus(self, code: str, data: ProgramStatusData):
        if code in self._programs:
            self._programs[code].data_count = data.data_length
            self._programs[code].runtime = data.runtime
            self._programs[code].mode = data.mode

    def updateProgramLogging(self, code: str, logging_details: typing.Dict[str, str]):
        if code in self._programs:
            self._programs[code].logging_count[logging_details["levelno"]] += 1

    def getNames(self) -> typing.Set[str]:
        return set(self._programs.keys())
