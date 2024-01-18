# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'createScriptPage.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QSizePolicy, QVBoxLayout,
    QWidget)

from ..funcSelector import FuncSelector

class Ui_CreateScriptPage(object):
    def setupUi(self, CreateScriptPage):
        if not CreateScriptPage.objectName():
            CreateScriptPage.setObjectName(u"CreateScriptPage")
        CreateScriptPage.resize(590, 482)
        self.verticalLayout = QVBoxLayout(CreateScriptPage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(CreateScriptPage)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.funcSelectorWidget = FuncSelector(CreateScriptPage)
        self.funcSelectorWidget.setObjectName(u"funcSelectorWidget")

        self.verticalLayout.addWidget(self.funcSelectorWidget)


        self.retranslateUi(CreateScriptPage)

        QMetaObject.connectSlotsByName(CreateScriptPage)
    # setupUi

    def retranslateUi(self, CreateScriptPage):
        CreateScriptPage.setWindowTitle(QCoreApplication.translate("CreateScriptPage", u"CreateScriptPage", None))
        self.label.setText(QCoreApplication.translate("CreateScriptPage", u"Input the script or select it from a library", None))
    # retranslateUi

