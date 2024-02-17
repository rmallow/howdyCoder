# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'parameterCheckWidget.ui'
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
from PySide6.QtWidgets import (QApplication, QHeaderView, QSizePolicy, QTableView,
    QVBoxLayout, QWidget)

class Ui_ParameterCheckWidget(object):
    def setupUi(self, ParameterCheckWidget):
        if not ParameterCheckWidget.objectName():
            ParameterCheckWidget.setObjectName(u"ParameterCheckWidget")
        ParameterCheckWidget.resize(459, 397)
        self.verticalLayout = QVBoxLayout(ParameterCheckWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.parameter_table = QTableView(ParameterCheckWidget)
        self.parameter_table.setObjectName(u"parameter_table")
        self.parameter_table.horizontalHeader().setMinimumSectionSize(30)
        self.parameter_table.verticalHeader().setVisible(False)

        self.verticalLayout.addWidget(self.parameter_table)


        self.retranslateUi(ParameterCheckWidget)

        QMetaObject.connectSlotsByName(ParameterCheckWidget)
    # setupUi

    def retranslateUi(self, ParameterCheckWidget):
        ParameterCheckWidget.setWindowTitle(QCoreApplication.translate("ParameterCheckWidget", u"Parameter Check Widget", None))
    # retranslateUi

