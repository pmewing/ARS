import os  # os.walk(), os.join.path()
import pickle
import csv


class Count:
    """
    This class is responsible for counting the number of barcodes present in the output of guppy_barcode
    """
    def __init__(self, input_directory, save_directory):
        """
        this is the main driver function, and will be ran when a Count() class is implemented
        Creates a file in the directory selected containing which barcode folders

        :return str barcode_file_location: This is the location of the parent folder
        """

        self.save_directory = save_directory
        self.input_directory = input_directory
        self.unclassified_folder_duplicate_value = 0
        self.barcode_correlations = {}

        #  get locations of all barcode files
        self.file_paths = sorted(self.__return_file_paths(self.input_directory))

        #  count barcodes
        self.total_barcodes = -1  # no barcodes found
        self.total_barcodes = self.__count_barcodes(self.file_paths)
        self.__write_correlations_to_file(self.save_directory)

    def __return_file_paths(self, barcode_parent):
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
                file_paths.append( os.path.join(root, name) )  # append file to file_paths
        return file_paths

    def __count_barcodes(self, barcode_file_path):
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

        :param list barcode_file_path: iterable (list, tuple)
        :return: int total_barcodes
        """

        # this will be returned
        total_barcodes = 0

        # create a simple progress bar
        # iterate over each barcode file
        for barcode_file in barcode_file_path:

            # open each `barcode_file` as `file`
            with open(barcode_file, 'r') as file:
                file_barcodes = 0
                # set the identifier for FASTQ ("@") or FASTA (">") files
                identifier = ""
                if ".fastq" in str(file):
                    identifier = "@"
                elif ".fasta" in str(file):
                    identifier = ">"

                # we only want to use files that have .fastq/.fasta in their file name
                # `identifier` is reset after opening each file. If identifier == "", .fastq/.fasta has not been found in the file name
                if identifier is not "":
                    # iterate over each line in the barcode file
                    for line in file:
                        # test if the beginning of a line has the identifier (`@` or `>`)
                        if line[0] == identifier:
                            total_barcodes += 1
                            file_barcodes += 1

                    self.correlate_barcodes( file_barcodes, file )

        return total_barcodes

    def correlate_barcodes(self, reads_in_file, file_path):
        """
        This function will correlate the number of barcodes to each barcode folder
        It will do this by adding a key/value pair to the dictionary self.barcode_correlations in __init__()
        This dictionary can be used in other class methods

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
            folder_number = str_file_path[barcode_index: barcode_index + 9]
        else:
            folder_number = str_file_path[unclassified_index: unclassified_index + 12]

        # we want to add a new entry if the current barcode has not been added
        if folder_number not in self.barcode_correlations.keys():
            self.barcode_correlations[folder_number] = reads_in_file

        # if the entry is already present, we want to add reads_in_file to the current value
        else:
            self.barcode_correlations[folder_number] += reads_in_file

    def __write_correlations_to_file(self, save_directory):
        """
        This function will write the dictionary self.barcode_correlations to a text file. This file can be specified by
        the user. For now, this will be saved in the same directory as the barcode folders under the name
        "barcode_counts.txt".

        :param _io.TextIO save_directory: File path where barcode_counts.txt file should be saved.
        :return: None
        """
        pickle_file_name = save_directory + "/barcode_pickle_dump.pkl"
        save_directory += "/barcode_counts.csv"

        sorted_keys = sorted(self.barcode_correlations)

        # make the directory to write files. The directory may exist, so move on if it does
        try:
            os.mkdir(self.save_directory)
        except FileExistsError:
            pass

        with open(save_directory, 'w') as file:
            csv_writer = csv.writer(file)

            # write a header row
            csv_writer.writerow( ['barcode_number', 'reads_in_barcode'] )

            # using each key
            for key in sorted_keys:
                # write data to file
                csv_writer.writerow( [key, '%d' % self.barcode_correlations[key]] )

        """
        Serialization is a process that saves data to a file so it can be used in its exact state at a later time
        Python's `pickle` module does this very easily
        I am using this on the self.barcode_correlations dictionary in case its data is needed again later
        """
        output_file = open(pickle_file_name, 'wb')
        pickle.dump(self.barcode_correlations, output_file)
        output_file.close()

        """
        Reading a pickle file can be done below
        This will result in the same exact variable type as self.barcode_correlations
        
        self.barcode_correlations = { 'barcode01': [123,
                                                    FILE_NAME_01],

                                      'barcode02': [456,
                                                    FILE_NAME_02]
                                      } etc.
            
        pickle_read = r"/home/joshl/minknow_data/CLC_2020-02-11/demultiplex_dual/barcode_pickle_dump.pkl"
        infile = open(pickle_read, 'rb')
        new_dict = pickle.load(infile)
        infile.close()

        for key in new_dict:
            print(key, new_dict[key])
        """
