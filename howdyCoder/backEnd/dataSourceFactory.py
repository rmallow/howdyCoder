from .dataBase import dataBase
from .dataSim import dataSim
from .dataFunc import dataFunc
from .dataStream import dataStream
from .dataThreaded import dataThreaded
from .dataInput import dataInput

from ..core.commonGlobals import DataSourcesTypeEnum


"""
Create a data source based on the passed in cretor type and configuration dict
"""

_DATA_SOURCE_FACTORY_TYPES = {
    DataSourcesTypeEnum.SIM.display: dataSim,
    DataSourcesTypeEnum.STREAM.display: dataStream,
    DataSourcesTypeEnum.FUNC.display: dataFunc,
    DataSourcesTypeEnum.THREADED.display: dataThreaded,
    DataSourcesTypeEnum.INPUT.display: dataInput,
}


class dataSourceFactory:
    def create(self, config: dict, creatorType: str) -> dataBase:
        dataSourceCreator = self._getCreator(creatorType)
        return dataSourceCreator(config)

    def validType(self, creatorType: str) -> bool:
        return creatorType.lower() in _DATA_SOURCE_FACTORY_TYPES

    def _getCreator(self, creatorType):
        if creatorType.lower() in _DATA_SOURCE_FACTORY_TYPES:
            return _DATA_SOURCE_FACTORY_TYPES[creatorType.lower()]
        else:
            None
