class CountReadsDialog(QtWidgets.QDialog):
    def __init__(self, width, height, parent=None):
        """
        This function is resposible for creating a new window that will interact with the GUI_CountReads.py file
        """
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

        self.red_text = "QLabel { color: red } "
        self.black_text = "QLabel { color: black } "

        # create buttons
        self.open_directory_button = QtWidgets.QPushButton(self)
        self.save_directory_button = QtWidgets.QPushButton(self)
        self.count_reads_button = QtWidgets.QPushButton(self)

        # create labels
        self.open_directory_label = QLabel(self)
        self.save_directory_label = QLabel(self)

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
        self.open_directory_button.clicked.connect(self.open_directory)
        self.save_directory_button.clicked.connect(self.save_directory)

        # modify label location
        self.open_directory_label.setGeometry(QtCore.QRect(350, 40, 129, 34))
        self.save_directory_label.setGeometry(QtCore.QRect(350, 150, 129, 34))

        # modify label text
        self.open_directory_label.setText("Input Directory Not Set")
        self.open_directory_label.setStyleSheet(self.red_text)
        self.save_directory_label.setText("Save Directory Not Set")
        self.save_directory_label.setStyleSheet(self.red_text)

    def open_directory(self):
        barcode_folder_location = QFileDialog.getExistingDirectory(parent=self,
                                                                   caption="Select the barcode parent directory",
                                                                   directory=initial_directory)
        self.open_directory_label.setText(barcode_folder_location + "/")

        # get length of input directory. If user pressed cancel, the length of the directory will be 1 (`/`)
        # tell them they have not input a directory yet
        if len(self.barcode_parent_label.text()) == 1:
            self.barcode_parent_label.setStyleSheet(self.red_text)
            self.barcode_parent_label.setText("Save Location Not Set")
        else:
            self.barcode_parent_label.setStyleSheet(self.black_text)
            self.barcode_parent_label.adjustSize()

    def save_directory(self):
        pass