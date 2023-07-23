# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'outputSelectSettings.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QStackedWidget,
    QVBoxLayout, QWidget)

class Ui_OutputSelectSettings(object):
    def setupUi(self, OutputSelectSettings):
        if not OutputSelectSettings.objectName():
            OutputSelectSettings.setObjectName(u"OutputSelectSettings")
        OutputSelectSettings.resize(434, 279)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(OutputSelectSettings.sizePolicy().hasHeightForWidth())
        OutputSelectSettings.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(OutputSelectSettings)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.mainLabel = QLabel(OutputSelectSettings)
        self.mainLabel.setObjectName(u"mainLabel")
        self.mainLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.mainLabel)

        self.periodLayout = QHBoxLayout()
        self.periodLayout.setObjectName(u"periodLayout")
        self.periodLabel = QLabel(OutputSelectSettings)
        self.periodLabel.setObjectName(u"periodLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.periodLabel.sizePolicy().hasHeightForWidth())
        self.periodLabel.setSizePolicy(sizePolicy1)

        self.periodLayout.addWidget(self.periodLabel)

        self.periodSpinBox = QSpinBox(OutputSelectSettings)
        self.periodSpinBox.setObjectName(u"periodSpinBox")
        self.periodSpinBox.setMaximum(9999)
        self.periodSpinBox.setValue(10)

        self.periodLayout.addWidget(self.periodSpinBox)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.periodLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.periodLayout)

        self.backtrackLayout = QHBoxLayout()
        self.backtrackLayout.setObjectName(u"backtrackLayout")
        self.backtrackLabel = QLabel(OutputSelectSettings)
        self.backtrackLabel.setObjectName(u"backtrackLabel")

        self.backtrackLayout.addWidget(self.backtrackLabel)

        self.backtrackSpinBox = QSpinBox(OutputSelectSettings)
        self.backtrackSpinBox.setObjectName(u"backtrackSpinBox")
        self.backtrackSpinBox.setMinimum(-1)
        self.backtrackSpinBox.setMaximum(1000)

        self.backtrackLayout.addWidget(self.backtrackSpinBox)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.backtrackLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.backtrackLayout)

        self.typeSpecificStackedWidget = QStackedWidget(OutputSelectSettings)
        self.typeSpecificStackedWidget.setObjectName(u"typeSpecificStackedWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.typeSpecificStackedWidget.sizePolicy().hasHeightForWidth())
        self.typeSpecificStackedWidget.setSizePolicy(sizePolicy2)
        self.typeSpecificStackedWidgetPage1 = QWidget()
        self.typeSpecificStackedWidgetPage1.setObjectName(u"typeSpecificStackedWidgetPage1")
        self.verticalLayout_3 = QVBoxLayout(self.typeSpecificStackedWidgetPage1)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.typeSpecificStackedWidget.addWidget(self.typeSpecificStackedWidgetPage1)

        self.verticalLayout.addWidget(self.typeSpecificStackedWidget)

        self.errorLabel = QLabel(OutputSelectSettings)
        self.errorLabel.setObjectName(u"errorLabel")
        self.errorLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.errorLabel)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.acceptButton = QPushButton(OutputSelectSettings)
        self.acceptButton.setObjectName(u"acceptButton")
        sizePolicy3 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.acceptButton.sizePolicy().hasHeightForWidth())
        self.acceptButton.setSizePolicy(sizePolicy3)

        self.horizontalLayout.addWidget(self.acceptButton)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(OutputSelectSettings)

        QMetaObject.connectSlotsByName(OutputSelectSettings)
    # setupUi

    def retranslateUi(self, OutputSelectSettings):
        OutputSelectSettings.setWindowTitle(QCoreApplication.translate("OutputSelectSettings", u"outputSelectSettings", None))
        self.mainLabel.setText(QCoreApplication.translate("OutputSelectSettings", u"Settings", None))
        self.periodLabel.setText(QCoreApplication.translate("OutputSelectSettings", u"Period", None))
        self.backtrackLabel.setText(QCoreApplication.translate("OutputSelectSettings", u"Backtrack", None))
        self.errorLabel.setText("")
        self.acceptButton.setText(QCoreApplication.translate("OutputSelectSettings", u"Accept", None))
    # retranslateUi

