# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/cytu/usr/src/py/mycis/designer/win_ic.ui'
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

class Ui_win_ic(object):
    def setupUi(self, win_ic):
        win_ic.setObjectName(_fromUtf8("win_ic"))
        win_ic.setEnabled(True)
        win_ic.resize(951, 585)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Microsoft JhengHei"))
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        win_ic.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/res/img/text-x-vcard.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        win_ic.setWindowIcon(icon)
        win_ic.setStyleSheet(_fromUtf8("font: 75 12pt \"Microsoft JhengHei\";"))
        self.centralwidget = QtGui.QWidget(win_ic)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        win_ic.setCentralWidget(self.centralwidget)
        self.menuBar = QtGui.QMenuBar(win_ic)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 951, 29))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menu = QtGui.QMenu(self.menuBar)
        self.menu.setObjectName(_fromUtf8("menu"))
        self.menu_2 = QtGui.QMenu(self.menuBar)
        self.menu_2.setObjectName(_fromUtf8("menu_2"))
        self.menu_3 = QtGui.QMenu(self.menu_2)
        self.menu_3.setObjectName(_fromUtf8("menu_3"))
        self.menu_V = QtGui.QMenu(self.menuBar)
        self.menu_V.setObjectName(_fromUtf8("menu_V"))
        win_ic.setMenuBar(self.menuBar)
        self.act_get_basic = QtGui.QAction(win_ic)
        self.act_get_basic.setObjectName(_fromUtf8("act_get_basic"))
        self.act_update_hc = QtGui.QAction(win_ic)
        self.act_update_hc.setObjectName(_fromUtf8("act_update_hc"))
        self.act_set_pwd = QtGui.QAction(win_ic)
        self.act_set_pwd.setObjectName(_fromUtf8("act_set_pwd"))
        self.act_stop_pwd = QtGui.QAction(win_ic)
        self.act_stop_pwd.setObjectName(_fromUtf8("act_stop_pwd"))
        self.act_get_ord = QtGui.QAction(win_ic)
        self.act_get_ord.setObjectName(_fromUtf8("act_get_ord"))
        self.act_get_diag = QtGui.QAction(win_ic)
        self.act_get_diag.setObjectName(_fromUtf8("act_get_diag"))
        self.act_get_cum = QtGui.QAction(win_ic)
        self.act_get_cum.setObjectName(_fromUtf8("act_get_cum"))
        self.act_get_donate = QtGui.QAction(win_ic)
        self.act_get_donate.setObjectName(_fromUtf8("act_get_donate"))
        self.act_set_allergy = QtGui.QAction(win_ic)
        self.act_set_allergy.setObjectName(_fromUtf8("act_set_allergy"))
        self.act_set_tel = QtGui.QAction(win_ic)
        self.act_set_tel.setObjectName(_fromUtf8("act_set_tel"))
        self.act_verify_hpc = QtGui.QAction(win_ic)
        self.act_verify_hpc.setObjectName(_fromUtf8("act_verify_hpc"))
        self.act_set_hpc = QtGui.QAction(win_ic)
        self.act_set_hpc.setObjectName(_fromUtf8("act_set_hpc"))
        self.act_unlock_hpc = QtGui.QAction(win_ic)
        self.act_unlock_hpc.setObjectName(_fromUtf8("act_unlock_hpc"))
        self.act_get_tel = QtGui.QAction(win_ic)
        self.act_get_tel.setObjectName(_fromUtf8("act_get_tel"))
        self.act_new_tab = QtGui.QAction(win_ic)
        self.act_new_tab.setObjectName(_fromUtf8("act_new_tab"))
        self.act_get_allergy = QtGui.QAction(win_ic)
        self.act_get_allergy.setObjectName(_fromUtf8("act_get_allergy"))
        self.menu.addAction(self.act_new_tab)
        self.menu.addSeparator()
        self.menu_3.addAction(self.act_set_allergy)
        self.menu_3.addAction(self.act_set_tel)
        self.menu_2.addAction(self.act_get_basic)
        self.menu_2.addAction(self.act_update_hc)
        self.menu_2.addAction(self.act_set_pwd)
        self.menu_2.addAction(self.act_stop_pwd)
        self.menu_2.addSeparator()
        self.menu_2.addAction(self.act_get_ord)
        self.menu_2.addAction(self.act_get_diag)
        self.menu_2.addAction(self.act_get_allergy)
        self.menu_2.addAction(self.act_get_tel)
        self.menu_2.addAction(self.act_get_cum)
        self.menu_2.addAction(self.act_get_donate)
        self.menu_2.addSeparator()
        self.menu_2.addAction(self.menu_3.menuAction())
        self.menu_V.addAction(self.act_verify_hpc)
        self.menu_V.addAction(self.act_set_hpc)
        self.menu_V.addAction(self.act_unlock_hpc)
        self.menuBar.addAction(self.menu.menuAction())
        self.menuBar.addAction(self.menu_2.menuAction())
        self.menuBar.addAction(self.menu_V.menuAction())

        self.retranslateUi(win_ic)
        QtCore.QMetaObject.connectSlotsByName(win_ic)

    def retranslateUi(self, win_ic):
        win_ic.setWindowTitle(_translate("win_ic", "IC卡作業", None))
        self.menu.setTitle(_translate("win_ic", "檔案(&F)", None))
        self.menu_2.setTitle(_translate("win_ic", "IC卡(&I)", None))
        self.menu_3.setTitle(_translate("win_ic", "寫入", None))
        self.menu_V.setTitle(_translate("win_ic", "醫事人員卡(&H)", None))
        self.act_get_basic.setText(_translate("win_ic", "基本資料(&B)", None))
        self.act_get_basic.setToolTip(_translate("win_ic", "基本資料", None))
        self.act_update_hc.setText(_translate("win_ic", "卡片更新(&N)", None))
        self.act_update_hc.setToolTip(_translate("win_ic", "卡片更新", None))
        self.act_set_pwd.setText(_translate("win_ic", "啟用密碼(&P)", None))
        self.act_set_pwd.setToolTip(_translate("win_ic", "啟用密碼", None))
        self.act_stop_pwd.setText(_translate("win_ic", "停用密碼(&S)", None))
        self.act_stop_pwd.setToolTip(_translate("win_ic", "停用密碼", None))
        self.act_get_ord.setText(_translate("win_ic", "醫令(&O)", None))
        self.act_get_ord.setToolTip(_translate("win_ic", "醫令", None))
        self.act_get_diag.setText(_translate("win_ic", "診斷(&D)", None))
        self.act_get_diag.setToolTip(_translate("win_ic", "讀取診斷", None))
        self.act_get_cum.setText(_translate("win_ic", "累計資料(&C)", None))
        self.act_get_cum.setToolTip(_translate("win_ic", "讀取就醫累計資料", None))
        self.act_get_donate.setText(_translate("win_ic", "器官捐贈(&G)", None))
        self.act_get_donate.setToolTip(_translate("win_ic", "讀取器官捐贈註記", None))
        self.act_set_allergy.setText(_translate("win_ic", "過敏藥物(&A)", None))
        self.act_set_allergy.setToolTip(_translate("win_ic", "寫入過敏藥物", None))
        self.act_set_tel.setText(_translate("win_ic", "聯絡電話(&T)", None))
        self.act_set_tel.setToolTip(_translate("win_ic", "寫入聯絡電話", None))
        self.act_verify_hpc.setText(_translate("win_ic", "密碼認證(&V)", None))
        self.act_verify_hpc.setToolTip(_translate("win_ic", "醫事人員卡密碼認證", None))
        self.act_set_hpc.setText(_translate("win_ic", "更改密碼(&U)", None))
        self.act_set_hpc.setToolTip(_translate("win_ic", "醫事人員卡密碼更改", None))
        self.act_unlock_hpc.setText(_translate("win_ic", "解除鎖卡(&L)", None))
        self.act_unlock_hpc.setToolTip(_translate("win_ic", "解除醫事人員卡鎖卡", None))
        self.act_get_tel.setText(_translate("win_ic", "聯絡電話(&E)", None))
        self.act_get_tel.setToolTip(_translate("win_ic", "聯絡電話", None))
        self.act_new_tab.setText(_translate("win_ic", "新分頁(&T)", None))
        self.act_new_tab.setToolTip(_translate("win_ic", "新分頁", None))
        self.act_get_allergy.setText(_translate("win_ic", "過敏藥物(&M)", None))
        self.act_get_allergy.setToolTip(_translate("win_ic", "讀取過敏藥物(M)", None))

import mycis_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    win_ic = QtGui.QMainWindow()
    ui = Ui_win_ic()
    ui.setupUi(win_ic)
    win_ic.show()
    sys.exit(app.exec_())

