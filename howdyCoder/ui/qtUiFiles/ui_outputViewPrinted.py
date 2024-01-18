# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'outputViewPrinted.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QListView, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_OutputViewPrinted(object):
    def setupUi(self, OutputViewPrinted):
        if not OutputViewPrinted.objectName():
            OutputViewPrinted.setObjectName(u"OutputViewPrinted")
        OutputViewPrinted.resize(716, 414)
        self.verticalLayout = QVBoxLayout(OutputViewPrinted)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.list_view = QListView(OutputViewPrinted)
        self.list_view.setObjectName(u"list_view")
        self.list_view.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.verticalLayout.addWidget(self.list_view)


        self.retranslateUi(OutputViewPrinted)

        QMetaObject.connectSlotsByName(OutputViewPrinted)
    # setupUi

    def retranslateUi(self, OutputViewPrinted):
        OutputViewPrinted.setWindowTitle(QCoreApplication.translate("OutputViewPrinted", u"OutputViewPrinted", None))
    # retranslateUi

