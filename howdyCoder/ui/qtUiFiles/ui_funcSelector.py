# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'funcSelector.ui'
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
from PySide6.QtWidgets import (QApplication, QSizePolicy, QTabWidget, QVBoxLayout,
    QWidget)

from ..funcSelectorCodePage import FuncSelectorCodePage
from ..funcSelectorLibPage import FuncSelectorLibPage

class Ui_FuncSelector(object):
    def setupUi(self, FuncSelector):
        if not FuncSelector.objectName():
            FuncSelector.setObjectName(u"FuncSelector")
        FuncSelector.resize(1013, 781)
        self.verticalLayout = QVBoxLayout(FuncSelector)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(FuncSelector)
        self.tabWidget.setObjectName(u"tabWidget")
        self.codePage = QWidget()
        self.codePage.setObjectName(u"codePage")
        self.verticalLayout_2 = QVBoxLayout(self.codePage)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, -1, 0, 0)
        self.codeWidget = FuncSelectorCodePage(self.codePage)
        self.codeWidget.setObjectName(u"codeWidget")

        self.verticalLayout_2.addWidget(self.codeWidget)

        self.tabWidget.addTab(self.codePage, "")
        self.libPage = QWidget()
        self.libPage.setObjectName(u"libPage")
        self.verticalLayout_3 = QVBoxLayout(self.libPage)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, -1, 0, 0)
        self.libWidget = FuncSelectorLibPage(self.libPage)
        self.libWidget.setObjectName(u"libWidget")

        self.verticalLayout_3.addWidget(self.libWidget)

        self.tabWidget.addTab(self.libPage, "")

        self.verticalLayout.addWidget(self.tabWidget)


        self.retranslateUi(FuncSelector)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(FuncSelector)
    # setupUi

    def retranslateUi(self, FuncSelector):
        FuncSelector.setWindowTitle(QCoreApplication.translate("FuncSelector", u"Function Selector", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.codePage), QCoreApplication.translate("FuncSelector", u"Code", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.libPage), QCoreApplication.translate("FuncSelector", u"Library", None))
    # retranslateUi

