# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'createDataSourceType.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHBoxLayout, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_CreateDataSourceType(object):
    def setupUi(self, CreateDataSourceType):
        if not CreateDataSourceType.objectName():
            CreateDataSourceType.setObjectName(u"CreateDataSourceType")
        CreateDataSourceType.resize(764, 488)
        self.verticalLayout = QVBoxLayout(CreateDataSourceType)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget_3 = QWidget(CreateDataSourceType)
        self.widget_3.setObjectName(u"widget_3")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.widget_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.widget_3)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label)

        self.widget = QWidget(self.widget_3)
        self.widget.setObjectName(u"widget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy1)
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.name_label = QLabel(self.widget)
        self.name_label.setObjectName(u"name_label")
        font1 = QFont()
        font1.setPointSize(20)
        self.name_label.setFont(font1)

        self.horizontalLayout.addWidget(self.name_label)

        self.name_edit = QLineEdit(self.widget)
        self.name_edit.setObjectName(u"name_edit")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.name_edit.sizePolicy().hasHeightForWidth())
        self.name_edit.setSizePolicy(sizePolicy2)
        self.name_edit.setMaximumSize(QSize(16777215, 300))
        self.name_edit.setFont(font1)

        self.horizontalLayout.addWidget(self.name_edit)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addWidget(self.widget)


        self.verticalLayout.addWidget(self.widget_3)

        self.type_and_sub_type_box = QWidget(CreateDataSourceType)
        self.type_and_sub_type_box.setObjectName(u"type_and_sub_type_box")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(3)
        sizePolicy3.setHeightForWidth(self.type_and_sub_type_box.sizePolicy().hasHeightForWidth())
        self.type_and_sub_type_box.setSizePolicy(sizePolicy3)
        self.horizontalLayout_4 = QHBoxLayout(self.type_and_sub_type_box)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(6, 12, 6, 12)
        self.type_box = QWidget(self.type_and_sub_type_box)
        self.type_box.setObjectName(u"type_box")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(1)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.type_box.sizePolicy().hasHeightForWidth())
        self.type_box.setSizePolicy(sizePolicy4)
        self.horizontalLayout_2 = QHBoxLayout(self.type_box)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.type_list_box = QWidget(self.type_box)
        self.type_list_box.setObjectName(u"type_list_box")
        sizePolicy4.setHeightForWidth(self.type_list_box.sizePolicy().hasHeightForWidth())
        self.type_list_box.setSizePolicy(sizePolicy4)
        self.verticalLayout_3 = QVBoxLayout(self.type_list_box)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.type_label = QLabel(self.type_list_box)
        self.type_label.setObjectName(u"type_label")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.type_label.sizePolicy().hasHeightForWidth())
        self.type_label.setSizePolicy(sizePolicy5)
        self.type_label.setFont(font1)

        self.verticalLayout_3.addWidget(self.type_label)

        self.type_view = QListWidget(self.type_list_box)
        self.type_view.setObjectName(u"type_view")
        sizePolicy6 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.type_view.sizePolicy().hasHeightForWidth())
        self.type_view.setSizePolicy(sizePolicy6)
        self.type_view.setFont(font1)
        self.type_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.type_view.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.verticalLayout_3.addWidget(self.type_view)


        self.horizontalLayout_2.addWidget(self.type_list_box)

        self.type_description = QLabel(self.type_box)
        self.type_description.setObjectName(u"type_description")
        sizePolicy7 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy7.setHorizontalStretch(3)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.type_description.sizePolicy().hasHeightForWidth())
        self.type_description.setSizePolicy(sizePolicy7)
        font2 = QFont()
        font2.setPointSize(17)
        self.type_description.setFont(font2)
        self.type_description.setAlignment(Qt.AlignCenter)
        self.type_description.setWordWrap(True)

        self.horizontalLayout_2.addWidget(self.type_description)


        self.horizontalLayout_4.addWidget(self.type_box)

        self.sub_type_box = QWidget(self.type_and_sub_type_box)
        self.sub_type_box.setObjectName(u"sub_type_box")
        sizePolicy4.setHeightForWidth(self.sub_type_box.sizePolicy().hasHeightForWidth())
        self.sub_type_box.setSizePolicy(sizePolicy4)
        self.verticalLayout_5 = QVBoxLayout(self.sub_type_box)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(4, 0, 4, 0)
        self.sub_type_wrapper = QWidget(self.sub_type_box)
        self.sub_type_wrapper.setObjectName(u"sub_type_wrapper")
        sizePolicy1.setHeightForWidth(self.sub_type_wrapper.sizePolicy().hasHeightForWidth())
        self.sub_type_wrapper.setSizePolicy(sizePolicy1)
        self.horizontalLayout_3 = QHBoxLayout(self.sub_type_wrapper)
