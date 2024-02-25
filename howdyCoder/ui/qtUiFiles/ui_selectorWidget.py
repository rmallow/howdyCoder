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
    QSizePolicy, QVBoxLayout, QWidget)

from ..util.qtUtil import ExpandingLabelWidget

class Ui_SelectorWidget(object):
    def setupUi(self, SelectorWidget):
        if not SelectorWidget.objectName():
            SelectorWidget.setObjectName(u"SelectorWidget")
        SelectorWidget.resize(630, 154)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SelectorWidget.sizePolicy().hasHeightForWidth())
        SelectorWidget.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(SelectorWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.helper_label = QLabel(SelectorWidget)
        self.helper_label.setObjectName(u"helper_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.helper_label.sizePolicy().hasHeightForWidth())
        self.helper_label.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.helper_label)

        self.widget = QWidget(SelectorWidget)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.selectorButton = QPushButton(self.widget)
        self.selectorButton.setObjectName(u"selectorButton")

        self.horizontalLayout_2.addWidget(self.selectorButton)

        self.selectionLabel = QLabel(self.widget)
        self.selectionLabel.setObjectName(u"selectionLabel")

        self.horizontalLayout_2.addWidget(self.selectionLabel)

        self.extraDescriptionLabel = ExpandingLabelWidget(self.widget)
        self.extraDescriptionLabel.setObjectName(u"extraDescriptionLabel")

        self.horizontalLayout_2.addWidget(self.extraDescriptionLabel)


        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(SelectorWidget)

        QMetaObject.connectSlotsByName(SelectorWidget)
    # setupUi

    def retranslateUi(self, SelectorWidget):
        SelectorWidget.setWindowTitle(QCoreApplication.translate("SelectorWidget", u"selectorWidget", None))
        self.helper_label.setText(QCoreApplication.translate("SelectorWidget", u"Use the button below to open a selector dialog.", None))
        self.selectorButton.setText(QCoreApplication.translate("SelectorWidget", u"Select", None))
        self.selectionLabel.setText(QCoreApplication.translate("SelectorWidget", u"No Item Selected", None))
    # retranslateUi

