# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/cytu/usr/src/py/mycis/designer/win_fav.ui'
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

class Ui_win_fav(object):
    def setupUi(self, win_fav):
        win_fav.setObjectName(_fromUtf8("win_fav"))
        win_fav.setEnabled(True)
        win_fav.resize(1026, 688)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Microsoft JhengHei"))
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        win_fav.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/res/img/folder_bookmarks.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        win_fav.setWindowIcon(icon)
        win_fav.setStyleSheet(_fromUtf8("font: 75 12pt \"Microsoft JhengHei\";"))
        self.centralwidget = QtGui.QWidget(win_fav)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_7 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        win_fav.setCentralWidget(self.centralwidget)
        self.mnb = QtGui.QMenuBar(win_fav)
        self.mnb.setGeometry(QtCore.QRect(0, 0, 1026, 33))
        self.mnb.setObjectName(_fromUtf8("mnb"))
        self.mnu = QtGui.QMenu(self.mnb)
        self.mnu.setObjectName(_fromUtf8("mnu"))
        win_fav.setMenuBar(self.mnb)
        self.tb = QtGui.QToolBar(win_fav)
        self.tb.setObjectName(_fromUtf8("tb"))
        win_fav.addToolBar(QtCore.Qt.TopToolBarArea, self.tb)
        self.act_import = QtGui.QAction(win_fav)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/res/img/fileimport.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.act_import.setIcon(icon1)
        self.act_import.setObjectName(_fromUtf8("act_import"))
        self.act_export = QtGui.QAction(win_fav)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/res/img/file_export.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.act_export.setIcon(icon2)
        self.act_export.setObjectName(_fromUtf8("act_export"))
        self.mnu.addAction(self.act_import)
        self.mnu.addAction(self.act_export)
        self.mnb.addAction(self.mnu.menuAction())
        self.tb.addAction(self.act_import)
        self.tb.addAction(self.act_export)

        self.retranslateUi(win_fav)
        QtCore.QMetaObject.connectSlotsByName(win_fav)

    def retranslateUi(self, win_fav):
        win_fav.setWindowTitle(_translate("win_fav", "代碼管理", None))
        self.mnu.setTitle(_translate("win_fav", "工作(&W)", None))
        self.tb.setWindowTitle(_translate("win_fav", "toolBar", None))
        self.act_import.setText(_translate("win_fav", "匯入", None))
        self.act_import.setToolTip(_translate("win_fav", "匯入", None))
        self.act_import.setShortcut(_translate("win_fav", "Ctrl+I", None))
        self.act_export.setText(_translate("win_fav", "匯出", None))
        self.act_export.setShortcut(_translate("win_fav", "Ctrl+E", None))

import mycis_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    win_fav = QtGui.QMainWindow()
    ui = Ui_win_fav()
    ui.setupUi(win_fav)
    win_fav.show()
    sys.exit(app.exec_())

