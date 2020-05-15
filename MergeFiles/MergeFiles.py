import os  # os.walk()
import sys  # sys.argv, not used but needed for PyQt
import getpass  # get username
from PyQt5.QtWidgets import QFileDialog, QApplication, QWidget  # graphical folder selection
import re  # split strings on multiple characters


class Merge:
    def __init__(self, barcode_file_location):
        """
        This class is responsible for methods that will combine mulitple text files in one folder to one file

        self.concatonate_files_controll() will call first call self.return_new_file_name()

        self.return_new_file_name() will return the file name of the new output folder where the concatonated files
            will go

        Then, self.return_new_file_name() will return back to self.concatonate_files_control(), and self.concatonate_files()
            will take all files from the folder directory and place them into a new file, with the name returned by
            self.return_new_file_name()
        """
        self.barcode_file_location = barcode_file_location
        self.concatonate_files_controller()

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

        # find all barcode file paths
        barcode_directories = []
        for root, directory, files in os.walk(self.barcode_file_location):
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

        barcode_files = []
        for root, directory, files in os.walk(parent_folder):
            # we need to remove the barcode folder that will be created, otherwise it will add data onto itself
            for name in files:
                barcode_files.append(name)
            for file in barcode_files:
                if "_unclassified.fast" in file or "_barcode" in file:  # remove barcode or unclassified output files
                    barcode_files.remove(file)

            # concatonate data from files into the output file
            with open(output_file, 'w') as writer_file:                         # open the output file (_BARCODE##.fastq)
                for name in barcode_files:                                      # for all files in directory
                    with open( os.path.join(root, name), 'r' ) as input_file:   # open the input file
                        for line in input_file:                                 # for each line in the input file
                            writer_file.writelines(line)                        # write the line to the output file
