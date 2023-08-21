# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'algoStatusWidget.ui'
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

class Ui_AlgoStatusWidget(object):
    def setupUi(self, AlgoStatusWidget):
        if not AlgoStatusWidget.objectName():
            AlgoStatusWidget.setObjectName(u"AlgoStatusWidget")
        AlgoStatusWidget.resize(520, 209)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AlgoStatusWidget.sizePolicy().hasHeightForWidth())
        AlgoStatusWidget.setSizePolicy(sizePolicy)
        AlgoStatusWidget.setMaximumSize(QSize(520, 209))
        AlgoStatusWidget.setStyleSheet(u"")
        self.verticalLayout_3 = QVBoxLayout(AlgoStatusWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.widget_4 = QWidget(AlgoStatusWidget)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.widget_3 = QWidget(self.widget_4)
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout_2 = QVBoxLayout(self.widget_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.name_label = QLabel(self.widget_3)
        self.name_label.setObjectName(u"name_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(2)
        sizePolicy1.setHeightForWidth(self.name_label.sizePolicy().hasHeightForWidth())
        self.name_label.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setPointSize(24)
        self.name_label.setFont(font)
        self.name_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.name_label)

        self.runtimeBox = QWidget(self.widget_3)
        self.runtimeBox.setObjectName(u"runtimeBox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.runtimeBox.sizePolicy().hasHeightForWidth())
        self.runtimeBox.setSizePolicy(sizePolicy2)
        self.horizontalLayout = QHBoxLayout(self.runtimeBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.runtime_label = QLabel(self.runtimeBox)
        self.runtime_label.setObjectName(u"runtime_label")

        self.horizontalLayout.addWidget(self.runtime_label)

        self.runtime_value = QLabel(self.runtimeBox)
        self.runtime_value.setObjectName(u"runtime_value")

        self.horizontalLayout.addWidget(self.runtime_value)


        self.verticalLayout_2.addWidget(self.runtimeBox)

        self.feedLengthBox = QWidget(self.widget_3)
        self.feedLengthBox.setObjectName(u"feedLengthBox")
        sizePolicy2.setHeightForWidth(self.feedLengthBox.sizePolicy().hasHeightForWidth())
        self.feedLengthBox.setSizePolicy(sizePolicy2)
        self.horizontalLayout_5 = QHBoxLayout(self.feedLengthBox)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.data_count_label = QLabel(self.feedLengthBox)
        self.data_count_label.setObjectName(u"data_count_label")
        sizePolicy.setHeightForWidth(self.data_count_label.sizePolicy().hasHeightForWidth())
        self.data_count_label.setSizePolicy(sizePolicy)

        self.horizontalLayout_5.addWidget(self.data_count_label)

        self.data_count_value = QLabel(self.feedLengthBox)
        self.data_count_value.setObjectName(u"data_count_value")

        self.horizontalLayout_5.addWidget(self.data_count_value)


        self.verticalLayout_2.addWidget(self.feedLengthBox)


        self.horizontalLayout_2.addWidget(self.widget_3)

        self.status_label = QLabel(self.widget_4)
        self.status_label.setObjectName(u"status_label")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(3)
        sizePolicy3.setHeightForWidth(self.status_label.sizePolicy().hasHeightForWidth())
        self.status_label.setSizePolicy(sizePolicy3)
        self.status_label.setAutoFillBackground(True)
        self.status_label.setStyleSheet(u"")
        self.status_label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.status_label)


        self.verticalLayout_3.addWidget(self.widget_4)

        self.widget = QWidget(AlgoStatusWidget)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_3 = QHBoxLayout(self.widget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.start_button = QPushButton(self.widget)
        self.start_button.setObjectName(u"start_button")
        sizePolicy4 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.start_button.sizePolicy().hasHeightForWidth())
        self.start_button.setSizePolicy(sizePolicy4)
        self.start_button.setMinimumSize(QSize(110, 40))
        self.start_button.setMaximumSize(QSize(110, 40))

        self.horizontalLayout_3.addWidget(self.start_button)

        self.remove_button = QPushButton(self.widget)
        self.remove_button.setObjectName(u"remove_button")
        sizePolicy4.setHeightForWidth(self.remove_button.sizePolicy().hasHeightForWidth())
        self.remove_button.setSizePolicy(sizePolicy4)
        self.remove_button.setMinimumSize(QSize(110, 40))
        self.remove_button.setMaximumSize(QSize(110, 40))

        self.horizontalLayout_3.addWidget(self.remove_button)

        self.save_button = QPushButton(self.widget)
        self.save_button.setObjectName(u"save_button")
        sizePolicy5 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.save_button.sizePolicy().hasHeightForWidth())
        self.save_button.setSizePolicy(sizePolicy5)
        self.save_button.setMinimumSize(QSize(110, 40))
        self.save_button.setMaximumSize(QSize(110, 40))

        self.horizontalLayout_3.addWidget(self.save_button)

        self.export_button = QPushButton(self.widget)
        self.export_button.setObjectName(u"export_button")
        sizePolicy5.setHeightForWidth(self.export_button.sizePolicy().hasHeightForWidth())
        self.export_button.setSizePolicy(sizePolicy5)
        self.export_button.setMinimumSize(QSize(110, 40))
        self.export_button.setMaximumSize(QSize(110, 40))

        self.horizontalLayout_3.addWidget(self.export_button)


        self.verticalLayout_3.addWidget(self.widget)


        self.retranslateUi(AlgoStatusWidget)

        QMetaObject.connectSlotsByName(AlgoStatusWidget)
    # setupUi

    def retranslateUi(self, AlgoStatusWidget):
        AlgoStatusWidget.setWindowTitle(QCoreApplication.translate("AlgoStatusWidget", u"Algo Status Widget", None))
        self.name_label.setText(QCoreApplication.translate("AlgoStatusWidget", u"example name", None))
        self.runtime_label.setText(QCoreApplication.translate("AlgoStatusWidget", u"Runtime:", None))
        self.runtime_value.setText("")
        self.data_count_label.setText(QCoreApplication.translate("AlgoStatusWidget", u"Data Count:", None))
        self.data_count_value.setText("")
        self.status_label.setText("")
        self.start_button.setText(QCoreApplication.translate("AlgoStatusWidget", u"Start", None))
        self.remove_button.setText(QCoreApplication.translate("AlgoStatusWidget", u"Remove", None))
        self.save_button.setText(QCoreApplication.translate("AlgoStatusWidget", u"Save Config", None))
        self.export_button.setText(QCoreApplication.translate("AlgoStatusWidget", u"Export", None))
    # retranslateUi

