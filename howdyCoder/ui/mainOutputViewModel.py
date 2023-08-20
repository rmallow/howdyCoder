from .uiConstants import outputTypesEnum
from .sparseDictListModel import SparseDictListModel
from .algoData import AlgoDict

from ..core.commonGlobals import ITEM, AlgoStatusData
from ..core.configConstants import (
    DATA_SOURCES,
    ACTION_LIST,
    OUTPUT,
    TYPE,
    ActionTypeEnum,
    ENUM_DISPLAY,
)
from ..core import message as msg

import platform
import os

from PySide6 import QtGui, QtCore


class mainOutputViewModel(QtCore.QObject):
    addOutputViewSignal = QtCore.Signal(msg.message)

    def __init__(self, parent=None):
        super().__init__(parent)

        # All selectors will refer back to the same models
        # this way we only need to update one set of models and all selectors will be updated
        self.blockComboModel: QtGui.QStandardItemModel = QtGui.QStandardItemModel()
        self.handlerComboModel: QtGui.QStandardItemModel = QtGui.QStandardItemModel()

        # graph is disabled for mac unless environment variable has been set
        # There's lots of stuff online for why this doesn't work ie:
        # https://stackoverflow.com/questions/50168647/multiprocessing-causes-python-to-crash-and-gives-an-error-may-have-been-in-progr
        # based on debugging, issue happened when creating graph, so disabling it for mac
        # unless the user has the envionrment variable workaround
        typeStrings = [
            val.value for val in outputTypesEnum if val != outputTypesEnum.GRAPH
        ]
        if (
            platform.system() != "Darwin"
            or os.environ.get("OBJC_DISABLE_INITIALIZE_FORK_SAFETY", "NO") == "YES"
        ):
            typeStrings.append(outputTypesEnum.GRAPH.value)

        self.typeModel: QtCore.QStringListModel = QtCore.QStringListModel(typeStrings)

        # this will be assigned during main window creation
        self.algo_dict: AlgoDict = None
        self.outputViewModels = {}

    def addItem(self, model, key, value):
        item = QtGui.QStandardItem(str(key))
        item.setData(value)
        model.appendRow(item)

    def addBlocks(self, blockDict):
        for key, value in blockDict.items():
            self.addItem(self.blockComboModel, key, value)

    def addHandlers(self, handlerDict):
        for key, value in handlerDict.items():
            self.addItem(self.handlerComboModel, key, value)

    @QtCore.Slot()
    def receiveData(self, message: msg.message):
        if message.key.sourceCode in self.outputViewModels:
            modelList = self.outputViewModels[message.key.sourceCode]
            for model in modelList:
                model.appendData(message.details)

    @QtCore.Slot()
    def receiveColumns(self, message: msg.message):
        """
        From a status signal, updating what columns are avaialable for a block
        """
        data = AlgoStatusData(**message.details)
        if data.columns:
            # only override columns in there if there are any
            findList = self.blockComboModel.findItems(message.key.sourceCode)
            if len(findList) == 1:
                # there should be only one that matches
                findList[0].setData(data.columns)

    def setupOutputView(self, selectionDict):
        """
        Output select has finished selecting output, message mainframe to start sending data
        Return model for output view, mainOutputViewModel owns these models
        """

        m = msg.message(
            msg.MessageType.COMMAND,
            msg.CommandType.ADD_OUTPUT_VIEW,
            details=selectionDict,
        )

        self.addOutputViewSignal.emit(m)

        model = SparseDictListModel(**selectionDict)
        modelList = self.outputViewModels.get(selectionDict[ITEM], [])
        modelList.append(model)
        self.outputViewModels[selectionDict[ITEM]] = modelList
        return model

    @QtCore.Slot()
    def dataChanged(self):
        """On startup message add blocks and handlers to their combo models"""
        self.blockComboModel.clear()
        # add data from algo dict here
        for config in self.algo_dict.getConfigs():
            key = next(iter(config.keys()))
            columns = []
            for ds_key, ds_config in config[key].get(DATA_SOURCES, {}).items():
                try:
                    columns.extend(list(ds_config[OUTPUT].values()))
                except AttributeError:
                    columns.extend(ds_config[OUTPUT])

            for act_key, act_config in config[key].get(ACTION_LIST, {}).items():
                if act_config[TYPE] == getattr(ActionTypeEnum.EVENT, ENUM_DISPLAY):
                    columns.append(act_key)
            self.addItem(self.blockComboModel, key, columns)
