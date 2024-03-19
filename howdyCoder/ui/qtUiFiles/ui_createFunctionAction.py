# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'createFunctionAction.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QGraphicsView,
    QHBoxLayout, QHeaderView, QLabel, QListView,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QSpacerItem, QTableView, QVBoxLayout, QWidget)

class Ui_CreateFunctionAction(object):
    def setupUi(self, CreateFunctionAction):
        if not CreateFunctionAction.objectName():
            CreateFunctionAction.setObjectName(u"CreateFunctionAction")
        CreateFunctionAction.resize(959, 805)
        self.verticalLayout = QVBoxLayout(CreateFunctionAction)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_4 = QLabel(CreateFunctionAction)
        self.label_4.setObjectName(u"label_4")
        font = QFont()
        font.setPointSize(25)
        self.label_4.setFont(font)
        self.label_4.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_4)

        self.function_box_widget = QWidget(CreateFunctionAction)
        self.function_box_widget.setObjectName(u"function_box_widget")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.function_box_widget.sizePolicy().hasHeightForWidth())
        self.function_box_widget.setSizePolicy(sizePolicy)
        self.verticalLayout_5 = QVBoxLayout(self.function_box_widget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.calc_func_box = QWidget(self.function_box_widget)
        self.calc_func_box.setObjectName(u"calc_func_box")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(4)
        sizePolicy1.setHeightForWidth(self.calc_func_box.sizePolicy().hasHeightForWidth())
        self.calc_func_box.setSizePolicy(sizePolicy1)
        self.verticalLayout_7 = QVBoxLayout(self.calc_func_box)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.calc_func_label = QLabel(self.calc_func_box)
        self.calc_func_label.setObjectName(u"calc_func_label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(2)
        sizePolicy2.setHeightForWidth(self.calc_func_label.sizePolicy().hasHeightForWidth())
        self.calc_func_label.setSizePolicy(sizePolicy2)
        font1 = QFont()
        font1.setPointSize(15)
        self.calc_func_label.setFont(font1)
        self.calc_func_label.setAlignment(Qt.AlignCenter)
        self.calc_func_label.setWordWrap(True)

        self.verticalLayout_7.addWidget(self.calc_func_label)

        self.calcFuncWidget = QWidget(self.calc_func_box)
        self.calcFuncWidget.setObjectName(u"calcFuncWidget")
        self.horizontalLayout_2 = QHBoxLayout(self.calcFuncWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")

        self.verticalLayout_7.addWidget(self.calcFuncWidget)


        self.verticalLayout_5.addWidget(self.calc_func_box)

        self.triggerWidget = QWidget(self.function_box_widget)
        self.triggerWidget.setObjectName(u"triggerWidget")
        sizePolicy1.setHeightForWidth(self.triggerWidget.sizePolicy().hasHeightForWidth())
        self.triggerWidget.setSizePolicy(sizePolicy1)
        self.verticalLayout_4 = QVBoxLayout(self.triggerWidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_6 = QLabel(self.triggerWidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font1)
        self.label_6.setAlignment(Qt.AlignCenter)
        self.label_6.setWordWrap(True)

        self.verticalLayout_4.addWidget(self.label_6)

        self.outputFuncWidget = QWidget(self.triggerWidget)
        self.outputFuncWidget.setObjectName(u"outputFuncWidget")
        self.horizontalLayout_3 = QHBoxLayout(self.outputFuncWidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")

        self.verticalLayout_4.addWidget(self.outputFuncWidget)


        self.verticalLayout_5.addWidget(self.triggerWidget)

        self.suggested_data_box_widget = QWidget(self.function_box_widget)
        self.suggested_data_box_widget.setObjectName(u"suggested_data_box_widget")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(1)
        sizePolicy3.setHeightForWidth(self.suggested_data_box_widget.sizePolicy().hasHeightForWidth())
        self.suggested_data_box_widget.setSizePolicy(sizePolicy3)
        self.verticalLayout_6 = QVBoxLayout(self.suggested_data_box_widget)
#ifndef Q_OS_MAC
        self.verticalLayout_6.setSpacing(-1)
#endif
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.suggested_data_box_widget)
        self.label.setObjectName(u"label")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy4)
        self.label.setFont(font1)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)

        self.verticalLayout_6.addWidget(self.label)

        self.suggested_data_set = QListWidget(self.suggested_data_box_widget)
        self.suggested_data_set.setObjectName(u"suggested_data_set")
        sizePolicy5 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.suggested_data_set.sizePolicy().hasHeightForWidth())
        self.suggested_data_set.setSizePolicy(sizePolicy5)
        self.suggested_data_set.setMinimumSize(QSize(0, 0))
        self.suggested_data_set.setMaximumSize(QSize(16777215, 50))
        self.suggested_data_set.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.suggested_data_set.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.suggested_data_set.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.suggested_data_set.setSelectionMode(QAbstractItemView.NoSelection)
        self.suggested_data_set.setFlow(QListView.LeftToRight)

        self.verticalLayout_6.addWidget(self.suggested_data_set)


        self.verticalLayout_5.addWidget(self.suggested_data_box_widget)


        self.verticalLayout.addWidget(self.function_box_widget)

        self.data_set_label = QLabel(CreateFunctionAction)
        self.data_set_label.setObjectName(u"data_set_label")
        self.data_set_label.setFont(font1)
        self.data_set_label.setAlignment(Qt.AlignCenter)
        self.data_set_label.setWordWrap(True)

        self.verticalLayout.addWidget(self.data_set_label)

        self.widget = QWidget(CreateFunctionAction)
        self.widget.setObjectName(u"widget")
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        self.verticalLayout_3 = QVBoxLayout(self.widget_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.widget_5 = QWidget(self.widget_2)
        self.widget_5.setObjectName(u"widget_5")
        self.horizontalLayout_6 = QHBoxLayout(self.widget_5)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(-1, 8, -1, 8)
        self.select_button = QPushButton(self.widget_5)
        self.select_button.setObjectName(u"select_button")
        self.select_button.setMinimumSize(QSize(100, 0))
        self.select_button.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_6.addWidget(self.select_button)

        self.label_2 = QLabel(self.widget_5)
        self.label_2.setObjectName(u"label_2")
        font2 = QFont()
        font2.setPointSize(20)
        self.label_2.setFont(font2)
        self.label_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_6.addWidget(self.label_2)

        self.horizontalSpacer = QSpacerItem(100, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer)


        self.verticalLayout_3.addWidget(self.widget_5)

        self.graphics_view = QGraphicsView(self.widget_2)
        self.graphics_view.setObjectName(u"graphics_view")

        self.verticalLayout_3.addWidget(self.graphics_view)


        self.horizontalLayout.addWidget(self.widget_2)

        self.widget_3 = QWidget(self.widget)
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout_2 = QVBoxLayout(self.widget_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.widget_6 = QWidget(self.widget_3)
        self.widget_6.setObjectName(u"widget_6")
        self.horizontalLayout_7 = QHBoxLayout(self.widget_6)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(-1, 8, -1, 8)
        self.label_3 = QLabel(self.widget_6)
        self.label_3.setObjectName(u"label_3")
        font3 = QFont()
        font3.setPointSize(20)
        font3.setBold(False)
        self.label_3.setFont(font3)
        self.label_3.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_7.addWidget(self.label_3)


        self.verticalLayout_2.addWidget(self.widget_6)

        self.widget_4 = QWidget(self.widget_3)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_2.addWidget(self.widget_4)

        self.selected_table_view = QTableView(self.widget_3)
        self.selected_table_view.setObjectName(u"selected_table_view")
        self.selected_table_view.setAcceptDrops(True)
        self.selected_table_view.setProperty("showDropIndicator", True)
        self.selected_table_view.setDragEnabled(True)
        self.selected_table_view.setDragDropMode(QAbstractItemView.DropOnly)
        self.selected_table_view.setDefaultDropAction(Qt.MoveAction)
        self.selected_table_view.verticalHeader().setVisible(False)

        self.verticalLayout_2.addWidget(self.selected_table_view)

        self.removeButton = QPushButton(self.widget_3)
        self.removeButton.setObjectName(u"removeButton")

        self.verticalLayout_2.addWidget(self.removeButton)


        self.horizontalLayout.addWidget(self.widget_3)


        self.verticalLayout.addWidget(self.widget)

        self.data_type_box = QWidget(CreateFunctionAction)
        self.data_type_box.setObjectName(u"data_type_box")
        self.horizontalLayout_5 = QHBoxLayout(self.data_type_box)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label_5 = QLabel(self.data_type_box)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font1)

        self.horizontalLayout_5.addWidget(self.label_5)

        self.dataTypeCombo = QComboBox(self.data_type_box)
        self.dataTypeCombo.setObjectName(u"dataTypeCombo")
        self.dataTypeCombo.setFont(font1)

        self.horizontalLayout_5.addWidget(self.dataTypeCombo)


        self.verticalLayout.addWidget(self.data_type_box)


        self.retranslateUi(CreateFunctionAction)

        QMetaObject.connectSlotsByName(CreateFunctionAction)
    # setupUi

    def retranslateUi(self, CreateFunctionAction):
        CreateFunctionAction.setWindowTitle(QCoreApplication.translate("CreateFunctionAction", u"CreateFunctionAction", None))
        self.label_4.setText(QCoreApplication.translate("CreateFunctionAction", u"Function", None))
        self.calc_func_label.setText(QCoreApplication.translate("CreateFunctionAction", u"Select the function that will operate on the data. Select by hitting the button below which will open a window for selection. The function selected determines what input is needed, so when selecting a function make sure the input you've seleced above works with that function. For more information on required input, see the documentation or guides. Extra parameters will be set on the next page.", None))
        self.label_6.setText(QCoreApplication.translate("CreateFunctionAction", u"For triggers, assign a output function to be performed if the above function returns true.", None))
        self.label.setText(QCoreApplication.translate("CreateFunctionAction", u"The below are names that we parsed from the functions that accessed data_set. It is suggested to assign inputs to these names.", None))
        self.data_set_label.setText(QCoreApplication.translate("CreateFunctionAction", u"Select the data using the select button or right click. Modify the settings of the data in the table to right.", None))
        self.select_button.setText(QCoreApplication.translate("CreateFunctionAction", u"Select", None))
        self.label_2.setText(QCoreApplication.translate("CreateFunctionAction", u"Selectable Data Set", None))
        self.label_3.setText(QCoreApplication.translate("CreateFunctionAction", u"Selected Data", None))
        self.removeButton.setText(QCoreApplication.translate("CreateFunctionAction", u"Remove", None))
        self.label_5.setText(QCoreApplication.translate("CreateFunctionAction", u"Select the data type that you'd like to be the input for your function", None))
    # retranslateUi

