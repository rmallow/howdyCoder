# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'controlWidget.ui'
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
from PySide6.QtWidgets import (QApplication, QSizePolicy, QVBoxLayout, QWidget)

class Ui_ControlWidget(object):
    def setupUi(self, ControlWidget):
        if not ControlWidget.objectName():
            ControlWidget.setObjectName(u"ControlWidget")
        ControlWidget.resize(582, 487)
        self.verticalLayout = QVBoxLayout(ControlWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.mainWidget = QWidget(ControlWidget)
        self.mainWidget.setObjectName(u"mainWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(5)
        sizePolicy.setHeightForWidth(self.mainWidget.sizePolicy().hasHeightForWidth())
        self.mainWidget.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.mainWidget)


        self.retranslateUi(ControlWidget)

        QMetaObject.connectSlotsByName(ControlWidget)
    # setupUi

    def retranslateUi(self, ControlWidget):
        ControlWidget.setWindowTitle(QCoreApplication.translate("ControlWidget", u"Control Widget", None))
    # retranslateUi

