# from tkinter import filedialog
# import tkinter as tk
import os  # os.walk(), os.join.path()
import getpass  # get username


class Count:
    """
    This class is responsible for counting the number of barcodes present in the output of guppy
    TODO: Give the user a more refined option on selecting a file location
    filedialog.askdirectory(initialdir="") is the best method I have now
    """
    def __init__(self):

        # this will be more robust with user opening a dialog box
        username = getpass.getuser()
        self.barcode_parent_file = r"/home/%s/minknow_data/CLC_2020-02-11/demultiplex_dual/" % username

        # get locations of all barcode files
        self.file_paths = self.return_file_paths(self.barcode_parent_file)
        self.total_barcodes = self.count_barcodes(self.file_paths)
        print("Total barcodes: %s" % self.total_barcodes)

        # tkinter method, use once basic functionality is complete
        # self.barcode_parent_file = filedialog.askdirectory(title="Select the barcode parent directory", initialdir="~/minknow_data/CLC_2020-02-11/demultiplex_dual/", mustexist=True)

    def return_file_paths(self, barcode_parent):
        """
        This method will use the os.walk() function to collect the file path of all files that have "fastq_runid" in
            the name. This is important because guppy will output multiple files; we are only interested in the ones
            that have barcodes in the file

        :param barcode_parent: The parent directory of the barcode files
        :return: A list containing paths of barcode files.
            Ex: /home/USERNAME/minknow_data/CLC_2020-02-11/demultiplex_dual/barcode01/fastq_runid_67a0761ea992f55d7000e748e88761780ca1bb60_0.fastq
        """
        # os.walk() documentation: https://www.tutorialspoint.com/python/os_walk.htm

        file_paths = []  # this will be returned

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

        I have included a progress bar in this function for the sake of future-proofing. I am unsure how large
            files may be, and want to let the user know work is still being done.
        In all actuality, I believe adding a barcode makes this process take considerably longer.

        :param barcode_file_path: iterable (list, tuple)
        :return: total_barcodes
        """

        #  may be useful to implement a progress bar if the number of items is large
        number_of_files = len(barcode_file_path)

        # this will be returned
        total_barcodes = 0
        base_pairs = ['A', 'T', 'G', 'C']

        # create a simple progress bar
        # iterate over each barcode file
        for barcode_file in barcode_file_path:

            # open each `barcode_file` as `file`
            with open(barcode_file, 'r') as file:

                # iterate over each line in the barcode file
                for line in file:

                    # make sure that the line has DNA nucleotides in it before we count it
                    # this assumes that each read is the line containing DNA nucleotides
                    if line[0] in base_pairs and line[1] in base_pairs:
                        total_barcodes += 1
                file.close()

        return total_barcodes
