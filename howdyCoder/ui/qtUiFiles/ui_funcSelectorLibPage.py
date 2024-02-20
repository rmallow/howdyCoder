# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'funcSelectorLibPage.ui'
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
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QTextEdit, QTreeView, QVBoxLayout,
    QWidget)

class Ui_FuncSelectorLibPage(object):
    def setupUi(self, FuncSelectorLibPage):
        if not FuncSelectorLibPage.objectName():
            FuncSelectorLibPage.setObjectName(u"FuncSelectorLibPage")
        FuncSelectorLibPage.resize(877, 580)
        self.verticalLayout = QVBoxLayout(FuncSelectorLibPage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget_2 = QWidget(FuncSelectorLibPage)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.libraryButton = QPushButton(self.widget_2)
        self.libraryButton.setObjectName(u"libraryButton")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.libraryButton.sizePolicy().hasHeightForWidth())
        self.libraryButton.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.libraryButton)

        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName(u"label_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy1)
        self.label_2.setWordWrap(True)

        self.horizontalLayout_2.addWidget(self.label_2)


        self.verticalLayout.addWidget(self.widget_2)

        self.search_box = QWidget(FuncSelectorLibPage)
        self.search_box.setObjectName(u"search_box")
        self.horizontalLayout_3 = QHBoxLayout(self.search_box)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(self.search_box)
        self.label.setObjectName(u"label")

        self.horizontalLayout_3.addWidget(self.label)

        self.search_edit = QLineEdit(self.search_box)
        self.search_edit.setObjectName(u"search_edit")
        self.search_edit.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_3.addWidget(self.search_edit)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout.addWidget(self.search_box)

        self.widget_4 = QWidget(FuncSelectorLibPage)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.libView = QTreeView(self.widget_4)
        self.libView.setObjectName(u"libView")
        self.libView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.libView.setAlternatingRowColors(False)

        self.horizontalLayout_4.addWidget(self.libView)

        self.funcDescription = QTextEdit(self.widget_4)
        self.funcDescription.setObjectName(u"funcDescription")
        self.funcDescription.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.horizontalLayout_4.addWidget(self.funcDescription)


        self.verticalLayout.addWidget(self.widget_4)

        self.widget = QWidget(FuncSelectorLibPage)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.bottomLabel = QLabel(self.widget)
        self.bottomLabel.setObjectName(u"bottomLabel")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.bottomLabel.sizePolicy().hasHeightForWidth())
        self.bottomLabel.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.bottomLabel)

        self.selectButton = QPushButton(self.widget)
        self.selectButton.setObjectName(u"selectButton")

        self.horizontalLayout.addWidget(self.selectButton)


        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(FuncSelectorLibPage)

        QMetaObject.connectSlotsByName(FuncSelectorLibPage)
    # setupUi

    def retranslateUi(self, FuncSelectorLibPage):
        FuncSelectorLibPage.setWindowTitle(QCoreApplication.translate("FuncSelectorLibPage", u"FuncSelectorLibPage", None))
        self.libraryButton.setText(QCoreApplication.translate("FuncSelectorLibPage", u"Load Library", None))
        self.label_2.setText(QCoreApplication.translate("FuncSelectorLibPage", u"For loading libraries compatible with Howdy Coder", None))
        self.label.setText(QCoreApplication.translate("FuncSelectorLibPage", u"Search:", None))
        self.funcDescription.setHtml(QCoreApplication.translate("FuncSelectorLibPage", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'.AppleSystemUIFont'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Select a function</p></body></html>", None))
        self.funcDescription.setPlaceholderText("")
        self.bottomLabel.setText("")
        self.selectButton.setText(QCoreApplication.translate("FuncSelectorLibPage", u"Select", None))
    # retranslateUi

