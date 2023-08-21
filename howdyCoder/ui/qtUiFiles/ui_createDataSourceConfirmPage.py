# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'createDataSourceConfirmPage.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPlainTextEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_CreateDataSourceConfirmPage(object):
    def setupUi(self, CreateDataSourceConfirmPage):
        if not CreateDataSourceConfirmPage.objectName():
            CreateDataSourceConfirmPage.setObjectName(u"CreateDataSourceConfirmPage")
        CreateDataSourceConfirmPage.resize(540, 329)
        self.verticalLayout = QVBoxLayout(CreateDataSourceConfirmPage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(CreateDataSourceConfirmPage)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)

        self.configTextView = QPlainTextEdit(CreateDataSourceConfirmPage)
        self.configTextView.setObjectName(u"configTextView")
        self.configTextView.setFont(font)
        self.configTextView.setUndoRedoEnabled(False)
        self.configTextView.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.verticalLayout.addWidget(self.configTextView)

        self.label_2 = QLabel(CreateDataSourceConfirmPage)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_2)

        self.buttonWidget = QWidget(CreateDataSourceConfirmPage)
        self.buttonWidget.setObjectName(u"buttonWidget")
        self.horizontalLayout = QHBoxLayout(self.buttonWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.confirmButton = QPushButton(self.buttonWidget)
        self.confirmButton.setObjectName(u"confirmButton")

        self.horizontalLayout.addWidget(self.confirmButton)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.addButton = QPushButton(self.buttonWidget)
        self.addButton.setObjectName(u"addButton")

        self.horizontalLayout.addWidget(self.addButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addWidget(self.buttonWidget)


        self.retranslateUi(CreateDataSourceConfirmPage)

        QMetaObject.connectSlotsByName(CreateDataSourceConfirmPage)
    # setupUi

    def retranslateUi(self, CreateDataSourceConfirmPage):
        CreateDataSourceConfirmPage.setWindowTitle(QCoreApplication.translate("CreateDataSourceConfirmPage", u"CreateDataSourceConfirmPage", None))
        self.label.setText(QCoreApplication.translate("CreateDataSourceConfirmPage", u"The final config for your data source. Confirm to add or use the back buttons to go back and modify.", None))
        self.label_2.setText("")
        self.confirmButton.setText(QCoreApplication.translate("CreateDataSourceConfirmPage", u"Confirm", None))
        self.addButton.setText(QCoreApplication.translate("CreateDataSourceConfirmPage", u"Add Another", None))
    # retranslateUi

