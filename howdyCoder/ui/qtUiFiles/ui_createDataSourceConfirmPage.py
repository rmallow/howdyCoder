# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'createDataSourceConfirmPage.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QScrollArea, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_CreateDataSourceConfirmPage(object):
    def setupUi(self, CreateDataSourceConfirmPage):
        if not CreateDataSourceConfirmPage.objectName():
            CreateDataSourceConfirmPage.setObjectName(u"CreateDataSourceConfirmPage")
        CreateDataSourceConfirmPage.resize(540, 329)
        self.verticalLayout = QVBoxLayout(CreateDataSourceConfirmPage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.title_label = QLabel(CreateDataSourceConfirmPage)
        self.title_label.setObjectName(u"title_label")
        font = QFont()
        font.setPointSize(20)
        self.title_label.setFont(font)
        self.title_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.title_label)

        self.scrollArea = QScrollArea(CreateDataSourceConfirmPage)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(20)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(False)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 514, 243))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)

        self.confirm_label = QLabel(CreateDataSourceConfirmPage)
        self.confirm_label.setObjectName(u"confirm_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.confirm_label.sizePolicy().hasHeightForWidth())
        self.confirm_label.setSizePolicy(sizePolicy1)
        font1 = QFont()
        font1.setPointSize(15)
        self.confirm_label.setFont(font1)
        self.confirm_label.setAlignment(Qt.AlignCenter)
        self.confirm_label.setWordWrap(True)

        self.verticalLayout.addWidget(self.confirm_label)


        self.retranslateUi(CreateDataSourceConfirmPage)

        QMetaObject.connectSlotsByName(CreateDataSourceConfirmPage)
    # setupUi

    def retranslateUi(self, CreateDataSourceConfirmPage):
        CreateDataSourceConfirmPage.setWindowTitle(QCoreApplication.translate("CreateDataSourceConfirmPage", u"CreateDataSourceConfirmPage", None))
        self.title_label.setText(QCoreApplication.translate("CreateDataSourceConfirmPage", u"TextLabel", None))
        self.confirm_label.setText(QCoreApplication.translate("CreateDataSourceConfirmPage", u"Confirm your item before finishing. You can go back and modify.", None))
    # retranslateUi

