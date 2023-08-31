# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'createDataSourceParametersPage.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QDateTimeEdit,
    QHBoxLayout, QHeaderView, QLabel, QListView,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QSpacerItem, QTimeEdit, QVBoxLayout, QWidget)

from ..editableTable import EditableTableView

class Ui_CreateDataSourceParametersPage(object):
    def setupUi(self, CreateDataSourceParametersPage):
        if not CreateDataSourceParametersPage.objectName():
            CreateDataSourceParametersPage.setObjectName(u"CreateDataSourceParametersPage")
        CreateDataSourceParametersPage.resize(861, 884)
        self.verticalLayout = QVBoxLayout(CreateDataSourceParametersPage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(CreateDataSourceParametersPage)
        self.widget.setObjectName(u"widget")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.periodWidgetBox = QWidget(self.widget)
        self.periodWidgetBox.setObjectName(u"periodWidgetBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(3)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.periodWidgetBox.sizePolicy().hasHeightForWidth())
        self.periodWidgetBox.setSizePolicy(sizePolicy1)
        self.verticalLayout_2 = QVBoxLayout(self.periodWidgetBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.periodLabel = QLabel(self.periodWidgetBox)
        self.periodLabel.setObjectName(u"periodLabel")
        font = QFont()
        font.setPointSize(15)
        self.periodLabel.setFont(font)
        self.periodLabel.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.periodLabel)

        self.widget_11 = QWidget(self.periodWidgetBox)
        self.widget_11.setObjectName(u"widget_11")
        self.horizontalLayout_9 = QHBoxLayout(self.widget_11)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_3 = QLabel(self.widget_11)
        self.label_3.setObjectName(u"label_3")
        sizePolicy2 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy2)
        self.label_3.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_9.addWidget(self.label_3)

        self.time_edit = QTimeEdit(self.widget_11)
        self.time_edit.setObjectName(u"time_edit")
        self.time_edit.setAlignment(Qt.AlignCenter)
        self.time_edit.setDate(QDate(2000, 1, 1))
        self.time_edit.setMinimumTime(QTime(0, 0, 1))
        self.time_edit.setCurrentSection(QDateTimeEdit.HourSection)
        self.time_edit.setCurrentSectionIndex(0)
        self.time_edit.setTime(QTime(0, 0, 1))

        self.horizontalLayout_9.addWidget(self.time_edit)

        self.single_shot_check = QCheckBox(self.widget_11)
        self.single_shot_check.setObjectName(u"single_shot_check")
        self.single_shot_check.setLayoutDirection(Qt.RightToLeft)

        self.horizontalLayout_9.addWidget(self.single_shot_check)


        self.verticalLayout_2.addWidget(self.widget_11)


        self.horizontalLayout.addWidget(self.periodWidgetBox)

        self.flattenWidgetBox = QWidget(self.widget)
        self.flattenWidgetBox.setObjectName(u"flattenWidgetBox")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(2)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.flattenWidgetBox.sizePolicy().hasHeightForWidth())
        self.flattenWidgetBox.setSizePolicy(sizePolicy3)
        self.verticalLayout_3 = QVBoxLayout(self.flattenWidgetBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label = QLabel(self.flattenWidgetBox)
        self.label.setObjectName(u"label")
        self.label.setFont(font)
        self.label.setWordWrap(True)

        self.verticalLayout_3.addWidget(self.label)

        self.widget_4 = QWidget(self.flattenWidgetBox)
        self.widget_4.setObjectName(u"widget_4")
        self.widget_4.setLayoutDirection(Qt.LeftToRight)
        self.horizontalLayout_2 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(12, -1, -1, -1)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.flattenedCheck = QCheckBox(self.widget_4)
        self.flattenedCheck.setObjectName(u"flattenedCheck")
        self.flattenedCheck.setFont(font)
        self.flattenedCheck.setChecked(True)

        self.horizontalLayout_2.addWidget(self.flattenedCheck)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout_3.addWidget(self.widget_4)


        self.horizontalLayout.addWidget(self.flattenWidgetBox)


        self.verticalLayout.addWidget(self.widget)

        self.label_4 = QLabel(CreateDataSourceParametersPage)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)
        self.label_4.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_4)

        self.parameter_list_widget = QListWidget(CreateDataSourceParametersPage)
        self.parameter_list_widget.setObjectName(u"parameter_list_widget")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(1)
        sizePolicy4.setHeightForWidth(self.parameter_list_widget.sizePolicy().hasHeightForWidth())
        self.parameter_list_widget.setSizePolicy(sizePolicy4)
        self.parameter_list_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.parameter_list_widget.setFlow(QListView.LeftToRight)

        self.verticalLayout.addWidget(self.parameter_list_widget)

        self.widget_6 = QWidget(CreateDataSourceParametersPage)
        self.widget_6.setObjectName(u"widget_6")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(1)
        sizePolicy5.setVerticalStretch(8)
        sizePolicy5.setHeightForWidth(self.widget_6.sizePolicy().hasHeightForWidth())
        self.widget_6.setSizePolicy(sizePolicy5)
        self.horizontalLayout_6 = QHBoxLayout(self.widget_6)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
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
        self.parameterView.setEnabled(True)

        self.verticalLayout_4.addWidget(self.parameterView)

        self.buttonWidget = QWidget(self.widget_7)
        self.buttonWidget.setObjectName(u"buttonWidget")
        self.horizontalLayout_7 = QHBoxLayout(self.buttonWidget)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.addParameterButton = QPushButton(self.buttonWidget)
        self.addParameterButton.setObjectName(u"addParameterButton")
        self.addParameterButton.setEnabled(True)

        self.horizontalLayout_7.addWidget(self.addParameterButton)

        self.removeParameterButton = QPushButton(self.buttonWidget)
        self.removeParameterButton.setObjectName(u"removeParameterButton")
        self.removeParameterButton.setEnabled(True)

        self.horizontalLayout_7.addWidget(self.removeParameterButton)

        self.clearParameterButton = QPushButton(self.buttonWidget)
        self.clearParameterButton.setObjectName(u"clearParameterButton")
        self.clearParameterButton.setEnabled(True)

        self.horizontalLayout_7.addWidget(self.clearParameterButton)


        self.verticalLayout_4.addWidget(self.buttonWidget)


        self.horizontalLayout_6.addWidget(self.widget_7)


        self.verticalLayout.addWidget(self.widget_6)


        self.retranslateUi(CreateDataSourceParametersPage)

        QMetaObject.connectSlotsByName(CreateDataSourceParametersPage)
    # setupUi

    def retranslateUi(self, CreateDataSourceParametersPage):
        CreateDataSourceParametersPage.setWindowTitle(QCoreApplication.translate("CreateDataSourceParametersPage", u"CreateDataSourceParametersPage", None))
        self.periodLabel.setText(QCoreApplication.translate("CreateDataSourceParametersPage", u"Set the period for the data source. The period is how often the data source will query the input.  IE if it is a stream data source, it will call the API URL every period number of seconds. Or set singleshot which will make the data source run only once, regardless of period.", None))
        self.label_3.setText(QCoreApplication.translate("CreateDataSourceParametersPage", u"Period (hh:mm:ss)", None))
        self.time_edit.setDisplayFormat(QCoreApplication.translate("CreateDataSourceParametersPage", u"hh:mm:ss", None))
        self.single_shot_check.setText(QCoreApplication.translate("CreateDataSourceParametersPage", u"Single Shot", None))
        self.label.setText(QCoreApplication.translate("CreateDataSourceParametersPage", u"Set if the output should be flattened. If any of the output is lists, flattening will cause each data point to be counted as individual data. If the ouput is a dict and contains multiple lists, flattening will only happen if all lists are the same length.", None))
        self.flattenedCheck.setText(QCoreApplication.translate("CreateDataSourceParametersPage", u"Flatten", None))
        self.label_4.setText(QCoreApplication.translate("CreateDataSourceParametersPage", u"Set the parameters to be used by your function. The top box shows the parameters that are used by the functions you've entered on the previous page. In the bottom box, enter the parameter name, select the type and then enter a value.", None))
        self.label_2.setText(QCoreApplication.translate("CreateDataSourceParametersPage", u"Parameters", None))
        self.addParameterButton.setText(QCoreApplication.translate("CreateDataSourceParametersPage", u"Add", None))
        self.removeParameterButton.setText(QCoreApplication.translate("CreateDataSourceParametersPage", u"Remove", None))
        self.clearParameterButton.setText(QCoreApplication.translate("CreateDataSourceParametersPage", u"Clear", None))
    # retranslateUi

