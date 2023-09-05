from PySide6 import QtWidgets, QtCore, QtGui


class HorizontalExpander(QtWidgets.QWidget):
    def __init__(self, parent=None, title="", animationDuration=300):
        super().__init__(parent=parent)

        self.animationDuration = animationDuration
        self.toggleAnimation = QtCore.QParallelAnimationGroup()
        self.contentArea = QtWidgets.QScrollArea()
        self.toggleButton = QtWidgets.QToolButton()
        self.mainLayout = QtWidgets.QHBoxLayout()

        self.toggleButton.setStyleSheet("QToolButton { border: none; }")
        self.toggleButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toggleButton.setArrowType(QtCore.Qt.RightArrow)
        self.toggleButton.setText(str(title))
        self.toggleButton.setCheckable(True)
        self.toggleButton.setChecked(False)

        self.contentArea.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding
        )
        # start out collapsed
        self.contentArea.setMaximumWidth(0)
        self.contentArea.setMinimumWidth(0)
        # let the entire widget grow and shrink with its content
        self.toggleAnimation = self.toggleAnimation
        self.toggleAnimation.addAnimation(
            QtCore.QPropertyAnimation(self, b"minimumWidth")
        )
        self.toggleAnimation.addAnimation(
            QtCore.QPropertyAnimation(self, b"maximumWidth")
        )
        self.toggleAnimation.addAnimation(
            QtCore.QPropertyAnimation(self.contentArea, b"maximumWidth")
        )
        # don't waste space
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.addWidget(self.toggleButton, QtCore.Qt.AlignLeft)
        self.mainLayout.addWidget(self.contentArea)
        self.setLayout(self.mainLayout)

        def start_animation(checked):
            arrow_type = QtCore.Qt.DownArrow if checked else QtCore.Qt.RightArrow
            direction = (
                QtCore.QAbstractAnimation.Forward
                if checked
                else QtCore.QAbstractAnimation.Backward
            )
            self.toggleButton.setArrowType(arrow_type)
            self.toggleAnimation.setDirection(direction)
            self.toggleAnimation.start()

        self.toggleButton.clicked.connect(start_animation)

    def setContentLayout(self, contentLayout):
        self.contentArea.destroy()
        self.contentArea.setLayout(contentLayout)
        collapsedWidth = self.sizeHint().width() - self.contentArea.maximumWidth()
        contentWidth = contentLayout.sizeHint().width()
        for i in range(self.toggleAnimation.animationCount() - 1):
            expandAnimation = self.toggleAnimation.animationAt(i)
            expandAnimation.setDuration(self.animationDuration)
            expandAnimation.setStartValue(collapsedWidth)
            expandAnimation.setEndValue(collapsedWidth + contentWidth)
        contentAnimation = self.toggleAnimation.animationAt(
            self.toggleAnimation.animationCount() - 1
        )
        contentAnimation.setDuration(self.animationDuration)
        contentAnimation.setStartValue(0)
        contentAnimation.setEndValue(contentWidth)
