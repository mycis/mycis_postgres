# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/cytu/usr/src/py/mycis/designer/dlg_ent_inst.ui'
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

class Ui_dlg_ent_inst(object):
    def setupUi(self, dlg_ent_inst):
        dlg_ent_inst.setObjectName(_fromUtf8("dlg_ent_inst"))
        dlg_ent_inst.resize(721, 299)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Microsoft JhengHei"))
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        dlg_ent_inst.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/res/img/patient.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dlg_ent_inst.setWindowIcon(icon)
        dlg_ent_inst.setStyleSheet(_fromUtf8("font: 75 12pt \"Microsoft JhengHei\";"))
        self.gridLayout_2 = QtGui.QGridLayout(dlg_ent_inst)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lbl_gender = QtGui.QLabel(dlg_ent_inst)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_gender.sizePolicy().hasHeightForWidth())
        self.lbl_gender.setSizePolicy(sizePolicy)
        self.lbl_gender.setText(_fromUtf8(""))
        self.lbl_gender.setPixmap(QtGui.QPixmap(_fromUtf8(":/res/img/user-female.png")))
        self.lbl_gender.setObjectName(_fromUtf8("lbl_gender"))
        self.horizontalLayout.addWidget(self.lbl_gender)
        spacerItem = QtGui.QSpacerItem(5, 40, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.lbl_details = QtGui.QLabel(dlg_ent_inst)
        self.lbl_details.setText(_fromUtf8(""))
        self.lbl_details.setObjectName(_fromUtf8("lbl_details"))
        self.horizontalLayout.addWidget(self.lbl_details)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.tbv = QtGui.QTableView(dlg_ent_inst)
        self.tbv.setObjectName(_fromUtf8("tbv"))
        self.gridLayout.addWidget(self.tbv, 1, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(dlg_ent_inst)
        QtCore.QMetaObject.connectSlotsByName(dlg_ent_inst)

    def retranslateUi(self, dlg_ent_inst):
        dlg_ent_inst.setWindowTitle(_translate("dlg_ent_inst", "案件選擇", None))

import mycis_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    dlg_ent_inst = QtGui.QDialog()
    ui = Ui_dlg_ent_inst()
    ui.setupUi(dlg_ent_inst)
    dlg_ent_inst.show()
    sys.exit(app.exec_())

