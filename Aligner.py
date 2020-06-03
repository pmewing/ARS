import time
import re
import os
import shutil
import subprocess
from subprocess import PIPE
import pandas as pd
import numpy as np
from pathlib import Path
from Global import Update, Log


class GuppyAlignment:

    def __init__(self, input_directory: str, save_directory: str, align_reference: str):
        """
        This class will be responsible for results pertaining to read alignments. This class uses the guppy_alignment tool.
        guppy_aligner MUST be added to your $PATH, otherwise it will not work

        @param input_directory: The location of input files (usually a directory)
        @param save_directory: The location of output files (usually a directory)
        @param align_reference: The location of the reference file to use (a file)
        @return None
        """

        self.input_directory = input_directory
        self.save_directory = save_directory
        self.alignment_reference = align_reference
        self.file_names = []
        self.iteration = 1
        self.number_of_files = 0

        self.alignment_summary_path = self.save_directory + "/AlignmentSummary"
        self.log_path = self.save_directory + "/logs"
        self.temp_folder = self.save_directory + "/.temp"

        self.__collect_files()
        self.__perform_alignment()
        self.__write_simple_statistics()

        self.__remove_temp_folder()

    def __collect_files(self):
        """
        This function will collect all fastq/fasta files to be analyzed by guppy_aligner.
        @param: None
        @return None
        """
        for root, directory, files in os.walk(self.input_directory):
            for file in files:
                if ".fastq" in file or ".fasta" in file:
                    self.file_names.append(file)
                    self.number_of_files += 1

    def __perform_alignment(self):
        """
        This function will iterate through self.file_paths and perform guppy_aligner on each file
        @return None
        """

        # we want to make a temporary folder. If it exists, no error will arise. This is safe to try for every run
        Path.mkdir( self=Path(self.temp_folder), exist_ok=True )

        for file in self.file_names:
            # we want to remove all files in the .temp directory before running guppy_aligner
            self.__remove_temp_files()

            # copy our current file to the temporary folder
            shutil.copy(src=self.input_directory + "/" + file,
                        dst=self.temp_folder + "/" + file)

            # create the command for guppy_aligner
            message = "guppy_aligner --input_path {input} --save_path {save} --align_ref {alignment}".format(
                input=self.temp_folder, save=self.save_directory + "/SAM_Files", alignment=self.alignment_reference )

            # write to logs the file we are running
            self.__write_log_to_file(file_path=self.input_directory + "/" + file)

            # we must split the messgae into a list before subprocess.run() will accept it
            # additionally, we are capturing output from the guppy_aligner. I do not plan on using the output as of now, but it is there in case it is needed
            message = message.split(" ")
            command = subprocess.run(message, stdout=PIPE, stderr=PIPE)

            # we need to move the alignment_summary.txt file into the appropriate place immediately after running guppy_aligner
            self.__move_summary_files(file)

    def __move_summary_files(self, file_name):
        """
        guppy_aligner creates a result file, log file, and a .sam file for every .fastq file used. I don't like these files
        in the same directory, as the result file is more useful.

        Because of this, all files are initially saved to the
        SAM_Files directory, then the result and log files are moved one level up.

        @return new_file_path: This is the path of the new file location. It can be used to modify files further (if needed)
        """

        # make the AlignmentSummary and logs folders
        Path.mkdir(self=Path(self.alignment_summary_path), exist_ok=True)
        Path.mkdir(self=Path(self.log_path), exist_ok=True)

        # get the barcode number from the file name. It will be the second to last item after splitting by `_` and `.`
        barcode_name = re.split('[_.]', file_name)[-2]

        # move the alignment_summary.txt and read_processor to the parent directory
        sam_files = self.save_directory + "/SAM_Files"
        for root, directory, files in os.walk(sam_files):
            for file in files:
                # move alignment summary into the AlignmentSummary folder (located one folder up)
                if "alignment_summary" in file:
                    shutil.move(src=sam_files + "/" + file,
                                dst=self.alignment_summary_path + "/guppy_aligner_" + barcode_name + ".csv")
                elif "read_processor" in file:
                    # this will rename files to the current date/time and barcode number
                    file_name = self.__get_date_time(barcode_number=barcode_name)
                    shutil.move(src=sam_files + "/" + file,
                                dst=self.log_path + "/" + file_name)

    def __write_simple_statistics(self):
        """
        This function will look at the alignment_summary.txt in the folder specified by self.save_directory.
        It will calculate the percentage of reads that have been classified, and save its own text file in the same location

        @return None
        """

        # read file into a data frame
        file_paths = []
        for root, directory, files in os.walk( self.save_directory + "/AlignmentSummary" ):
            for file in files:
                if "guppy_aligner_barcode" in file:
                    file_paths.append( os.path.join(root, file) )

        # iterate through each file in the file_paths list
        for file in file_paths:

            # set up the data frame for reading
            data_frame = pd.read_csv(filepath_or_buffer=file,
                                     sep="\t",
                                     header=0,
                                     dtype={
                                         "read_id": np.str,
                                         "alignment_genome": np.str,
                                         "alignment_genome_start": np.int,
                                         "alignment_genome_end": np.int,
                                         "alignment_strand_start": np.int,
                                         "alignment_strand_end": np.int,
                                         "alignment_num_insertions": np.int,
                                         "alignment_num_deletions": np.int,
                                         "alignment_num_aligned": np.int,
                                         "alignment_num_correct": np.int,
                                         "alignment_identity": np.float,
                                         "alignment_accuracy": np.float,
                                         "alignment_score": np.int
                                     })

            # set up our total reads, classified reads, and unclassified reads variables
            total_id = 0
            classified_id = 0
            unclassified_id = 0

            for row in data_frame['alignment_genome']:

                # if the item in `alignment_genome` has data not equal to an asterisk, it is classified
                if row != "*":
                    classified_id += 1

                # otherwise it is unclassified
                else:
                    unclassified_id += 1
                total_id += 1  # always increment total reads

            # set up our output results
            rows = [
                "Total reads: {0}".format(total_id),
                "Classified reads: {0}".format(classified_id),
                "Unclassified reads: {0}".format(unclassified_id),
                "Percent classified: {:.3f}%".format( (classified_id / total_id) * 100 ) ,
                "Percent unclassified: {:.3f}%".format( (unclassified_id / total_id) * 100 )
            ]

            # we want to make an new folder to hold the simple statistics that will be generated for each file
            simple_statistics_folder = self.save_directory + "/SimpleStatistics"
            Path.mkdir( self=Path(simple_statistics_folder), exist_ok=True )

            barcode_number = re.split('[_.]', file)[-2]  # we want the second to last item in the path, the barcode number

            # open the output file, and write our data from the `rows` list
            with open(simple_statistics_folder + "/simple_statistics_{0}.txt".format(barcode_number), 'w') as output_file:
                for row in rows:
                    output_file.write(row)
                    output_file.write("\n")

    def __remove_temp_files(self):
        """
        This function will remove temporary files/directories in the self.save_directory + "/temp" folder, if any are present.
        """

        for root, directory, files in os.walk(self.temp_folder):
            for temp_file in files:
                os.remove(self.temp_folder + "/" + temp_file)
            for direc in directory:
                os.rmdir(self.temp_folder + "/" + direc)

    def __remove_temp_folder(self):
        """
        This function will be called at the very end of the GuppyAligner class to remove the .temp folder.
        The folder is not needed for long term storage, and can be safely deleted
        """
        shutil.rmtree(self.temp_folder)

    def __get_date_time(self, barcode_number):
        """
        This function is simply responsible for getting the date in the following format
        YEAR_MONTH_DAY-HOUR-MINUTE-BARCODE##.txt

        @return None
        """
        return time.strftime("%Y_%m_%d-%H_%M-{0}.txt".format(barcode_number))

    def __update_task(self):
        Update("Guppy aligner", self.iteration, self.number_of_files)
        self.iteration += 1

    def __write_log_to_file(self, file_path):
        """
        This function will call the Log class to write a specific line to the log file named below
        """

        log_path = "ScriptResults/Script_Logs/guppy_aligner_log.txt"
        line = "guppy_aligner --input_path {input} --save_path {save} --align_ref {alignment}".format(
            input=file_path, save=self.save_directory, alignment=self.alignment_reference )

        Log(log_line=line,
            log_path=log_path,
            erase_file=False)


