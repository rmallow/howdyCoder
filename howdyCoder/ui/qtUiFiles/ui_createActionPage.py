# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'createActionPage.ui'
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
from PySide6.QtWidgets import (QApplication, QSizePolicy, QStackedWidget, QVBoxLayout,
    QWidget)

from ..create.createFunctionAction import CreateFunctionAction

class Ui_CreateActionPage(object):
    def setupUi(self, CreateActionPage):
        if not CreateActionPage.objectName():
            CreateActionPage.setObjectName(u"CreateActionPage")
        CreateActionPage.resize(961, 890)
        self.verticalLayout = QVBoxLayout(CreateActionPage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.stacked_widget = QStackedWidget(CreateActionPage)
        self.stacked_widget.setObjectName(u"stacked_widget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.stacked_widget.addWidget(self.page)
        self.create_function_action = CreateFunctionAction()
        self.create_function_action.setObjectName(u"create_function_action")
        self.stacked_widget.addWidget(self.create_function_action)

        self.verticalLayout.addWidget(self.stacked_widget)


        self.retranslateUi(CreateActionPage)

        self.stacked_widget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(CreateActionPage)
    # setupUi

    def retranslateUi(self, CreateActionPage):
        CreateActionPage.setWindowTitle(QCoreApplication.translate("CreateActionPage", u"CreateActionPage", None))
    # retranslateUi

