from PyQt4 import uic
from PyQt4.QtGui import *

help_ui = uic.loadUiType("gtk/help.ui")[0]

file_txt = "config/uji.txt"


class Specifications(QDialog, help_ui):
    def __init__(self, title, file, parent=None):
        # Initialization help interface from QT to Python

        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.label_title.setText(title)
        self.printContentFile(file)
        self.pushButton_close.clicked.connect(self.closeWinHelp)

    def parsingContentFile(self, file):
        pars_content = open(file, "r")
        return pars_content.read()

    def closeWinHelp(self):
        self.close()

    def printContentFile(self, file):
        pars = self.parsingContentFile(file)
        self.label_content.setText(pars)