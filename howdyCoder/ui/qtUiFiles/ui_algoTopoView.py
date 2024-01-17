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
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_AlgoTopoView(object):
    def setupUi(self, AlgoTopoView):
        if not AlgoTopoView.objectName():
            AlgoTopoView.setObjectName(u"AlgoTopoView")
        AlgoTopoView.resize(784, 583)
        self.verticalLayout = QVBoxLayout(AlgoTopoView)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget_3 = QWidget(AlgoTopoView)
        self.widget_3.setObjectName(u"widget_3")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.nameEdit = QLineEdit(self.widget_3)
        self.nameEdit.setObjectName(u"nameEdit")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nameEdit.sizePolicy().hasHeightForWidth())
        self.nameEdit.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.nameEdit)

        self.bottomText = QLabel(self.widget_3)
        self.bottomText.setObjectName(u"bottomText")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(5)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.bottomText.sizePolicy().hasHeightForWidth())
        self.bottomText.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setPointSize(15)
        self.bottomText.setFont(font)
        self.bottomText.setAlignment(Qt.AlignCenter)
        self.bottomText.setWordWrap(True)

        self.horizontalLayout_2.addWidget(self.bottomText)

        self.finishButton = QPushButton(self.widget_3)
        self.finishButton.setObjectName(u"finishButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.finishButton.sizePolicy().hasHeightForWidth())
        self.finishButton.setSizePolicy(sizePolicy2)

        self.horizontalLayout_2.addWidget(self.finishButton)


        self.verticalLayout.addWidget(self.widget_3)

        self.widget_2 = QWidget(AlgoTopoView)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(1)
        sizePolicy3.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy3)
        self.verticalLayout_2 = QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(self.widget_2)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, -1)
        self.addButton = QPushButton(self.widget)
        self.addButton.setObjectName(u"addButton")
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.addButton.sizePolicy().hasHeightForWidth())
        self.addButton.setSizePolicy(sizePolicy4)

        self.horizontalLayout.addWidget(self.addButton)

        self.horizontalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.removeButton = QPushButton(self.widget)
        self.removeButton.setObjectName(u"removeButton")
        sizePolicy4.setHeightForWidth(self.removeButton.sizePolicy().hasHeightForWidth())
        self.removeButton.setSizePolicy(sizePolicy4)

        self.horizontalLayout.addWidget(self.removeButton)

        self.horizontalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.editButton = QPushButton(self.widget)
        self.editButton.setObjectName(u"editButton")
        sizePolicy4.setHeightForWidth(self.editButton.sizePolicy().hasHeightForWidth())
        self.editButton.setSizePolicy(sizePolicy4)

        self.horizontalLayout.addWidget(self.editButton)

        self.horizontalSpacer = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.copyButton = QPushButton(self.widget)
        self.copyButton.setObjectName(u"copyButton")

        self.horizontalLayout.addWidget(self.copyButton)


        self.verticalLayout_2.addWidget(self.widget)


        self.verticalLayout.addWidget(self.widget_2)

        self.graphicsView = QGraphicsView(AlgoTopoView)
        self.graphicsView.setObjectName(u"graphicsView")
        sizePolicy5 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(10)
        sizePolicy5.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy5)
        self.graphicsView.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout.addWidget(self.graphicsView)


        self.retranslateUi(AlgoTopoView)

        QMetaObject.connectSlotsByName(AlgoTopoView)
    # setupUi

    def retranslateUi(self, AlgoTopoView):
        AlgoTopoView.setWindowTitle(QCoreApplication.translate("AlgoTopoView", u"AlgoTopoView", None))
        self.nameEdit.setText("")
        self.bottomText.setText(QCoreApplication.translate("AlgoTopoView", u"Use the tools below, or right click an item for editing. Click Finish when you are done.", None))
        self.finishButton.setText(QCoreApplication.translate("AlgoTopoView", u"Finish", None))
        self.addButton.setText(QCoreApplication.translate("AlgoTopoView", u"Add", None))
        self.removeButton.setText(QCoreApplication.translate("AlgoTopoView", u"Remove", None))
        self.editButton.setText(QCoreApplication.translate("AlgoTopoView", u"Edit", None))
        self.copyButton.setText(QCoreApplication.translate("AlgoTopoView", u"Copy", None))
    # retranslateUi

