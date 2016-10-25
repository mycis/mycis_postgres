# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/cytu/usr/src/py/mycis/designer/win_app.ui'
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

class Ui_win_app(object):
    def setupUi(self, win_app):
        win_app.setObjectName(_fromUtf8("win_app"))
        win_app.setEnabled(True)
        win_app.resize(727, 565)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Microsoft JhengHei"))
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        win_app.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/res/img/db_comit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        win_app.setWindowIcon(icon)
        win_app.setStyleSheet(_fromUtf8("font: 75 12pt \"Microsoft JhengHei\";"))
        self.wdg = QtGui.QWidget(win_app)
        self.wdg.setObjectName(_fromUtf8("wdg"))
        self.verticalLayout = QtGui.QVBoxLayout(self.wdg)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gl = QtGui.QGridLayout()
        self.gl.setObjectName(_fromUtf8("gl"))
        self.label_2 = QtGui.QLabel(self.wdg)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gl.addWidget(self.label_2, 0, 0, 1, 1)
        self.log = QtGui.QPlainTextEdit(self.wdg)
        self.log.setObjectName(_fromUtf8("log"))
        self.gl.addWidget(self.log, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.gl)
        win_app.setCentralWidget(self.wdg)
        self.tb = QtGui.QToolBar(win_app)
        self.tb.setIconSize(QtCore.QSize(48, 48))
        self.tb.setObjectName(_fromUtf8("tb"))
        win_app.addToolBar(QtCore.Qt.TopToolBarArea, self.tb)
        self.stb = QtGui.QStatusBar(win_app)
        self.stb.setObjectName(_fromUtf8("stb"))
        win_app.setStatusBar(self.stb)

        self.retranslateUi(win_app)
        QtCore.QMetaObject.connectSlotsByName(win_app)

    def retranslateUi(self, win_app):
        win_app.setWindowTitle(_translate("win_app", "申報作業", None))
        self.label_2.setText(_translate("win_app", "連線訊息", None))
        self.log.setStyleSheet(_translate("win_app", "background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 255, 255);", None))
        self.tb.setWindowTitle(_translate("win_app", "toolBar", None))

import mycis_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    win_app = QtGui.QMainWindow()
    ui = Ui_win_app()
    ui.setupUi(win_app)
    win_app.show()
    sys.exit(app.exec_())

