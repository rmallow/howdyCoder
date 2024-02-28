# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'createFileDataSource.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
    QSizePolicy, QVBoxLayout, QWidget)

from ..fileTableView import FileTableView

class Ui_CreateFileDataSource(object):
    def setupUi(self, CreateFileDataSource):
        if not CreateFileDataSource.objectName():
            CreateFileDataSource.setObjectName(u"CreateFileDataSource")
        CreateFileDataSource.resize(700, 509)
        self.verticalLayout = QVBoxLayout(CreateFileDataSource)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.top_label = QLabel(CreateFileDataSource)
        self.top_label.setObjectName(u"top_label")
        font = QFont()
        font.setPointSize(30)
        self.top_label.setFont(font)
        self.top_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.top_label)

        self.selector_widget_box = QWidget(CreateFileDataSource)
        self.selector_widget_box.setObjectName(u"selector_widget_box")

        self.verticalLayout.addWidget(self.selector_widget_box)

        self.file_status_label = QLabel(CreateFileDataSource)
        self.file_status_label.setObjectName(u"file_status_label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.file_status_label.sizePolicy().hasHeightForWidth())
        self.file_status_label.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setPointSize(24)
        self.file_status_label.setFont(font1)

        self.verticalLayout.addWidget(self.file_status_label)

        self.output_label = QLabel(CreateFileDataSource)
        self.output_label.setObjectName(u"output_label")
        self.output_label.setFont(font)
        self.output_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.output_label)

        self.file_view_box = QWidget(CreateFileDataSource)
        self.file_view_box.setObjectName(u"file_view_box")
        self.horizontalLayout = QHBoxLayout(self.file_view_box)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.file_view = FileTableView(self.file_view_box)
        self.file_view.setObjectName(u"file_view")
        self.file_view.horizontalHeader().setVisible(True)
        self.file_view.verticalHeader().setVisible(True)
        self.file_view.verticalHeader().setHighlightSections(True)

        self.horizontalLayout.addWidget(self.file_view)


        self.verticalLayout.addWidget(self.file_view_box)


        self.retranslateUi(CreateFileDataSource)

        QMetaObject.connectSlotsByName(CreateFileDataSource)
    # setupUi

    def retranslateUi(self, CreateFileDataSource):
        CreateFileDataSource.setWindowTitle(QCoreApplication.translate("CreateFileDataSource", u"CreateFileDataSource", None))
        self.top_label.setText(QCoreApplication.translate("CreateFileDataSource", u"Select File", None))
        self.file_status_label.setText("")
        self.output_label.setText(QCoreApplication.translate("CreateFileDataSource", u"View Data", None))
    # retranslateUi

