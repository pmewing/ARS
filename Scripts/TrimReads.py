import re
import subprocess
from subprocess import PIPE
import os
from Scripts.Global import Update, Log, Files


class Trim:
    def __init__(self, input_directory: str, save_directory: str):
        """
        This class is responsible for orienting and trimming reads using the cutadapt program
        Analysis will be performed on initiating class instance

        Args:
            input_directory: Where to read files from
            save_directory: Where to save program results
        Returns: None
        """

        self.input_directory = input_directory
        self.save_directory = save_directory
        self.file_paths = []
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

    def __collect_files(self):
        """
        This will call DataFiles, which is responsible for collecting all files with the extension file_extensions and returning a list
        Returns: None
        """
        self.file_paths = Files(input_directory=self.input_directory,
                                file_extensions=[".fastq", ".fasta"]).return_file_paths

    def trim_reads(self):
        """
        This function will iterate through the files found in self.file_paths and perform cutadapt analysis on them.
        Returns: None
        """
        for file in self.file_paths:
            self.__update_task()
            output_file = self.__create_output_files(file)

            message = "cutadapt --revcomp --quiet -j 0 -a {primer_3} -g {primer_5} -e {error_rate} -o {out_file_path} {in_file_path}".format(
                primer_3=self.primer_3,
                primer_5=self.primer_5,
                error_rate=self.error_rate,
                save_direc=self.save_directory,
                out_file_path=output_file,
                in_file_path=file
            )
            self.__write_logs_to_file(message)
            message = message.split(" ")
            command = subprocess.run(message, stdout=PIPE, stderr=PIPE, universal_newlines=True)

            if "input file format" in command.stderr.lower():
                self.unknown_files.append(file)

    def __create_output_files(self, file_path: str):
        """
        Cutadapt needs the output file to be created before it is able to write to it.
        This function will create the appropriate directories/files needed for cutadapt
        Args:
            file_path: This is the name of the file to be analyzed by cutadapt. The directory will be pulled from self.save_directory
        Returns:
            new_save_directory: This is where the output data should be saved
        """
        # split the file path by '/' and get the last item (the file name)
        # use re.split() to split by '_' and '.', which will separate the barcode number from the rest of the file name.
        # the barcode number is the second to last item
        file_name = file_path.split("/")[-1]
        barcode_number = re.split('[_.]', file_name)[-2]
        file_extension = re.split('[_.]', file_name)[-1]
        new_save_directory = self.save_directory + "/trimmed_reads{0}.{1}".format(barcode_number, file_extension)
        file = open(new_save_directory, 'w')
        file.close()
        return new_save_directory

    def __write_logs_to_file(self, command: str):
        """
        This function will output logs to the location below after trimming reads
        Args:
            command: This is the exact line that should be written to the log file
        """

        log_path = "Results/Script_Logs/trim_reads_log.txt"
        Log(command,
            log_path=log_path,
            erase_file=False)

    def __update_task(self):
        """
        This function will simply over-write the current line and print and update statement
        """
        Update("Cutadapt", self.iteration, self.num_files)
        self.iteration += 1


class Pychopper:
    def __init__(self):
        """
        This class will call pychopper from the command line through subprocess.run()
        Returns: None
        """


        subprocess.run("python2.7 pychopper/scripts/cdna_classifier.py".split(" "))