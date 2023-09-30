# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'keySetWindow.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QSizePolicy,
    QVBoxLayout, QWidget)

from ..keySetWidget import KeySetWidget

class Ui_KeySetWindow(object):
    def setupUi(self, KeySetWindow):
        if not KeySetWindow.objectName():
            KeySetWindow.setObjectName(u"KeySetWindow")
        KeySetWindow.resize(430, 240)
        self.verticalLayout = QVBoxLayout(KeySetWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.key_choice_combo = QComboBox(KeySetWindow)
        self.key_choice_combo.setObjectName(u"key_choice_combo")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.key_choice_combo.sizePolicy().hasHeightForWidth())
        self.key_choice_combo.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.key_choice_combo)

        self.key_set_widget = KeySetWidget(KeySetWindow)
        self.key_set_widget.setObjectName(u"key_set_widget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(5)
        sizePolicy1.setHeightForWidth(self.key_set_widget.sizePolicy().hasHeightForWidth())
        self.key_set_widget.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.key_set_widget)


        self.retranslateUi(KeySetWindow)

        QMetaObject.connectSlotsByName(KeySetWindow)
    # setupUi

    def retranslateUi(self, KeySetWindow):
        KeySetWindow.setWindowTitle(QCoreApplication.translate("KeySetWindow", u"Key Set Window", None))
    # retranslateUi

