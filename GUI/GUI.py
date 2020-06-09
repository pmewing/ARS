import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QFileDialog

# add the parent folder to the path so other folders can be used. Fixes import lines when running this from the command line
sys.path.append("../")
from Scripts.CountReads import Count

# add these items to path so they can be imported
# sys.path.append("/home/joshl/PycharmProjects/ARS Projects/CountReads/")
# from CountReads.CountReads import Count

# file constants
initial_directory = r"/home/joshl/"
red_text = "QLabel { color: red } "
black_text = "QLabel { color: black } "


class MainWindow(QMainWindow):
    def __init__(self, screen_width, screen_height):

        # set up the main window size and location
        super(MainWindow, self).__init__()
        self.setWindowTitle("Pipeline Analysis")
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x_size = 2250
        self.y_size = 500
        self.x_coord = (self.screen_width / 2) - (self.x_size / 2)
        self.y_coord = (self.screen_height / 2) - (self.y_size / 2)
        self.setFixedSize(self.x_size, self.y_size)
        self.move(self.x_coord, self.y_coord)

        # create menu bar items
        self.menubar = self.menuBar()                    # main menu bar at top of window
        self.methods_menu = self.menubar.addMenu("&Methods")   # heading in the main bar
        self.action_count_reads = self.methods_menu.addAction("Count Reads")       # subheading in the heading
        self.action_merge_files = self.methods_menu.addAction("Merge DataFiles")
        self.action_count_reads.triggered.connect(self.connect_count_reads)
        self.action_merge_files.triggered.connect(self.connect_merge_files)

        # create buttons for interaction
        self.barcode_parent_button = QPushButton(self)
        self.merged_reads_button = QPushButton(self)
        self.guppy_alignment_button = QPushButton(self)
        self.analyze_button = QPushButton(self)

        # create labels for displaying information
        self.barcode_parent_label = QLabel(self)
        self.merged_reads_label = QLabel(self)

        QtCore.QMetaObject.connectSlotsByName(self)
        self.set_UI_elements()

    def set_UI_elements(self):
        """
        This function will set the UI aspects of each button and label on the screen
        """

        analyze_button_width = 150
        analyze_button_x_size = int((self.x_size / 2) - (analyze_button_width / 2))

        # set button geometry
        self.barcode_parent_button.setGeometry(QtCore.QRect(70, 70, 425, 48))
        self.merged_reads_button.setGeometry(QtCore.QRect(70, 150, 525, 48))
        self.guppy_alignment_button.setGeometry(QtCore.QRect(70, 230, 375, 48))
        self.analyze_button.setGeometry(QtCore.QRect(analyze_button_x_size, 350, analyze_button_width, 48))

        # set button names
        self.barcode_parent_button.setObjectName("Barcode Parent")
        self.merged_reads_button.setObjectName("Merged Reads")
        self.guppy_alignment_button.setObjectName("Guppy GuppyAlignment")
        self.analyze_button.setObjectName("analyze_button")

        # set label geometry
        self.barcode_parent_label.setGeometry(QtCore.QRect(700, 70, 671, 34))
        self.merged_reads_label.setGeometry(QtCore.QRect(700, 150, 671, 34))

        # set text on button
        self.barcode_parent_button.setText("Select Barcode Parent Folder")
        self.merged_reads_button.setText("Select Save Location of Merged Reads")
        self.guppy_alignment_button.setText("Guppy GuppyAlignment Settings")
        self.analyze_button.setText("Analyze")

        # bind buttons to functions
        self.barcode_parent_button.clicked.connect( lambda x: open_directory(self.barcode_parent_label) )
        self.merged_reads_button.clicked.connect( lambda x: open_directory(self.merged_reads_label))
        self.guppy_alignment_button.clicked.connect(self.clicked_guppy_alignment)
        self.analyze_button.clicked.connect(self.clicked_analyze)

        # set label text
        self.barcode_parent_label.setStyleSheet(red_text)
        self.barcode_parent_label.setText("Location Not Set")

        self.merged_reads_label.setStyleSheet(red_text)
        self.merged_reads_label.setText("Location Not Set")

    def clicked_guppy_alignment(self):
        print("Guppy")

    def clicked_analyze(self):
        print("Analyze")

    def connect_count_reads(self):
        count_reads_dialog = CountReadsDialog(width=self.screen_width,
                                              height=self.screen_height,
                                              parent=self)
        count_reads_dialog.show()

    def connect_merge_files(self):
        print("merge files")


