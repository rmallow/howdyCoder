# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'creatorTypeSelector.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_CreatorTypeSelector(object):
    def setupUi(self, CreatorTypeSelector):
        if not CreatorTypeSelector.objectName():
            CreatorTypeSelector.setObjectName(u"CreatorTypeSelector")
        CreatorTypeSelector.resize(545, 474)
        self.verticalLayout = QVBoxLayout(CreatorTypeSelector)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(CreatorTypeSelector)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.widget = QWidget(CreatorTypeSelector)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.program_type_view = QListWidget(self.widget)
        self.program_type_view.setObjectName(u"program_type_view")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.program_type_view.sizePolicy().hasHeightForWidth())
        self.program_type_view.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(30)
        self.program_type_view.setFont(font)

        self.horizontalLayout.addWidget(self.program_type_view)

        self.program_type_description = QLabel(self.widget)
        self.program_type_description.setObjectName(u"program_type_description")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(2)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.program_type_description.sizePolicy().hasHeightForWidth())
        self.program_type_description.setSizePolicy(sizePolicy1)
        font1 = QFont()
        font1.setPointSize(18)
        self.program_type_description.setFont(font1)
        self.program_type_description.setWordWrap(True)

        self.horizontalLayout.addWidget(self.program_type_description)


        self.verticalLayout.addWidget(self.widget)

        self.button_box = QDialogButtonBox(CreatorTypeSelector)
        self.button_box.setObjectName(u"button_box")
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.button_box)


        self.retranslateUi(CreatorTypeSelector)
        self.button_box.accepted.connect(CreatorTypeSelector.accept)
        self.button_box.rejected.connect(CreatorTypeSelector.reject)

        QMetaObject.connectSlotsByName(CreatorTypeSelector)
    # setupUi

    def retranslateUi(self, CreatorTypeSelector):
        CreatorTypeSelector.setWindowTitle(QCoreApplication.translate("CreatorTypeSelector", u"Creator Type Selector", None))
        self.label.setText(QCoreApplication.translate("CreatorTypeSelector", u"Select the type of program to load the creator. Hit Ok when done or hit cancel to return.", None))
        self.program_type_description.setText(QCoreApplication.translate("CreatorTypeSelector", u"Select the type of program to create.", None))
    # retranslateUi

