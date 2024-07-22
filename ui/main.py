import sys

from PySide6.QtWidgets import QMainWindow, QPushButton, QWidget, QApplication
from 计算器 import Ui_Form
class File_Manager(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("计算器")
        self.bind()

    def bind(self):

        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = File_Manager()
    window.show()
    app.exec()