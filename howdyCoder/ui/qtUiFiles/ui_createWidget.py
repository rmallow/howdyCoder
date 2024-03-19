# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'createWidget.ui'
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
from PySide6.QtWidgets import (QApplication, QSizePolicy, QStackedWidget, QVBoxLayout,
    QWidget)

from ..create.algoTopoView import AlgoTopoView
from ..create.createWizard import CreateWizard
from ..create.creatorTypeWidget import CreatorTypeWidget

class Ui_CreateWidget(object):
    def setupUi(self, CreateWidget):
        if not CreateWidget.objectName():
            CreateWidget.setObjectName(u"CreateWidget")
        CreateWidget.resize(763, 745)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CreateWidget.sizePolicy().hasHeightForWidth())
        CreateWidget.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(CreateWidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget = QStackedWidget(CreateWidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.createWizard = CreateWizard()
        self.createWizard.setObjectName(u"createWizard")
        self.stackedWidget.addWidget(self.createWizard)
        self.creatorTypeWidget = CreatorTypeWidget()
        self.creatorTypeWidget.setObjectName(u"creatorTypeWidget")
        self.stackedWidget.addWidget(self.creatorTypeWidget)
        self.algoTopoView = AlgoTopoView()
        self.algoTopoView.setObjectName(u"algoTopoView")
        self.stackedWidget.addWidget(self.algoTopoView)

        self.verticalLayout.addWidget(self.stackedWidget)


        self.retranslateUi(CreateWidget)

        QMetaObject.connectSlotsByName(CreateWidget)
    # setupUi

    def retranslateUi(self, CreateWidget):
        CreateWidget.setWindowTitle(QCoreApplication.translate("CreateWidget", u"createWidget", None))
    # retranslateUi

