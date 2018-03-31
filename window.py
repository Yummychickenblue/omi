from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
import sys


class App(QApplication):
    def __init__(self, args):
        super().__init__(args)
        
    def make_window(self):
        self.window = uic.loadUi("mainwindow.ui")
        
    def show_window(self):
        self.window.show()
        
    def set_window_title(self, name):
        self.window.setWindowTitle(name)
 

if __name__ == '__main__':
    app = App( args=sys.argv, ui='ui')
    app.make_window()
    app.show_window()
    sys.exit(app.exec_())
