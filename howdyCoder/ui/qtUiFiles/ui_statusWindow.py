# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'statusWindow.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QHeaderView,
    QSizePolicy, QTreeView, QWidget)

class Ui_StatusWindow(object):
    def setupUi(self, StatusWindow):
        if not StatusWindow.objectName():
            StatusWindow.setObjectName(u"StatusWindow")
        StatusWindow.resize(400, 300)
        self.horizontalLayout = QHBoxLayout(StatusWindow)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.processView = QTreeView(StatusWindow)
        self.processView.setObjectName(u"processView")

        self.horizontalLayout.addWidget(self.processView)


        self.retranslateUi(StatusWindow)

        QMetaObject.connectSlotsByName(StatusWindow)
    # setupUi

    def retranslateUi(self, StatusWindow):
        StatusWindow.setWindowTitle(QCoreApplication.translate("StatusWindow", u"Status Window", None))
    # retranslateUi

