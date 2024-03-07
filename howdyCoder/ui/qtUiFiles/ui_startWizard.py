# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'startWizard.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QSpacerItem, QStackedWidget, QVBoxLayout,
    QWidget)

from ..fileCheckWidget import FileCheckWidget
from ..modInstallWidget import ModInstallWidget
from ..parameterCheckWidget import ParameterCheckWidget

class Ui_StartWizard(object):
    def setupUi(self, StartWizard):
        if not StartWizard.objectName():
            StartWizard.setObjectName(u"StartWizard")
        StartWizard.resize(998, 584)
        self.verticalLayout = QVBoxLayout(StartWizard)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(StartWizard)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.page_status_list_widget = QListWidget(self.widget)
        self.page_status_list_widget.setObjectName(u"page_status_list_widget")
        self.page_status_list_widget.setMaximumSize(QSize(150, 16777215))
        font = QFont()
        font.setPointSize(15)
        self.page_status_list_widget.setFont(font)
        self.page_status_list_widget.setFrameShape(QFrame.NoFrame)
        self.page_status_list_widget.setFrameShadow(QFrame.Plain)
        self.page_status_list_widget.setLineWidth(0)
        self.page_status_list_widget.setMidLineWidth(0)
        self.page_status_list_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.page_status_list_widget.setWordWrap(True)

        self.horizontalLayout_2.addWidget(self.page_status_list_widget)

        self.stacked_widget = QStackedWidget(self.widget)
        self.stacked_widget.setObjectName(u"stacked_widget")
        self.module_install_widget = ModInstallWidget()
        self.module_install_widget.setObjectName(u"module_install_widget")
        self.stacked_widget.addWidget(self.module_install_widget)
        self.file_check_widget = FileCheckWidget()
        self.file_check_widget.setObjectName(u"file_check_widget")
        self.stacked_widget.addWidget(self.file_check_widget)
        self.parameter_check_widget = ParameterCheckWidget()
        self.parameter_check_widget.setObjectName(u"parameter_check_widget")
        self.stacked_widget.addWidget(self.parameter_check_widget)
        self.launch_widget = QWidget()
        self.launch_widget.setObjectName(u"launch_widget")
        self.horizontalLayout_3 = QHBoxLayout(self.launch_widget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.launch_label = QLabel(self.launch_widget)
        self.launch_label.setObjectName(u"launch_label")
        font1 = QFont()
        font1.setPointSize(40)
        self.launch_label.setFont(font1)
        self.launch_label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.launch_label)

        self.stacked_widget.addWidget(self.launch_widget)
        self.load_file_widget = QWidget()
        self.load_file_widget.setObjectName(u"load_file_widget")
        self.horizontalLayout_4 = QHBoxLayout(self.load_file_widget)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.load_file_label = QLabel(self.load_file_widget)
        self.load_file_label.setObjectName(u"load_file_label")
        self.load_file_label.setFont(font1)
        self.load_file_label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.load_file_label)

        self.stacked_widget.addWidget(self.load_file_widget)

        self.horizontalLayout_2.addWidget(self.stacked_widget)


        self.verticalLayout.addWidget(self.widget)

        self.widget_2 = QWidget(StartWizard)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout = QHBoxLayout(self.widget_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(833, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.ok_button = QPushButton(self.widget_2)
        self.ok_button.setObjectName(u"ok_button")
        self.ok_button.setMinimumSize(QSize(100, 0))

        self.horizontalLayout.addWidget(self.ok_button)


        self.verticalLayout.addWidget(self.widget_2)


        self.retranslateUi(StartWizard)

        self.stacked_widget.setCurrentIndex(4)


        QMetaObject.connectSlotsByName(StartWizard)
    # setupUi

    def retranslateUi(self, StartWizard):
        StartWizard.setWindowTitle(QCoreApplication.translate("StartWizard", u"Start Wizard", None))
        self.launch_label.setText(QCoreApplication.translate("StartWizard", u"<html><head/><body><p>All checks passed.</p><p>Launching Program...</p></body></html>", None))
        self.load_file_label.setText(QCoreApplication.translate("StartWizard", u"Loading Files...", None))
        self.ok_button.setText(QCoreApplication.translate("StartWizard", u"Override", None))
    # retranslateUi

