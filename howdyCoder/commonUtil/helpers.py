from ..core.commonGlobals import ENUM_DISPLAY

import time
import typing
from datetime import timedelta
from aenum import Enum


def getStrTime(epochTime: float) -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(epochTime))


def getStrElapsedTime(elapsed: float) -> str:
    td = timedelta(seconds=elapsed)
    return f"{td.days} days,  {(td.seconds // (60 * 60)):02d} : {(td.seconds // (60)):02d} : {td.seconds%60:02d}"


def getEnumAttributeList(enum, attribute: str) -> typing.List[str]:
    """Return a list of the enum attributes"""
    return [getattr(e, attribute, None) for e in enum]


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


def createErrorLabel(errorLabel: str, errorList=typing.List[str]) -> str:
    # determine error formatting based on number of errors
    if len(errorList) > 2:
        for error in errorList[:-1]:
            errorLabel = f"{errorLabel} {error}, "
        errorLabel = f"{errorLabel} and {errorList[-1]}"
    elif len(errorList) > 1:
        errorLabel = f"{errorLabel} {errorList[0]} and {errorList[1]}"
    else:
        errorLabel = f"{errorLabel} {errorList[0]}"
    return errorLabel
