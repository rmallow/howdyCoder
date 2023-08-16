# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QPushButton,
    QSizePolicy, QStackedWidget, QStatusBar, QToolBar,
    QVBoxLayout, QWidget)

from ..controlWidget import ControlWidget
from ..create.createWidget import CreateWidget
from ..mainOutputView import mainOutputView
from . import res_rc

class Ui_AlgoBuilder(object):
    def setupUi(self, AlgoBuilder):
        if not AlgoBuilder.objectName():
            AlgoBuilder.setObjectName(u"AlgoBuilder")
        AlgoBuilder.resize(800, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AlgoBuilder.sizePolicy().hasHeightForWidth())
        AlgoBuilder.setSizePolicy(sizePolicy)
        self.actionStart_All = QAction(AlgoBuilder)
        self.actionStart_All.setObjectName(u"actionStart_All")
        self.actionStart_All.setCheckable(False)
        self.actionStart_All.setMenuRole(QAction.NoRole)
        self.actionStatus = QAction(AlgoBuilder)
        self.actionStatus.setObjectName(u"actionStatus")
        self.actionStatus.setMenuRole(QAction.NoRole)
        self.actionLoad_Config = QAction(AlgoBuilder)
        self.actionLoad_Config.setObjectName(u"actionLoad_Config")
        self.actionLoad_Config.setMenuRole(QAction.NoRole)
        self.actionLogging = QAction(AlgoBuilder)
        self.actionLogging.setObjectName(u"actionLogging")
        self.actionLogging.setMenuRole(QAction.NoRole)
        self.actionEnd_All = QAction(AlgoBuilder)
        self.actionEnd_All.setObjectName(u"actionEnd_All")
        self.actionEnd_All.setMenuRole(QAction.NoRole)
        self.action_help_menu = QAction(AlgoBuilder)
        self.action_help_menu.setObjectName(u"action_help_menu")
        icon = QIcon()
        icon.addFile(u":/images/help.png", QSize(), QIcon.Normal, QIcon.Off)
        icon.addFile(u":/icons/help.png", QSize(), QIcon.Normal, QIcon.On)
        self.action_help_menu.setIcon(icon)
        self.action_help_menu.setMenuRole(QAction.TextHeuristicRole)
        self.invisible_action = QAction(AlgoBuilder)
        self.invisible_action.setObjectName(u"invisible_action")
        self.invisible_action.setMenuRole(QAction.NoRole)
        self.action_tutorial = QAction(AlgoBuilder)
        self.action_tutorial.setObjectName(u"action_tutorial")
        self.action_tutorial.setMenuRole(QAction.NoRole)
        self.action_documentation = QAction(AlgoBuilder)
        self.action_documentation.setObjectName(u"action_documentation")
        self.action_documentation.setMenuRole(QAction.NoRole)
        self.centralwidget = QWidget(AlgoBuilder)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.changePageButton = QPushButton(self.centralwidget)
        self.changePageButton.setObjectName(u"changePageButton")

        self.verticalLayout.addWidget(self.changePageButton)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.stackedWidget = QStackedWidget(self.widget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(6)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy1)
        self.controlPage = ControlWidget()
        self.controlPage.setObjectName(u"controlPage")
        self.stackedWidget.addWidget(self.controlPage)
        self.createPage = CreateWidget()
        self.createPage.setObjectName(u"createPage")
        self.stackedWidget.addWidget(self.createPage)
        self.outputPage = mainOutputView()
        self.outputPage.setObjectName(u"outputPage")
        self.stackedWidget.addWidget(self.outputPage)

        self.horizontalLayout.addWidget(self.stackedWidget)


        self.verticalLayout.addWidget(self.widget)

        AlgoBuilder.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(AlgoBuilder)
        self.statusbar.setObjectName(u"statusbar")
        AlgoBuilder.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(AlgoBuilder)
        self.toolBar.setObjectName(u"toolBar")
        self.toolBar.setMovable(False)
        self.toolBar.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.toolBar.setFloatable(False)
        AlgoBuilder.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.toolBar.addAction(self.actionStart_All)
        self.toolBar.addAction(self.actionEnd_All)
        self.toolBar.addAction(self.actionStatus)
        self.toolBar.addAction(self.actionLoad_Config)
        self.toolBar.addAction(self.actionLogging)
        self.toolBar.addAction(self.invisible_action)
        self.toolBar.addAction(self.action_help_menu)

        self.retranslateUi(AlgoBuilder)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(AlgoBuilder)
    # setupUi

    def retranslateUi(self, AlgoBuilder):
        AlgoBuilder.setWindowTitle(QCoreApplication.translate("AlgoBuilder", u"algoBuilder", None))
        self.actionStart_All.setText(QCoreApplication.translate("AlgoBuilder", u"Start All", None))
        self.actionStatus.setText(QCoreApplication.translate("AlgoBuilder", u"Status", None))
        self.actionLoad_Config.setText(QCoreApplication.translate("AlgoBuilder", u"Load Config", None))
        self.actionLogging.setText(QCoreApplication.translate("AlgoBuilder", u"Logging", None))
        self.actionEnd_All.setText(QCoreApplication.translate("AlgoBuilder", u"End All", None))
#if QT_CONFIG(tooltip)
        self.actionEnd_All.setToolTip(QCoreApplication.translate("AlgoBuilder", u"End All", None))
#endif // QT_CONFIG(tooltip)
        self.action_help_menu.setText(QCoreApplication.translate("AlgoBuilder", u"Help", None))
#if QT_CONFIG(tooltip)
        self.action_help_menu.setToolTip(QCoreApplication.translate("AlgoBuilder", u"Help", None))
#endif // QT_CONFIG(tooltip)
        self.invisible_action.setText("")
        self.action_tutorial.setText(QCoreApplication.translate("AlgoBuilder", u"Tutorial", None))
        self.action_documentation.setText(QCoreApplication.translate("AlgoBuilder", u"Documentation", None))
        self.changePageButton.setText(QCoreApplication.translate("AlgoBuilder", u"Go To Output Page", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("AlgoBuilder", u"toolBar", None))
    # retranslateUi

