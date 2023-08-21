# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'actionListCreator.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHBoxLayout, QHeaderView,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

from ..actionCreator import ActionCreator
from ..feedView import FeedView

class Ui_ActionListCreator(object):
    def setupUi(self, ActionListCreator):
        if not ActionListCreator.objectName():
            ActionListCreator.setObjectName(u"ActionListCreator")
        ActionListCreator.resize(915, 847)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(ActionListCreator.sizePolicy().hasHeightForWidth())
        ActionListCreator.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(ActionListCreator)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.feedLabel = QLabel(ActionListCreator)
        self.feedLabel.setObjectName(u"feedLabel")
        font = QFont()
        font.setPointSize(17)
        font.setBold(True)
        font.setUnderline(False)
        self.feedLabel.setFont(font)
        self.feedLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.feedLabel)

        self.feedView = FeedView(ActionListCreator)
        self.feedView.setObjectName(u"feedView")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(2)
        sizePolicy1.setHeightForWidth(self.feedView.sizePolicy().hasHeightForWidth())
        self.feedView.setSizePolicy(sizePolicy1)
        self.feedView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.feedView.setAlternatingRowColors(False)
        self.feedView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.feedView.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.feedView.horizontalHeader().setHighlightSections(False)
        self.feedView.verticalHeader().setHighlightSections(False)

        self.verticalLayout.addWidget(self.feedView)

        self.buttonBox = QWidget(ActionListCreator)
        self.buttonBox.setObjectName(u"buttonBox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy2)
        self.horizontalLayout_8 = QHBoxLayout(self.buttonBox)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer)

        self.widget_5 = QWidget(self.buttonBox)
        self.widget_5.setObjectName(u"widget_5")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_5)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, 0, -1, 0)
        self.modifyActionButton = QPushButton(self.widget_5)
        self.modifyActionButton.setObjectName(u"modifyActionButton")

        self.horizontalLayout_5.addWidget(self.modifyActionButton)

        self.removeActionButton = QPushButton(self.widget_5)
        self.removeActionButton.setObjectName(u"removeActionButton")

        self.horizontalLayout_5.addWidget(self.removeActionButton)


        self.horizontalLayout_8.addWidget(self.widget_5)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addWidget(self.buttonBox)

        self.label = QLabel(ActionListCreator)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setPointSize(17)
        font1.setBold(True)
        self.label.setFont(font1)
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.actionCreator = ActionCreator(ActionListCreator)
        self.actionCreator.setObjectName(u"actionCreator")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(4)
        sizePolicy3.setHeightForWidth(self.actionCreator.sizePolicy().hasHeightForWidth())
        self.actionCreator.setSizePolicy(sizePolicy3)

        self.verticalLayout.addWidget(self.actionCreator)

        self.widget = QWidget(ActionListCreator)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget_3 = QWidget(self.widget)
        self.widget_3.setObjectName(u"widget_3")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, 0)
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)


        self.horizontalLayout.addWidget(self.widget_3)

        self.widget_4 = QWidget(self.widget)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(-1, 0, -1, 0)
        self.clearActionButton = QPushButton(self.widget_4)
        self.clearActionButton.setObjectName(u"clearActionButton")

        self.horizontalLayout_4.addWidget(self.clearActionButton)

        self.addActionButton = QPushButton(self.widget_4)
        self.addActionButton.setObjectName(u"addActionButton")

        self.horizontalLayout_4.addWidget(self.addActionButton)


        self.horizontalLayout.addWidget(self.widget_4)

        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, 0)
        self.errorLabel = QLabel(self.widget_2)
        self.errorLabel.setObjectName(u"errorLabel")

        self.horizontalLayout_2.addWidget(self.errorLabel)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_5)


        self.horizontalLayout.addWidget(self.widget_2)


        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(ActionListCreator)

        QMetaObject.connectSlotsByName(ActionListCreator)
    # setupUi

    def retranslateUi(self, ActionListCreator):
        ActionListCreator.setWindowTitle(QCoreApplication.translate("ActionListCreator", u"Action List Creator", None))
        self.feedLabel.setText(QCoreApplication.translate("ActionListCreator", u"Feed", None))
        self.modifyActionButton.setText(QCoreApplication.translate("ActionListCreator", u"Modify", None))
        self.removeActionButton.setText(QCoreApplication.translate("ActionListCreator", u"Remove", None))
        self.label.setText(QCoreApplication.translate("ActionListCreator", u"Add an Action", None))
        self.clearActionButton.setText(QCoreApplication.translate("ActionListCreator", u"Clear Action", None))
        self.addActionButton.setText(QCoreApplication.translate("ActionListCreator", u"Add Action", None))
        self.errorLabel.setText("")
    # retranslateUi

