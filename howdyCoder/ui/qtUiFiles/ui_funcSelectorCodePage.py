# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'funcSelectorCodePage.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QLineEdit, QPlainTextEdit, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

from ..keyMonitorWidget import KeyMonitorWidget

class Ui_FuncSelectorCodePage(object):
    def setupUi(self, FuncSelectorCodePage):
        if not FuncSelectorCodePage.objectName():
            FuncSelectorCodePage.setObjectName(u"FuncSelectorCodePage")
        FuncSelectorCodePage.resize(985, 835)
        self.verticalLayout = QVBoxLayout(FuncSelectorCodePage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.key_monitor_widget = KeyMonitorWidget(FuncSelectorCodePage)
        self.key_monitor_widget.setObjectName(u"key_monitor_widget")

        self.verticalLayout.addWidget(self.key_monitor_widget)

        self.prompt_select_box = QWidget(FuncSelectorCodePage)
        self.prompt_select_box.setObjectName(u"prompt_select_box")
        self.horizontalLayout_4 = QHBoxLayout(self.prompt_select_box)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.prompt_label = QLabel(self.prompt_select_box)
        self.prompt_label.setObjectName(u"prompt_label")

        self.horizontalLayout_4.addWidget(self.prompt_label)

        self.prompt_combo_box = QComboBox(self.prompt_select_box)
        self.prompt_combo_box.setObjectName(u"prompt_combo_box")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.prompt_combo_box.sizePolicy().hasHeightForWidth())
        self.prompt_combo_box.setSizePolicy(sizePolicy)
        self.prompt_combo_box.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_4.addWidget(self.prompt_combo_box)

        self.horizontalSpacer_5 = QSpacerItem(461, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_5)


        self.verticalLayout.addWidget(self.prompt_select_box)

        self.infoLabel = QLabel(FuncSelectorCodePage)
        self.infoLabel.setObjectName(u"infoLabel")
        font = QFont()
        font.setPointSize(15)
        self.infoLabel.setFont(font)
        self.infoLabel.setWordWrap(True)

        self.verticalLayout.addWidget(self.infoLabel)

        self.promptBox = QWidget(FuncSelectorCodePage)
        self.promptBox.setObjectName(u"promptBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.promptBox.sizePolicy().hasHeightForWidth())
        self.promptBox.setSizePolicy(sizePolicy1)
        self.horizontalLayout_6 = QHBoxLayout(self.promptBox)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.prompt_text_edit = QPlainTextEdit(self.promptBox)
        self.prompt_text_edit.setObjectName(u"prompt_text_edit")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.prompt_text_edit.sizePolicy().hasHeightForWidth())
        self.prompt_text_edit.setSizePolicy(sizePolicy2)
        font1 = QFont()
        font1.setPointSize(16)
        self.prompt_text_edit.setFont(font1)
        self.prompt_text_edit.setTabStopDistance(4.000000000000000)

        self.horizontalLayout_6.addWidget(self.prompt_text_edit)

        self.label_2 = QLabel(self.promptBox)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_6.addWidget(self.label_2)

        self.widget_5 = QWidget(self.promptBox)
        self.widget_5.setObjectName(u"widget_5")
        self.verticalLayout_2 = QVBoxLayout(self.widget_5)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.create_new_api_button = QPushButton(self.widget_5)
        self.create_new_api_button.setObjectName(u"create_new_api_button")
        self.create_new_api_button.setEnabled(False)

        self.verticalLayout_2.addWidget(self.create_new_api_button)

        self.modify_api_button = QPushButton(self.widget_5)
        self.modify_api_button.setObjectName(u"modify_api_button")
        self.modify_api_button.setEnabled(False)

        self.verticalLayout_2.addWidget(self.modify_api_button)


        self.horizontalLayout_6.addWidget(self.widget_5)


        self.verticalLayout.addWidget(self.promptBox)

        self.widget_2 = QWidget(FuncSelectorCodePage)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout.addWidget(self.widget_2)

        self.prompt_error = QLabel(FuncSelectorCodePage)
        self.prompt_error.setObjectName(u"prompt_error")
        self.prompt_error.setStyleSheet(u"color:red;")

        self.verticalLayout.addWidget(self.prompt_error)

        self.widget_3 = QWidget(FuncSelectorCodePage)
        self.widget_3.setObjectName(u"widget_3")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.entry_function_label = QLabel(self.widget_3)
        self.entry_function_label.setObjectName(u"entry_function_label")

        self.horizontalLayout_3.addWidget(self.entry_function_label)

        self.entry_function_edit = QLineEdit(self.widget_3)
        self.entry_function_edit.setObjectName(u"entry_function_edit")

        self.horizontalLayout_3.addWidget(self.entry_function_edit)

        self.horizontalSpacer_3 = QSpacerItem(303, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addWidget(self.widget_3)

        self.label = QLabel(FuncSelectorCodePage)
        self.label.setObjectName(u"label")
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)

        self.code_edit_box = QWidget(FuncSelectorCodePage)
        self.code_edit_box.setObjectName(u"code_edit_box")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(5)
        sizePolicy3.setHeightForWidth(self.code_edit_box.sizePolicy().hasHeightForWidth())
        self.code_edit_box.setSizePolicy(sizePolicy3)
        self.horizontalLayout_5 = QHBoxLayout(self.code_edit_box)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.codeEdit = QPlainTextEdit(self.code_edit_box)
        self.codeEdit.setObjectName(u"codeEdit")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(10)
        sizePolicy4.setVerticalStretch(5)
        sizePolicy4.setHeightForWidth(self.codeEdit.sizePolicy().hasHeightForWidth())
        self.codeEdit.setSizePolicy(sizePolicy4)
        self.codeEdit.setFont(font1)
        self.codeEdit.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.codeEdit.setTabStopDistance(4.000000000000000)

        self.horizontalLayout_5.addWidget(self.codeEdit)


        self.verticalLayout.addWidget(self.code_edit_box)

        self.statusLabel = QLabel(FuncSelectorCodePage)
        self.statusLabel.setObjectName(u"statusLabel")
        self.statusLabel.setWordWrap(True)

        self.verticalLayout.addWidget(self.statusLabel)

        self.widget = QWidget(FuncSelectorCodePage)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(40, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.saveStatusLabel = QLabel(self.widget)
        self.saveStatusLabel.setObjectName(u"saveStatusLabel")

        self.horizontalLayout.addWidget(self.saveStatusLabel)

        self.saveButton = QPushButton(self.widget)
        self.saveButton.setObjectName(u"saveButton")

        self.horizontalLayout.addWidget(self.saveButton)

        self.selectButton = QPushButton(self.widget)
        self.selectButton.setObjectName(u"selectButton")

        self.horizontalLayout.addWidget(self.selectButton)


        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(FuncSelectorCodePage)

        QMetaObject.connectSlotsByName(FuncSelectorCodePage)
    # setupUi

    def retranslateUi(self, FuncSelectorCodePage):
        FuncSelectorCodePage.setWindowTitle(QCoreApplication.translate("FuncSelectorCodePage", u"FuncSelectorCodePage", None))
        self.prompt_label.setText(QCoreApplication.translate("FuncSelectorCodePage", u"Initial Prompt:", None))
        self.infoLabel.setText(QCoreApplication.translate("FuncSelectorCodePage", u"If using AI generation in app, enter your prompt here. Click Create New Function to create a new function based on the prompt below. Click Modify Function to modify the current entered code based on the prompt you've provided. Additional information will be given to the AI with your prompts to assist with making compatible code.", None))
        self.prompt_text_edit.setPlaceholderText(QCoreApplication.translate("FuncSelectorCodePage", u"AI prompt goes here.", None))
        self.label_2.setText(QCoreApplication.translate("FuncSelectorCodePage", u"Send to AI:", None))
        self.create_new_api_button.setText(QCoreApplication.translate("FuncSelectorCodePage", u"Create New Function", None))
        self.modify_api_button.setText(QCoreApplication.translate("FuncSelectorCodePage", u"Modify Function", None))
        self.prompt_error.setText("")
        self.entry_function_label.setText(QCoreApplication.translate("FuncSelectorCodePage", u"Entry Function Name:", None))
        self.label.setText(QCoreApplication.translate("FuncSelectorCodePage", u"If you are not using AI generation in app, paste your code will below. The code in the editor will be analyzed for compilation errors. If the AI provided an explanation it will be shown in the explanation expander. If your code has multiple functions, enter the entry function above. The AI generated code should handle this automatically.", None))
        self.codeEdit.setPlaceholderText(QCoreApplication.translate("FuncSelectorCodePage", u"Code goes here.", None))
        self.statusLabel.setText("")
        self.saveStatusLabel.setText("")
        self.saveButton.setText(QCoreApplication.translate("FuncSelectorCodePage", u"Save", None))
        self.selectButton.setText(QCoreApplication.translate("FuncSelectorCodePage", u"Select", None))
    # retranslateUi

