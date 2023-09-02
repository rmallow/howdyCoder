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

class Ui_FuncSelectorCodePage(object):
    def setupUi(self, FuncSelectorCodePage):
        if not FuncSelectorCodePage.objectName():
            FuncSelectorCodePage.setObjectName(u"FuncSelectorCodePage")
        FuncSelectorCodePage.resize(759, 637)
        self.verticalLayout = QVBoxLayout(FuncSelectorCodePage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.infoLabel = QLabel(FuncSelectorCodePage)
        self.infoLabel.setObjectName(u"infoLabel")
        self.infoLabel.setWordWrap(True)

        self.verticalLayout.addWidget(self.infoLabel)

        self.widget_4 = QWidget(FuncSelectorCodePage)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 4, 0, 4)
        self.prompt_label = QLabel(self.widget_4)
        self.prompt_label.setObjectName(u"prompt_label")

        self.horizontalLayout_4.addWidget(self.prompt_label)

        self.prompt_combo_box = QComboBox(self.widget_4)
        self.prompt_combo_box.setObjectName(u"prompt_combo_box")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.prompt_combo_box.sizePolicy().hasHeightForWidth())
        self.prompt_combo_box.setSizePolicy(sizePolicy)
        self.prompt_combo_box.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_4.addWidget(self.prompt_combo_box)

        self.horizontalSpacer_5 = QSpacerItem(437, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_5)


        self.verticalLayout.addWidget(self.widget_4)

        self.prompt_text_edit = QPlainTextEdit(FuncSelectorCodePage)
        self.prompt_text_edit.setObjectName(u"prompt_text_edit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(2)
        sizePolicy1.setHeightForWidth(self.prompt_text_edit.sizePolicy().hasHeightForWidth())
        self.prompt_text_edit.setSizePolicy(sizePolicy1)
        self.prompt_text_edit.setTabStopDistance(4.000000000000000)

        self.verticalLayout.addWidget(self.prompt_text_edit)

        self.widget_2 = QWidget(FuncSelectorCodePage)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)

        self.call_api_button = QPushButton(self.widget_2)
        self.call_api_button.setObjectName(u"call_api_button")

        self.horizontalLayout_2.addWidget(self.call_api_button)

        self.horizontalSpacer_2 = QSpacerItem(304, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addWidget(self.widget_2)

        self.widget_3 = QWidget(FuncSelectorCodePage)
        self.widget_3.setObjectName(u"widget_3")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 4)
        self.entry_function_label = QLabel(self.widget_3)
        self.entry_function_label.setObjectName(u"entry_function_label")

        self.horizontalLayout_3.addWidget(self.entry_function_label)

        self.entry_function_edit = QLineEdit(self.widget_3)
        self.entry_function_edit.setObjectName(u"entry_function_edit")

        self.horizontalLayout_3.addWidget(self.entry_function_edit)

        self.horizontalSpacer_3 = QSpacerItem(291, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addWidget(self.widget_3)

        self.label = QLabel(FuncSelectorCodePage)
        self.label.setObjectName(u"label")
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)

        self.codeEdit = QPlainTextEdit(FuncSelectorCodePage)
        self.codeEdit.setObjectName(u"codeEdit")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(5)
        sizePolicy2.setHeightForWidth(self.codeEdit.sizePolicy().hasHeightForWidth())
        self.codeEdit.setSizePolicy(sizePolicy2)
        self.codeEdit.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.codeEdit.setTabStopDistance(4.000000000000000)

        self.verticalLayout.addWidget(self.codeEdit)

        self.statusLabel = QLabel(FuncSelectorCodePage)
        self.statusLabel.setObjectName(u"statusLabel")
        self.statusLabel.setWordWrap(True)

        self.verticalLayout.addWidget(self.statusLabel)

        self.widget = QWidget(FuncSelectorCodePage)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

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
        self.infoLabel.setText(QCoreApplication.translate("FuncSelectorCodePage", u"Paste code or query the API to generate code for you. The bottom editor will check that the code compiles and is compatible. If there is an error, the error message will be displayed at the bottom. Based on the type of function you are requesting from the API select an initial prompt from the combo box below.", None))
        self.prompt_label.setText(QCoreApplication.translate("FuncSelectorCodePage", u"Initial Prompt:", None))
        self.prompt_text_edit.setPlaceholderText(QCoreApplication.translate("FuncSelectorCodePage", u"AI prompt goes here.", None))
        self.call_api_button.setText(QCoreApplication.translate("FuncSelectorCodePage", u"Send to AI", None))
        self.entry_function_label.setText(QCoreApplication.translate("FuncSelectorCodePage", u"Entry Function Name:", None))
        self.label.setText(QCoreApplication.translate("FuncSelectorCodePage", u"Only have code entered in the text edit box below. If there is more than just code, such as AI explanation, delete that. Oftentimes AI will generate a main function with helper functions, enter the entry point function that is supposed to be called first in the box above. This function name must be found in the code below.", None))
        self.codeEdit.setPlaceholderText(QCoreApplication.translate("FuncSelectorCodePage", u"Code goes here.", None))
        self.statusLabel.setText("")
        self.saveStatusLabel.setText("")
        self.saveButton.setText(QCoreApplication.translate("FuncSelectorCodePage", u"Save", None))
        self.selectButton.setText(QCoreApplication.translate("FuncSelectorCodePage", u"Select", None))
    # retranslateUi

