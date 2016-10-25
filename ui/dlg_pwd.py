# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/cytu/usr/src/py/mycis/designer/dlg_pwd.ui'
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

class Ui_dlg_pwd(object):
    def setupUi(self, dlg_pwd):
        dlg_pwd.setObjectName(_fromUtf8("dlg_pwd"))
        dlg_pwd.resize(351, 217)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Microsoft JhengHei"))
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        dlg_pwd.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/res/img/surgeon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dlg_pwd.setWindowIcon(icon)
        dlg_pwd.setStyleSheet(_fromUtf8("font: 75 12pt \"Microsoft JhengHei\";"))
        dlg_pwd.setSizeGripEnabled(True)
        self.horizontalLayout_5 = QtGui.QHBoxLayout(dlg_pwd)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lbl_user = QtGui.QLabel(dlg_pwd)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Microsoft JhengHei"))
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.lbl_user.setFont(font)
        self.lbl_user.setObjectName(_fromUtf8("lbl_user"))
        self.horizontalLayout.addWidget(self.lbl_user)
        self.led_user = QtGui.QLineEdit(dlg_pwd)
        self.led_user.setText(_fromUtf8(""))
        self.led_user.setEchoMode(QtGui.QLineEdit.Password)
        self.led_user.setObjectName(_fromUtf8("led_user"))
        self.horizontalLayout.addWidget(self.led_user)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.lbl_pwd = QtGui.QLabel(dlg_pwd)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Microsoft JhengHei"))
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.lbl_pwd.setFont(font)
        self.lbl_pwd.setObjectName(_fromUtf8("lbl_pwd"))
        self.horizontalLayout_2.addWidget(self.lbl_pwd)
        self.led_pwd = QtGui.QLineEdit(dlg_pwd)
        self.led_pwd.setText(_fromUtf8(""))
        self.led_pwd.setEchoMode(QtGui.QLineEdit.Password)
        self.led_pwd.setObjectName(_fromUtf8("led_pwd"))
        self.horizontalLayout_2.addWidget(self.led_pwd)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.lbl_pwd_2 = QtGui.QLabel(dlg_pwd)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Microsoft JhengHei"))
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.lbl_pwd_2.setFont(font)
        self.lbl_pwd_2.setObjectName(_fromUtf8("lbl_pwd_2"))
        self.horizontalLayout_3.addWidget(self.lbl_pwd_2)
        self.led_pwd_2 = QtGui.QLineEdit(dlg_pwd)
        self.led_pwd_2.setText(_fromUtf8(""))
        self.led_pwd_2.setEchoMode(QtGui.QLineEdit.Password)
        self.led_pwd_2.setObjectName(_fromUtf8("led_pwd_2"))
        self.horizontalLayout_3.addWidget(self.led_pwd_2)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)
        self.bnb = QtGui.QDialogButtonBox(dlg_pwd)
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
        self.gridLayout.addWidget(self.bnb, 4, 0, 1, 1)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.lbl_pwd_3 = QtGui.QLabel(dlg_pwd)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Microsoft JhengHei"))
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.lbl_pwd_3.setFont(font)
        self.lbl_pwd_3.setObjectName(_fromUtf8("lbl_pwd_3"))
        self.horizontalLayout_4.addWidget(self.lbl_pwd_3)
        self.led_pwd_3 = QtGui.QLineEdit(dlg_pwd)
        self.led_pwd_3.setText(_fromUtf8(""))
        self.led_pwd_3.setEchoMode(QtGui.QLineEdit.Password)
        self.led_pwd_3.setObjectName(_fromUtf8("led_pwd_3"))
        self.horizontalLayout_4.addWidget(self.led_pwd_3)
        self.gridLayout.addLayout(self.horizontalLayout_4, 3, 0, 1, 1)
        self.horizontalLayout_5.addLayout(self.gridLayout)
        self.lbl_user.setBuddy(self.led_user)
        self.lbl_pwd.setBuddy(self.led_pwd)
        self.lbl_pwd_2.setBuddy(self.led_pwd_2)
        self.lbl_pwd_3.setBuddy(self.led_pwd_3)

        self.retranslateUi(dlg_pwd)
        QtCore.QObject.connect(self.bnb, QtCore.SIGNAL(_fromUtf8("accepted()")), dlg_pwd.accept)
        QtCore.QObject.connect(self.bnb, QtCore.SIGNAL(_fromUtf8("rejected()")), dlg_pwd.reject)
        QtCore.QMetaObject.connectSlotsByName(dlg_pwd)

    def retranslateUi(self, dlg_pwd):
        dlg_pwd.setWindowTitle(_translate("dlg_pwd", "新增用戶", None))
        self.lbl_user.setText(_translate("dlg_pwd", "用戶名", None))
        self.lbl_pwd.setText(_translate("dlg_pwd", "舊密碼", None))
        self.lbl_pwd_2.setText(_translate("dlg_pwd", "新密碼", None))
        self.lbl_pwd_3.setText(_translate("dlg_pwd", "新密碼", None))

import mycis_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    dlg_pwd = QtGui.QDialog()
    ui = Ui_dlg_pwd()
    ui.setupUi(dlg_pwd)
    dlg_pwd.show()
    sys.exit(app.exec_())

