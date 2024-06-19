import sys

from PySide6.QtWidgets import QMainWindow, QPushButton, QWidget, QApplication, QLabel, QLineEdit
class File_Manager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Manager")
        btn = QPushButton('Click me!', self)
        btn.setGeometry(100, 100, 100, 100)
        lb = QLabel('Hello World', self)
        lb.setGeometry(200, 200, 100, 100)
        lb.setText('Hello New World!')
        line = QLineEdit(self)
        line.setPlaceholderText('请选择导入文件夹')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = File_Manager()
    window.show()
    app.exec()
