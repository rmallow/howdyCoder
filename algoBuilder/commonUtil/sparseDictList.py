from __future__ import annotations
from typing import Any
import typing
from dataclasses import dataclass


@dataclass(frozen=True)
class SparseData:
    index: int
    value: Any

    def to_string(self, show_index: bool = False):
        return f"{self.index} : {str(self.value)}" if show_index else str(self.value)


class SparseDictList(dict):
    """
    Conveince Class for supporting dicts that are dict[key] -> list
    """

    def __init__(self):
        super().__init__()
        self.indexKey = None
        self.longest_list = 0

    def __setitem__(self, key: str, value: Any) -> Any:
        super().__setitem__(key, value)
        # without this hasattr check there is some weird pickling issues
        if hasattr(self, "longest_list") and len(self[key]) > self.longest_list:
            self.longest_list = len(self[key])

    def __getattribute__(self, name: str) -> Any:
        if name == "index":
            if self.indexKey is not None:
                return self[self.indexKey]
            else:
                return None
        else:
            return super().__getattribute__(name)

    def __getstate__(self):
        """because we overrided __getattribute__ we must explicitly define these for pickling"""
        return self.__dict__

    def __setstate__(self, d):
        """because we overrided __getattribute__ we must explicitly define these for pickling"""
        self.__dict__.update(d)

    def setIndex(self, indexKey: str) -> None:
        if indexKey in self:
            self.indexKey = indexKey
        else:
            self.indexKey = None

    def getNthKey(self, index: int = 0) -> Any:
        if index < 0:
            index += len(self)
        for i, key in enumerate(self):
            if index == i:
                return key

    def appendDictList(self, b: dict):
        if b is not None:
            for key in b.keys():
                if key not in self:
                    self[key] = []
                if isinstance(b[key], list):
                    self[key].extend(b[key])
                else:
                    self[key].append(b[key])
                if len(self[key]) > self.longest_list:
                    self.longest_list = len(self[key])

    def sliceDictListEnd(self, length: int) -> SparseDictList:
        returnDict = SparseDictList()
        for key, value in self.items():
            returnDict[key] = value[(-1 * length) :]
        return returnDict

    def sliceDictList(self, start: int, end: int) -> SparseDictList:
        returnDict = SparseDictList()
        for key, value in self.items():
            returnDict[key] = value[start:end]
        return returnDict

    def getLengthOfLongestList(self) -> int:
        return self.longest_list

    def getFirstListLength(self) -> int:
        return len(next(iter(self.values())))

    def appendDataList(self, data_list: typing.List) -> None:
        max_len = 1 if data_list else 0
        for data, code, flatten in data_list:
            for key, value in data.items():
                valid_key = f"{code}-{key}" if code else key
                if valid_key not in self:
                    self[valid_key] = []
                if isinstance(value, list) and flatten:
                    max_len = max(max_len, len(value))
                    for x in range(len(value)):
                        self[valid_key].append(SparseData(self.longest_list + x, value))
                else:
                    self[valid_key].append(
                        SparseData(self.longest_list + max_len - 1, value)
                    )
        self.longest_list += max_len

    def appendData(self, key: str, index: int, value: typing.Any):
        if key not in self:
            self[key] = []
        self[key].append(SparseData(index, value))
