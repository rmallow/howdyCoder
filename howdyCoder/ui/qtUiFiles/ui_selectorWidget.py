# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'selectorWidget.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QWidget)

from ..util.qtUtil import ExpandingLabelWidget

class Ui_SelectorWidget(object):
    def setupUi(self, SelectorWidget):
        if not SelectorWidget.objectName():
            SelectorWidget.setObjectName(u"SelectorWidget")
        SelectorWidget.resize(646, 209)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SelectorWidget.sizePolicy().hasHeightForWidth())
        SelectorWidget.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(SelectorWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.selectorButton = QPushButton(SelectorWidget)
        self.selectorButton.setObjectName(u"selectorButton")

        self.horizontalLayout.addWidget(self.selectorButton)

        self.selectionLabel = QLabel(SelectorWidget)
        self.selectionLabel.setObjectName(u"selectionLabel")

        self.horizontalLayout.addWidget(self.selectionLabel)

        self.extraDescriptionLabel = ExpandingLabelWidget(SelectorWidget)
        self.extraDescriptionLabel.setObjectName(u"extraDescriptionLabel")

        self.horizontalLayout.addWidget(self.extraDescriptionLabel)


        self.retranslateUi(SelectorWidget)

        QMetaObject.connectSlotsByName(SelectorWidget)
    # setupUi

    def retranslateUi(self, SelectorWidget):
        SelectorWidget.setWindowTitle(QCoreApplication.translate("SelectorWidget", u"selectorWidget", None))
        self.selectorButton.setText(QCoreApplication.translate("SelectorWidget", u"Select", None))
        self.selectionLabel.setText(QCoreApplication.translate("SelectorWidget", u"No Item Selected", None))
    # retranslateUi

