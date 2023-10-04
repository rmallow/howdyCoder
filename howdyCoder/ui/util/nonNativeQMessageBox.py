from PySide6 import QtWidgets, QtCore


class NonNativeQMessageBox(QtWidgets.QMessageBox):
    def exec(self) -> int:
        QtCore.QCoreApplication.instance().setAttribute(
            QtCore.Qt.ApplicationAttribute.AA_DontUseNativeDialogs,
            True,
        )
        res = super().exec()
        QtCore.QCoreApplication.instance().setAttribute(
            QtCore.Qt.ApplicationAttribute.AA_DontUseNativeDialogs,
            False,
        )
        return res
