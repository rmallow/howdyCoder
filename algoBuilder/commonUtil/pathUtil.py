import os


def getFileDirPath(filename: str) -> str:
    """
    Pass in filename and get the path the dir of that file
    """

    dirPath, _ = os.path.split(os.path.realpath(filename))
    return dirPath


def getPathToFileFromFile(filename: str, fileToGetPathOf: str) -> str:
    dirPath = getFileDirPath(filename)
    return os.path.join(dirPath, fileToGetPathOf)
