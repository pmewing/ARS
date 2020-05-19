from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QFileDialog


class MainWindow(QMainWindow):
    def __init__(self, screen_width, screen_height):
        # set up the main window size and location
        super(MainWindow, self).__init__()
        self.setWindowTitle("Analysis")
        self.x_size = 2250
        self.y_size = 500
        self.x_coord = (screen_width / 2) - (self.x_size / 2)
        self.y_coord = (screen_height / 2) - (self.y_size / 2)

        self.setFixedSize(self.x_size, self.y_size)
        self.move(self.x_coord, self.y_coord)
        self.initial_directory = r"/home/joshl/"

        # create buttons for interaction
        self.barcode_parent_button = QPushButton(self)
        self.merged_reads_button = QPushButton(self)
        self.guppy_alignment_button = QPushButton(self)
        self.analyze_button = QPushButton(self)

        # create labels for displaying information
        self.barcode_parent_label = QLabel(self)
        self.merged_reads_label = QLabel(self)

        self.set_UI_elements()

    def set_UI_elements(self):
        """
        This function will set the UI aspects of each button and label on the screen
        """

        # set button positions
        self.barcode_parent_button.setGeometry(QtCore.QRect(70, 50, 425, 48))
        self.merged_reads_button.setGeometry(QtCore.QRect(70, 120, 525, 48))
        self.guppy_alignment_button.setGeometry(QtCore.QRect(70, 190, 375, 48))
        self.analyze_button.setGeometry(QtCore.QRect(625, 350, 150, 48))

        # set text on button
        self.barcode_parent_button.setText("Select Barcode Parent Folder")
        self.merged_reads_button.setText("Select Save Location of Merged Reads")
        self.guppy_alignment_button.setText("Guppy Alignment Settings")
        self.analyze_button.setText("Analyze")

        # bind buttons to functions
        self.barcode_parent_button.clicked.connect(self.clicked_barcode_parent)
        self.merged_reads_button.clicked.connect(self.clicked_merged_reads)
        self.guppy_alignment_button.clicked.connect(self.clicked_guppy_alignment)
        self.analyze_button.clicked.connect(self.clicked_analyze)

        # set label positions
        self.barcode_parent_label.setGeometry(QtCore.QRect(700, 50, 671, 34))
        self.merged_reads_label.setGeometry(QtCore.QRect(700, 130, 671, 34))

        # set label text
        self.barcode_parent_label.setStyleSheet("QLabel { color: red } ")
        self.barcode_parent_label.setText("Save Location Not Set")

        self.merged_reads_label.setStyleSheet("QLabel { color: red } ")
        self.merged_reads_label.setText("Save Location Not Set")

    def clicked_barcode_parent(self):

        barcode_folder_location = QFileDialog.getExistingDirectory(parent=self,
                                                                   caption="Select the barcode parent directory",
                                                                   directory=self.initial_directory)
        self.barcode_parent_label.setText(barcode_folder_location + "/")
        self.barcode_parent_label.adjustSize()
        self.barcode_parent_label.setStyleSheet("QLabel { color: black }")

    def clicked_merged_reads(self):
        merge_read_save_folder = QFileDialog.getExistingDirectory(parent=self,
                                                                  caption="Set the save location",
                                                                  directory=self.initial_directory)

        self.merged_reads_label.setText(merge_read_save_folder + "/")
        self.merged_reads_label.adjustSize()
        self.merged_reads_label.setStyleSheet("QLabel { color: black }")

    def clicked_guppy_alignment(self):
        print("Guppy")

    def clicked_analyze(self):
        print("Analyze")

class GuppyAlignment():
    def __init__(self):
        super(GuppyAlignment, self).__init__()



if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    screen = app.primaryScreen()
    rect = screen.availableGeometry()

    gui = MainWindow(rect.width(), rect.height())
    gui.show()
    sys.exit(app.exec_())

