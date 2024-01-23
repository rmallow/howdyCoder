# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'outputSelectItem.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_OutputSelectItem(object):
    def setupUi(self, OutputSelectItem):
        if not OutputSelectItem.objectName():
            OutputSelectItem.setObjectName(u"OutputSelectItem")
        OutputSelectItem.resize(432, 118)
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

        self.widget = QWidget(OutputSelectItem)
        self.widget.setObjectName(u"widget")
        self.mainHLayout = QHBoxLayout(self.widget)
        self.mainHLayout.setObjectName(u"mainHLayout")
        self.blockWidget = QWidget(self.widget)
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
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.blockComboBox.sizePolicy().hasHeightForWidth())
        self.blockComboBox.setSizePolicy(sizePolicy1)
        self.blockComboBox.setMinimumSize(QSize(200, 0))
        self.blockComboBox.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)

        self.blockVLayout.addWidget(self.blockComboBox)


        self.mainHLayout.addWidget(self.blockWidget)


        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(OutputSelectItem)

        QMetaObject.connectSlotsByName(OutputSelectItem)
    # setupUi

    def retranslateUi(self, OutputSelectItem):
        OutputSelectItem.setWindowTitle(QCoreApplication.translate("OutputSelectItem", u"outputSelectItem", None))
        self.label.setText(QCoreApplication.translate("OutputSelectItem", u"Select an Item", None))
        self.blockLabel.setText(QCoreApplication.translate("OutputSelectItem", u"Algos", None))
    # retranslateUi

