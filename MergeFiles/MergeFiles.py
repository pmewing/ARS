import os  # os.walk()
import sys  # sys.argv, not used but needed for PyQt
import getpass  # get username
from PyQt5.QtWidgets import QFileDialog, QApplication, QWidget  # graphical folder selection

import random  # TODO: remove this once done, only needed to make temporary files
import string

class Merge:
    def __init__(self):
        """
        This class is responsible for methods that will combine mulitple text files in one folder to one file
                               Example
        ------------------------------------------------------
        -folder1                --->        -folder1
        |---file01.txt                      |---file01_new.txt
        |---file02.txt
        -folder2                --->        -folder2
        |---file03.txt                      |---file03_new.txt
        |---file04.txt
        -folder3                --->        -folder3
        |---file05.txt                      |---file05.txt
        """

        # TODO: Change self.initial_directory to `r"/home/%s" % username` before production
        username = getpass.getuser()
        self.initial_directory = r"/home/%s/minknow_data/CLC_2020-02-11/" % username

        print("In the next window, select the **parent** folder of all barcode folders")
        print("Press enter to continue")
        print("(NOTE: A warning will appear; this warning cannot be resolved. Trust nothing is wrong.)", end="")
        print("\n")
        # input()

        #  sys.argv allows for passing arguments into the dialog box. This will not be used
        #  graphical interface for opening a folder
        self.q_application = QApplication(sys.argv)
        self.widget = QWidget()

        # self.barcode_file_location = str(QFileDialog.getExistingDirectory(parent=self.widget,
        #                                                                   caption="Select the barcode parent directory",
        #                                                                   directory=self.initial_directory))
        # self.make_files()
        self.concatonate_files()


    def make_files(self):
        """
        This is a temporary function to make a series of text files for testing purposes
        """
        folder_location = r"/home/joshl/PycharmProjects/ARS Projects/MergeFiles/old/"

        # make 8 files
        for i in range(8):
            file_location = folder_location + "file%s.txt" % str(i)
            with open(file_location, 'w') as file:
                file.writelines("file%s\n" % str(i))
                data_length = random.choice(range(50, 150))
                payload = ""
                for x in range(data_length):
                    payload += random.choice(string.printable)
                file.writelines("%s\n" % payload)

    def concatonate_files(self):
        folder_location = r"/home/joshl/PycharmProjects/ARS Projects/MergeFiles/old/"
        output_path = r"/home/joshl/PycharmProjects/ARS Projects/MergeFiles/new/output.txt"
        file_paths = []
        for root, dir, files in os.walk(folder_location):
            for name in files:
                file_paths.append(os.path.join(root, name))

        self.clear_file(output_path)

        file_paths = sorted(file_paths)
        for file in file_paths:
            with open(output_path, 'a') as output:
                with open(file, 'r') as input:
                    for line in input:
                        output.writelines(line)
                output.writelines("\n")

    def clear_file(self, file):
        with open(file, 'w') as clear:
            pass
