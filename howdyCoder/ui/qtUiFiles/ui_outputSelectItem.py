# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'outputSelectItem.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_OutputSelectItem(object):
    def setupUi(self, OutputSelectItem):
        if not OutputSelectItem.objectName():
            OutputSelectItem.setObjectName(u"OutputSelectItem")
        OutputSelectItem.resize(432, 99)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(OutputSelectItem.sizePolicy().hasHeightForWidth())
        OutputSelectItem.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(OutputSelectItem)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(OutputSelectItem)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.mainHLayout = QHBoxLayout()
        self.mainHLayout.setObjectName(u"mainHLayout")
        self.blockWidget = QWidget(OutputSelectItem)
        self.blockWidget.setObjectName(u"blockWidget")
        self.blockVLayout = QVBoxLayout(self.blockWidget)
        self.blockVLayout.setSpacing(0)
        self.blockVLayout.setObjectName(u"blockVLayout")
        self.blockLabel = QLabel(self.blockWidget)
        self.blockLabel.setObjectName(u"blockLabel")
        self.blockLabel.setAlignment(Qt.AlignCenter)

        self.blockVLayout.addWidget(self.blockLabel)

        self.blockComboBox = QComboBox(self.blockWidget)
        self.blockComboBox.setObjectName(u"blockComboBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.blockComboBox.sizePolicy().hasHeightForWidth())
        self.blockComboBox.setSizePolicy(sizePolicy1)

        self.blockVLayout.addWidget(self.blockComboBox)


        self.mainHLayout.addWidget(self.blockWidget)

        self.handlerBox = QWidget(OutputSelectItem)
        self.handlerBox.setObjectName(u"handlerBox")
        self.handlerVLayout = QVBoxLayout(self.handlerBox)
        self.handlerVLayout.setSpacing(0)
        self.handlerVLayout.setObjectName(u"handlerVLayout")
        self.handlerLabel = QLabel(self.handlerBox)
        self.handlerLabel.setObjectName(u"handlerLabel")
        self.handlerLabel.setAlignment(Qt.AlignCenter)

        self.handlerVLayout.addWidget(self.handlerLabel)

        self.handlerComboBox = QComboBox(self.handlerBox)
        self.handlerComboBox.setObjectName(u"handlerComboBox")
        sizePolicy1.setHeightForWidth(self.handlerComboBox.sizePolicy().hasHeightForWidth())
        self.handlerComboBox.setSizePolicy(sizePolicy1)

        self.handlerVLayout.addWidget(self.handlerComboBox)


        self.mainHLayout.addWidget(self.handlerBox)


        self.verticalLayout.addLayout(self.mainHLayout)


        self.retranslateUi(OutputSelectItem)

        QMetaObject.connectSlotsByName(OutputSelectItem)
    # setupUi

    def retranslateUi(self, OutputSelectItem):
        OutputSelectItem.setWindowTitle(QCoreApplication.translate("OutputSelectItem", u"outputSelectItem", None))
        self.label.setText(QCoreApplication.translate("OutputSelectItem", u"Select an Item", None))
        self.blockLabel.setText(QCoreApplication.translate("OutputSelectItem", u"Algos", None))
        self.handlerLabel.setText(QCoreApplication.translate("OutputSelectItem", u"Handlers", None))
    # retranslateUi

