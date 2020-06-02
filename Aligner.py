import time
import re
import os
import shutil
import subprocess
from subprocess import PIPE
import pandas as pd
import numpy as np
from pathlib import Path
from UpdateTask import Update
from WriteLogs import Log


class GuppyAlignment:

    def __init__(self, input_directory, save_directory, align_reference):
        """
        This class will be responsible for results pertaining to read alignments. This class uses the guppy_alignment tool.
        guppy_aligner MUST be added to your $PATH, otherwise it will not work

        :param str input_directory: The location of input files (usually a directory)
        :param str save_directory: The location of output files (usually a directory)
        :param str align_reference: The location of the reference file to use (a file)
        :return: None
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
        :param: None
        :return: None
        """
        for root, directory, files in os.walk(self.input_directory):
            for file in files:
                if ".fastq" in file or ".fasta" in file:
                    self.file_names.append(file)
                    self.number_of_files += 1

    def __perform_alignment(self):
        """
        This function will iterate through self.file_paths and perform guppy_aligner on each file
        :return: None
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

        :return: new_file_path: This is the path of the new file location. It can be used to modify files further (if needed)
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

        :return: None
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

        :return: None
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

        :return: None
        """

        for root, directory, files in os.walk(self.input_directory):
            for file in files:
                if ".fasta" in file or ".fastq" in file:
                    self.file_paths.append( os.path.join( root, file ) )
                    self.number_of_files += 1

    def __perform_alignment(self):
        """
        This function will perform MiniMap2 alignment on the file paths located in self.file_paths using the self.alignment_reference as the reference file

        :return: None
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

        :return: save_path: The full file path of the new file
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

        :param str input_path: This is the input file path
        :param str save_path: This is where files will be saved
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
    def __init__(self, input_directory, save_directory):
        """
        This class will handle alignment using vsearch (a cousin of usearch)
        As of July 2nd, I've manually ran vsearch on barcode56 (positive control) with an id of 0.5 (50%).
        These results will be saved to the ScriptResults/Alignment/vsearch folder. Results will be saved to a .txt file with the
            specified barcode number as the file name

        :param str input_directory: This is the directory containing .fastx files
        :param str save_directory: This is the directory where results should be saved. Files will have the barcode number of the input file
        """
        self.input_directory = input_directory
        self.save_directory = save_directory
        command = "vsearch --allpairs_global {input_file} --id 0.5 --alnout {output_file}"