class CountReadsDialog(QtWidgets.QDialog):
    def __init__(self, width, height, parent=None):
        """
        This function is resposible for creating a new window that will interact with the GUI_CountReads.py file
        """

        # TODO: ALlow the user to select a file name for saving the output of CountReads (barcode_counts.csv and
        #   barcode_pickle_dump.pkl)
        super(CountReadsDialog, self).__init__(parent)

        # set up the dialog box information
        self.screen_width = width
        self.screen_height = height
        self.x_size = 1300
        self.y_size = 350
        self.x_coord = (self.screen_width / 2) - (self.x_size / 2) - 250
        self.y_coord = (self.screen_height / 2) - (self.y_size / 2) - 250
        self.setFixedSize(self.x_size, self.y_size)
        self.move(self.x_coord, self.y_coord)

        # create buttons
        self.open_directory_button = QtWidgets.QPushButton(self)
        self.save_directory_button = QtWidgets.QPushButton(self)
        self.count_reads_button = QtWidgets.QPushButton(self)

        # create labels
        self.open_directory_label = QLabel(self)
        self.save_directory_label = QLabel(self)
        self.status_label = QLabel(self)

        self.initUI()

    def initUI(self):
        """
        This function will set up the UI elements for the items listed in __init__ (buttons/labels/etc)
        """

        # modify button location
        self.open_directory_button.setGeometry(QtCore.QRect(40, 40, 225, 48))
        self.save_directory_button.setGeometry(QtCore.QRect(40, 150, 200, 48))
        self.count_reads_button.setGeometry(QtCore.QRect(538, 250, 225, 48))

        # modify button text
        self.open_directory_button.setText("Input Directory")
        self.save_directory_button.setText("Save Directory")
        self.count_reads_button.setText("Count Reads")

        # bind buttons to functions
        self.open_directory_button.clicked.connect(lambda x: open_directory(self.open_directory_label))
        self.save_directory_button.clicked.connect(lambda x: open_directory(self.save_directory_label))
        self.count_reads_button.clicked.connect(self.call_count_reads)

        # modify label location
        self.open_directory_label.setGeometry(QtCore.QRect(340, 40, 129, 34))
        self.save_directory_label.setGeometry(QtCore.QRect(340, 150, 129, 34))
        self.status_label.setGeometry(QtCore.QRect(40, 310, 150, 34))

        # modify label text
        self.open_directory_label.setText("Location Not Set")
        self.open_directory_label.setStyleSheet(red_text)
        self.open_directory_label.adjustSize()

        self.save_directory_label.setText("Location Not Set")
        self.save_directory_label.setStyleSheet(red_text)
        self.save_directory_label.adjustSize()

    def call_count_reads(self):

        if "location not set" not in [self.save_directory_label.text().lower(), self.open_directory_label.text().lower()]:
            Count(open_directory=self.open_directory_label.text(),
                  save_directory=self.save_directory_label.text())
            self.status_label.setText("Count reads compleed")

        else:
            self.status_label.setText("Select a directory for each of the locations.")

        self.status_label.adjustSize()


def open_directory(label: QLabel):
    """
    This function will accept a label and ensure that its properties (text and text color) are set appropriately

    :param QLabel label: this is the info label to be changed. Used only with labels associated with opening file dialogs
    :return: None
    """
    new_directory = label.text()
    if "Not Set" in new_directory:
        new_directory = initial_directory

    barcode_folder_location = QFileDialog.getExistingDirectory(caption=str( label.objectName() ),
                                                               directory=new_directory)
    label.setText(barcode_folder_location + "/")

    # get length of input directory. If user pressed cancel, the length of the directory will be 1 (`/`)
    # tell them they have not input a directory yet
    if len(label.text()) == 1:
        label.setStyleSheet(red_text)
        label.setText("Location Not Set")
    else:
        label.setStyleSheet(black_text)
    label.adjustSize()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    screen = app.primaryScreen()
    rect = screen.availableGeometry()

    gui = MainWindow(rect.width(), rect.height())
    gui.show()
    sys.exit(app.exec_())
