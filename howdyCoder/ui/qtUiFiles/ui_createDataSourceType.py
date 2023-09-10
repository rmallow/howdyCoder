# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'createDataSourceType.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHBoxLayout, QLabel,
    QLineEdit, QListView, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_CreateDataSourceType(object):
    def setupUi(self, CreateDataSourceType):
        if not CreateDataSourceType.objectName():
            CreateDataSourceType.setObjectName(u"CreateDataSourceType")
        CreateDataSourceType.resize(764, 488)
        self.verticalLayout = QVBoxLayout(CreateDataSourceType)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget_3 = QWidget(CreateDataSourceType)
        self.widget_3.setObjectName(u"widget_3")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.widget_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.widget_3)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label)

        self.widget = QWidget(self.widget_3)
        self.widget.setObjectName(u"widget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy1)
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.nameLabel = QLabel(self.widget)
        self.nameLabel.setObjectName(u"nameLabel")

        self.horizontalLayout.addWidget(self.nameLabel)

        self.nameEdit = QLineEdit(self.widget)
        self.nameEdit.setObjectName(u"nameEdit")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.nameEdit.sizePolicy().hasHeightForWidth())
        self.nameEdit.setSizePolicy(sizePolicy2)
        self.nameEdit.setMaximumSize(QSize(16777215, 300))
        font1 = QFont()
        font1.setPointSize(25)
        self.nameEdit.setFont(font1)

        self.horizontalLayout.addWidget(self.nameEdit)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addWidget(self.widget)


        self.verticalLayout.addWidget(self.widget_3)

        self.widget_2 = QWidget(CreateDataSourceType)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(3)
        sizePolicy3.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy3)
        self.horizontalLayout_2 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.widget_4 = QWidget(self.widget_2)
        self.widget_4.setObjectName(u"widget_4")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(2)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy4)
        self.verticalLayout_3 = QVBoxLayout(self.widget_4)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.typeLabel = QLabel(self.widget_4)
        self.typeLabel.setObjectName(u"typeLabel")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.typeLabel.sizePolicy().hasHeightForWidth())
        self.typeLabel.setSizePolicy(sizePolicy5)

        self.verticalLayout_3.addWidget(self.typeLabel)

        self.typeView = QListView(self.widget_4)
        self.typeView.setObjectName(u"typeView")
        font2 = QFont()
        font2.setPointSize(20)
        self.typeView.setFont(font2)
        self.typeView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.typeView.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.verticalLayout_3.addWidget(self.typeView)


        self.horizontalLayout_2.addWidget(self.widget_4)

        self.typeDescription = QLabel(self.widget_2)
        self.typeDescription.setObjectName(u"typeDescription")
        sizePolicy6 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(3)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.typeDescription.sizePolicy().hasHeightForWidth())
        self.typeDescription.setSizePolicy(sizePolicy6)
        self.typeDescription.setFont(font)
        self.typeDescription.setAlignment(Qt.AlignCenter)
        self.typeDescription.setWordWrap(True)

        self.horizontalLayout_2.addWidget(self.typeDescription)


        self.verticalLayout.addWidget(self.widget_2)


        self.retranslateUi(CreateDataSourceType)

        QMetaObject.connectSlotsByName(CreateDataSourceType)
    # setupUi

    def retranslateUi(self, CreateDataSourceType):
        CreateDataSourceType.setWindowTitle(QCoreApplication.translate("CreateDataSourceType", u"CreateDataSourceType", None))
        self.label.setText(QCoreApplication.translate("CreateDataSourceType", u"Enter a name and select a type based on desired functionality", None))
        self.nameLabel.setText(QCoreApplication.translate("CreateDataSourceType", u"Name", None))
        self.typeLabel.setText(QCoreApplication.translate("CreateDataSourceType", u"Data Source Type:", None))
        self.typeDescription.setText(QCoreApplication.translate("CreateDataSourceType", u"Select a type to the left to view its description", None))
    # retranslateUi

