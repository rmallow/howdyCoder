# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'outputViewFeed.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QTableView, QVBoxLayout,
    QWidget)

class Ui_OutputViewFeed(object):
    def setupUi(self, OutputViewFeed):
        if not OutputViewFeed.objectName():
            OutputViewFeed.setObjectName(u"OutputViewFeed")
        OutputViewFeed.resize(690, 444)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(OutputViewFeed.sizePolicy().hasHeightForWidth())
        OutputViewFeed.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(OutputViewFeed)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.filterWidget = QWidget(OutputViewFeed)
        self.filterWidget.setObjectName(u"filterWidget")
        self.horizontalLayout = QHBoxLayout(self.filterWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.filterWidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.filterEdit = QLineEdit(self.filterWidget)
        self.filterEdit.setObjectName(u"filterEdit")
        self.filterEdit.setClearButtonEnabled(True)

        self.horizontalLayout.addWidget(self.filterEdit)

        self.filterButton = QPushButton(self.filterWidget)
        self.filterButton.setObjectName(u"filterButton")

        self.horizontalLayout.addWidget(self.filterButton)

        self.horizontalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.showIndexBox = QCheckBox(self.filterWidget)
        self.showIndexBox.setObjectName(u"showIndexBox")

        self.horizontalLayout.addWidget(self.showIndexBox)

        self.horizontalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.word_wrap_box = QCheckBox(self.filterWidget)
        self.word_wrap_box.setObjectName(u"word_wrap_box")
        self.word_wrap_box.setChecked(True)

        self.horizontalLayout.addWidget(self.word_wrap_box)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addWidget(self.filterWidget)

        self.tableView = QTableView(OutputViewFeed)
        self.tableView.setObjectName(u"tableView")
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tableView.sizePolicy().hasHeightForWidth())
        self.tableView.setSizePolicy(sizePolicy1)
        self.tableView.setMaximumSize(QSize(16777215, 16777215))
        self.tableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableView.horizontalHeader().setMinimumSectionSize(100)
        self.tableView.verticalHeader().setDefaultSectionSize(50)

        self.verticalLayout.addWidget(self.tableView)


        self.retranslateUi(OutputViewFeed)

        QMetaObject.connectSlotsByName(OutputViewFeed)
    # setupUi

    def retranslateUi(self, OutputViewFeed):
        OutputViewFeed.setWindowTitle(QCoreApplication.translate("OutputViewFeed", u"outputViewFeed", None))
        self.label.setText(QCoreApplication.translate("OutputViewFeed", u"Filter:", None))
        self.filterButton.setText(QCoreApplication.translate("OutputViewFeed", u"Apply Filter", None))
        self.showIndexBox.setText(QCoreApplication.translate("OutputViewFeed", u"Show Index", None))
        self.word_wrap_box.setText(QCoreApplication.translate("OutputViewFeed", u"Show All Text", None))
    # retranslateUi

