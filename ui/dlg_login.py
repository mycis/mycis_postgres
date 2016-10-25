# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/cytu/usr/src/py/mycis/designer/dlg_login.ui'
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

class Ui_dlg_login(object):
    def setupUi(self, dlg_login):
        dlg_login.setObjectName(_fromUtf8("dlg_login"))
        dlg_login.resize(380, 137)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Microsoft JhengHei"))
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        dlg_login.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/res/img/surgeon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dlg_login.setWindowIcon(icon)
        dlg_login.setStyleSheet(_fromUtf8("font: 75 12pt \"Microsoft JhengHei\";"))
        self.verticalLayout = QtGui.QVBoxLayout(dlg_login)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lbl_user = QtGui.QLabel(dlg_login)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_user.sizePolicy().hasHeightForWidth())
        self.lbl_user.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Microsoft JhengHei"))
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.lbl_user.setFont(font)
        self.lbl_user.setObjectName(_fromUtf8("lbl_user"))
        self.horizontalLayout.addWidget(self.lbl_user)
        self.cmb_user = QtGui.QComboBox(dlg_login)
        self.cmb_user.setObjectName(_fromUtf8("cmb_user"))
        self.horizontalLayout.addWidget(self.cmb_user)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.lbl_pwd = QtGui.QLabel(dlg_login)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Microsoft JhengHei"))
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.lbl_pwd.setFont(font)
        self.lbl_pwd.setObjectName(_fromUtf8("lbl_pwd"))
        self.horizontalLayout_2.addWidget(self.lbl_pwd)
        self.led_pwd = QtGui.QLineEdit(dlg_login)
        self.led_pwd.setText(_fromUtf8(""))
        self.led_pwd.setEchoMode(QtGui.QLineEdit.Password)
        self.led_pwd.setObjectName(_fromUtf8("led_pwd"))
        self.horizontalLayout_2.addWidget(self.led_pwd)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.bnb = QtGui.QDialogButtonBox(dlg_login)
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
        self.verticalLayout.addWidget(self.bnb)

        self.retranslateUi(dlg_login)
        QtCore.QObject.connect(self.bnb, QtCore.SIGNAL(_fromUtf8("accepted()")), dlg_login.accept)
        QtCore.QObject.connect(self.bnb, QtCore.SIGNAL(_fromUtf8("rejected()")), dlg_login.reject)
        QtCore.QMetaObject.connectSlotsByName(dlg_login)

    def retranslateUi(self, dlg_login):
        dlg_login.setWindowTitle(_translate("dlg_login", "用戶登入", None))
        self.lbl_user.setText(_translate("dlg_login", "用戶名", None))
        self.lbl_pwd.setText(_translate("dlg_login", "密    碼", None))

import mycis_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    dlg_login = QtGui.QDialog()
    ui = Ui_dlg_login()
    ui.setupUi(dlg_login)
    dlg_login.show()
    sys.exit(app.exec_())

