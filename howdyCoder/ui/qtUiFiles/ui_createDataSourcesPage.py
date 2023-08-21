# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'createDataSourcesPage.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QListView,
    QPushButton, QSizePolicy, QSpinBox, QStackedWidget,
    QVBoxLayout, QWidget)

from ..editableTable import EditableTableView
from ..enumComboBox import EnumComboBox

class Ui_CreateDataSourcesPage(object):
    def setupUi(self, CreateDataSourcesPage):
        if not CreateDataSourcesPage.objectName():
            CreateDataSourcesPage.setObjectName(u"CreateDataSourcesPage")
        CreateDataSourcesPage.resize(1048, 723)
        self.horizontalLayout_3 = QHBoxLayout(CreateDataSourcesPage)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.widget_3 = QWidget(CreateDataSourcesPage)
        self.widget_3.setObjectName(u"widget_3")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.widget_3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(self.widget_3)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.addButton = QPushButton(self.widget)
        self.addButton.setObjectName(u"addButton")

        self.horizontalLayout_2.addWidget(self.addButton)

        self.removeButton = QPushButton(self.widget)
        self.removeButton.setObjectName(u"removeButton")

        self.horizontalLayout_2.addWidget(self.removeButton)


        self.verticalLayout.addWidget(self.widget)

        self.dataSourcesView = EditableTableView(self.widget_3)
        self.dataSourcesView.setObjectName(u"dataSourcesView")
        self.dataSourcesView.setSelectionMode(QAbstractItemView.SingleSelection)

        self.verticalLayout.addWidget(self.dataSourcesView)


        self.horizontalLayout_3.addWidget(self.widget_3)

        self.widget_2 = QWidget(CreateDataSourcesPage)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy1)
        self.verticalLayout_2 = QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.widget_4 = QWidget(self.widget_2)
        self.widget_4.setObjectName(u"widget_4")
        sizePolicy2 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(3)
        sizePolicy2.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy2)
        self.horizontalLayout_4 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.widget_9 = QWidget(self.widget_4)
        self.widget_9.setObjectName(u"widget_9")
        sizePolicy3 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(1)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.widget_9.sizePolicy().hasHeightForWidth())
        self.widget_9.setSizePolicy(sizePolicy3)
        self.verticalLayout_5 = QVBoxLayout(self.widget_9)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.widget_10 = QWidget(self.widget_9)
        self.widget_10.setObjectName(u"widget_10")
        self.horizontalLayout_8 = QHBoxLayout(self.widget_10)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_3 = QLabel(self.widget_10)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_8.addWidget(self.label_3)

        self.nameEdit = QLineEdit(self.widget_10)
        self.nameEdit.setObjectName(u"nameEdit")
        self.nameEdit.setEnabled(False)

        self.horizontalLayout_8.addWidget(self.nameEdit)


        self.verticalLayout_5.addWidget(self.widget_10)

        self.typeBox = QWidget(self.widget_9)
        self.typeBox.setObjectName(u"typeBox")
        sizePolicy.setHeightForWidth(self.typeBox.sizePolicy().hasHeightForWidth())
        self.typeBox.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(self.typeBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.typeLabel = QLabel(self.typeBox)
        self.typeLabel.setObjectName(u"typeLabel")
        self.typeLabel.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.typeLabel)

        self.typeComboBox = EnumComboBox(self.typeBox)
        self.typeComboBox.setObjectName(u"typeComboBox")
        self.typeComboBox.setEnabled(False)

        self.horizontalLayout.addWidget(self.typeComboBox)


        self.verticalLayout_5.addWidget(self.typeBox)

        self.widget_11 = QWidget(self.widget_9)
        self.widget_11.setObjectName(u"widget_11")
        self.horizontalLayout_9 = QHBoxLayout(self.widget_11)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label = QLabel(self.widget_11)
        self.label.setObjectName(u"label")
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_9.addWidget(self.label)

        self.periodSpinBox = QSpinBox(self.widget_11)
        self.periodSpinBox.setObjectName(u"periodSpinBox")
        self.periodSpinBox.setEnabled(False)
        sizePolicy4 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.periodSpinBox.sizePolicy().hasHeightForWidth())
        self.periodSpinBox.setSizePolicy(sizePolicy4)
        self.periodSpinBox.setMinimumSize(QSize(100, 0))
        self.periodSpinBox.setMinimum(1)
        self.periodSpinBox.setMaximum(99999999)

        self.horizontalLayout_9.addWidget(self.periodSpinBox)


        self.verticalLayout_5.addWidget(self.widget_11)

        self.widget_12 = QWidget(self.widget_9)
        self.widget_12.setObjectName(u"widget_12")
        self.horizontalLayout_10 = QHBoxLayout(self.widget_12)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.seqCheckBox = QCheckBox(self.widget_12)
        self.seqCheckBox.setObjectName(u"seqCheckBox")
        self.seqCheckBox.setEnabled(False)

        self.horizontalLayout_10.addWidget(self.seqCheckBox)


        self.verticalLayout_5.addWidget(self.widget_12)


        self.horizontalLayout_4.addWidget(self.widget_9)

        self.widget_5 = QWidget(self.widget_4)
        self.widget_5.setObjectName(u"widget_5")
        self.verticalLayout_7 = QVBoxLayout(self.widget_5)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_4 = QLabel(self.widget_5)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignCenter)

        self.verticalLayout_7.addWidget(self.label_4)

        self.outputView = QListView(self.widget_5)
        self.outputView.setObjectName(u"outputView")
        self.outputView.setEditTriggers(QAbstractItemView.DoubleClicked)

        self.verticalLayout_7.addWidget(self.outputView)

        self.widget_8 = QWidget(self.widget_5)
        self.widget_8.setObjectName(u"widget_8")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_8)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.addOutputButton = QPushButton(self.widget_8)
        self.addOutputButton.setObjectName(u"addOutputButton")
        sizePolicy4.setHeightForWidth(self.addOutputButton.sizePolicy().hasHeightForWidth())
        self.addOutputButton.setSizePolicy(sizePolicy4)

        self.horizontalLayout_5.addWidget(self.addOutputButton)

        self.removeOutputButton = QPushButton(self.widget_8)
        self.removeOutputButton.setObjectName(u"removeOutputButton")
        sizePolicy4.setHeightForWidth(self.removeOutputButton.sizePolicy().hasHeightForWidth())
        self.removeOutputButton.setSizePolicy(sizePolicy4)

        self.horizontalLayout_5.addWidget(self.removeOutputButton)


        self.verticalLayout_7.addWidget(self.widget_8)


        self.horizontalLayout_4.addWidget(self.widget_5)

        self.dataSourceSpecificBox = QWidget(self.widget_4)
        self.dataSourceSpecificBox.setObjectName(u"dataSourceSpecificBox")
        self.verticalLayout_6 = QVBoxLayout(self.dataSourceSpecificBox)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.specificStackedWidget = QStackedWidget(self.dataSourceSpecificBox)
        self.specificStackedWidget.setObjectName(u"specificStackedWidget")
        self.nonePage = QWidget()
        self.nonePage.setObjectName(u"nonePage")
        self.specificStackedWidget.addWidget(self.nonePage)

        self.verticalLayout_6.addWidget(self.specificStackedWidget)


        self.horizontalLayout_4.addWidget(self.dataSourceSpecificBox)


        self.verticalLayout_2.addWidget(self.widget_4)

        self.dataSourceBox = QWidget(self.widget_2)
        self.dataSourceBox.setObjectName(u"dataSourceBox")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(7)
        sizePolicy5.setHeightForWidth(self.dataSourceBox.sizePolicy().hasHeightForWidth())
        self.dataSourceBox.setSizePolicy(sizePolicy5)
        self.verticalLayout_3 = QVBoxLayout(self.dataSourceBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.widget_6 = QWidget(self.dataSourceBox)
        self.widget_6.setObjectName(u"widget_6")
        sizePolicy6 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(1)
        sizePolicy6.setVerticalStretch(3)
        sizePolicy6.setHeightForWidth(self.widget_6.sizePolicy().hasHeightForWidth())
        self.widget_6.setSizePolicy(sizePolicy6)
        self.horizontalLayout_6 = QHBoxLayout(self.widget_6)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.widget_7 = QWidget(self.widget_6)
        self.widget_7.setObjectName(u"widget_7")
        self.verticalLayout_4 = QVBoxLayout(self.widget_7)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_2 = QLabel(self.widget_7)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.label_2)

        self.parameterView = EditableTableView(self.widget_7)
        self.parameterView.setObjectName(u"parameterView")
        self.parameterView.setEnabled(False)

        self.verticalLayout_4.addWidget(self.parameterView)

        self.buttonWidget = QWidget(self.widget_7)
        self.buttonWidget.setObjectName(u"buttonWidget")
        self.horizontalLayout_7 = QHBoxLayout(self.buttonWidget)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.addParameterButton = QPushButton(self.buttonWidget)
        self.addParameterButton.setObjectName(u"addParameterButton")
        self.addParameterButton.setEnabled(False)

        self.horizontalLayout_7.addWidget(self.addParameterButton)

        self.removeParameterButton = QPushButton(self.buttonWidget)
        self.removeParameterButton.setObjectName(u"removeParameterButton")
        self.removeParameterButton.setEnabled(False)

        self.horizontalLayout_7.addWidget(self.removeParameterButton)

        self.clearParameterButton = QPushButton(self.buttonWidget)
        self.clearParameterButton.setObjectName(u"clearParameterButton")
        self.clearParameterButton.setEnabled(False)

        self.horizontalLayout_7.addWidget(self.clearParameterButton)


        self.verticalLayout_4.addWidget(self.buttonWidget)


        self.horizontalLayout_6.addWidget(self.widget_7)


        self.verticalLayout_3.addWidget(self.widget_6)


        self.verticalLayout_2.addWidget(self.dataSourceBox)


        self.horizontalLayout_3.addWidget(self.widget_2)


        self.retranslateUi(CreateDataSourcesPage)

        self.specificStackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(CreateDataSourcesPage)
    # setupUi

    def retranslateUi(self, CreateDataSourcesPage):
        CreateDataSourcesPage.setWindowTitle(QCoreApplication.translate("CreateDataSourcesPage", u"createDataSourcesPage", None))
        self.addButton.setText(QCoreApplication.translate("CreateDataSourcesPage", u"Add", None))
        self.removeButton.setText(QCoreApplication.translate("CreateDataSourcesPage", u"Remove", None))
        self.label_3.setText(QCoreApplication.translate("CreateDataSourcesPage", u"Name:", None))
        self.typeLabel.setText(QCoreApplication.translate("CreateDataSourcesPage", u"Type:", None))
        self.label.setText(QCoreApplication.translate("CreateDataSourcesPage", u"Period", None))
        self.seqCheckBox.setText(QCoreApplication.translate("CreateDataSourcesPage", u"Sequential", None))
        self.label_4.setText(QCoreApplication.translate("CreateDataSourcesPage", u"Output", None))
        self.addOutputButton.setText(QCoreApplication.translate("CreateDataSourcesPage", u"+", None))
        self.removeOutputButton.setText(QCoreApplication.translate("CreateDataSourcesPage", u"-", None))
        self.label_2.setText(QCoreApplication.translate("CreateDataSourcesPage", u"Parameters", None))
        self.addParameterButton.setText(QCoreApplication.translate("CreateDataSourcesPage", u"Add", None))
        self.removeParameterButton.setText(QCoreApplication.translate("CreateDataSourcesPage", u"Remove", None))
        self.clearParameterButton.setText(QCoreApplication.translate("CreateDataSourcesPage", u"Clear", None))
    # retranslateUi

