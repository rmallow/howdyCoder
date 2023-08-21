# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'newBlockWidget.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_NewBlockWidget(object):
    def setupUi(self, NewBlockWidget):
        if not NewBlockWidget.objectName():
            NewBlockWidget.setObjectName(u"NewBlockWidget")
        NewBlockWidget.resize(192, 202)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(NewBlockWidget.sizePolicy().hasHeightForWidth())
        NewBlockWidget.setSizePolicy(sizePolicy)
        NewBlockWidget.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setFamilies([u"Courier"])
        NewBlockWidget.setFont(font)
        NewBlockWidget.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(NewBlockWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(NewBlockWidget)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        font1 = QFont()
        font1.setFamilies([u".AppleSystemUIFont"])
        font1.setPointSize(15)
        self.label.setFont(font1)
        self.label.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.label)


        self.verticalLayout.addWidget(self.widget, 0, Qt.AlignHCenter|Qt.AlignBottom)

        self.widget_2 = QWidget(NewBlockWidget)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy2 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy2)
        self.horizontalLayout_2 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.createButton = QPushButton(self.widget_2)
        self.createButton.setObjectName(u"createButton")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.createButton.sizePolicy().hasHeightForWidth())
        self.createButton.setSizePolicy(sizePolicy3)
        self.createButton.setMinimumSize(QSize(102, 102))
        font2 = QFont()
        font2.setFamilies([u".AppleSystemUIFont"])
        font2.setPointSize(100)
        font2.setKerning(False)
        self.createButton.setFont(font2)
        self.createButton.setStyleSheet(u"QPushButton {\n"
"    color: white;\n"
"    border: 1px solid #87CEEB,;\n"
"    border-radius: 50px;\n"
"    border-style: outset;\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0 #87CEEB, stop: 1 	#A7C7E7\n"
"        );\n"
"	min-width: 100px;\n"
"min-height: 85px;\n"
"max-width:100px;\n"
"max-height:85px;\n"
"padding-bottom: 15px;\n"
"    }\n"
"\n"
"QPushButton:hover {\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0 #87CEEB, stop: 1 	#B6D0E2\n"
"        );\n"
"    }\n"
"\n"
"QPushButton:pressed {\n"
"    border-style: inset;\n"
"    background: qradialgradient(\n"
"        cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
"        radius: 1.35, stop: 0 #87CEEB, stop: 1 	#B6D0E2\n"
"        );\n"
"    }")

        self.horizontalLayout_2.addWidget(self.createButton)


        self.verticalLayout.addWidget(self.widget_2, 0, Qt.AlignHCenter)


        self.retranslateUi(NewBlockWidget)

        self.createButton.setDefault(False)


        QMetaObject.connectSlotsByName(NewBlockWidget)
    # setupUi

    def retranslateUi(self, NewBlockWidget):
        NewBlockWidget.setWindowTitle(QCoreApplication.translate("NewBlockWidget", u"NewBlockWidget", None))
        self.label.setText(QCoreApplication.translate("NewBlockWidget", u"Create New", None))
        self.createButton.setText(QCoreApplication.translate("NewBlockWidget", u"+", None))
#if QT_CONFIG(shortcut)
        self.createButton.setShortcut("")
#endif // QT_CONFIG(shortcut)
    # retranslateUi