class MiniMap2:
    def __init__(self, input_directory, save_directory, align_reference):
        self.input_directory = input_directory
        self.save_directory = save_directory
        self.alignment_reference = align_reference
        self.file_paths = []
        self.iteration = 1
        self.number_of_files = 0

        self.__collect_files()
        self.__perform_alignment()
        # reset iteration to 1, go to next line for new output
        self.iteration = 1
        print("")

        # self.__create_table_headers()

    def __collect_files(self):
        """
        This function will collect .fastq/.fasta files from the self.input_directory and save their file path to the self.file_paths list.

        @return None
        """

        for root, directory, files in os.walk(self.input_directory):
            for file in files:
                if ".fasta" in file or ".fastq" in file:
                    self.file_paths.append( os.path.join( root, file ) )
                    self.number_of_files += 1

    def __perform_alignment(self):
        """
        This function will perform MiniMap2 alignment on the file paths located in self.file_paths using the self.alignment_reference as the reference file

        @return None
        """
        for file in self.file_paths:
            self.__update_task()
            save_path = self.__return_save_path(file)

            # try to make the output path to ensure it exists
            Path.mkdir( self=Path(self.save_directory), exist_ok=True )

            # -a: output in SAM format
            # -x: use map-ont for mapping results
            message = "minimap2 -ax map-ont {reference} {input} -o {output}".format(reference=self.alignment_reference, input=file, output=save_path)
            self.__write_logs_to_file(file, save_path)

            message = message.split(" ")
            # I am collecting all output from the MiniMap2 commands because it is not needed. If it is needed in the future, remove the PIPE commands from here
            # alternatively, print the results with print(command.stdout) and print(command.stderr)
            command = subprocess.run( message, stdout=PIPE, stderr=PIPE, universal_newlines=True )

    def __create_table_headers(self):
        """
        MiniMap2 does not provide a header row for their output. Because of this, it is very difficult to create a data frame from their results.
        This function works to resolve this by adding a header to the very beginning of the file
        """
        for root, directory, files in os.walk(self.save_directory):
            for file in files:
                file_path = os.path.join( root, file )

                # read data from file
                input_content = []
                with open(file_path, 'r') as input_file:
                    for line in input_file:
                        input_content.append(line)

                # TODO: A header line needs to be added to the MiniMap2 output before it can be read into a data frame
                header_line = "this\tis\tmy\theader\trow\tfor\tminimap2\tcsv\tfile\n"
                output_content = [header_line]
                for line in input_content:
                    output_content.append(line)

                with open(file_path, 'w') as output_file:
                    for line in output_content:
                        output_file.write(line)

    def __return_save_path(self, input_file):
        """
        This function will extract the barcode number of the file MiniMap2 is going to analyze. It will return the full file path of where this output should be stored
        MiniMap2 will create the files as needed

        @return save_path: The full file path of the new file
        """
        barcode_number = re.split('[_.]', input_file)[-2]  # we want the second to last item in the list, the barcode number
        save_path = self.save_directory + "/minimap_{0}.csv".format(barcode_number)
        return save_path

    def __update_task(self):
        Update("MiniMap2", self.iteration, self.number_of_files)
        self.iteration += 1

    def __write_logs_to_file(self, input_path, save_path):
        """
        This function will use the Log class to write logs to the file specified below.

        @param str input_path: This is the input file path
        @param str save_path: This is where files will be saved
        """

        log_path = "ScriptResults/Script_Logs/minimap_aligner_log.txt"
        line = "minimap2 {reference} {input} -o {output}".format(
            reference=self.alignment_reference,
            input=input_path,
            output=save_path)

        Log(log_line=line,
            log_path=log_path,
            erase_file=False)


