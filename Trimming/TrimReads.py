import subprocess
from subprocess import PIPE
import os


class Trim:
    def __init__(self, input_directory, save_directory):
        """
        This class is responsible for orienting and trimming reads using the cutadapt program
        Analysis will be performed on initiating class instance
        :param str input_directory: Where to read files from
        :param str save_directory: Where to save program results
        :return: None
        """
        # cutadapt --revcomp -a <3' PRIMER SEQUENCE> -g <5' PRIMER SEQUENCE> -e <ERROR RATE (0.2)> -o <OUTPUT DIRECTORY> <INPUT FILE>

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

                message = ("cutadapt --revcomp --quiet -j 0 -a %s -g %s -e %s -o %s/%s %s" % (
                    self.primer_3, self.primer_5, self.error_rate, self.save_directory, file, os.path.join(root, file) ) ).split(" ")

                command = subprocess.run(message, stdout=PIPE, stderr=PIPE, universal_newlines=True)
                if "input file format" in command.stderr.lower():
                    self.unknown_files.append(file)

    def __update_task(self):
        """
        This function will simply over-write the current line and print and update statement
        """
        print("\rTrimming {0} of {1} of possible files".format(self.iteration, self.num_files), end='')
        # print('\r', 'Trimming %s of %s' % (self.iteration, self.num_files), end='')
        self.iteration += 1
