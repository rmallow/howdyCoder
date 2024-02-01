# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'globalParameterPageWidget.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QFrame,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QStackedWidget,
    QVBoxLayout, QWidget)

from ..editableTable import EditableTableView
from ..keySetWidget import KeySetWidget

class Ui_GlobalParameterPageWidget(object):
    def setupUi(self, GlobalParameterPageWidget):
        if not GlobalParameterPageWidget.objectName():
            GlobalParameterPageWidget.setObjectName(u"GlobalParameterPageWidget")
        GlobalParameterPageWidget.resize(945, 724)
        self.verticalLayout = QVBoxLayout(GlobalParameterPageWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget_4 = QWidget(GlobalParameterPageWidget)
        self.widget_4.setObjectName(u"widget_4")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy)
        self.widget_4.setMinimumSize(QSize(0, 300))
        self.horizontalLayout = QHBoxLayout(self.widget_4)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 0, -1, 0)
        self.widget = QWidget(self.widget_4)
        self.widget.setObjectName(u"widget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy1)
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy2)
        font = QFont()
        font.setPointSize(24)
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_2)

        self.name_box = QWidget(self.widget)
        self.name_box.setObjectName(u"name_box")
        self.horizontalLayout_3 = QHBoxLayout(self.name_box)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(6, 6, 6, 6)
        self.horizontalSpacer_3 = QSpacerItem(80, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.label = QLabel(self.name_box)
        self.label.setObjectName(u"label")
        sizePolicy3 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy3)

        self.horizontalLayout_3.addWidget(self.label)

        self.new_parameter_name_edit = QLineEdit(self.name_box)
        self.new_parameter_name_edit.setObjectName(u"new_parameter_name_edit")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.new_parameter_name_edit.sizePolicy().hasHeightForWidth())
        self.new_parameter_name_edit.setSizePolicy(sizePolicy4)

        self.horizontalLayout_3.addWidget(self.new_parameter_name_edit)

        self.horizontalSpacer_4 = QSpacerItem(80, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)


        self.verticalLayout_2.addWidget(self.name_box)

        self.type_box = QWidget(self.widget)
        self.type_box.setObjectName(u"type_box")
        self.horizontalLayout_4 = QHBoxLayout(self.type_box)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(6, 6, 6, 6)
        self.horizontalSpacer_5 = QSpacerItem(80, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_5)

        self.label_3 = QLabel(self.type_box)
        self.label_3.setObjectName(u"label_3")
        sizePolicy3.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy3)

        self.horizontalLayout_4.addWidget(self.label_3)

        self.new_parameter_type_combo = QComboBox(self.type_box)
        self.new_parameter_type_combo.setObjectName(u"new_parameter_type_combo")
        sizePolicy4.setHeightForWidth(self.new_parameter_type_combo.sizePolicy().hasHeightForWidth())
        self.new_parameter_type_combo.setSizePolicy(sizePolicy4)
        self.new_parameter_type_combo.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.horizontalLayout_4.addWidget(self.new_parameter_type_combo)

        self.horizontalSpacer_6 = QSpacerItem(80, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_6)


        self.verticalLayout_2.addWidget(self.type_box)

        self.new_parameter_stacked_widget = QStackedWidget(self.widget)
        self.new_parameter_stacked_widget.setObjectName(u"new_parameter_stacked_widget")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.new_parameter_stacked_widget.sizePolicy().hasHeightForWidth())
        self.new_parameter_stacked_widget.setSizePolicy(sizePolicy5)
        self.value_boxPage1 = QWidget()
        self.value_boxPage1.setObjectName(u"value_boxPage1")
        self.horizontalLayout_8 = QHBoxLayout(self.value_boxPage1)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.widget_10 = QWidget(self.value_boxPage1)
        self.widget_10.setObjectName(u"widget_10")

        self.horizontalLayout_8.addWidget(self.widget_10)

        self.new_parameter_stacked_widget.addWidget(self.value_boxPage1)

        self.verticalLayout_2.addWidget(self.new_parameter_stacked_widget)

        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.new_parameter_add_button = QPushButton(self.widget_2)
        self.new_parameter_add_button.setObjectName(u"new_parameter_add_button")

        self.horizontalLayout_5.addWidget(self.new_parameter_add_button)


        self.verticalLayout_2.addWidget(self.widget_2)


        self.horizontalLayout.addWidget(self.widget)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.line = QFrame(self.widget_4)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.widget_5 = QWidget(self.widget_4)
        self.widget_5.setObjectName(u"widget_5")
        sizePolicy6 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(1)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.widget_5.sizePolicy().hasHeightForWidth())
        self.widget_5.setSizePolicy(sizePolicy6)
        self.verticalLayout_4 = QVBoxLayout(self.widget_5)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_4 = QLabel(self.widget_5)
        self.label_4.setObjectName(u"label_4")
        sizePolicy2.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy2)
        self.label_4.setFont(font)
        self.label_4.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.label_4)

        self.key_set_widget = KeySetWidget(self.widget_5)
        self.key_set_widget.setObjectName(u"key_set_widget")
        sizePolicy1.setHeightForWidth(self.key_set_widget.sizePolicy().hasHeightForWidth())
        self.key_set_widget.setSizePolicy(sizePolicy1)

        self.verticalLayout_4.addWidget(self.key_set_widget)


        self.horizontalLayout.addWidget(self.widget_5)


        self.verticalLayout.addWidget(self.widget_4)

        self.line_2 = QFrame(GlobalParameterPageWidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.widget_3 = QWidget(GlobalParameterPageWidget)
        self.widget_3.setObjectName(u"widget_3")
        sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy)
        self.verticalLayout_3 = QVBoxLayout(self.widget_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, -1, -1, 0)
        self.widget_6 = QWidget(self.widget_3)
        self.widget_6.setObjectName(u"widget_6")
        sizePolicy.setHeightForWidth(self.widget_6.sizePolicy().hasHeightForWidth())
        self.widget_6.setSizePolicy(sizePolicy)
        self.horizontalLayout_2 = QHBoxLayout(self.widget_6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.widget_7 = QWidget(self.widget_6)
        self.widget_7.setObjectName(u"widget_7")
        sizePolicy1.setHeightForWidth(self.widget_7.sizePolicy().hasHeightForWidth())
        self.widget_7.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.widget_7)

        self.widget_9 = QWidget(self.widget_6)
        self.widget_9.setObjectName(u"widget_9")
        sizePolicy1.setHeightForWidth(self.widget_9.sizePolicy().hasHeightForWidth())
        self.widget_9.setSizePolicy(sizePolicy1)
        self.horizontalLayout_7 = QHBoxLayout(self.widget_9)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_5 = QLabel(self.widget_9)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)
        self.label_5.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_7.addWidget(self.label_5)


        self.horizontalLayout_2.addWidget(self.widget_9)

        self.widget_8 = QWidget(self.widget_6)
        self.widget_8.setObjectName(u"widget_8")
        sizePolicy1.setHeightForWidth(self.widget_8.sizePolicy().hasHeightForWidth())
        self.widget_8.setSizePolicy(sizePolicy1)
        self.horizontalLayout_6 = QHBoxLayout(self.widget_8)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.remove_parameter_button = QPushButton(self.widget_8)
        self.remove_parameter_button.setObjectName(u"remove_parameter_button")

        self.horizontalLayout_6.addWidget(self.remove_parameter_button)


        self.horizontalLayout_2.addWidget(self.widget_8)


        self.verticalLayout_3.addWidget(self.widget_6)

        self.all_parameter_table_view = EditableTableView(self.widget_3)
        self.all_parameter_table_view.setObjectName(u"all_parameter_table_view")
        sizePolicy7 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(10)
        sizePolicy7.setHeightForWidth(self.all_parameter_table_view.sizePolicy().hasHeightForWidth())
        self.all_parameter_table_view.setSizePolicy(sizePolicy7)
        self.all_parameter_table_view.setMinimumSize(QSize(0, 300))
        self.all_parameter_table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.all_parameter_table_view.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.verticalLayout_3.addWidget(self.all_parameter_table_view)


        self.verticalLayout.addWidget(self.widget_3)


        self.retranslateUi(GlobalParameterPageWidget)

        QMetaObject.connectSlotsByName(GlobalParameterPageWidget)
    # setupUi

    def retranslateUi(self, GlobalParameterPageWidget):
        GlobalParameterPageWidget.setWindowTitle(QCoreApplication.translate("GlobalParameterPageWidget", u"GlobalParameterPageWidget", None))
        self.label_2.setText(QCoreApplication.translate("GlobalParameterPageWidget", u"Add Parameter", None))
        self.label.setText(QCoreApplication.translate("GlobalParameterPageWidget", u"Name:", None))
        self.label_3.setText(QCoreApplication.translate("GlobalParameterPageWidget", u"Type:", None))
        self.new_parameter_add_button.setText(QCoreApplication.translate("GlobalParameterPageWidget", u"Add", None))
        self.label_4.setText(QCoreApplication.translate("GlobalParameterPageWidget", u"Set Howdy Coder API Keys", None))
        self.label_5.setText(QCoreApplication.translate("GlobalParameterPageWidget", u"All Parameters", None))
        self.remove_parameter_button.setText(QCoreApplication.translate("GlobalParameterPageWidget", u"Remove", None))
    # retranslateUi

