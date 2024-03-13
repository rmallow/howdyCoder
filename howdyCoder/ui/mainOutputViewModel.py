from ..core.dataStructs import ProgramStatusData
from .uiConstants import outputTypesEnum
from .sparseDictListModel import SparseDictListModel
from .programData import ProgramDict

from ..core.dataStructs import STDOutErrData
from ..core.commonGlobals import ITEM, TYPE, ActionTypeEnum, ENUM_DISPLAY, ProgramTypes
from ..core import message as msg
from ..commonUtil import helpers

import platform
import os
import time

from dataclass_wizard import fromlist

from PySide6 import QtGui, QtCore


class mainOutputViewModel(QtCore.QObject):
    addOutputViewSignal = QtCore.Signal(msg.message)

    def __init__(self, parent=None):
        super().__init__(parent)

        # All selectors will refer back to the same models
        # this way we only need to update one set of models and all selectors will be updated
        self.program_combo_model: QtGui.QStandardItemModel = QtGui.QStandardItemModel()
        self.handlerComboModel: QtGui.QStandardItemModel = QtGui.QStandardItemModel()

        # graph is disabled for mac unless environment variable has been set
        # There's lots of stuff online for why this doesn't work ie:
        # https://stackoverflow.com/questions/50168647/multiprocessing-causes-python-to-crash-and-gives-an-error-may-have-been-in-progr
        # based on debugging, issue happened when creating graph, so disabling it for mac
        # unless the user has the envionrment variable workaround
        type_strings = [
            val.value for val in outputTypesEnum if val != outputTypesEnum.GRAPH
        ]
        if (
            platform.system() != "Darwin"
            or os.environ.get("OBJC_DISABLE_INITIALIZE_FORK_SAFETY", "NO") == "YES"
        ):
            type_strings.append(outputTypesEnum.GRAPH.value)

        self.typeModel: QtCore.QStringListModel = QtCore.QStringListModel(type_strings)

        # this will be assigned during main window creation
        self.program_dict: ProgramDict = None
        self.outputViewModels = {}
        self.std_models = {}

    def addItem(self, model, key, value):
        item = QtGui.QStandardItem(str(key))
        item.setData(value)
        model.appendRow(item)

    def addBlocks(self, blockDict):
        for key, value in blockDict.items():
            self.addItem(self.program_combo_model, key, value)

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
        data = ProgramStatusData(**message.details)
        if data.columns:
            # only override columns in there if there are any
            findList = self.program_combo_model.findItems(message.key.sourceCode)
            if len(findList) == 1:
                # there should be only one that matches
                findList[0].setData(data.columns)

    def setupOutputView(self, selection_settings):
        """
        Output select has finished selecting output, message mainframe to start sending data
        Return model for output view, mainOutputViewModel owns these models
        """
        model = None
        if (
            selection_settings[TYPE] == outputTypesEnum.TABLE.value
            or selection_settings[TYPE] == outputTypesEnum.GRAPH.value
        ):
            m = msg.commandToChildWrapper(
                selection_settings[ITEM],
                msg.message(
                    msg.MessageType.COMMAND,
                    msg.CommandType.ADD_OUTPUT_VIEW,
                    details=selection_settings,
                    key=msg.messageKey(selection_settings[ITEM], None),
                ),
            )

            self.addOutputViewSignal.emit(m)

            model = SparseDictListModel(**selection_settings)
            modelList = self.outputViewModels.get(selection_settings[ITEM], [])
            modelList.append(model)
            self.outputViewModels[selection_settings[ITEM]] = modelList
        elif selection_settings[TYPE] == outputTypesEnum.PRINTED.value:
            if selection_settings[ITEM] not in self.std_models:
                self.std_models[selection_settings[ITEM]] = QtGui.QStandardItemModel()
            model = self.std_models[selection_settings[ITEM]]

        return model

    @QtCore.Slot()
    def dataChanged(self):
        """On startup message add blocks and handlers to their combo models"""
        self.program_combo_model.clear()
        # add data from algo dict here
        for config in self.program_dict.getConfigs():
            columns = []
            if config.type_ == ProgramTypes.ALGO:
                for ds_key, ds_config in config.settings.data_sources.items():
                    try:
                        columns.extend(list(ds_config.output.values()))
                    except AttributeError:
                        columns.extend(ds_config.output)

                for act_key, act_config in config.settings.action_list.items():
                    if act_config.type_ == ActionTypeEnum.EVENT.value:
                        columns.append(act_key)
            self.addItem(self.program_combo_model, config.name, columns)

    @QtCore.Slot()
    def receiveSTD(self, message: msg.message):
        if message.key.sourceCode not in self.std_models:
            self.std_models[message.key.sourceCode] = QtGui.QStandardItemModel()
        model = self.std_models[message.key.sourceCode]
        for data in fromlist(STDOutErrData, message.details):
            for s in data.out:
                s = s.strip()
                if s:
                    model.appendRow(
                        QtGui.QStandardItem(
                            f"{helpers.getStrTime(time.time())}: {data.action_name} - {s}"
                        )
                    )
            for s in data.err:
                s = s.strip()
                if s:
                    item = QtGui.QStandardItem(
                        f"{helpers.getStrTime(time.time())}: {data.action_name} - {s}"
                    )
                    item.setData(
                        QtGui.QBrush(QtCore.Qt.GlobalColor.yellow),
                        QtCore.Qt.ItemDataRole.BackgroundRole,
                    )
                    item.setData(
                        QtGui.QBrush(QtCore.Qt.GlobalColor.black),
                        QtCore.Qt.ItemDataRole.ForegroundRole,
                    )
                    model.appendRow(item)