#ifndef Q_OS_MAC
        self.horizontalLayout_3.setSpacing(-1)
#endif
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.sub_type_list_box = QWidget(self.sub_type_wrapper)
        self.sub_type_list_box.setObjectName(u"sub_type_list_box")
        sizePolicy4.setHeightForWidth(self.sub_type_list_box.sizePolicy().hasHeightForWidth())
        self.sub_type_list_box.setSizePolicy(sizePolicy4)
        self.verticalLayout_4 = QVBoxLayout(self.sub_type_list_box)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.sub_type_label = QLabel(self.sub_type_list_box)
        self.sub_type_label.setObjectName(u"sub_type_label")
        sizePolicy5.setHeightForWidth(self.sub_type_label.sizePolicy().hasHeightForWidth())
        self.sub_type_label.setSizePolicy(sizePolicy5)
        self.sub_type_label.setFont(font1)

        self.verticalLayout_4.addWidget(self.sub_type_label)

        self.sub_type_view = QListWidget(self.sub_type_list_box)
        self.sub_type_view.setObjectName(u"sub_type_view")
        sizePolicy6.setHeightForWidth(self.sub_type_view.sizePolicy().hasHeightForWidth())
        self.sub_type_view.setSizePolicy(sizePolicy6)
        self.sub_type_view.setFont(font1)
        self.sub_type_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.sub_type_view.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.verticalLayout_4.addWidget(self.sub_type_view)


        self.horizontalLayout_3.addWidget(self.sub_type_list_box)

        self.sub_type_description = QLabel(self.sub_type_wrapper)
        self.sub_type_description.setObjectName(u"sub_type_description")
        sizePolicy7.setHeightForWidth(self.sub_type_description.sizePolicy().hasHeightForWidth())
        self.sub_type_description.setSizePolicy(sizePolicy7)
        self.sub_type_description.setFont(font2)
        self.sub_type_description.setAlignment(Qt.AlignCenter)
        self.sub_type_description.setWordWrap(True)

        self.horizontalLayout_3.addWidget(self.sub_type_description)


        self.verticalLayout_5.addWidget(self.sub_type_wrapper)


        self.horizontalLayout_4.addWidget(self.sub_type_box)


        self.verticalLayout.addWidget(self.type_and_sub_type_box)


        self.retranslateUi(CreateDataSourceType)

        QMetaObject.connectSlotsByName(CreateDataSourceType)
    # setupUi

    def retranslateUi(self, CreateDataSourceType):
        CreateDataSourceType.setWindowTitle(QCoreApplication.translate("CreateDataSourceType", u"CreateDataSourceType", None))
        self.label.setText(QCoreApplication.translate("CreateDataSourceType", u"Enter a name and select a type based on desired functionality", None))
        self.name_label.setText(QCoreApplication.translate("CreateDataSourceType", u"Name", None))
        self.type_label.setText(QCoreApplication.translate("CreateDataSourceType", u"Type:", None))
        self.type_description.setText(QCoreApplication.translate("CreateDataSourceType", u"Select a type to the left to view its description", None))
        self.sub_type_label.setText(QCoreApplication.translate("CreateDataSourceType", u"Sub-Type:", None))
        self.sub_type_description.setText(QCoreApplication.translate("CreateDataSourceType", u"Select a sub-type to the left to view its description", None))
    # retranslateUi

