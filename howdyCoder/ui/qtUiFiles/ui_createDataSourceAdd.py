# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'createDataSourceAdd.ui'
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
    QListView, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_CreateDataSourceAdd(object):
    def setupUi(self, CreateDataSourceAdd):
        if not CreateDataSourceAdd.objectName():
            CreateDataSourceAdd.setObjectName(u"CreateDataSourceAdd")
        CreateDataSourceAdd.resize(789, 577)
        self.verticalLayout = QVBoxLayout(CreateDataSourceAdd)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget_2 = QWidget(CreateDataSourceAdd)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.topText = QLabel(self.widget_2)
        self.topText.setObjectName(u"topText")
        font = QFont()
        font.setPointSize(15)
        self.topText.setFont(font)
        self.topText.setAlignment(Qt.AlignCenter)
        self.topText.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.topText)

        self.bottomText = QLabel(self.widget_2)
        self.bottomText.setObjectName(u"bottomText")
        self.bottomText.setFont(font)
        self.bottomText.setAlignment(Qt.AlignCenter)
        self.bottomText.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.bottomText)

        self.widget = QWidget(self.widget_2)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.addButton = QPushButton(self.widget)
        self.addButton.setObjectName(u"addButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.addButton.sizePolicy().hasHeightForWidth())
        self.addButton.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.addButton)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.removeButton = QPushButton(self.widget)
        self.removeButton.setObjectName(u"removeButton")
        sizePolicy1.setHeightForWidth(self.removeButton.sizePolicy().hasHeightForWidth())
        self.removeButton.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.removeButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.skipButton = QPushButton(self.widget)
        self.skipButton.setObjectName(u"skipButton")
        sizePolicy1.setHeightForWidth(self.skipButton.sizePolicy().hasHeightForWidth())
        self.skipButton.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.skipButton)


        self.verticalLayout_2.addWidget(self.widget)


        self.verticalLayout.addWidget(self.widget_2)

        self.dataSourcesView = QListView(CreateDataSourceAdd)
        self.dataSourcesView.setObjectName(u"dataSourcesView")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(2)
        sizePolicy2.setHeightForWidth(self.dataSourcesView.sizePolicy().hasHeightForWidth())
        self.dataSourcesView.setSizePolicy(sizePolicy2)
        font1 = QFont()
        font1.setPointSize(50)
        self.dataSourcesView.setFont(font1)
        self.dataSourcesView.setStyleSheet(u"")
        self.dataSourcesView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.dataSourcesView.setSelectionMode(QAbstractItemView.SingleSelection)

        self.verticalLayout.addWidget(self.dataSourcesView)


        self.retranslateUi(CreateDataSourceAdd)

        QMetaObject.connectSlotsByName(CreateDataSourceAdd)
    # setupUi

    def retranslateUi(self, CreateDataSourceAdd):
        CreateDataSourceAdd.setWindowTitle(QCoreApplication.translate("CreateDataSourceAdd", u"CreateDataSourceAdd", None))
        self.topText.setText(QCoreApplication.translate("CreateDataSourceAdd", u"The Data Source is the base of the algo,  it will be the input data whether from an API,  file or custom function is up to you.", None))
        self.bottomText.setText(QCoreApplication.translate("CreateDataSourceAdd", u"Click add to start adding a new item  or select a item and hit remove to delete.", None))
        self.addButton.setText(QCoreApplication.translate("CreateDataSourceAdd", u"Add", None))
        self.removeButton.setText(QCoreApplication.translate("CreateDataSourceAdd", u"Remove", None))
        self.skipButton.setText(QCoreApplication.translate("CreateDataSourceAdd", u"Skip", None))
    # retranslateUi

