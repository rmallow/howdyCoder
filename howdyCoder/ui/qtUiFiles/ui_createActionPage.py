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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QHBoxLayout,
    QHeaderView, QLabel, QListView, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QTableView,
    QVBoxLayout, QWidget)

class Ui_CreateActionPage(object):
    def setupUi(self, CreateActionPage):
        if not CreateActionPage.objectName():
            CreateActionPage.setObjectName(u"CreateActionPage")
        CreateActionPage.resize(887, 837)
        self.verticalLayout = QVBoxLayout(CreateActionPage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.calc_func_label = QLabel(CreateActionPage)
        self.calc_func_label.setObjectName(u"calc_func_label")
        font = QFont()
        font.setPointSize(15)
        self.calc_func_label.setFont(font)
        self.calc_func_label.setAlignment(Qt.AlignCenter)
        self.calc_func_label.setWordWrap(True)

        self.verticalLayout.addWidget(self.calc_func_label)

        self.calcFuncWidget = QWidget(CreateActionPage)
        self.calcFuncWidget.setObjectName(u"calcFuncWidget")
        self.horizontalLayout_2 = QHBoxLayout(self.calcFuncWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")

        self.verticalLayout.addWidget(self.calcFuncWidget)

        self.triggerWidget = QWidget(CreateActionPage)
        self.triggerWidget.setObjectName(u"triggerWidget")
        self.verticalLayout_4 = QVBoxLayout(self.triggerWidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_6 = QLabel(self.triggerWidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font)
        self.label_6.setAlignment(Qt.AlignCenter)
        self.label_6.setWordWrap(True)

        self.verticalLayout_4.addWidget(self.label_6)

        self.outputFuncWidget = QWidget(self.triggerWidget)
        self.outputFuncWidget.setObjectName(u"outputFuncWidget")
        self.horizontalLayout_3 = QHBoxLayout(self.outputFuncWidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")

        self.verticalLayout_4.addWidget(self.outputFuncWidget)


        self.verticalLayout.addWidget(self.triggerWidget)

        self.label = QLabel(CreateActionPage)
        self.label.setObjectName(u"label")
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)

        self.suggested_data_set = QListWidget(CreateActionPage)
        self.suggested_data_set.setObjectName(u"suggested_data_set")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.suggested_data_set.sizePolicy().hasHeightForWidth())
        self.suggested_data_set.setSizePolicy(sizePolicy)
        self.suggested_data_set.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.suggested_data_set.setSelectionMode(QAbstractItemView.NoSelection)
        self.suggested_data_set.setFlow(QListView.LeftToRight)

        self.verticalLayout.addWidget(self.suggested_data_set)

        self.data_set_label = QLabel(CreateActionPage)
        self.data_set_label.setObjectName(u"data_set_label")
        self.data_set_label.setFont(font)
        self.data_set_label.setAlignment(Qt.AlignCenter)
        self.data_set_label.setWordWrap(True)

        self.verticalLayout.addWidget(self.data_set_label)

        self.widget = QWidget(CreateActionPage)
        self.widget.setObjectName(u"widget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(4)
        sizePolicy1.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy1)
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        self.verticalLayout_3 = QVBoxLayout(self.widget_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_2)

        self.availableInputTable = QTableView(self.widget_2)
        self.availableInputTable.setObjectName(u"availableInputTable")
        font1 = QFont()
        font1.setPointSize(18)
        self.availableInputTable.setFont(font1)
        self.availableInputTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.availableInputTable.setSelectionMode(QAbstractItemView.NoSelection)
        self.availableInputTable.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_3.addWidget(self.availableInputTable)


        self.horizontalLayout.addWidget(self.widget_2)

        self.widget_3 = QWidget(self.widget)
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout_2 = QVBoxLayout(self.widget_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_3 = QLabel(self.widget_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_3)

        self.selectedInputTable = QTableView(self.widget_3)
        self.selectedInputTable.setObjectName(u"selectedInputTable")
        self.selectedInputTable.setFont(font1)
        self.selectedInputTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.selectedInputTable.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_2.addWidget(self.selectedInputTable)

        self.widget_4 = QWidget(self.widget_3)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.removeButton = QPushButton(self.widget_4)
        self.removeButton.setObjectName(u"removeButton")

        self.horizontalLayout_4.addWidget(self.removeButton)


        self.verticalLayout_2.addWidget(self.widget_4)


        self.horizontalLayout.addWidget(self.widget_3)


        self.verticalLayout.addWidget(self.widget)

        self.data_type_box = QWidget(CreateActionPage)
        self.data_type_box.setObjectName(u"data_type_box")
        self.horizontalLayout_5 = QHBoxLayout(self.data_type_box)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label_5 = QLabel(self.data_type_box)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)

        self.horizontalLayout_5.addWidget(self.label_5)

        self.dataTypeCombo = QComboBox(self.data_type_box)
        self.dataTypeCombo.setObjectName(u"dataTypeCombo")
        self.dataTypeCombo.setFont(font)

        self.horizontalLayout_5.addWidget(self.dataTypeCombo)


        self.verticalLayout.addWidget(self.data_type_box)


        self.retranslateUi(CreateActionPage)

        QMetaObject.connectSlotsByName(CreateActionPage)
    # setupUi

    def retranslateUi(self, CreateActionPage):
        CreateActionPage.setWindowTitle(QCoreApplication.translate("CreateActionPage", u"CreateActionPage", None))
        self.calc_func_label.setText(QCoreApplication.translate("CreateActionPage", u"Select the function that will operate on the data. Select by hitting the button below which will open a window for selection. The function selected determines what input is needed, so when selecting a function make sure the input you've seleced above works with that function. For more information on required input, see the documentation or guides. Extra parameters will be set on the next page.", None))
        self.label_6.setText(QCoreApplication.translate("CreateActionPage", u"For triggers, assign a output function to be performed if the above function returns true. The splitting of these functions is done to enable reusability of functions. Although, you can just do your intended outputting in the above function. This makes the below output function not required.", None))
        self.label.setText(QCoreApplication.translate("CreateActionPage", u"The below are names that we parsed from the functions that accessed data_set. It is suggested to assign inputs to these names, unless you know otherwise.", None))
        self.data_set_label.setText(QCoreApplication.translate("CreateActionPage", u"From the left table,  select which columns you'd need as input. These will be added to the table on the right.  For use in the function, you can rename them in the table on the right as needed. To remove, select a row in the input table and then hit the remove button.", None))
        self.label_2.setText(QCoreApplication.translate("CreateActionPage", u"Available Inputs", None))
        self.label_3.setText(QCoreApplication.translate("CreateActionPage", u"Selected Input", None))
        self.removeButton.setText(QCoreApplication.translate("CreateActionPage", u"Remove", None))
        self.label_5.setText(QCoreApplication.translate("CreateActionPage", u"Select the data type that you'd like to be the input for your function", None))
    # retranslateUi

