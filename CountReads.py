import subprocess
import os  # os.walk(), os.join.path()
import pickle
import csv
from Global import Log


class Count:
    """
    This class is responsible for counting the number of barcodes present in the output of guppy_barcode
    """
    def __init__(self, input_directory, save_directory, file_name=None):
        """
        this is the main driver function, and will be ran when a Count() class is implemented
        Creates a file in the directory selected containing which barcode folders
        This will only work on .fastq/.fasta files

        :param str input_directory: The input location of .fastx files that you would like to count the number of reads of
        :param str save_directory: This is where the resulting .csv file will be saved
        :param str file_name: An optional parameter of the name of the file. A `.csv` extension will automatically be added at the end of your file name
        :return: None
        """

        self.save_directory = save_directory
        self.input_directory = input_directory
        self.file_name = file_name
        self.unclassified_folder_duplicate_value = 0
        self.barcode_correlations = {}

        #  get locations of all barcode files
        self.file_paths = sorted(self.__return_file_paths(self.input_directory))

        # we want to check the output of paths, and ensure that the argument input is correct
        self.__validate_file_argument_input()

        #  count barcodes
        self.total_barcodes = -1  # no barcodes found
        self.total_barcodes = self.__count_barcodes(self.file_paths)
        self.__write_correlations_to_file()

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

    def __validate_file_argument_input(self):
        correct_input = True

        # try to clear the screen
        try:
            subprocess.run("clear")
        except FileNotFoundError:
            subprocess.run("cls")

        if len(self.file_paths) == 0:
            print("")
            print("No files were returned from your input path")
            print("If your path contains spaces, please place quotations around them when calling CountReads.py")
            print( "Input path: {0}".format(self.input_directory) )
            correct_input = False

        if not os.path.isdir(self.input_directory):
            print("")
            print("Your input path is not a directory")
            print("If your path contains spaces, please place quotations around them when calling CountReads.py")
            print( "Input path: {0}".format(self.save_directory) )
            correct_input = False

        if not os.path.isdir(self.save_directory):
            print("")
            print("Your save path is not a directory")
            print( "Save path: {0}".format(self.save_directory) )
            correct_input = False

        # if `/` or `\` in self.file_name, tell user they cannot do this
        if self.file_name is not None and any(x in "\\/" for x in self.file_name):
            print("")
            print("You cannot have a slash (forward or backward) in your file name")
            print("File name: {0}".format(self.file_name))
            correct_input = False

        if not correct_input:
            exit(0)

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

                    self.__correlate_barcodes(file_barcodes, file)

        return total_barcodes

    def __correlate_barcodes(self, reads_in_file, file_path):
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
            greater than -1. Use this index to determine the folder name
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

    def __write_correlations_to_file(self):
        """
        This function will write the dictionary self.barcode_correlations to a text file. This file can be specified by
        the user. For now, this will be saved in the same directory as the barcode folders under the name
        "barcode_counts.txt".

        :param: None
        :return: None
        """

        if self.file_name is None:
            pickle_file_name = self.save_directory + "/barcode_pickle_dump.pkl"
            save_directory = self.save_directory + "/barcode_counts.csv"
        else:
            pickle_file_name = self.save_directory + "/{0}.pkl".format(self.file_name)
            save_directory = self.save_directory + "/{0}.csv".format(self.file_name)

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
                self.__write_log_to_file(key)

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

    def __write_log_to_file(self, barcode_number: str):
        """
        This function will write to a log file stating what barcode is being counted

        It will write logs in the following format: YEAR-MONTH-DAY HOUR:MINUTE -- COMMAND LINE
                                                    2020-06-01 09:35 | barcode03 completed counting
                                                    2020-06-01 15:05 | barcode45 completed counting

        :param str barcode_number: This is the current file path that is being counted
        """

        try:
            log_path = snakemake.input.log_path
        except FileNotFoundError:
            log_path = r"ScriptResults/Script_Logs/count_reads_log.txt"

        # find the barcode index to know that it has been counted
        barcode_index = -1
        for index in range(len(self.file_paths)):
            if barcode_number in self.file_paths[index]:
                barcode_index = index

        # the barcode has NOT been found
        if barcode_index is -1:
            Log("Unknown Barcode: {0}".format(barcode_number),
                log_path=log_path,
                erase_file=False)

        # the barcode HAS been found
        else:
            Log("Completed count on: {0}".format(self.file_paths[barcode_index]),
                log_path=log_path,
                erase_file=False)


def get_input_directory():
    return snakemake.input.input_directory


def get_save_directory():
    return snakemake.output.save_directory


def start_counts():
    arguments = []
    # the file name is always passed in as an argument, so we must add 1 to the total number of argv's we think we are getting
    if len(arguments) == 3:
        Count(input_directory=arguments[1], save_directory=arguments[2])
    elif len(arguments) == 4:
        Count(input_directory=arguments[1], save_directory=arguments[2], file_name=arguments[3])
    else:
        print(arguments)
        print("")
        print("You must include an argument for the following parameters:")
        print("input_directory: The input location of .fastx files that you would like to count the number of reads ")
        print("save_directory: This is where the resulting .csv file will be saved")
        print("(optional) file_name: An optional parameter of the name of the file. A `.csv` extension will automatically be added at the end of your file name")
        print("")


if __name__ == '__main__':
    Count(input_directory=get_input_directory(),
          save_directory=get_save_directory())
