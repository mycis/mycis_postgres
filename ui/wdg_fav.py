# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/cytu/usr/src/py/mycis/designer/wdg_fav.ui'
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

class Ui_wdg_fav(object):
    def setupUi(self, wdg_fav):
        wdg_fav.setObjectName(_fromUtf8("wdg_fav"))
        wdg_fav.resize(1364, 688)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Microsoft JhengHei"))
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        wdg_fav.setFont(font)
        wdg_fav.setWindowTitle(_fromUtf8(""))
        self.horizontalLayout = QtGui.QHBoxLayout(wdg_fav)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.spl_2 = QtGui.QSplitter(wdg_fav)
        self.spl_2.setOrientation(QtCore.Qt.Horizontal)
        self.spl_2.setObjectName(_fromUtf8("spl_2"))
        self.tbv_fav = QtGui.QTableView(self.spl_2)
        self.tbv_fav.setObjectName(_fromUtf8("tbv_fav"))
        self.spl_1 = QtGui.QSplitter(self.spl_2)
        self.spl_1.setOrientation(QtCore.Qt.Vertical)
        self.spl_1.setObjectName(_fromUtf8("spl_1"))
        self.led_find = QtGui.QLineEdit(self.spl_1)
        self.led_find.setObjectName(_fromUtf8("led_find"))
        self.tbv_diag = QtGui.QTableView(self.spl_1)
        self.tbv_diag.setObjectName(_fromUtf8("tbv_diag"))
        self.tbv_ord = QtGui.QTableView(self.spl_1)
        self.tbv_ord.setObjectName(_fromUtf8("tbv_ord"))
        self.tbv_med = QtGui.QTableView(self.spl_1)
        self.tbv_med.setObjectName(_fromUtf8("tbv_med"))
        self.tbv_mat = QtGui.QTableView(self.spl_1)
        self.tbv_mat.setObjectName(_fromUtf8("tbv_mat"))
        self.horizontalLayout.addWidget(self.spl_2)

        self.retranslateUi(wdg_fav)
        QtCore.QMetaObject.connectSlotsByName(wdg_fav)

    def retranslateUi(self, wdg_fav):
        pass


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    wdg_fav = QtGui.QWidget()
    ui = Ui_wdg_fav()
    ui.setupUi(wdg_fav)
    wdg_fav.show()
    sys.exit(app.exec_())

