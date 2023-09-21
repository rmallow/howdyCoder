# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'createDataSourceSettingsPage.ui'
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
    QListView, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QStackedWidget, QVBoxLayout, QWidget)

class Ui_CreateDataSourceSettingsPage(object):
    def setupUi(self, CreateDataSourceSettingsPage):
        if not CreateDataSourceSettingsPage.objectName():
            CreateDataSourceSettingsPage.setObjectName(u"CreateDataSourceSettingsPage")
        CreateDataSourceSettingsPage.resize(785, 609)
        self.verticalLayout = QVBoxLayout(CreateDataSourceSettingsPage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(CreateDataSourceSettingsPage)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.stackedWidget = QStackedWidget(CreateDataSourceSettingsPage)
        self.stackedWidget.setObjectName(u"stackedWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.stackedWidget)

        self.outputHelpText = QLabel(CreateDataSourceSettingsPage)
        self.outputHelpText.setObjectName(u"outputHelpText")
        sizePolicy.setHeightForWidth(self.outputHelpText.sizePolicy().hasHeightForWidth())
        self.outputHelpText.setSizePolicy(sizePolicy)
        self.outputHelpText.setAlignment(Qt.AlignCenter)
        self.outputHelpText.setWordWrap(True)

        self.verticalLayout.addWidget(self.outputHelpText)

        self.suggested_output_box = QWidget(CreateDataSourceSettingsPage)
        self.suggested_output_box.setObjectName(u"suggested_output_box")
        sizePolicy.setHeightForWidth(self.suggested_output_box.sizePolicy().hasHeightForWidth())
        self.suggested_output_box.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(self.suggested_output_box)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(self.suggested_output_box)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.suggested_output = QListWidget(self.suggested_output_box)
        self.suggested_output.setObjectName(u"suggested_output")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.suggested_output.sizePolicy().hasHeightForWidth())
        self.suggested_output.setSizePolicy(sizePolicy1)
        self.suggested_output.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.suggested_output.setSelectionMode(QAbstractItemView.NoSelection)
        self.suggested_output.setFlow(QListView.LeftToRight)

        self.horizontalLayout.addWidget(self.suggested_output)


        self.verticalLayout.addWidget(self.suggested_output_box)

        self.outputView = QListView(CreateDataSourceSettingsPage)
        self.outputView.setObjectName(u"outputView")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(2)
        sizePolicy2.setHeightForWidth(self.outputView.sizePolicy().hasHeightForWidth())
        self.outputView.setSizePolicy(sizePolicy2)
        font = QFont()
        font.setPointSize(30)
        self.outputView.setFont(font)

        self.verticalLayout.addWidget(self.outputView)

        self.widget_8 = QWidget(CreateDataSourceSettingsPage)
        self.widget_8.setObjectName(u"widget_8")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_8)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.addOutputButton = QPushButton(self.widget_8)
        self.addOutputButton.setObjectName(u"addOutputButton")
        sizePolicy3 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.addOutputButton.sizePolicy().hasHeightForWidth())
        self.addOutputButton.setSizePolicy(sizePolicy3)

        self.horizontalLayout_5.addWidget(self.addOutputButton)

        self.removeOutputButton = QPushButton(self.widget_8)
        self.removeOutputButton.setObjectName(u"removeOutputButton")
        sizePolicy3.setHeightForWidth(self.removeOutputButton.sizePolicy().hasHeightForWidth())
        self.removeOutputButton.setSizePolicy(sizePolicy3)

        self.horizontalLayout_5.addWidget(self.removeOutputButton)


        self.verticalLayout.addWidget(self.widget_8)


        self.retranslateUi(CreateDataSourceSettingsPage)

        QMetaObject.connectSlotsByName(CreateDataSourceSettingsPage)
    # setupUi

    def retranslateUi(self, CreateDataSourceSettingsPage):
        CreateDataSourceSettingsPage.setWindowTitle(QCoreApplication.translate("CreateDataSourceSettingsPage", u"CreateDataSourceSettingsPage", None))
        self.label.setText(QCoreApplication.translate("CreateDataSourceSettingsPage", u"Select settings for the data source", None))
        self.outputHelpText.setText(QCoreApplication.translate("CreateDataSourceSettingsPage", u"Since functions are able to be made outside of this environment, this setup wizard can't tell you what data the function will output, unless the AI that generates the code specifies.\n"
"If the AI did specify, we have added these to the suggestion box and you can add them to the output box using the + and - buttons here.\n"
"After adding the outputs, double click them to change their names.\n"
"If you don't do this you won't be able to see the data from this data source.\n"
"For further questions, consult the user manual.", None))
        self.label_2.setText(QCoreApplication.translate("CreateDataSourceSettingsPage", u"Output Suggestions:", None))
        self.addOutputButton.setText(QCoreApplication.translate("CreateDataSourceSettingsPage", u"+", None))
        self.removeOutputButton.setText(QCoreApplication.translate("CreateDataSourceSettingsPage", u"-", None))
    # retranslateUi

