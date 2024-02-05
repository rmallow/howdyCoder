# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'globalParameterPage.ui'
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
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QFrame, QScrollArea,
    QSizePolicy, QVBoxLayout, QWidget)

from ..globalParameterPageWidget import GlobalParameterPageWidget

class Ui_GlobalParameterPage(object):
    def setupUi(self, GlobalParameterPage):
        if not GlobalParameterPage.objectName():
            GlobalParameterPage.setObjectName(u"GlobalParameterPage")
        GlobalParameterPage.resize(885, 648)
        self.verticalLayout = QVBoxLayout(GlobalParameterPage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea = QScrollArea(GlobalParameterPage)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShadow(QFrame.Sunken)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(Qt.AlignCenter)
        self.globalParameterPageWidget = GlobalParameterPageWidget()
        self.globalParameterPageWidget.setObjectName(u"globalParameterPageWidget")
        self.globalParameterPageWidget.setGeometry(QRect(0, 0, 859, 622))
        self.scrollArea.setWidget(self.globalParameterPageWidget)

        self.verticalLayout.addWidget(self.scrollArea)


        self.retranslateUi(GlobalParameterPage)

        QMetaObject.connectSlotsByName(GlobalParameterPage)
    # setupUi

    def retranslateUi(self, GlobalParameterPage):
        GlobalParameterPage.setWindowTitle(QCoreApplication.translate("GlobalParameterPage", u"Global Parameter Page", None))
    # retranslateUi

