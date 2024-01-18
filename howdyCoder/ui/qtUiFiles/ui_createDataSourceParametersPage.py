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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHBoxLayout, QHeaderView,
    QLabel, QListView, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

from ..editableTable import EditableTableView

class Ui_CreateDataSourceParametersPage(object):
    def setupUi(self, CreateDataSourceParametersPage):
        if not CreateDataSourceParametersPage.objectName():
            CreateDataSourceParametersPage.setObjectName(u"CreateDataSourceParametersPage")
        CreateDataSourceParametersPage.resize(861, 884)
        self.verticalLayout = QVBoxLayout(CreateDataSourceParametersPage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.suggested_label = QLabel(CreateDataSourceParametersPage)
        self.suggested_label.setObjectName(u"suggested_label")
        font = QFont()
        font.setPointSize(15)
        self.suggested_label.setFont(font)
        self.suggested_label.setWordWrap(True)

        self.verticalLayout.addWidget(self.suggested_label)

        self.parameter_list_widget = QListWidget(CreateDataSourceParametersPage)
        self.parameter_list_widget.setObjectName(u"parameter_list_widget")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.parameter_list_widget.sizePolicy().hasHeightForWidth())
        self.parameter_list_widget.setSizePolicy(sizePolicy)
        self.parameter_list_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.parameter_list_widget.setFlow(QListView.LeftToRight)

        self.verticalLayout.addWidget(self.parameter_list_widget)

        self.widget_6 = QWidget(CreateDataSourceParametersPage)
        self.widget_6.setObjectName(u"widget_6")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(8)
        sizePolicy1.setHeightForWidth(self.widget_6.sizePolicy().hasHeightForWidth())
        self.widget_6.setSizePolicy(sizePolicy1)
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
        self.label_2.setWordWrap(True)

        self.verticalLayout_4.addWidget(self.label_2)

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

        self.parameterView = EditableTableView(self.widget_7)
        self.parameterView.setObjectName(u"parameterView")
        self.parameterView.setEnabled(True)

        self.verticalLayout_4.addWidget(self.parameterView)


        self.horizontalLayout_6.addWidget(self.widget_7)


        self.verticalLayout.addWidget(self.widget_6)


        self.retranslateUi(CreateDataSourceParametersPage)

        QMetaObject.connectSlotsByName(CreateDataSourceParametersPage)
    # setupUi

    def retranslateUi(self, CreateDataSourceParametersPage):
        CreateDataSourceParametersPage.setWindowTitle(QCoreApplication.translate("CreateDataSourceParametersPage", u"CreateDataSourceParametersPage", None))
        self.suggested_label.setText(QCoreApplication.translate("CreateDataSourceParametersPage", u"Set the parameters to be used by your function. The top box shows the parameters that are used by the functions you've entered on the previous page. In the bottom box, enter the parameter name, select the type and then enter a value.", None))
        self.label_2.setText(QCoreApplication.translate("CreateDataSourceParametersPage", u"The Name, Type, and Value columns must all have valid values for each row for the parameter to be saved. Otherwise it will not be saved and will not be accessible by the function. Double click on an item to change its value.", None))
        self.addParameterButton.setText(QCoreApplication.translate("CreateDataSourceParametersPage", u"Add", None))
        self.removeParameterButton.setText(QCoreApplication.translate("CreateDataSourceParametersPage", u"Remove", None))
        self.clearParameterButton.setText(QCoreApplication.translate("CreateDataSourceParametersPage", u"Clear", None))
    # retranslateUi

