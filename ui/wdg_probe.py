# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/cytu/usr/src/py/mycis/designer/wdg_probe.ui'
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

class Ui_wdg_probe(object):
    def setupUi(self, wdg_probe):
        wdg_probe.setObjectName(_fromUtf8("wdg_probe"))
        wdg_probe.resize(1364, 688)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Microsoft JhengHei"))
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        wdg_probe.setFont(font)
        wdg_probe.setWindowTitle(_fromUtf8(""))
        self.horizontalLayout = QtGui.QHBoxLayout(wdg_probe)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.spl = QtGui.QSplitter(wdg_probe)
        self.spl.setOrientation(QtCore.Qt.Vertical)
        self.spl.setObjectName(_fromUtf8("spl"))
        self.led_find = QtGui.QLineEdit(self.spl)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Noto Sans Mono CJK TC"))
        font.setBold(False)
        font.setWeight(50)
        self.led_find.setFont(font)
        self.led_find.setObjectName(_fromUtf8("led_find"))
        self.tbv_diag = QtGui.QTableView(self.spl)
        self.tbv_diag.setObjectName(_fromUtf8("tbv_diag"))
        self.tbv_ord = QtGui.QTableView(self.spl)
        self.tbv_ord.setObjectName(_fromUtf8("tbv_ord"))
        self.tbv_med = QtGui.QTableView(self.spl)
        self.tbv_med.setObjectName(_fromUtf8("tbv_med"))
        self.tbv_mat = QtGui.QTableView(self.spl)
        self.tbv_mat.setObjectName(_fromUtf8("tbv_mat"))
        self.horizontalLayout.addWidget(self.spl)

        self.retranslateUi(wdg_probe)
        QtCore.QMetaObject.connectSlotsByName(wdg_probe)

    def retranslateUi(self, wdg_probe):
        pass


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    wdg_probe = QtGui.QWidget()
    ui = Ui_wdg_probe()
    ui.setupUi(wdg_probe)
    wdg_probe.show()
    sys.exit(app.exec_())

