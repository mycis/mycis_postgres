# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/cytu/usr/src/py/mycis/designer/win_inst.ui'
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

class Ui_win_inst(object):
    def setupUi(self, win_inst):
        win_inst.setObjectName(_fromUtf8("win_inst"))
        win_inst.setEnabled(True)
        win_inst.resize(727, 688)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Microsoft JhengHei"))
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        win_inst.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/res/img/document-open.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        win_inst.setWindowIcon(icon)
        win_inst.setStyleSheet(_fromUtf8("font: 75 12pt \"Microsoft JhengHei\";"))
        self.wdg = QtGui.QWidget(win_inst)
        self.wdg.setObjectName(_fromUtf8("wdg"))
        self.verticalLayout = QtGui.QVBoxLayout(self.wdg)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gl = QtGui.QGridLayout()
        self.gl.setObjectName(_fromUtf8("gl"))
        self.label = QtGui.QLabel(self.wdg)
        self.label.setObjectName(_fromUtf8("label"))
        self.gl.addWidget(self.label, 0, 0, 1, 1)
        self.trv = QtGui.QTreeView(self.wdg)
        self.trv.setFocusPolicy(QtCore.Qt.NoFocus)
        self.trv.setObjectName(_fromUtf8("trv"))
        self.gl.addWidget(self.trv, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.gl)
        win_inst.setCentralWidget(self.wdg)
        self.tb = QtGui.QToolBar(win_inst)
        self.tb.setIconSize(QtCore.QSize(48, 48))
        self.tb.setObjectName(_fromUtf8("tb"))
        win_inst.addToolBar(QtCore.Qt.TopToolBarArea, self.tb)
        self.stb = QtGui.QStatusBar(win_inst)
        self.stb.setObjectName(_fromUtf8("stb"))
        win_inst.setStatusBar(self.stb)

        self.retranslateUi(win_inst)
        QtCore.QMetaObject.connectSlotsByName(win_inst)

    def retranslateUi(self, win_inst):
        win_inst.setWindowTitle(_translate("win_inst", "案件", None))
        self.label.setText(_translate("win_inst", "案件選擇", None))
        self.tb.setWindowTitle(_translate("win_inst", "toolBar", None))

import mycis_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    win_inst = QtGui.QMainWindow()
    ui = Ui_win_inst()
    ui.setupUi(win_inst)
    win_inst.show()
    sys.exit(app.exec_())

