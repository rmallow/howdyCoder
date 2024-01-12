# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'algoTopoView.ui'
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
from PySide6.QtWidgets import (QApplication, QGraphicsView, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_AlgoTopoView(object):
    def setupUi(self, AlgoTopoView):
        if not AlgoTopoView.objectName():
            AlgoTopoView.setObjectName(u"AlgoTopoView")
        AlgoTopoView.resize(529, 416)
        self.verticalLayout = QVBoxLayout(AlgoTopoView)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget_2 = QWidget(AlgoTopoView)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.bottomText = QLabel(self.widget_2)
        self.bottomText.setObjectName(u"bottomText")
        font = QFont()
        font.setPointSize(15)
        self.bottomText.setFont(font)
        self.bottomText.setAlignment(Qt.AlignCenter)
        self.bottomText.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.bottomText)

        self.widget = QWidget(self.widget_2)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, -1)
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

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.editButton = QPushButton(self.widget)
        self.editButton.setObjectName(u"editButton")
        sizePolicy1.setHeightForWidth(self.editButton.sizePolicy().hasHeightForWidth())
        self.editButton.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.editButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.finishButton = QPushButton(self.widget)
        self.finishButton.setObjectName(u"finishButton")
        sizePolicy1.setHeightForWidth(self.finishButton.sizePolicy().hasHeightForWidth())
        self.finishButton.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.finishButton)


        self.verticalLayout_2.addWidget(self.widget)


        self.verticalLayout.addWidget(self.widget_2)

        self.graphicsView = QGraphicsView(AlgoTopoView)
        self.graphicsView.setObjectName(u"graphicsView")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(10)
        sizePolicy2.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy2)
        self.graphicsView.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout.addWidget(self.graphicsView)


        self.retranslateUi(AlgoTopoView)

        QMetaObject.connectSlotsByName(AlgoTopoView)
    # setupUi

    def retranslateUi(self, AlgoTopoView):
        AlgoTopoView.setWindowTitle(QCoreApplication.translate("AlgoTopoView", u"AlgoTopoView", None))
        self.bottomText.setText(QCoreApplication.translate("AlgoTopoView", u"Click add to start adding a new item  or select a item and hit remove to delete.", None))
        self.addButton.setText(QCoreApplication.translate("AlgoTopoView", u"Add", None))
        self.removeButton.setText(QCoreApplication.translate("AlgoTopoView", u"Remove", None))
        self.editButton.setText(QCoreApplication.translate("AlgoTopoView", u"Edit", None))
        self.finishButton.setText(QCoreApplication.translate("AlgoTopoView", u"Finish", None))
    # retranslateUi

