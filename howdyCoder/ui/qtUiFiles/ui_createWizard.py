# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'createWizard.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QPushButton, QScrollArea,
    QSizePolicy, QVBoxLayout, QWidget)

from ..create.progressSteps import ProgressSteps

class Ui_CreateWizard(object):
    def setupUi(self, CreateWizard):
        if not CreateWizard.objectName():
            CreateWizard.setObjectName(u"CreateWizard")
        CreateWizard.resize(763, 745)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CreateWizard.sizePolicy().hasHeightForWidth())
        CreateWizard.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(CreateWizard)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.progress_steps_box = QWidget(CreateWizard)
        self.progress_steps_box.setObjectName(u"progress_steps_box")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.progress_steps_box.sizePolicy().hasHeightForWidth())
        self.progress_steps_box.setSizePolicy(sizePolicy1)
        self.progress_steps_box.setMinimumSize(QSize(0, 0))
        self.progress_steps_box.setMaximumSize(QSize(16777215, 16777215))
        self.progress_steps_box.setLayoutDirection(Qt.LeftToRight)
        self.progress_steps_box.setStyleSheet(u"")
        self.horizontalLayout = QHBoxLayout(self.progress_steps_box)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.progressSteps = ProgressSteps(self.progress_steps_box)
        self.progressSteps.setObjectName(u"progressSteps")
        sizePolicy2 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.progressSteps.sizePolicy().hasHeightForWidth())
        self.progressSteps.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.progressSteps)


        self.verticalLayout.addWidget(self.progress_steps_box)

        self.widget_3 = QWidget(CreateWizard)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setMinimumSize(QSize(0, 0))
        self.widget_3.setLayoutDirection(Qt.LeftToRight)
        self.horizontalLayout_3 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.exitButton = QPushButton(self.widget_3)
        self.exitButton.setObjectName(u"exitButton")

        self.horizontalLayout_3.addWidget(self.exitButton)


        self.verticalLayout.addWidget(self.widget_3, 0, Qt.AlignRight)

        self.scrollArea = QScrollArea(CreateWizard)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 761, 655))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.createWidgetBox = QWidget(self.scrollAreaWidgetContents)
        self.createWidgetBox.setObjectName(u"createWidgetBox")
        sizePolicy3 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(10)
        sizePolicy3.setHeightForWidth(self.createWidgetBox.sizePolicy().hasHeightForWidth())
        self.createWidgetBox.setSizePolicy(sizePolicy3)
        self.createWidgetBox.setStyleSheet(u"")

        self.verticalLayout_2.addWidget(self.createWidgetBox)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)

        self.buttonBox = QWidget(CreateWizard)
        self.buttonBox.setObjectName(u"buttonBox")
        self.horizontalLayout_2 = QHBoxLayout(self.buttonBox)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 12, -1, 12)
        self.backButton = QPushButton(self.buttonBox)
        self.backButton.setObjectName(u"backButton")
        sizePolicy4 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.backButton.sizePolicy().hasHeightForWidth())
        self.backButton.setSizePolicy(sizePolicy4)

        self.horizontalLayout_2.addWidget(self.backButton)

        self.nextButton = QPushButton(self.buttonBox)
        self.nextButton.setObjectName(u"nextButton")
        sizePolicy4.setHeightForWidth(self.nextButton.sizePolicy().hasHeightForWidth())
        self.nextButton.setSizePolicy(sizePolicy4)

        self.horizontalLayout_2.addWidget(self.nextButton)


        self.verticalLayout.addWidget(self.buttonBox, 0, Qt.AlignHCenter)


        self.retranslateUi(CreateWizard)

        QMetaObject.connectSlotsByName(CreateWizard)
    # setupUi

    def retranslateUi(self, CreateWizard):
        CreateWizard.setWindowTitle(QCoreApplication.translate("CreateWizard", u"createWizard", None))
        self.exitButton.setText(QCoreApplication.translate("CreateWizard", u"Exit Creator", None))
        self.scrollArea.setProperty("scrollBarSize", QCoreApplication.translate("CreateWizard", u"big", None))
        self.backButton.setText(QCoreApplication.translate("CreateWizard", u"Back", None))
        self.nextButton.setText(QCoreApplication.translate("CreateWizard", u"Next", None))
    # retranslateUi

