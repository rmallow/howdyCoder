# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'graphSettingsWidget.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QSpinBox, QVBoxLayout, QWidget)

class Ui_GraphSettingsWidget(object):
    def setupUi(self, GraphSettingsWidget):
        if not GraphSettingsWidget.objectName():
            GraphSettingsWidget.setObjectName(u"GraphSettingsWidget")
        GraphSettingsWidget.resize(735, 300)
        self.verticalLayout = QVBoxLayout(GraphSettingsWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.columDirections = QLabel(GraphSettingsWidget)
        self.columDirections.setObjectName(u"columDirections")
        self.columDirections.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.columDirections)

        self.columnSelectionWidget = QWidget(GraphSettingsWidget)
        self.columnSelectionWidget.setObjectName(u"columnSelectionWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.columnSelectionWidget.sizePolicy().hasHeightForWidth())
        self.columnSelectionWidget.setSizePolicy(sizePolicy)
        self.horizontalLayout_3 = QHBoxLayout(self.columnSelectionWidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.columnLabel = QLabel(self.columnSelectionWidget)
        self.columnLabel.setObjectName(u"columnLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.columnLabel.sizePolicy().hasHeightForWidth())
        self.columnLabel.setSizePolicy(sizePolicy1)
        self.columnLabel.setMinimumSize(QSize(0, 0))
        self.columnLabel.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_2.addWidget(self.columnLabel)

        self.columnComboBox = QComboBox(self.columnSelectionWidget)
        self.columnComboBox.setObjectName(u"columnComboBox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.columnComboBox.sizePolicy().hasHeightForWidth())
        self.columnComboBox.setSizePolicy(sizePolicy2)
        self.columnComboBox.setMinimumSize(QSize(0, 0))
        self.columnComboBox.setEditable(True)
        self.columnComboBox.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.verticalLayout_2.addWidget(self.columnComboBox)

        self.columnDeleteButton = QPushButton(self.columnSelectionWidget)
        self.columnDeleteButton.setObjectName(u"columnDeleteButton")

        self.verticalLayout_2.addWidget(self.columnDeleteButton)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

        self.columnList = QListWidget(self.columnSelectionWidget)
        self.columnList.setObjectName(u"columnList")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.columnList.sizePolicy().hasHeightForWidth())
        self.columnList.setSizePolicy(sizePolicy3)

        self.horizontalLayout_3.addWidget(self.columnList)


        self.verticalLayout.addWidget(self.columnSelectionWidget)

        self.columnSettingWidget = QWidget(GraphSettingsWidget)
        self.columnSettingWidget.setObjectName(u"columnSettingWidget")
        self.horizontalLayout_2 = QHBoxLayout(self.columnSettingWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.graphTypeLabel = QLabel(self.columnSettingWidget)
        self.graphTypeLabel.setObjectName(u"graphTypeLabel")

        self.verticalLayout_4.addWidget(self.graphTypeLabel)

        self.graphTypeComboBox = QComboBox(self.columnSettingWidget)
        self.graphTypeComboBox.setObjectName(u"graphTypeComboBox")

        self.verticalLayout_4.addWidget(self.graphTypeComboBox)


        self.horizontalLayout_2.addLayout(self.verticalLayout_4)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.graphColorLabel = QLabel(self.columnSettingWidget)
        self.graphColorLabel.setObjectName(u"graphColorLabel")

        self.verticalLayout_5.addWidget(self.graphColorLabel)

        self.graphColorComboBox = QComboBox(self.columnSettingWidget)
        self.graphColorComboBox.setObjectName(u"graphColorComboBox")

        self.verticalLayout_5.addWidget(self.graphColorComboBox)


        self.horizontalLayout_2.addLayout(self.verticalLayout_5)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.YMaxLabel = QLabel(self.columnSettingWidget)
        self.YMaxLabel.setObjectName(u"YMaxLabel")

        self.gridLayout.addWidget(self.YMaxLabel, 2, 0, 1, 1)

        self.yMinLabel = QLabel(self.columnSettingWidget)
        self.yMinLabel.setObjectName(u"yMinLabel")

        self.gridLayout.addWidget(self.yMinLabel, 0, 0, 1, 1)

        self.yMinBox = QSpinBox(self.columnSettingWidget)
        self.yMinBox.setObjectName(u"yMinBox")
        self.yMinBox.setMinimum(-999999999)
        self.yMinBox.setMaximum(999999999)

        self.gridLayout.addWidget(self.yMinBox, 0, 1, 1, 1)

        self.yMaxBox = QSpinBox(self.columnSettingWidget)
        self.yMaxBox.setObjectName(u"yMaxBox")
        self.yMaxBox.setMinimum(-999999999)
        self.yMaxBox.setMaximum(999999999)

        self.gridLayout.addWidget(self.yMaxBox, 2, 1, 1, 1)


        self.horizontalLayout_2.addLayout(self.gridLayout)


        self.verticalLayout.addWidget(self.columnSettingWidget)


        self.retranslateUi(GraphSettingsWidget)

        QMetaObject.connectSlotsByName(GraphSettingsWidget)
    # setupUi

    def retranslateUi(self, GraphSettingsWidget):
        GraphSettingsWidget.setWindowTitle(QCoreApplication.translate("GraphSettingsWidget", u"graphSettingsWidget", None))
        self.columDirections.setText(QCoreApplication.translate("GraphSettingsWidget", u"Add a column and select it to edit its settings", None))
        self.columnLabel.setText(QCoreApplication.translate("GraphSettingsWidget", u"Columns", None))
        self.columnDeleteButton.setText(QCoreApplication.translate("GraphSettingsWidget", u"Delete", None))
        self.graphTypeLabel.setText(QCoreApplication.translate("GraphSettingsWidget", u"Graph Type", None))
        self.graphColorLabel.setText(QCoreApplication.translate("GraphSettingsWidget", u"Graph Color", None))
        self.YMaxLabel.setText(QCoreApplication.translate("GraphSettingsWidget", u"Y-Max", None))
        self.yMinLabel.setText(QCoreApplication.translate("GraphSettingsWidget", u"Y-Min", None))
    # retranslateUi

