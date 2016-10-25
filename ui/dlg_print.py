# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/cytu/usr/src/py/mycis/designer/dlg_print.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_dlg_print(object):
    def setupUi(self, dlg_print):
        dlg_print.setObjectName(_fromUtf8("dlg_print"))
        dlg_print.resize(521, 331)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Microsoft JhengHei"))
        font.setPointSize(12)
        dlg_print.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/res/img/printer.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dlg_print.setWindowIcon(icon)
        self.gridLayout = QtGui.QGridLayout(dlg_print)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tbv = QtGui.QTableView(dlg_print)
        self.tbv.setObjectName(_fromUtf8("tbv"))
        self.gridLayout.addWidget(self.tbv, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(dlg_print)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(dlg_print)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), dlg_print.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), dlg_print.reject)
        QtCore.QMetaObject.connectSlotsByName(dlg_print)

    def retranslateUi(self, dlg_print):
        dlg_print.setWindowTitle(_translate("dlg_print", "列印選擇", None))

import mycis_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    dlg_print = QtGui.QDialog()
    ui = Ui_dlg_print()
    ui.setupUi(dlg_print)
    dlg_print.show()
    sys.exit(app.exec_())

