import os  # os.walk()
import sys  # sys.argv, not used but needed for PyQt
import getpass  # get username
from PyQt5.QtWidgets import QFileDialog, QApplication, QWidget  # graphical folder selection
import re  # split strings on multiple characters

import random  # TODO: remove this once done, only needed to make temporary files
import string


class Merge:
    def __init__(self):
        # TODO: Document the rest of this class
        # TODO: Make these functions work with .fastq/.fasta/etc files
        """
        This class is responsible for methods that will combine mulitple text files in one folder to one file
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
        self.concatonate_files_controller()

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

    def concatonate_files_controller(self):
        """
        This function will move multiple files into one
        It is responsible for calling multiple secondary methods: return_new_file_name and concatonate_files
        return_new_file_name will return the name of the new file that the current barcode reads will go into
        concatonate_files will
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
        username = getpass.getuser()
        parent_folder_path = r"/home/%s/minknow_data/CLC_2020-02-11/demultiplex_dual/" % username

        # find all barcode file paths
        barcode_directories = []
        for root, directory, files in os.walk(parent_folder_path):
            for name in directory:
                barcode_directories.append( os.path.join(root, name) )

        # iterate through each barcode directory
        for item in barcode_directories:
            number_of_files = 0
            # get all subitems in barcode directories (this will be the fastq/fasta files)
            for root, directory, files in os.walk(item):
                for name in files:
                    number_of_files += 1

            # more than one file exists in this subdirectory, concatonate them
            if number_of_files > 1:

                file_name = os.listdir(item)[0]     # get the first file name in the directory
                root = os.path.abspath(item)        # get the absolute path for the file

                new_file_path = self.return_new_file_name(file_name, root)
                self.concatonate_files(new_file_path, root)

    def return_new_file_name(self, file_name, root_path):
        """
        This function will generate the appropriate file name for multiple files in the barcode folders
        It will append the barcode number to the end of the file (but before the file extension)
        :param str file_name: This should be a file name; by default, it will be in the formst fastq_runid_RunIDNumber_##.fastq
        :param str root_path: This is the absolute path of the file_name parameter
        :return str file_output_path: This is the path of the new file. It will have the barcode number between the end of the file and the file extension
        """
        fastq_runid = re.split('[_.]', file_name)   # split on `_` or `.`
        barcode_number = root_path.split("/")[-1]   # get the barcode number
        fastq_or_fasta = fastq_runid[-1]            # get the .fastq/.fasta file extension

        # create the new file name
        new_file_name = "_".join(fastq_runid[:3])                       # join first three elements
        new_file_name += "_%s.%s" % (barcode_number, fastq_or_fasta)    # append the barcode number and file extension

        # this will merge the root_path and file_name variables to make the path for the output file
        file_output = root_path + "/" + new_file_name

        return file_output

    def concatonate_files(self, output_file, parent_folder):
        """
        This function will concatonate all files in parent_folder and place their contents in output_file
        :param str output_file: This is the location of the output file. At the start of this function, this file has not yet been created
        :param str parent_folder: This is the location of the parent folder of the output_file. It will be used to get all files in the folder
        :return: None
        """

        # print("output: %s" % output_file)
        # print("Parent folder: %s" % parent_folder)
        # for root, directory, files in os.walk(parent_folder):
        #     for d in directory:
        #         print(d)
        #     for n in files:
        #         print(n)

        # we need to remove the barcode folder we are creating, otherwise it will add data onto itself
        barcode_files = []

        for root, directory, files in os.walk(parent_folder):                   # get all files in directory
            for name in files:
                barcode_files.append(name)

        # TODO: remove _barcode## from barcode_files. It will recursivley add its own data into itself right now




            # with open(output_file, 'w') as writer_file:                         # open the output file (_BARCODE##.fastq)
            #     for name in files:                                              # for all files in directory
            #         with open( os.path.join(root, name), 'r' ) as input_file:   # open the input file
            #             for line in input_file:                                 # for each line in the input file
            #                 writer_file.writelines(line)                        # write the line to the output file



    def clear_file(self, file):
        f = open(file, 'w')
        f.close()
