# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'createOptionsPage.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
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
    QLineEdit, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_CreateOptionsPage(object):
    def setupUi(self, CreateOptionsPage):
        if not CreateOptionsPage.objectName():
            CreateOptionsPage.setObjectName(u"CreateOptionsPage")
        CreateOptionsPage.resize(400, 300)
        CreateOptionsPage.setLayoutDirection(Qt.LeftToRight)
        self.horizontalLayout = QHBoxLayout(CreateOptionsPage)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.widget = QWidget(CreateOptionsPage)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.nameLabel = QLabel(self.widget_2)
        self.nameLabel.setObjectName(u"nameLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nameLabel.sizePolicy().hasHeightForWidth())
        self.nameLabel.setSizePolicy(sizePolicy)
        self.nameLabel.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.nameLabel)

        self.nameEdit = QLineEdit(self.widget_2)
        self.nameEdit.setObjectName(u"nameEdit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.nameEdit.sizePolicy().hasHeightForWidth())
        self.nameEdit.setSizePolicy(sizePolicy1)
        self.nameEdit.setAutoFillBackground(False)
        self.nameEdit.setStyleSheet(u"")
        self.nameEdit.setFrame(False)
        self.nameEdit.setEchoMode(QLineEdit.Normal)
        self.nameEdit.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.nameEdit)


        self.verticalLayout_2.addWidget(self.widget_2)

        self.widget_3 = QWidget(self.widget)
        self.widget_3.setObjectName(u"widget_3")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.csvCheckBox = QCheckBox(self.widget_3)
        self.csvCheckBox.setObjectName(u"csvCheckBox")

        self.horizontalLayout_3.addWidget(self.csvCheckBox)


        self.verticalLayout_2.addWidget(self.widget_3)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)


        self.horizontalLayout.addWidget(self.widget)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.retranslateUi(CreateOptionsPage)

        QMetaObject.connectSlotsByName(CreateOptionsPage)
    # setupUi

    def retranslateUi(self, CreateOptionsPage):
        CreateOptionsPage.setWindowTitle(QCoreApplication.translate("CreateOptionsPage", u"createOptionsPage", None))
        self.nameLabel.setText(QCoreApplication.translate("CreateOptionsPage", u"Name:", None))
        self.csvCheckBox.setText(QCoreApplication.translate("CreateOptionsPage", u"Export to CSV", None))
    # retranslateUi

