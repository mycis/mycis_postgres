# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/cytu/usr/src/py/mycis/designer/win_stat.ui'
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

class Ui_win_stat(object):
    def setupUi(self, win_stat):
        win_stat.setObjectName(_fromUtf8("win_stat"))
        win_stat.setEnabled(True)
        win_stat.resize(951, 591)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Microsoft JhengHei"))
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        win_stat.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/res/img/chart.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        win_stat.setWindowIcon(icon)
        win_stat.setStyleSheet(_fromUtf8("font: 75 12pt \"Microsoft JhengHei\";"))
        self.wdg = QtGui.QWidget(win_stat)
        self.wdg.setObjectName(_fromUtf8("wdg"))
        self.verticalLayout = QtGui.QVBoxLayout(self.wdg)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gr = QtWebKit.QWebView(self.wdg)
        self.gr.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.gr.setObjectName(_fromUtf8("gr"))
        self.verticalLayout.addWidget(self.gr)
        win_stat.setCentralWidget(self.wdg)
        self.tb = QtGui.QToolBar(win_stat)
        self.tb.setIconSize(QtCore.QSize(48, 48))
        self.tb.setObjectName(_fromUtf8("tb"))
        win_stat.addToolBar(QtCore.Qt.TopToolBarArea, self.tb)
        self.stb = QtGui.QStatusBar(win_stat)
        self.stb.setObjectName(_fromUtf8("stb"))
        win_stat.setStatusBar(self.stb)

        self.retranslateUi(win_stat)
        QtCore.QMetaObject.connectSlotsByName(win_stat)

    def retranslateUi(self, win_stat):
        win_stat.setWindowTitle(_translate("win_stat", "統計圖表", None))
        self.tb.setWindowTitle(_translate("win_stat", "toolBar", None))

from PyQt4 import QtWebKit
import mycis_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    win_stat = QtGui.QMainWindow()
    ui = Ui_win_stat()
    ui.setupUi(win_stat)
    win_stat.show()
    sys.exit(app.exec_())

