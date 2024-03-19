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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialogButtonBox, QFrame,
    QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_CreatorTypeSelector(object):
    def setupUi(self, CreatorTypeSelector):
        if not CreatorTypeSelector.objectName():
            CreatorTypeSelector.setObjectName(u"CreatorTypeSelector")
        CreatorTypeSelector.resize(759, 555)
        self.horizontalLayout_2 = QHBoxLayout(CreatorTypeSelector)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.widget_4 = QWidget(CreatorTypeSelector)
        self.widget_4.setObjectName(u"widget_4")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.widget_4)

        self.widget_2 = QWidget(CreatorTypeSelector)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(5)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy1)
        self.verticalLayout_2 = QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.widget_7 = QWidget(self.widget_2)
        self.widget_7.setObjectName(u"widget_7")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.widget_7.sizePolicy().hasHeightForWidth())
        self.widget_7.setSizePolicy(sizePolicy2)

        self.verticalLayout_2.addWidget(self.widget_7)

        self.widget_3 = QWidget(self.widget_2)
        self.widget_3.setObjectName(u"widget_3")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(5)
        sizePolicy3.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy3)
        self.verticalLayout = QVBoxLayout(self.widget_3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.widget_3)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.widget = QWidget(self.widget_3)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.program_type_view = QListWidget(self.widget)
        self.program_type_view.setObjectName(u"program_type_view")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(1)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.program_type_view.sizePolicy().hasHeightForWidth())
        self.program_type_view.setSizePolicy(sizePolicy4)
        font = QFont()
        font.setPointSize(30)
        self.program_type_view.setFont(font)

        self.horizontalLayout.addWidget(self.program_type_view)

        self.program_type_description = QLabel(self.widget)
        self.program_type_description.setObjectName(u"program_type_description")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        sizePolicy5.setHorizontalStretch(2)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.program_type_description.sizePolicy().hasHeightForWidth())
        self.program_type_description.setSizePolicy(sizePolicy5)
        self.program_type_description.setMaximumSize(QSize(16777215, 16777212))
        font1 = QFont()
        font1.setPointSize(16)
        self.program_type_description.setFont(font1)
        self.program_type_description.setStyleSheet(u"")
        self.program_type_description.setFrameShape(QFrame.NoFrame)
        self.program_type_description.setScaledContents(False)
        self.program_type_description.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.program_type_description.setWordWrap(True)

        self.horizontalLayout.addWidget(self.program_type_description)


        self.verticalLayout.addWidget(self.widget)

        self.button_box = QDialogButtonBox(self.widget_3)
        self.button_box.setObjectName(u"button_box")
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.button_box)


        self.verticalLayout_2.addWidget(self.widget_3)

        self.widget_6 = QWidget(self.widget_2)
        self.widget_6.setObjectName(u"widget_6")
        sizePolicy2.setHeightForWidth(self.widget_6.sizePolicy().hasHeightForWidth())
        self.widget_6.setSizePolicy(sizePolicy2)

        self.verticalLayout_2.addWidget(self.widget_6)


        self.horizontalLayout_2.addWidget(self.widget_2)

        self.widget_5 = QWidget(CreatorTypeSelector)
        self.widget_5.setObjectName(u"widget_5")
        sizePolicy.setHeightForWidth(self.widget_5.sizePolicy().hasHeightForWidth())
        self.widget_5.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.widget_5)


        self.retranslateUi(CreatorTypeSelector)

        QMetaObject.connectSlotsByName(CreatorTypeSelector)
    # setupUi

    def retranslateUi(self, CreatorTypeSelector):
        CreatorTypeSelector.setWindowTitle(QCoreApplication.translate("CreatorTypeSelector", u"Creator Type Selector", None))
        self.label.setText(QCoreApplication.translate("CreatorTypeSelector", u"Select the type of program to load the creator. Hit Ok when done.", None))
        self.program_type_description.setText(QCoreApplication.translate("CreatorTypeSelector", u"Select the type of program to create.", None))
    # retranslateUi

