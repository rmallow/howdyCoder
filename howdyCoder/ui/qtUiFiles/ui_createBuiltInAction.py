# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'createBuiltInAction.ui'
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
from PySide6.QtWidgets import (QApplication, QGraphicsView, QHBoxLayout, QHeaderView,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QTableView, QVBoxLayout, QWidget)

from ..variableTextEdit import VariableTextEdit

class Ui_CreateBuiltInAction(object):
    def setupUi(self, CreateBuiltInAction):
        if not CreateBuiltInAction.objectName():
            CreateBuiltInAction.setObjectName(u"CreateBuiltInAction")
        CreateBuiltInAction.resize(800, 682)
        self.verticalLayout_4 = QVBoxLayout(CreateBuiltInAction)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.widget = QWidget(CreateBuiltInAction)
        self.widget.setObjectName(u"widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")
        font = QFont()
        font.setPointSize(25)
        self.label_4.setFont(font)
        self.label_4.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_4)

        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setPointSize(17)
        self.label.setFont(font1)
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)

        self.variable_edit = VariableTextEdit(self.widget)
        self.variable_edit.setObjectName(u"variable_edit")
        self.variable_edit.setFont(font1)

        self.verticalLayout.addWidget(self.variable_edit)


        self.verticalLayout_4.addWidget(self.widget)

        self.data_set_box = QWidget(CreateBuiltInAction)
        self.data_set_box.setObjectName(u"data_set_box")
        self.horizontalLayout = QHBoxLayout(self.data_set_box)
#ifndef Q_OS_MAC
        self.horizontalLayout.setSpacing(-1)
#endif
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget_3 = QWidget(self.data_set_box)
        self.widget_3.setObjectName(u"widget_3")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy)
        self.verticalLayout_3 = QVBoxLayout(self.widget_3)
#ifndef Q_OS_MAC
        self.verticalLayout_3.setSpacing(-1)
#endif
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.widget_2 = QWidget(self.widget_3)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.select_button = QPushButton(self.widget_2)
        self.select_button.setObjectName(u"select_button")
        self.select_button.setMinimumSize(QSize(100, 0))
        self.select_button.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_3.addWidget(self.select_button)

        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName(u"label_2")
        font2 = QFont()
        font2.setPointSize(20)
        self.label_2.setFont(font2)
        self.label_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label_2)

        self.horizontalSpacer = QSpacerItem(100, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout_3.addWidget(self.widget_2)

        self.graphics_view = QGraphicsView(self.widget_3)
        self.graphics_view.setObjectName(u"graphics_view")

        self.verticalLayout_3.addWidget(self.graphics_view)


        self.horizontalLayout.addWidget(self.widget_3)

        self.input_table_box = QWidget(self.data_set_box)
        self.input_table_box.setObjectName(u"input_table_box")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.input_table_box.sizePolicy().hasHeightForWidth())
        self.input_table_box.setSizePolicy(sizePolicy1)
        self.verticalLayout_2 = QVBoxLayout(self.input_table_box)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.widget_4 = QWidget(self.input_table_box)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_3 = QLabel(self.widget_4)
        self.label_3.setObjectName(u"label_3")
        font3 = QFont()
        font3.setPointSize(20)
        font3.setBold(False)
        self.label_3.setFont(font3)
        self.label_3.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label_3)


        self.verticalLayout_2.addWidget(self.widget_4)

        self.selected_table_view = QTableView(self.input_table_box)
        self.selected_table_view.setObjectName(u"selected_table_view")
        self.selected_table_view.verticalHeader().setVisible(False)

        self.verticalLayout_2.addWidget(self.selected_table_view)


        self.horizontalLayout.addWidget(self.input_table_box)


        self.verticalLayout_4.addWidget(self.data_set_box)


        self.retranslateUi(CreateBuiltInAction)

        QMetaObject.connectSlotsByName(CreateBuiltInAction)
    # setupUi

    def retranslateUi(self, CreateBuiltInAction):
        CreateBuiltInAction.setWindowTitle(QCoreApplication.translate("CreateBuiltInAction", u"CreateBuiltInAction", None))
        self.label_4.setText(QCoreApplication.translate("CreateBuiltInAction", u"Text Merger", None))
        self.label.setText(QCoreApplication.translate("CreateBuiltInAction", u"Merge your own text and data from the data set together. Use the Text Editor below to add words and select data by dragging and dropping or using the select button.", None))
        self.variable_edit.setPlaceholderText(QCoreApplication.translate("CreateBuiltInAction", u"Enter your text here.", None))
        self.select_button.setText(QCoreApplication.translate("CreateBuiltInAction", u"Select", None))
        self.label_2.setText(QCoreApplication.translate("CreateBuiltInAction", u"Selectable Data Set", None))
        self.label_3.setText(QCoreApplication.translate("CreateBuiltInAction", u"Selected Data", None))
    # retranslateUi

