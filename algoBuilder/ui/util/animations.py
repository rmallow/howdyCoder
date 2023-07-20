from PySide2 import QtWidgets, QtCore


def fadeStart(obj, fromWidget, toWidget, layout, finishedSlot=None):
    setattr(obj, "_utilEffect", QtWidgets.QGraphicsOpacityEffect(fromWidget))
    fromWidget.setGraphicsEffect(obj._utilEffect)
    setattr(
        obj,
        "_utilAnimation",
        QtCore.QPropertyAnimation(
            fromWidget.graphicsEffect(), QtCore.QByteArray(b"opacity")
        ),
    )
    obj._utilAnimation.setDuration(500)
    obj._utilAnimation.setStartValue(1)
    obj._utilAnimation.setEndValue(0)
    obj._utilAnimation.setEasingCurve(QtCore.QEasingCurve.Linear)
    obj._utilAnimation.finished.connect(
        lambda: fadeEnd(obj, fromWidget, toWidget, layout, finishedSlot=finishedSlot)
    )
    obj._utilAnimation.start()


def fadeEnd(obj, fromWidget, toWidget, layout, finishedSlot=None):
    layout.replaceWidget(fromWidget, toWidget)
    fromWidget.hide()
    toWidget.show()
    setattr(obj, "_utilEffect", QtWidgets.QGraphicsOpacityEffect(toWidget))
    toWidget.setGraphicsEffect(obj._utilEffect)
    setattr(
        obj,
        "_utilAnimation",
        QtCore.QPropertyAnimation(
            toWidget.graphicsEffect(), QtCore.QByteArray(b"opacity")
        ),
    )
    obj._utilAnimation.setDuration(500)
    obj._utilAnimation.setStartValue(0)
    obj._utilAnimation.setEndValue(1)
    obj._utilAnimation.setEasingCurve(QtCore.QEasingCurve.Linear)
    obj._utilAnimation.finished.connect(lambda: obj._utilEffect.deleteLater())
    if finishedSlot is not None:
        obj._utilAnimation.finished.connect(finishedSlot)
    obj._utilAnimation.start()
