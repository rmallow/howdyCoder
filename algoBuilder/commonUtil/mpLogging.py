from . import queueManager

import logging

_extraKwargs = ["group", "source", "description"]

_mpKwarg = "_mpKwarg"


def adjustKwarg(kwargs):
    if "extra" not in kwargs:
        kwargs["extra"] = {}
    kwargs["extra"][_mpKwarg] = True
    kwargs["exc_info"] = True
    for kwarg in _extraKwargs:
        if kwarg in kwargs:
            kwargs["extra"][kwarg] = kwargs[kwarg]
            del kwargs[kwarg]


def handleRecordData(recordData):
    if recordData is not None:
        try:
            record = logging.makeLogRecord(recordData)

            logger = logging.getLogger(record.name)
            if logger.isEnabledFor(record.levelno):
                logger.handle(record)
        except Exception:
            logging.exception("Error in log handler")


class MPLogger(logging.Logger):
    log_queue = None
    mpKey: str = None

    def isEnabledFor(self, level):
        return True

    def handle(self, record):
        if getattr(record, _mpKwarg, False):
            if record.exc_info:
                # to get traceback text into record.exc_text
                logging._defaultFormatter.format(record)
                record.exc_info = None  # not needed any more
            d = dict(record.__dict__)
            d["msg"] = record.getMessage()
            d["args"] = None
            d["mpKey"] = self.mpKey
            self.log_queue.put(d)
        elif False:  # can be changed to show all logs but will spam the feed
            # TODO: change this to not just be False and based on cl arg
            super().handle(record)

    def log(self, level, msg, *args, **kwargs):
        # stacklevel is used in logging.findCaller, it is the number of frames on the stack
        # to go back, in our case it needs to go four back to find where the mpLogging was called
        super().log(level, msg, *args, **kwargs, stacklevel=4)

    def critical(self, msg, *args, **kwargs):
        self.log(logging.CRITICAL, msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.log(logging.ERROR, msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.log(logging.WARNING, msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.log(logging.INFO, msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.log(logging.DEBUG, msg, *args, **kwargs)


def makeMpLogged(isLocal, mpKey):
    clientServerManager = queueManager.createQueueManager(isLocal)
    clientServerManager.connect()
    assert hasattr(clientServerManager, queueManager.GET_LOGGING_QUEUE)
    MPLogger.log_queue = getattr(clientServerManager, queueManager.GET_LOGGING_QUEUE)()
    MPLogger.mpKey = mpKey
    logging.setLoggerClass(MPLogger)
    # monkey patch root logger and already defined loggers
    logging.root.__class__ = MPLogger
    for logger in logging.Logger.manager.loggerDict.values():
        if not isinstance(logger, logging.PlaceHolder):
            logger.__class__ = MPLogger


def loggedProcess(isLocal, mpKey, func, *args, **kwargs):
    makeMpLogged(isLocal, mpKey)
    func(isLocal, *args, **kwargs)


# Basic functions to mimic logging.debug type functions but for mpLogging
# These are safe to use as regular logging too


def mpLoggingCheck(msg, kwargs):
    if not isinstance(logging.getLogger(), MPLogger):
        for kwarg in _extraKwargs:
            if kwarg in kwargs:
                msg += f" {kwarg}: {kwargs[kwarg]}"
                del kwargs[kwarg]
    return msg


def critical(msg, *args, **kwargs):
    msg = mpLoggingCheck(msg, kwargs)
    adjustKwarg(kwargs)
    logging.getLogger().critical(msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    msg = mpLoggingCheck(msg, kwargs)
    adjustKwarg(kwargs)
    logging.getLogger().error(msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    msg = mpLoggingCheck(msg, kwargs)
    adjustKwarg(kwargs)
    logging.getLogger().warning(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    msg = mpLoggingCheck(msg, kwargs)
    adjustKwarg(kwargs)
    logging.getLogger().info(msg, *args, **kwargs)


def debug(msg, *args, **kwargs):
    msg = mpLoggingCheck(msg, kwargs)
    adjustKwarg(kwargs)
    logging.getLogger().debug(msg, *args, **kwargs)
