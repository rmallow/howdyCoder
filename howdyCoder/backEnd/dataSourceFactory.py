from .dataBase import DataBase
from .dataFunc import dataFunc
from .dataStream import dataStream
from .dataThreaded import dataThreaded
from .dataExternal import DataExternal

from ..core.commonGlobals import DataSourcesTypeEnum


"""
Create a data source based on the passed in cretor type and configuration dict
"""

_DATA_SOURCE_FACTORY_TYPES = {
    DataSourcesTypeEnum.FILE.display.lower(): DataExternal,
    DataSourcesTypeEnum.STREAM.display.lower(): dataStream,
    DataSourcesTypeEnum.FUNC.display.lower(): dataFunc,
    DataSourcesTypeEnum.THREADED.display.lower(): dataThreaded,
    DataSourcesTypeEnum.INPUT.display.lower(): DataExternal,
}


class dataSourceFactory:
    def create(self, config: dict, creatorType: str) -> DataBase:
        dataSourceCreator = self._getCreator(creatorType)
        return dataSourceCreator(config)

    def validType(self, creatorType: str) -> bool:
        return creatorType.lower() in _DATA_SOURCE_FACTORY_TYPES

    def _getCreator(self, creatorType):
        if creatorType.lower() in _DATA_SOURCE_FACTORY_TYPES:
            return _DATA_SOURCE_FACTORY_TYPES[creatorType.lower()]
        else:
            None
