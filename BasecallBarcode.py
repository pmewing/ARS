import subprocess
from subprocess import PIPE
import os
import shutil
from WriteLogs import Log
from UpdateTask import Update


class Basecall:
    def __init__(self, input_directory, save_directory):
        self.iteration = 1
        self.total_files = 0
        self.input_directory = input_directory
        self.save_directory = save_directory

        self.__count_files()
        self.__basecall(input_directory=input_directory, save_directory=save_directory)

    def __count_files(self):
        for root, directory, files in os.walk(self.input_directory):
            for file in files:
                self.total_files += 1

    def __basecall(self, input_directory, save_directory):
        """
        This is a direct copy-paste from the bash script provided by patrick
        Basecall using the fast neural network.
        Two underscores on this function classifies this as a private function

        :param str input_directory: This is where basecalling should get files from
        :param str save_directory: This is where the output of basecalling should be saved
        :return: None
        """

        self.__update_task()
        message = "guppy_basecaller " \
                  "--recursive " \
                  "--input_path {0} " \
                  "--save_path {1} " \
                  "--config dna_r9.4.1_450bps_fast.cfg " \
                  "--num_callers 1 " \
                  "--cpu_threads_per_caller 12".format(input_directory, save_directory)

        self.__write_logs_to_file(command=message)
        message = message.split(" ")
        subprocess.run(message, stderr=PIPE, stdout=PIPE, universal_newlines=True)
        move_log_files(save_directory=save_directory)

    def __write_logs_to_file(self, command):
        log_path = "ScriptResults/Script_Logs/basecall_log.txt"
        Log(log_line=command,
            log_path=log_path,
            erase_file=False)

    def __update_task(self):
        Update("Guppy basecaller", self.iteration, self.total_files)
        self.iteration += 1


class Barcode:
    def __init__(self, input_directory, save_directory):
        self.iteration = 1
        self.total_files = 0
        self.input_directory = input_directory
        self.save_directory = save_directory

        self.__count_files()
        self.__barcode(input_directory=input_directory, save_directory=save_directory)

    def __count_files(self):
        for root, directory, files in os.walk(self.input_directory):
            for file in files:
                self.total_files += 1

    def __barcode(self, input_directory, save_directory):
        """
        This function will call guppy_barcoder on the input_directory, and save files into the save_directory
        :param str input_directory: This is where barcoding should get files from
        :param str save_directory: This is where the output of barcoding should be saved
        :return: None
        """
        self.__update_task()
        message = "guppy_barcoder " \
                  "--input_path {0} " \
                  "--save_path {1} " \
                  "--recursive " \
                  "--config configuration.cfg " \
                  "--worker_threads 12 " \
                  "--barcode_kits EXP-PBC096 " \
                  "--require_barcodes_both_ends".format(input_directory, save_directory)
        self.__write_logs_to_file(message)
        message = message.split(" ")
        subprocess.run(message, stdout=PIPE, stderr=PIPE)

        move_log_files(save_directory=save_directory)

    def __write_logs_to_file(self, command):
        log_path = "ScriptResults/Script_Logs/barcode_log.txt"
        Log(log_line=command,
            log_path=log_path,
            erase_file=False)

    def __update_task(self):
        Update("Guppy basecaller", self.iteration, self.total_files)
        self.iteration += 1


def move_log_files(save_directory):
    """
    This function will move log files to their own folder within the save_directory parameter
    :param str save_directory: This is the location where the output is stored. A new folder`logs` will be created here
    """

    # these lines will move log files into their own folder within the save_directory
    new_path = save_directory + "/logs"
    for root, directory, files in os.walk(save_directory):
        for file in files:
            if ".log" in file:
                # the output files may not be created. Try to move files. If they cannot be moved, create them
                try:
                    shutil.move(os.path.join(root, file), os.path.join(new_path, file))
                except FileNotFoundError:
                    os.mkdir(new_path)
                    shutil.move(os.path.join(root, file), os.path.join(new_path, file))
