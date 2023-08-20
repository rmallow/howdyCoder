from PySide6 import QtCore, QtUiTools


def loadUiWidget(uifilename, widgetsToRegister=[], parent=None):
    loader = QtUiTools.QUiLoader()
    for widget in widgetsToRegister:
        loader.registerCustomWidget(widget)
    uifile = QtCore.QFile(uifilename)
    uifile.open(QtCore.QFile.ReadOnly)
    ui = loader.load(uifile, parent)
    uifile.close()
    return ui
