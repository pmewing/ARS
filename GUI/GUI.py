from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # set up window properties
        self.x_coord = 0
        self.y_coord = 0
        self.width = 1400
        self.height = 500
        self.title = "Analysis"
        self.setCentralWidget(self)
        self.setGeometry(self.x_coord, self.y_coord, self.width, self.height)



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.show()
    sys.exit(app.exec_())
