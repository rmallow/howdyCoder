from . import configLoader
from ..core.commonGlobals import LOCAL_AUTH, LOCAL_PORT

# Note here we are using the dill version of the manger as we want dill queues
# multiprocess is dill wherhas multiprocessing is python built in
# Choosing SyncManger over BaseManager as this manager will also supply the program
# but those will not be acessible by outside connections
from multiprocessing.managers import BaseManager


class QueueManager(BaseManager):
    pass


GET_MAINFRAME_QUEUE = "getMainframeQueue"
GET_UI_QUEUE = "getUiQueue"
GET_LOGGING_QUEUE = "getLoggingQueue"

QueueManager.register(GET_MAINFRAME_QUEUE)
QueueManager.register(GET_UI_QUEUE)
QueueManager.register(GET_LOGGING_QUEUE)


def createQueueManager(isLocal: bool):
    # Get server settings, if none then assume local
    # TODO: Fix for data refactoring
    settingsDict = {}
    serverDict = None
    if not isLocal and "server" in settingsDict:
        serverDict = configLoader.getKeyValueIni(settingsDict["server"])

    port = None
    authkey = None
    ip = None
    if not isLocal and serverDict and "port" in serverDict:
        port = int(serverDict["port"])
    else:
        port = LOCAL_PORT

    if not isLocal and serverDict and "authkey" in serverDict:
        authkey = str.encode(serverDict["authkey"])
    else:
        authkey = LOCAL_AUTH

    if not isLocal and serverDict and "ip" in serverDict:
        ip = serverDict["ip"]
    else:
        ip = "127.0.0.1"

    # Connect to clientServerManager
    address = (ip, port)
    return QueueManager(address=address, authkey=authkey)
