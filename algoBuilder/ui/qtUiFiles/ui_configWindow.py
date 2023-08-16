# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'configWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_ConfigWindow(object):
    def setupUi(self, ConfigWindow):
        if not ConfigWindow.objectName():
            ConfigWindow.setObjectName(u"ConfigWindow")
        ConfigWindow.resize(291, 127)
        self.verticalLayout = QVBoxLayout(ConfigWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(ConfigWindow)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.loadButton = QPushButton(self.widget)
        self.loadButton.setObjectName(u"loadButton")

        self.horizontalLayout.addWidget(self.loadButton)


        self.verticalLayout.addWidget(self.widget)

        self.config_edit = QLineEdit(ConfigWindow)
        self.config_edit.setObjectName(u"config_edit")
        self.config_edit.setReadOnly(True)

        self.verticalLayout.addWidget(self.config_edit)

        self.buttonBox = QDialogButtonBox(ConfigWindow)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(ConfigWindow)
        self.buttonBox.accepted.connect(ConfigWindow.accept)
        self.buttonBox.rejected.connect(ConfigWindow.reject)

        QMetaObject.connectSlotsByName(ConfigWindow)
    # setupUi

    def retranslateUi(self, ConfigWindow):
        ConfigWindow.setWindowTitle(QCoreApplication.translate("ConfigWindow", u"Config Loader", None))
        self.label.setText(QCoreApplication.translate("ConfigWindow", u"Config File:", None))
        self.loadButton.setText(QCoreApplication.translate("ConfigWindow", u"Select File", None))
    # retranslateUi

