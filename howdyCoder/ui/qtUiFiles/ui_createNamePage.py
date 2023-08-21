# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'createNamePage.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_CreateNamePage(object):
    def setupUi(self, CreateNamePage):
        if not CreateNamePage.objectName():
            CreateNamePage.setObjectName(u"CreateNamePage")
        CreateNamePage.resize(502, 358)
        self.verticalLayout = QVBoxLayout(CreateNamePage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.label = QLabel(CreateNamePage)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.widget = QWidget(CreateNamePage)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.nameEdit = QLineEdit(self.widget)
        self.nameEdit.setObjectName(u"nameEdit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(3)
        sizePolicy1.setHeightForWidth(self.nameEdit.sizePolicy().hasHeightForWidth())
        self.nameEdit.setSizePolicy(sizePolicy1)
        self.nameEdit.setMinimumSize(QSize(0, 0))
        font1 = QFont()
        font1.setPointSize(50)
        self.nameEdit.setFont(font1)
        self.nameEdit.setMaxLength(64)
        self.nameEdit.setFrame(False)
        self.nameEdit.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.nameEdit)


        self.verticalLayout.addWidget(self.widget)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(CreateNamePage)

        QMetaObject.connectSlotsByName(CreateNamePage)
    # setupUi

    def retranslateUi(self, CreateNamePage):
        CreateNamePage.setWindowTitle(QCoreApplication.translate("CreateNamePage", u"createNamePage", None))
        self.label.setText(QCoreApplication.translate("CreateNamePage", u"Enter a name for the algo for reference", None))
        self.nameEdit.setText("")
    # retranslateUi

