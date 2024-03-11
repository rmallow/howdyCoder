from ..core.commonGlobals import ENUM_DISPLAY
from functools import cache

import time
import typing
from datetime import timedelta
from aenum import Enum


def getStrTime(epochTime: float) -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(epochTime))


def getStrElapsedTime(elapsed: float) -> str:
    td = timedelta(seconds=elapsed)
    return f"{td.days} days,  {(td.seconds // (60 * 60)):02d} : {(td.seconds // (60)):02d} : {td.seconds%60:02d}"


@cache
def getEnumAttributeList(enum, attribute: str) -> typing.List[str]:
    """Return a list of the enum attributes"""
    return [getattr(e, attribute, None) for e in enum]


@cache
def findEnumByAttribute(enum, attribute: str, value: typing.Any):
    for e in enum:
        if getattr(e, attribute, None) == value:
            return e
    return None


def getConfigFromEnumDict(enumDict: typing.Dict[Enum, str]) -> typing.Dict[str, str]:
    return {
        getattr(k, ENUM_DISPLAY): v
        for k, v in enumDict.items()
        if getattr(k, ENUM_DISPLAY, "")
    }


def listToFormattedString(label: str, str_list: typing.List[str]) -> str:
    # determine label formatting based on number of strs
    res = ""
    if len(str_list) > 2:
        res = f"{label} {', '.join(str_list[:-1])}, and {str_list[-1]}"
    elif len(str_list) > 1:
        res = f"{label} {str_list[0]} and {str_list[1]}"
    else:
        res = f"{label} {str_list[0]}"
    return res


def getDupeName(
    name: str,
    name_container,
    copy_label: str = "copy",
    starting_number: int = 1,
    sub_blank_name=False,
) -> str:
    """Sure it should be a binary search, but why bother"""
    if sub_blank_name and not name:
        name = "blank_name"
    if name not in name_container:
        return name
    x = starting_number
    while f"{name}_{copy_label}_{x}" in (name_container):
        x += 1
    return f"{name}_{copy_label}_{x}"


def deDupeList(
    name_list: typing.List[str],
    copy_label: str = "copy",
    starting_number: int = 1,
    sub_blank_name: bool = False,
):
    name_set = set()
    res = []
    for name in name_list:
        new_name = getDupeName(
            name,
            name_set,
            copy_label=copy_label,
            starting_number=starting_number,
            sub_blank_name=sub_blank_name,
        )
        name_set.add(new_name)
        res.append(new_name)
    return res
