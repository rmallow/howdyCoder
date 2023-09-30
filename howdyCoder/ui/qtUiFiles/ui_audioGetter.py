# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'audioGetter.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QHBoxLayout,
    QLabel, QPlainTextEdit, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

from ..keyMonitorWidget import KeyMonitorWidget
from . import res_rc

class Ui_AudioGetter(object):
    def setupUi(self, AudioGetter):
        if not AudioGetter.objectName():
            AudioGetter.setObjectName(u"AudioGetter")
        AudioGetter.resize(611, 381)
        self.verticalLayout = QVBoxLayout(AudioGetter)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(AudioGetter)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)

        self.key_monitor_widget = KeyMonitorWidget(AudioGetter)
        self.key_monitor_widget.setObjectName(u"key_monitor_widget")

        self.verticalLayout.addWidget(self.key_monitor_widget)

        self.control_box = QWidget(AudioGetter)
        self.control_box.setObjectName(u"control_box")
        self.horizontalLayout = QHBoxLayout(self.control_box)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.active_check = QCheckBox(self.control_box)
        self.active_check.setObjectName(u"active_check")

        self.horizontalLayout.addWidget(self.active_check)

        self.input_label = QLabel(self.control_box)
        self.input_label.setObjectName(u"input_label")

        self.horizontalLayout.addWidget(self.input_label)

        self.input_combo = QComboBox(self.control_box)
        self.input_combo.setObjectName(u"input_combo")

        self.horizontalLayout.addWidget(self.input_combo)

        self.record_button = QPushButton(self.control_box)
        self.record_button.setObjectName(u"record_button")
        self.record_button.setEnabled(False)
        icon = QIcon()
        icon.addFile(u":/audio/mic.png", QSize(), QIcon.Normal, QIcon.Off)
        icon.addFile(u":/audio/stop_audio.png", QSize(), QIcon.Normal, QIcon.On)
        icon.addFile(u":/audio/stop_audio.png", QSize(), QIcon.Selected, QIcon.On)
        self.record_button.setIcon(icon)
        self.record_button.setCheckable(True)
        self.record_button.setChecked(False)

        self.horizontalLayout.addWidget(self.record_button)


        self.verticalLayout.addWidget(self.control_box)

        self.widget_2 = QWidget(AudioGetter)
        self.widget_2.setObjectName(u"widget_2")
        self.verticalLayout_2 = QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.transcribing_status = QLabel(self.widget_2)
        self.transcribing_status.setObjectName(u"transcribing_status")
        self.transcribing_status.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.transcribing_status)

        self.transcribed_text = QPlainTextEdit(self.widget_2)
        self.transcribed_text.setObjectName(u"transcribed_text")

        self.verticalLayout_2.addWidget(self.transcribed_text)


        self.verticalLayout.addWidget(self.widget_2)


        self.retranslateUi(AudioGetter)

        QMetaObject.connectSlotsByName(AudioGetter)
    # setupUi

    def retranslateUi(self, AudioGetter):
        AudioGetter.setWindowTitle(QCoreApplication.translate("AudioGetter", u"Audio Getter", None))
        self.label.setText(QCoreApplication.translate("AudioGetter", u"Hit the record button to start recording, hit space when active is checked. Hit the same button to stop recording, or space when active is checked. Once recorded, the audio will be transcribed as text before being sent off.  If active is checked the recording will automatically be sent otherwise hit enter to send. (Experimental)", None))
        self.active_check.setText(QCoreApplication.translate("AudioGetter", u"Active", None))
        self.input_label.setText(QCoreApplication.translate("AudioGetter", u"Input Device:", None))
        self.record_button.setText(QCoreApplication.translate("AudioGetter", u"Record", None))
        self.transcribing_status.setText("")
    # retranslateUi

