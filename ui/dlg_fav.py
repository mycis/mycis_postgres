# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/cytu/usr/src/py/mycis/designer/dlg_fav.ui'
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

class Ui_dlg_fav(object):
    def setupUi(self, dlg_fav):
        dlg_fav.setObjectName(_fromUtf8("dlg_fav"))
        dlg_fav.resize(548, 141)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Microsoft JhengHei"))
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        dlg_fav.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/res/img/favorites.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dlg_fav.setWindowIcon(icon)
        dlg_fav.setStyleSheet(_fromUtf8("font: 75 12pt \"Microsoft JhengHei\";"))
        dlg_fav.setSizeGripEnabled(True)
        self.horizontalLayout_3 = QtGui.QHBoxLayout(dlg_fav)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lbl_code = QtGui.QLabel(dlg_fav)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Microsoft JhengHei"))
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.lbl_code.setFont(font)
        self.lbl_code.setObjectName(_fromUtf8("lbl_code"))
        self.horizontalLayout.addWidget(self.lbl_code)
        self.led_code = QtGui.QLineEdit(dlg_fav)
        self.led_code.setText(_fromUtf8(""))
        self.led_code.setEchoMode(QtGui.QLineEdit.Normal)
        self.led_code.setObjectName(_fromUtf8("led_code"))
        self.horizontalLayout.addWidget(self.led_code)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.lbl_name = QtGui.QLabel(dlg_fav)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Microsoft JhengHei"))
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.lbl_name.setFont(font)
        self.lbl_name.setObjectName(_fromUtf8("lbl_name"))
        self.horizontalLayout_2.addWidget(self.lbl_name)
        self.led_name = QtGui.QLineEdit(dlg_fav)
        self.led_name.setText(_fromUtf8(""))
        self.led_name.setObjectName(_fromUtf8("led_name"))
        self.horizontalLayout_2.addWidget(self.led_name)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.bnb = QtGui.QDialogButtonBox(dlg_fav)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Microsoft JhengHei"))
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.bnb.setFont(font)
        self.bnb.setStyleSheet(_fromUtf8(""))
        self.bnb.setOrientation(QtCore.Qt.Horizontal)
        self.bnb.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.bnb.setCenterButtons(False)
        self.bnb.setObjectName(_fromUtf8("bnb"))
        self.gridLayout.addWidget(self.bnb, 2, 0, 1, 1)
        self.horizontalLayout_3.addLayout(self.gridLayout)
        self.lbl_code.setBuddy(self.led_code)
        self.lbl_name.setBuddy(self.led_name)

        self.retranslateUi(dlg_fav)
        QtCore.QObject.connect(self.bnb, QtCore.SIGNAL(_fromUtf8("accepted()")), dlg_fav.accept)
        QtCore.QObject.connect(self.bnb, QtCore.SIGNAL(_fromUtf8("rejected()")), dlg_fav.reject)
        QtCore.QMetaObject.connectSlotsByName(dlg_fav)

    def retranslateUi(self, dlg_fav):
        dlg_fav.setWindowTitle(_translate("dlg_fav", "新增代碼", None))
        self.lbl_code.setText(_translate("dlg_fav", "代碼", None))
        self.lbl_name.setText(_translate("dlg_fav", "名稱", None))

import mycis_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    dlg_fav = QtGui.QDialog()
    ui = Ui_dlg_fav()
    ui.setupUi(dlg_fav)
    dlg_fav.show()
    sys.exit(app.exec_())

