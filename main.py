#!/usr/bin/python3
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5 import QtGui,QtCore
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QShortcut,QLabel, QGridLayout, QWidget, QSystemTrayIcon, \
    QSpacerItem, QSizePolicy, QMenu, QAction, QStyle, qApp
from PyQt5.QtCore import Qt, QThread
from mainUI import Ui_MainWindow
from langs import Ui_MainWindow2
from GT import Gtranslate
import threading
class langse(QMainWindow, Ui_MainWindow2, Ui_MainWindow):
    def __init__(self, parent=None):
        super(langse, self).__init__(parent)
        self.setupUi(self)
        self.pushButton_2.clicked.connect(self.offchbtn)
    def slang(self):
        global window
        open("names.txt", "w").write("")
        langlist = open("langs.txt", "r").readlines()
        for i in self.__dict__.items():
            if "checkBox" in str(i[0]) and i[1].isChecked():
                lnum = int(str(i[0]).split("_")[1]) -2
                open("names.txt", "a+").write(langlist[lnum])
        window.scomlang()
    def offchbtn(self):
        self.slang()
        self.hide()

class myprog(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(myprog, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.setIcon(QIcon("icons/translate.svg"))
        self.pushButton.clicked.connect(lambda:self.trnsl(None))
        self.radioButton_2.toggled.connect(lambda:self.enableChoose())
        self.pushButton_5.clicked.connect(self.onchbtn)
        self.radioButton.toggled.connect(lambda:self.disableChoose())
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("icons/simin.png"))
        show_action = QAction("Open", self)
        quit_action = QAction("Exit", self)
        hide_action = QAction("Minimize to tray", self)

        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(qApp.quit)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        self.shortcut = QShortcut(QKeySequence("Ctrl+return"), self)
        self.shortcut.activated.connect(lambda:self.trnsl(None))
        self.shortcut2 = QShortcut(QKeySequence("Ctrl+q"), self)
        self.shortcut2.activated.connect(qApp.quit)

    def scomlang(self):
        self.comboBox.clear()
        self.comboBox_2.clear()
        names = str(open("names.txt", "r").read()).splitlines()
        for name in names:
            namel = name.split("|")
            self.comboBox.addItem(namel[1])
            self.comboBox_2.addItem(namel[1])
    def hideWindow(self):
        self.windoww = myprog()
        self.windoww.hide()
    def showWindow(self):
        self.windoww = myprog()
        self.windoww.show()
    def enableChoose(self):
        self.pushButton_5.setEnabled(True)

    def disableChoose(self):
        self.pushButton_5.setEnabled(False)

    def onchbtn(self):
        self.widget = langse()
        self.widget.show()

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def trnsl(self, word):
        if word is None:
            word = self.textEdit.toPlainText()
        else:
            self.textEdit.setText(word)
        sl = self.comboBox.currentText()
        tl = self.comboBox_2.currentText()
        tlangs = open("names.txt", "r").read().splitlines()
        chklng1 = False
        chklng2 = False
        for chck_lang in tlangs:
            langsplit = chck_lang.split("|")
            if len(langsplit) > 3:
                if langsplit[1] == sl:
                    chklng1 = True
                elif langsplit[1] == tl:
                    chklng2 = True
        num1 = 2
        num2 = 2
        if not chklng1:
            slfix = str(open("names.txt", "r").read().replace("|1|s", "")).replace(sl, sl + "|1|s")
            open("names.txt", "w").write(slfix)
            num1 = 0
        if not chklng2:
            tlfix = str(open("names.txt", "r").read().replace("|1|t", "")).replace(tl, tl + "|1|t")
            open("names.txt", "w").write(tlfix)
            num2 = 0
        if str(word).strip() != "":
            for lang in tlangs:
                if lang.split("|")[1] == sl:
                    sl = lang.split("|")[2+num1]
                if lang.split("|")[1] == tl:
                    tl = lang.split("|")[2+num2]
            gtrans = Gtranslate().translate(sl, tl, word)
            othermeans = str(gtrans["othermean"]).replace("'", "")
            if othermeans == "None":
                othermeans = ""
            self.textEdit_2.setText("{0}\n\n{1}".format(gtrans["exact"], othermeans))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        word = sys.argv[1]
        gtrans = Gtranslate().translate("", "fa", word, False)
        print(gtrans['exact'])
        sys.exit()
    app = QApplication(sys.argv)
    window = myprog()
    window.show()
    sys.exit(app.exec_())
