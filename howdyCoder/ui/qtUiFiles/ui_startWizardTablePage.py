# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'startWizardTablePage.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHeaderView, QSizePolicy,
    QTableView, QVBoxLayout, QWidget)

class Ui_StartWizardTablePage(object):
    def setupUi(self, StartWizardTablePage):
        if not StartWizardTablePage.objectName():
            StartWizardTablePage.setObjectName(u"StartWizardTablePage")
        StartWizardTablePage.resize(459, 397)
        self.verticalLayout = QVBoxLayout(StartWizardTablePage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.table = QTableView(StartWizardTablePage)
        self.table.setObjectName(u"table")
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setMinimumSectionSize(30)
        self.table.verticalHeader().setVisible(False)

        self.verticalLayout.addWidget(self.table)


        self.retranslateUi(StartWizardTablePage)

        QMetaObject.connectSlotsByName(StartWizardTablePage)
    # setupUi

    def retranslateUi(self, StartWizardTablePage):
        StartWizardTablePage.setWindowTitle(QCoreApplication.translate("StartWizardTablePage", u"Start Wizard Table Page", None))
    # retranslateUi

