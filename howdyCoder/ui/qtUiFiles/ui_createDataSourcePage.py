# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'createDataSourcePage.ui'
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
    QSizePolicy, QSpacerItem, QStackedWidget, QVBoxLayout,
    QWidget)

class Ui_CreateDataSourcePage(object):
    def setupUi(self, CreateDataSourcePage):
        if not CreateDataSourcePage.objectName():
            CreateDataSourcePage.setObjectName(u"CreateDataSourcePage")
        CreateDataSourcePage.resize(785, 609)
        self.verticalLayout = QVBoxLayout(CreateDataSourcePage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(CreateDataSourcePage)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.stackedWidget = QStackedWidget(CreateDataSourcePage)
        self.stackedWidget.setObjectName(u"stackedWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setMinimumSize(QSize(0, 150))

        self.verticalLayout.addWidget(self.stackedWidget)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.output_box = QWidget(CreateDataSourcePage)
        self.output_box.setObjectName(u"output_box")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.output_box.sizePolicy().hasHeightForWidth())
        self.output_box.setSizePolicy(sizePolicy1)
        self.verticalLayout_2 = QVBoxLayout(self.output_box)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_3 = QLabel(self.output_box)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)
        self.label_3.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_3)

        self.outputHelpText = QLabel(self.output_box)
        self.outputHelpText.setObjectName(u"outputHelpText")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.outputHelpText.sizePolicy().hasHeightForWidth())
        self.outputHelpText.setSizePolicy(sizePolicy2)
        font1 = QFont()
        font1.setPointSize(15)
        self.outputHelpText.setFont(font1)
        self.outputHelpText.setAlignment(Qt.AlignCenter)
        self.outputHelpText.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.outputHelpText)

        self.suggested_output_box = QWidget(self.output_box)
        self.suggested_output_box.setObjectName(u"suggested_output_box")
        sizePolicy2.setHeightForWidth(self.suggested_output_box.sizePolicy().hasHeightForWidth())
        self.suggested_output_box.setSizePolicy(sizePolicy2)
        self.horizontalLayout = QHBoxLayout(self.suggested_output_box)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(self.suggested_output_box)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.suggested_output = QListWidget(self.suggested_output_box)
        self.suggested_output.setObjectName(u"suggested_output")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(1)
        sizePolicy3.setHeightForWidth(self.suggested_output.sizePolicy().hasHeightForWidth())
        self.suggested_output.setSizePolicy(sizePolicy3)
        self.suggested_output.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.suggested_output.setSelectionMode(QAbstractItemView.NoSelection)
        self.suggested_output.setFlow(QListView.LeftToRight)

        self.horizontalLayout.addWidget(self.suggested_output)


        self.verticalLayout_2.addWidget(self.suggested_output_box)

        self.widget_8 = QWidget(self.output_box)
        self.widget_8.setObjectName(u"widget_8")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_8)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.addOutputButton = QPushButton(self.widget_8)
        self.addOutputButton.setObjectName(u"addOutputButton")
        sizePolicy4 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.addOutputButton.sizePolicy().hasHeightForWidth())
        self.addOutputButton.setSizePolicy(sizePolicy4)

        self.horizontalLayout_5.addWidget(self.addOutputButton)

        self.removeOutputButton = QPushButton(self.widget_8)
        self.removeOutputButton.setObjectName(u"removeOutputButton")
        sizePolicy4.setHeightForWidth(self.removeOutputButton.sizePolicy().hasHeightForWidth())
        self.removeOutputButton.setSizePolicy(sizePolicy4)

        self.horizontalLayout_5.addWidget(self.removeOutputButton)


        self.verticalLayout_2.addWidget(self.widget_8)

        self.outputView = QListView(self.output_box)
        self.outputView.setObjectName(u"outputView")
        sizePolicy5 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(2)
        sizePolicy5.setHeightForWidth(self.outputView.sizePolicy().hasHeightForWidth())
        self.outputView.setSizePolicy(sizePolicy5)
        font2 = QFont()
        font2.setPointSize(30)
        self.outputView.setFont(font2)

        self.verticalLayout_2.addWidget(self.outputView)


        self.verticalLayout.addWidget(self.output_box)


        self.retranslateUi(CreateDataSourcePage)

        QMetaObject.connectSlotsByName(CreateDataSourcePage)
    # setupUi

    def retranslateUi(self, CreateDataSourcePage):
        CreateDataSourcePage.setWindowTitle(QCoreApplication.translate("CreateDataSourcePage", u"CreateDataSourcePage", None))
        self.label.setText(QCoreApplication.translate("CreateDataSourcePage", u"Setup Data Source", None))
        self.label_3.setText(QCoreApplication.translate("CreateDataSourcePage", u"Determine Output", None))
        self.outputHelpText.setText(QCoreApplication.translate("CreateDataSourcePage", u"The AI will do its best to determine what data the function wil output. You will then need to input these suggestions into the bottom table using the add/remove buttons.\n"
"Ocassionally the AI will not give the output, or wrong output, you will need to look at the return value of the function to determine the output in this case. Consult the user manual for more info.", None))
        self.label_2.setText(QCoreApplication.translate("CreateDataSourcePage", u"Output Suggestions:", None))
        self.addOutputButton.setText(QCoreApplication.translate("CreateDataSourcePage", u"Add", None))
        self.removeOutputButton.setText(QCoreApplication.translate("CreateDataSourcePage", u"Remove", None))
    # retranslateUi

