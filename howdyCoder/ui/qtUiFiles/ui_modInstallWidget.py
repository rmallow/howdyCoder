# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'modInstallWidget.ui'
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
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QHBoxLayout, QHeaderView,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QTableView, QVBoxLayout, QWidget)

class Ui_ModInstallWidget(object):
    def setupUi(self, ModInstallWidget):
        if not ModInstallWidget.objectName():
            ModInstallWidget.setObjectName(u"ModInstallWidget")
        ModInstallWidget.resize(419, 393)
        self.verticalLayout = QVBoxLayout(ModInstallWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tableView = QTableView(ModInstallWidget)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.tableView.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout.addWidget(self.tableView)

        self.install_label = QLabel(ModInstallWidget)
        self.install_label.setObjectName(u"install_label")
        self.install_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.install_label)

        self.label = QLabel(ModInstallWidget)
        self.label.setObjectName(u"label")
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)

        self.label_2 = QLabel(ModInstallWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_2)

        self.widget = QWidget(ModInstallWidget)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.install_button = QPushButton(self.widget)
        self.install_button.setObjectName(u"install_button")

        self.horizontalLayout.addWidget(self.install_button)


        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(ModInstallWidget)

        QMetaObject.connectSlotsByName(ModInstallWidget)
    # setupUi

    def retranslateUi(self, ModInstallWidget):
        ModInstallWidget.setWindowTitle(QCoreApplication.translate("ModInstallWidget", u"Module Install Widget", None))
        self.install_label.setText(QCoreApplication.translate("ModInstallWidget", u"--- INSTALLING ---", None))
        self.label.setText(QCoreApplication.translate("ModInstallWidget", u"Install the modules that are missing. The name of the module and the package are not always the same (for example yaml is in the package PyYaml) so make sure to verify you are installing the correct package.  Edit the name of the package in the third column for missing modules.", None))
        self.label_2.setText(QCoreApplication.translate("ModInstallWidget", u"Hit Override to run without installing. (Not advised)", None))
        self.install_button.setText(QCoreApplication.translate("ModInstallWidget", u"Install", None))
    # retranslateUi

