from PyQt5.QtWidgets import QFileDialog, QApplication, QWidget  # graphical folder selection
import sys  # sys.argv, used to pass in arguments to graphical interface (not used, error when not included however)
import os  # os.walk(), os.join.path()
import getpass  # get username


class Count:
    """
    This class is responsible for counting the number of barcodes present in the output of guppy_barcode
    """
    def __init__(self):
        """
        this is the main driver function, and will be ran when a Count() class is implemented
        Creates a file in the directory selected containing which barcode folders
        """

        username = getpass.getuser()
        self.initial_directory = r"/home/%s/minknow_data/CLC_2020-02-11/" % username
        self.barcode_correlations = {}

        # give user info about warning that will occur using QFileDialog.getExistingDirectory()
        print("In the next window, select the **parent** folder of all barcode folders")
        print("Press enter to continue")
        print("(NOTE: A warning will appear; this warning cannot be resolved. Trust nothing is wrong.)", end="")
        input()

        #  sys.argv allows for passing arguments into the dialog box. This will not be used
        #  graphical interface for opening a folder
        self.q_application = QApplication(sys.argv)
        self.widget = QWidget()

        self.barcode_file_location = str(QFileDialog.getExistingDirectory(parent=self.widget,
                                                                          caption="Select the barcode parent directory",
                                                                          directory=self.initial_directory))

        #  get locations of all barcode files
        self.file_paths = self.return_file_paths(self.barcode_file_location)

        #  count barcodes
        self.total_barcodes = -1  # no barcodes found
        self.total_barcodes = self.count_barcodes(self.file_paths)

    def __repr__(self):
        """
        This returns data from __init__, as data cannot be returned from __init__ directly
        :return: int total barcodes
        """
        return str(self.total_barcodes)

    def return_file_paths(self, barcode_parent):
        """
        This method will use the os.walk() function to collect the file path of all files that have "fastq_runid" in
        the name. This is important because guppy will output multiple files; we are only interested in the ones
        that have barcodes in the file

        os.walk() documentation: https://www.tutorialspoint.com/python/os_walk.htm

        :param _io.TextIO barcode_parent: The parent directory of the barcode files
        :return: list

        Example return item: /home/USERNAME/minknow_data/CLC_2020-02-11/demultiplex_dual/barcode01/fastq_runid_67a0761ea992f55d7000e748e88761780ca1bb60_0.fastq
        """

        # this will be returned
        file_paths = []

        # iterate through each directory, and collect files that contain "fastq_runid" in the name
        for root, directory, files in os.walk(barcode_parent):
            for name in files:
                if "fastq_runid" in name:
                    file_paths.append( os.path.join(root, name) )  # append file to file_paths


        return file_paths

    def count_barcodes(self, barcode_file_path):
        """
        This function will take an iterable as its parameter and count the number of barcodes present in each file
        It does this by assuming that each line that starts with two DNA base pairs (ATCG) is a barcode
            If this is wrong, it can be modified later
        It will return an integer containing the total number of barcodes found throughout the files passed in

        ------------------------------- LIST EXAMPLE -------------------------------
        barcode_file_path = [
            "/home/USERNAME/minknow_data/2020-02-15/barcode01/text_file_with_barcodes_01.txt",
            "/home/USERNAME/minknow_data/2020-02-15/barcode01/text_file_with_barcodes_02.txt",
            "/home/USERNAME/minknow_data/2020-02-15/barcode01/text_file_with_barcodes_03.txt"
        ]

        I have included a progress bar in this function for the sake of future-proofing. I am unsure how large files may be, and want to let the user know work is still being done.
        In all actuality, I believe adding a barcode makes this process take considerably longer.

        :param iterable barcode_file_path: iterable (list, tuple)
        :return: int total_barcodes
        """

        #  may be useful to implement a progress bar if the number of items is large
        number_of_files = len(barcode_file_path)

        # this will be returned
        total_barcodes = 0

        # create a simple progress bar
        # iterate over each barcode file
        for barcode_file in barcode_file_path:

            # open each `barcode_file` as `file`
            with open(barcode_file, 'r') as file:
                file_barcodes = 0
                # set the identifier for FASTQ ("@") or FASTA (">") files
                if ".fastq" in str(file):
                    identifier = "@"
                elif ".fasta" in str(file):
                    identifier = ">"

                # iterate over each line in the barcode file
                for line in file:
                    # test if the beginning of a line has the identifier (`@` or `>`)
                    if line[0] == identifier:
                        total_barcodes += 1
                        file_barcodes += 1

                self.correlate_barcodes(file_barcodes, file)

        return total_barcodes

    def correlate_barcodes(self, reads_in_file, file_path):
        """
        This function will correlate the number of barcodes to each barcode folder
        It will do this by adding a key/value pair to the dictionary self.barcode_correlations in __init__()
        This dictionary can be used in other class methods

        TODO: create a dictionary (self.barcode_correlations) containing each barcode folder (ex: barcode45) along with
            the number of reads in the file.
            Save this file in the directory containing barcode folders

        :param int reads_in_file: the number of barcodes in the current file
        :param _io.TextIO file_path: the current file path
        :return: None
        """
        str_file_path = str(file_path)
        barcode_index = str_file_path.find("barcode")
        unclassified_index = str_file_path.find("unclassified")

        """
        Barcodes are classified into one of two categories: barcode## (where ## are integers), or unclassified
        If an unclassified folder is found, barcode_index will be -1. In this case, the unclassified_index will be
            greater than -1. Use this index to find what 
        """
        if barcode_index > 0:
            barcode_folder_number = str_file_path[barcode_index: barcode_index + 9]
            file_name = str_file_path[barcode_index + 11:]

            print(file_name)

        else:
            unclassified_folder = str_file_path[unclassified_index: unclassified_index + 12]
            file_name = str_file_path[unclassified_index + 14:]

            print(file_name)
