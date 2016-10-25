# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/cytu/usr/src/py/mycis/designer/dlg_fee.ui'
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

class Ui_dlg_fee(object):
    def setupUi(self, dlg_fee):
        dlg_fee.setObjectName(_fromUtf8("dlg_fee"))
        dlg_fee.resize(469, 165)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Microsoft JhengHei"))
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        dlg_fee.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/res/img/receptionist.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dlg_fee.setWindowIcon(icon)
        dlg_fee.setStyleSheet(_fromUtf8("font: 75 12pt \"Microsoft JhengHei\";"))
        self.gridLayout_2 = QtGui.QGridLayout(dlg_fee)
        self.gridLayout_2.setMargin(5)
        self.gridLayout_2.setSpacing(5)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setMargin(5)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(dlg_fee)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Microsoft JhengHei"))
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.groupBox.setFont(font)
        self.groupBox.setFlat(False)
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setMargin(5)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setMargin(5)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.rbn_gen = QtGui.QRadioButton(self.groupBox)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Microsoft JhengHei"))
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.rbn_gen.setFont(font)
        self.rbn_gen.setChecked(True)
        self.rbn_gen.setObjectName(_fromUtf8("rbn_gen"))
        self.horizontalLayout.addWidget(self.rbn_gen)
        self.rbn_ini = QtGui.QRadioButton(self.groupBox)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Microsoft JhengHei"))
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.rbn_ini.setFont(font)
        self.rbn_ini.setObjectName(_fromUtf8("rbn_ini"))
        self.horizontalLayout.addWidget(self.rbn_ini)
        self.rbn_na = QtGui.QRadioButton(self.groupBox)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Microsoft JhengHei"))
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.rbn_na.setFont(font)
        self.rbn_na.setObjectName(_fromUtf8("rbn_na"))
        self.horizontalLayout.addWidget(self.rbn_na)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.groupBox)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setMargin(5)
        self.gridLayout.setSpacing(5)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.chk_loan = QtGui.QCheckBox(dlg_fee)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Microsoft JhengHei"))
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.chk_loan.setFont(font)
        self.chk_loan.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.chk_loan.setChecked(False)
        self.chk_loan.setObjectName(_fromUtf8("chk_loan"))
        self.gridLayout.addWidget(self.chk_loan, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtGui.QDialogButtonBox(dlg_fee)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Microsoft JhengHei"))
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.buttonBox.setFont(font)
        self.buttonBox.setStyleSheet(_fromUtf8(""))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(dlg_fee)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), dlg_fee.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), dlg_fee.reject)
        QtCore.QMetaObject.connectSlotsByName(dlg_fee)
        dlg_fee.setTabOrder(self.rbn_gen, self.rbn_ini)
        dlg_fee.setTabOrder(self.rbn_ini, self.chk_loan)
        dlg_fee.setTabOrder(self.chk_loan, self.buttonBox)

    def retranslateUi(self, dlg_fee):
        dlg_fee.setWindowTitle(_translate("dlg_fee", "掛號費用", None))
        self.groupBox.setTitle(_translate("dlg_fee", "掛號費用", None))
        self.rbn_gen.setText(_translate("dlg_fee", "一般掛號（50）", None))
        self.rbn_ini.setText(_translate("dlg_fee", "初次掛號（100）", None))
        self.rbn_na.setText(_translate("dlg_fee", "免掛號費（0）", None))
        self.chk_loan.setText(_translate("dlg_fee", "欠卡押金（300）", None))

import mycis_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    dlg_fee = QtGui.QDialog()
    ui = Ui_dlg_fee()
    ui.setupUi(dlg_fee)
    dlg_fee.show()
    sys.exit(app.exec_())