class VSearch:
    def __init__(self, input_directory: str, save_directory: str, match_rate: float = 0.90):
        """

        This class will handle alignment using vsearch (a cousin of usearch)
        match_rate is a percentage. If its value is between 0 and 1, it will be taken as a percent (i.e. 0.42 = 42%).
            If this value is between 1 and 100, it will be divided by 100 to create a percent (i.e. 57 -> 0.57 = 57%)

        Args:
            input_directory: This is the directory containing .fasta/.fastq files
            save_directory: This is the directory where results should be saved. Files will have the barcode number of the input file
            match_rate: This is the `id` rate of vsearch. It specifies the specificity in percent that vsearch should use. By default, it is set to 0.90 (90%)

        Returns:
            None
        """
        self.input_directory = input_directory
        self.save_directory = save_directory
        self.match_rate = match_rate
        self.file_paths = []
        self.number_of_files = 0
        self.iteration = 1

        self.__check_match_rate()
        self.__collect_files()
        self.__perform_alignment()

    def __check_match_rate(self):
        """
        This function will check the match_input value.
        If it is greater than 1, it will divide by 100 to create a percentage (45 -> 0.45)
        If it is less than 0, it will break the script and give output that the match_rate is incorrect
        If it is between 0 and 1, it will do nothing
        Returns:
            None
        """
        # self.match rate greater than 1 and less than 100 (percent greater than 100 is not valid
        if 1.0 < self.match_rate < 100.0:
            self.match_rate /= 100
        elif self.match_rate <= 0:
            print("Sorry, your match_rate argument must be a percentage between 0 and 1.")
            exit(0)

    def __collect_files(self):
        """
        This will retrieve .fasta/.fastq files from the input_directory parameter.
        It will save entire file paths to self.file_paths, and add 1 to self.number_of_files in the process
        This will collect all .fasta/.fastq files in the input_directory, so be aware of where files are saved

        Returns:
            None
        """
        for root, directory, files in os.walk(self.input_directory):
            for file in files:
                # iterate through files and collect .fasta/.fastq files
                if ".fasta" in file or ".fastq" in file:
                    self.file_paths.append( os.path.join(root, file) )
                    self.number_of_files += 1

    def __perform_alignment(self):
        """
        This function will perform vsearch on all files in the self.file_paths list.

        Returns:
            None
        """
        for file in self.file_paths:
            self.__update_task()
            new_save_path = self.__return_new_save_path(file)
            message = "vsearch --id {id_rate} --allpairs_global {input_file} --alnout {output_file}".format(input_file=file,
                                                                                                            id_rate=self.match_rate,
                                                                                                            output_file=new_save_path)
            message = message.split(" ")
            command = subprocess.run(message, stdout=PIPE, stderr=PIPE, universal_newlines=True)

    def __return_new_save_path(self, file_path: str):
        """
        This function will take one a file input path and extract its barcode from the name (i.e. barcode45). It will then concatonate this number to
            self.save_directory, and return the new string. This provides the new save path.

        The new file will be created by this function to ensure it can be written to.
        Args:
            file_path: The file path that is going to be analyzed

        Returns:
            new_path: This is a file path that points to a valid file. The file will be created.
        """

        # we want to get the last item in the path, the file name
        # re.split() will split by `_` and `.`, both of which are in the file name. The second to last item is the barcode number (the last item is the file extension)
        file_name = file_path.split("/")[-1]
        barcode_number = re.split('[_.]', file_name)[-2]
        new_file_name = self.save_directory + "/vsearch_{0}.txt".format(barcode_number)

        # open the file path to ensure it exists
        try:
            file = open(new_file_name, 'w+')
            file.close()
        except FileNotFoundError:
            print("Your save directory does not exist. It will be created now, along with the output file.")
            print("path: {0}".format(new_file_name))
            print("")
            Path.mkdir(self=Path(self.save_directory), exist_ok=True)

            file = open(new_file_name, 'w')
            file.close()

        return new_file_name

    def __update_task(self):
        Update("vsearch", self.iteration, self.number_of_files)
        self.iteration += 1