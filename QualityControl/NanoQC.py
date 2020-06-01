import time
import re
import subprocess
from subprocess import PIPE
import os
import shutil
from UpdateTask import Update
from WriteLogs import Log


class NanoQCAnalysis:
    def __init__(self, input_directory, save_directory):
        self.input_directory = input_directory
        self.save_directory = save_directory
        self.iteration = 1
        self.num_files = len(os.listdir(self.input_directory))
        self.unknown_files = []

        # This will be updated by self.__perform_analysis. It will be used by self.__write_logs_to_file to write the file being analyzed
        self.log_message = ""

        for root, directory, files in os.walk(self.input_directory):
            for name in files:
                self.__update_task()
                self.__perform_analysis(os.path.join(root, name))

        """
        This will print some simple updates to the command line at the end of the process if items were unable to be processed by nanoQC.
        It is most likely that these files are csv files, log files, etc. and not .fastq files, but it doesn't hurt to let the user know that something went wrong 
        """
        if len(self.unknown_files) > 1:
            print("\rnanoQC could not perform analysis on the following files:")
            for file in self.unknown_files:
                print("\t%s" % file)
        elif len(self.unknown_files) == 1:
            print("\rnanoQC could not perform analysis on the following file: %s" % self.unknown_files[0])

    def __perform_analysis(self, file_path):
        """
        This function will perform QualityControl analysis on all files in the _merged_files folder. It does not work at the
            moment, but it will eventually

         :param str file_path: this is the location of the file to be analyzed
         :return: None
        """
        message = "nanoQC -o {0} {1}".format(self.save_directory, file_path)
        self.log_message = message
        message = message.split(" ")
        command = subprocess.run(message, stdout=PIPE, stderr=PIPE, universal_newlines=True)

        # we only want to bring the last item with us (the file name) to show on screen
        if "input error" in command.stderr.lower():
            self.unknown_files.append(file_path.split("/")[-1])

        self.rename_files(file_path)

    def rename_files(self, file_path):
        """
        This function will rename the generic `nanoQC.html` file into an html file with the barcode name; i.e. fastq_runid_67a0761ea992f55d7000e748e88761780ca1bb60_barcode01.html
        """
        """
        The following series of commands will extract the barcode number from the file path
        """
        file_path_list = re.split('[_.]', file_path)   # split on `_` or `.`
        barcode_number = file_path_list[-2]  # take the second to last item in the file (this will be the barcode number)
        new_file_name = "nanoQC_" + barcode_number + ".html"
        new_file_path = self.save_directory + "/" + new_file_name
        new_log_path = self.save_directory + "/logs/" + barcode_number + ".log"

        # we need to make sure the log directory exists
        try:
            os.mkdir(self.save_directory + "/logs")
        except FileExistsError:
            pass

        for root, directory, files in os.walk(self.save_directory):
            for name in files:

                # this will move nanoQC.html to nanoQC_barcode##.html
                # it will also remove the old nanoQC.html file
                if name.lower() == "nanoqc.html":
                    os.rename(file_path, new_file_path)
                    os.remove(self.save_directory + "/nanoQC.html")
                    self.__write_logs_to_file()

                # this will move NanoQC.log to nanoQC_barcode##.log, inside the log directory
                elif name.lower() == "nanoqc.log":
                    # the file needs to exist before we can move a new item into it
                    temp_file = open(new_log_path, 'w')
                    temp_file.close()
                    shutil.move(self.save_directory + "/NanoQC.log", new_log_path)

    def __write_logs_to_file(self):
        """
        This function will write log files to the location specified below after running NanoQC
        """

        log_path = "ScriptResults/Script_Logs/nanoqc_log.txt"

        Log(self.log_message,
            log_path=log_path,
            erase_file=False)

    def __update_task(self):
        """
        This function will simply over-write the current line and print and update statement
        """
        Update("nanoQC", self.iteration, self.num_files)
        self.iteration += 1

