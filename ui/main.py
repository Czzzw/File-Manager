import sys

from PySide6.QtWidgets import QMainWindow, QPushButton, QWidget, QApplication
class File_Manager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Manager")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = File_Manager()
    window.show()
    app.exec()