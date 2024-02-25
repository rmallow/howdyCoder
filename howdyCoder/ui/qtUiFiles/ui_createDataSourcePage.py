# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'createDataSourcePage.ui'
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

from ..create.createFileDataSource import CreateFileDataSource
from ..create.createStandardDataSource import CreateStandardDataSource

class Ui_CreateDataSourcePage(object):
    def setupUi(self, CreateDataSourcePage):
        if not CreateDataSourcePage.objectName():
            CreateDataSourcePage.setObjectName(u"CreateDataSourcePage")
        CreateDataSourcePage.resize(785, 609)
        self.verticalLayout = QVBoxLayout(CreateDataSourcePage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.stacked_widget = QStackedWidget(CreateDataSourcePage)
        self.stacked_widget.setObjectName(u"stacked_widget")
        self.create_standard_data_source = CreateStandardDataSource()
        self.create_standard_data_source.setObjectName(u"create_standard_data_source")
        self.stacked_widget.addWidget(self.create_standard_data_source)
        self.create_file_data_source = CreateFileDataSource()
        self.create_file_data_source.setObjectName(u"create_file_data_source")
        self.stacked_widget.addWidget(self.create_file_data_source)

        self.verticalLayout.addWidget(self.stacked_widget)


        self.retranslateUi(CreateDataSourcePage)

        QMetaObject.connectSlotsByName(CreateDataSourcePage)
    # setupUi

    def retranslateUi(self, CreateDataSourcePage):
        CreateDataSourcePage.setWindowTitle(QCoreApplication.translate("CreateDataSourcePage", u"CreateDataSourcePage", None))
    # retranslateUi

