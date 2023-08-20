from inspect import signature


def adjustArgs(func, argList):
    sig = signature(func)
    if len(sig.parameters) == 0:
        return func()
    elif len(sig.parameters) < len(argList):
        argList = argList[0:len(sig.parameters)]
    else:
        argList = argList + [None]*(len(sig.parameters) - len(argList))
    return func(*argList)


def iterableReturnValue(funcResult, returnNum):
    noneToAdd = returnNum - 1
    if isinstance(funcResult, tuple):
        if (len(funcResult)) >= returnNum:
            return funcResult[0:returnNum]
        else:
            noneToAdd = returnNum - len(funcResult)
    else:
        if returnNum > 1:
            funcResult = (funcResult,)
        else:
            return funcResult

    return funcResult + (None,) * noneToAdd
