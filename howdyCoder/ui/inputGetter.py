from .qtUiFiles.ui_mousePosGetter import Ui_MousePosGetter
from .qtUiFiles.ui_audioGetter import Ui_AudioGetter
from .util import abstractQt, audioRecordingUtil, genericWorker
from .uiConstants import GUI_REFRESH_INTERVAL
from .tutorialOverlay import AbstractTutorialClass

from ..commonUtil import openAIUtil
from ..core.dataStructs import InputData

from abc import abstractmethod
import typing
import time
import os

from PySide6 import QtWidgets, QtCore, QtGui

import pyautogui


class InputGetterBase(
    AbstractTutorialClass,
    QtWidgets.QWidget,
    metaclass=abstractQt.getAbstactQtResolver(QtWidgets.QWidget, AbstractTutorialClass),
):
    HIDE_ENTER = False
    HIDE_RESET = False

    inputEntered = QtCore.Signal(InputData)

    def __new__(self, *args, **kwargs):
        abstractQt.handleAbstractMethods(self)
        return super().__new__(self, *args, **kwargs)

    def __init__(self, resource_prefix: str, *args, **kwargs):
        super().__init__(resource_prefix, *args, **kwargs)
        self.setFocusPolicy(QtGui.Qt.FocusPolicy.StrongFocus)

    @abstractmethod
    def value(self):
        pass

    @abstractmethod
    def clear(self):
        pass


class MousePosGetter(InputGetterBase):
    TUTORIAL_RESOURCE_PREFIX = "test"

    HIDE_ENTER = True
    HIDE_RESET = True

    def __init__(
        self,
        parent: typing.Optional[QtWidgets.QWidget] = None,
        f: QtCore.Qt.WindowFlags = QtCore.Qt.WindowFlags(),
    ) -> None:
        super().__init__(self.TUTORIAL_RESOURCE_PREFIX, parent, f)
        self._ui = Ui_MousePosGetter()
        self._ui.setupUi(self)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.updatePos)
        self.timer.start(GUI_REFRESH_INTERVAL)

        self._last_check_time = time.time()
        self.x = self.y = None

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if (
            self._ui.active_check.isChecked()
            and event.key() == QtGui.Qt.Key.Key_Space
            and time.time() - self._last_check_time >= 1
            and self.x is not None
            and self.y is not None
        ):
            self._last_check_time = time.time()
            self.inputEntered.emit(InputData(val=(self.x, self.y)))
        return super().keyPressEvent(event)

    def getTutorialClasses(self) -> typing.List:
        return [self]

    def value(self):
        pass

    def clear(self):
        pass

    def updatePos(self):
        if self._ui.active_check.isChecked():
            self.x, self.y = pyautogui.position()
            self._ui.pos_label.setText(f"x:{self.x}, y:{self.y}")
        else:
            self.x = self.y = None
            self._ui.pos_label.setText("Not Active")


class AudioGetter(InputGetterBase):
    TUTORIAL_RESOURCE_PREFIX = "test"

    def __init__(
        self,
        parent: typing.Optional[QtWidgets.QWidget] = None,
        f: QtCore.Qt.WindowFlags = QtCore.Qt.WindowFlags(),
    ) -> None:
        super().__init__(self.TUTORIAL_RESOURCE_PREFIX, parent, f)
        self._ui = Ui_AudioGetter()
        self._ui.setupUi(self)

        self._ui.key_monitor_widget.allKeysValid.connect(self.setValidAPI)

        self._ui.key_monitor_widget.watchKey(openAIUtil.OPEN_AI_KEY_DATA_NAME)

        self._ui.record_button.released.connect(self.recordHit)

        for device in audioRecordingUtil.getInputDevices():
            self._ui.input_combo.addItem(device["name"], device["index"])

        self._recording_object: audioRecordingUtil.RecordingObject | None = None
        self._recording_thread = None
        self._recording_worker = None
        self._transcribing_thread = None
        self._transcribing_worker = None
        self._is_recording = False

    @QtCore.Slot()
    def setValidAPI(self, val: bool):
        self._valid_api = val
        self._ui.record_button.setEnabled(self._valid_api)

    def record(self):
        self._is_recording = True
        self._ui.record_button.setChecked(True)
        self._recording_object = audioRecordingUtil.RecordingObject()
        (
            self._recording_thread,
            self._recording_worker,
        ) = genericWorker.createThreadAndWorker(
            self._recording_object.record,
            self.handleRecord,
            self._ui.input_combo.currentData(),
        )

    def stopRecord(self):
        self._is_recording = False
        self._ui.record_button.setChecked(False)
        if self._recording_object is not None:
            self._recording_object.keep_running = False

    def handleRecord(self, filename: str):
        self.filename = filename
        self._ui.transcribing_status.setText("... TRANSCRIBING ...")
        (
            self._transcribing_thread,
            self._transcribing_worker,
        ) = genericWorker.createThreadAndWorker(
            openAIUtil.transcribeAudio, self.handleTranscribe, filename
        )

    def handleTranscribe(self, transcribed_text: typing.Dict[str, str]):
        self._ui.transcribed_text.setPlainText(transcribed_text["text"])
        self._ui.transcribing_status.setText("DONE TRANSCRIBING")
        if self._ui.active_check.isChecked():
            self.inputEntered.emit(InputData(val=transcribed_text["text"]))
        os.remove(self.filename)

    def clear(self):
        self._ui.transcribed_text.clear()
        self._ui.transcribing_status.clear()

    def value(self):
        if self._ui.transcribed_text.toPlainText():
            self.inputEntered.emit(
                InputData(val=self._ui.transcribed_text.toPlainText())
            )
            self.clear()

    @QtCore.Slot()
    def recordHit(self):
        if self._is_recording:
            self.stopRecord()
        else:
            self.record()

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if (
            self._ui.active_check.isChecked()
            and event.key() == QtGui.Qt.Key.Key_Space
            and self._ui.record_button.isEnabled()
        ):
            self.recordHit()
        return super().keyPressEvent(event)

    def getTutorialClasses(self) -> typing.List:
        return [self]
