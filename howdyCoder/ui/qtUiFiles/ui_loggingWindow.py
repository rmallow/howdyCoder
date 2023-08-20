# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'loggingWindow.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QHeaderView,
    QPushButton, QSizePolicy, QSpacerItem, QTableView,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_LoggingWindow(object):
    def setupUi(self, LoggingWindow):
        if not LoggingWindow.objectName():
            LoggingWindow.setObjectName(u"LoggingWindow")
        LoggingWindow.resize(927, 329)
        self.verticalLayout = QVBoxLayout(LoggingWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.keyButton = QPushButton(LoggingWindow)
        self.keyButton.setObjectName(u"keyButton")

        self.horizontalLayout.addWidget(self.keyButton)

        self.groupButton = QPushButton(LoggingWindow)
        self.groupButton.setObjectName(u"groupButton")

        self.horizontalLayout.addWidget(self.groupButton)

        self.severityButton = QPushButton(LoggingWindow)
        self.severityButton.setObjectName(u"severityButton")

        self.horizontalLayout.addWidget(self.severityButton)

        self.buttonSpacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.buttonSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.tableView = QTableView(LoggingWindow)
        self.tableView.setObjectName(u"tableView")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableView.sizePolicy().hasHeightForWidth())
        self.tableView.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.tableView)

        self.textView = QTextEdit(LoggingWindow)
        self.textView.setObjectName(u"textView")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.textView.sizePolicy().hasHeightForWidth())
        self.textView.setSizePolicy(sizePolicy1)
        self.textView.setReadOnly(True)
        self.textView.setAcceptRichText(False)

        self.horizontalLayout_2.addWidget(self.textView)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(LoggingWindow)

        QMetaObject.connectSlotsByName(LoggingWindow)
    # setupUi

    def retranslateUi(self, LoggingWindow):
        LoggingWindow.setWindowTitle(QCoreApplication.translate("LoggingWindow", u"Logging", None))
        self.keyButton.setText(QCoreApplication.translate("LoggingWindow", u"Key", None))
        self.groupButton.setText(QCoreApplication.translate("LoggingWindow", u"Group", None))
        self.severityButton.setText(QCoreApplication.translate("LoggingWindow", u"Severity", None))
        self.textView.setHtml(QCoreApplication.translate("LoggingWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'.AppleSystemUIFont'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.textView.setPlaceholderText("")
    # retranslateUi

