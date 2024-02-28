# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'fileDataSourceSettings.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QLabel, QSizePolicy, QVBoxLayout, QWidget)

from ..util.toggleSwitch import Switch

class Ui_FileDataSourceSettings(object):
    def setupUi(self, FileDataSourceSettings):
        if not FileDataSourceSettings.objectName():
            FileDataSourceSettings.setObjectName(u"FileDataSourceSettings")
        FileDataSourceSettings.resize(400, 300)
        self.verticalLayout = QVBoxLayout(FileDataSourceSettings)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.sheet_select_box = QWidget(FileDataSourceSettings)
        self.sheet_select_box.setObjectName(u"sheet_select_box")
        self.horizontalLayout_3 = QHBoxLayout(self.sheet_select_box)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_7 = QLabel(self.sheet_select_box)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.label_7)

        self.sheet_combo_box = QComboBox(self.sheet_select_box)
        self.sheet_combo_box.setObjectName(u"sheet_combo_box")

        self.horizontalLayout_3.addWidget(self.sheet_combo_box)


        self.verticalLayout.addWidget(self.sheet_select_box)

        self.label_4 = QLabel(FileDataSourceSettings)
        self.label_4.setObjectName(u"label_4")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setAlignment(Qt.AlignCenter)
        self.label_4.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_4)

        self.line_2 = QFrame(FileDataSourceSettings)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.label = QLabel(FileDataSourceSettings)
        self.label.setObjectName(u"label")
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.widget = QWidget(FileDataSourceSettings)
        self.widget.setObjectName(u"widget")
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.label_2)

        self.orientation_switch = Switch(self.widget)
        self.orientation_switch.setObjectName(u"orientation_switch")

        self.horizontalLayout.addWidget(self.orientation_switch)

        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)


        self.verticalLayout.addWidget(self.widget)

        self.line = QFrame(FileDataSourceSettings)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.label_6 = QLabel(FileDataSourceSettings)
        self.label_6.setObjectName(u"label_6")
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_6)

        self.widget_2 = QWidget(FileDataSourceSettings)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.horizontalLayout_2 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.first_header_label = QLabel(self.widget_2)
        self.first_header_label.setObjectName(u"first_header_label")
        self.first_header_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.first_header_label)

        self.header_switch = Switch(self.widget_2)
        self.header_switch.setObjectName(u"header_switch")

        self.horizontalLayout_2.addWidget(self.header_switch)

        self.label_5 = QLabel(self.widget_2)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_2.addWidget(self.label_5)


        self.verticalLayout.addWidget(self.widget_2)

        self.example_header_label = QLabel(FileDataSourceSettings)
        self.example_header_label.setObjectName(u"example_header_label")
        sizePolicy.setHeightForWidth(self.example_header_label.sizePolicy().hasHeightForWidth())
        self.example_header_label.setSizePolicy(sizePolicy)
        self.example_header_label.setWordWrap(True)

        self.verticalLayout.addWidget(self.example_header_label)


        self.retranslateUi(FileDataSourceSettings)

        QMetaObject.connectSlotsByName(FileDataSourceSettings)
    # setupUi

    def retranslateUi(self, FileDataSourceSettings):
        FileDataSourceSettings.setWindowTitle(QCoreApplication.translate("FileDataSourceSettings", u"FileDataSourceSettings", None))
        self.label_7.setText(QCoreApplication.translate("FileDataSourceSettings", u"Select the sheet:", None))
        self.label_4.setText(QCoreApplication.translate("FileDataSourceSettings", u"How the data is organized and what the headers are will affect how the data is represented and accessed by actions.", None))
        self.label.setText(QCoreApplication.translate("FileDataSourceSettings", u"Data is in:", None))
        self.label_2.setText(QCoreApplication.translate("FileDataSourceSettings", u"Columns", None))
        self.orientation_switch.setText(QCoreApplication.translate("FileDataSourceSettings", u"PushButton", None))
        self.label_3.setText(QCoreApplication.translate("FileDataSourceSettings", u"Rows", None))
        self.label_6.setText(QCoreApplication.translate("FileDataSourceSettings", u"Set Header:", None))
        self.first_header_label.setText(QCoreApplication.translate("FileDataSourceSettings", u"First row is header", None))
        self.header_switch.setText(QCoreApplication.translate("FileDataSourceSettings", u"PushButton", None))
        self.label_5.setText(QCoreApplication.translate("FileDataSourceSettings", u"Custom header", None))
        self.example_header_label.setText("")
    # retranslateUi

