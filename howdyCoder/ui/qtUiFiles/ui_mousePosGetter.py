# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mousePosGetter.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QLabel,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_MousePosGetter(object):
    def setupUi(self, MousePosGetter):
        if not MousePosGetter.objectName():
            MousePosGetter.setObjectName(u"MousePosGetter")
        MousePosGetter.resize(435, 117)
        self.verticalLayout = QVBoxLayout(MousePosGetter)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(MousePosGetter)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.active_check = QCheckBox(self.widget)
        self.active_check.setObjectName(u"active_check")

        self.horizontalLayout.addWidget(self.active_check)

        self.pos_label = QLabel(self.widget)
        self.pos_label.setObjectName(u"pos_label")

        self.horizontalLayout.addWidget(self.pos_label)


        self.verticalLayout.addWidget(self.widget)

        self.description_label = QLabel(MousePosGetter)
        self.description_label.setObjectName(u"description_label")
        self.description_label.setAlignment(Qt.AlignCenter)
        self.description_label.setWordWrap(True)

        self.verticalLayout.addWidget(self.description_label)


        self.retranslateUi(MousePosGetter)

        QMetaObject.connectSlotsByName(MousePosGetter)
    # setupUi

    def retranslateUi(self, MousePosGetter):
        MousePosGetter.setWindowTitle(QCoreApplication.translate("MousePosGetter", u"Mouse Pos Getter", None))
        self.active_check.setText(QCoreApplication.translate("MousePosGetter", u"Active", None))
        self.pos_label.setText("")
        self.description_label.setText(QCoreApplication.translate("MousePosGetter", u"Hit Space while active is checked to capture and send mouse position as coordinate point (x, y) (Experimental Feature)", None))
    # retranslateUi

