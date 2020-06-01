import subprocess
from subprocess import PIPE
import os
import time
from UpdateTask import Update
from WriteLogs import Log

class Trim:
    def __init__(self, input_directory, save_directory):
        """
        This class is responsible for orienting and trimming reads using the cutadapt program
        Analysis will be performed on initiating class instance
        :param str input_directory: Where to read files from
        :param str save_directory: Where to save program results
        :return: None
        """

        self.input_directory = input_directory
        self.save_directory = save_directory
        self.unknown_files = []

        self.primer_5 = "TTTCTGTTGGTGCTGATATTGCAGRGTTYGATYMTGGCTCAG"
        self.primer_3 = "ACTTGCCTGTCGCTCTATCTTCTACCTTGTTACGACTT"
        self.primer_5_no_adapter = "AGRGTTYGATYMTGGCTCAG"
        self.primer_3_no_adapter = "TACCTTGTTACGACTT"
        self.error_rate = 0.15

        self.num_files = len(os.listdir(self.input_directory))
        self.iteration = 1
        self.trim_reads()

        """
        This will print some simple updates to the command line at the end of the process if items were unable to be processed by cutadapt.
        It is most likely that these files are csv files, log files, etc. and not .fastq files, but it doesn't hurt to let the user know that something went wrong 
        """
        if len(self.unknown_files) > 1:
            print("\rCutadapt did not know how to process the following files:")
            for file in self.unknown_files:
                print("\t%s" % file)
        elif len(self.unknown_files) == 1:
            print("\rCutadapt did not know how to process the following file: %s" % self.unknown_files[0])

    def trim_reads(self):
        for root, directory, files in os.walk(self.input_directory):
            for file in files:
                self.__update_task()
                # cutadapt needs the output file to be created before it is able to write to it
                # we will create it here
                write_file = open(os.path.join(self.save_directory, file), 'w')
                write_file.close()

                message = "cutadapt --revcomp --quiet -j 0 -a {primer_3} -g {primer_5} -e {error_rate} -o {save_direc}/{out_file_name} {in_file_path}".format(
                    primer_3=self.primer_3,
                    primer_5=self.primer_5,
                    error_rate=self.error_rate,
                    save_direc=self.save_directory,
                    out_file_name=file,
                    in_file_path=os.path.join(root, file)
                )
                self.__write_logs_to_file(message)
                message = message.split(" ")
                command = subprocess.run(message, stdout=PIPE, stderr=PIPE, universal_newlines=True)
                if "input file format" in command.stderr.lower():
                    self.unknown_files.append(file)

    def __write_logs_to_file(self, command):
        """
        This function will output logs to the location below after trimming reads
        """

        log_path = "ScriptResults/Script_Logs/trim_reads_log.txt"
        Log(command,
            log_path=log_path,
            erase_file=False)

    def __update_task(self):
        """
        This function will simply over-write the current line and print and update statement
        """
        Update("Cutadapt", self.iteration, self.num_files)
        self.iteration += 1
