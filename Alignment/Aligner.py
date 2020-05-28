import time
import re
import os
import shutil
import subprocess
from subprocess import PIPE
import pandas as pd
import numpy as np
import pathlib


class GuppyAlignment:

    def __init__(self, input_directory, save_directory, align_reference):
        """
        This class will be responsible for results pertaining to read alignments. This class uses the guppy_alignment tool.
        guppy_aligner MUST be added to your $PATH, otherwise it will not work

        TODO: Instead of running guppy_aligner on the parent folder, run it on each fastq/fasta file within the parent folder to generate an alignment_summary.txt for each file
            instead of one summary for all files.
            This can be achieved by quieting the output of guppy_aligner and printing my own updates

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

        self.__collect_files()


        self.__perform_alignment()
        # self.__move_summary_files()
        # self.__read_percentage()

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
        # pass this temp folder in to guppy so an alignment sequence can be made for each file
        temp_folder = self.save_directory + "/.temp"
        pathlib.Path.mkdir(self=pathlib.Path( temp_folder ),  # convert a string to a path
                           exist_ok=True)                     # it is okay if the path already exists

        for file in self.file_names:
            print("\rPerforming alignent on file {0} / {1}.".format(self.iteration, self.number_of_files), end="")

            # we want to remove all files in the .temp directory after each run of the guppy_aligner
            for root, directory, files in os.walk(temp_folder):
                for temp_file in files:
                    os.remove(temp_folder + "/" + temp_file)
                for direc in directory:
                    os.rmdir(temp_folder + "/" + direc)

            # copy the file to the temp folder
            shutil.copy(src=self.input_directory + "/" + file,
                        dst=temp_folder + "/" + file)

            # create the command for guppy_aligner
            message = "guppy_aligner --quiet --input_path %s --save_path %s --align_ref %s" % (
                temp_folder, self.save_directory + "/SAM_Files", self.alignment_reference)

            # we must split the messgae into a list before subprocess.run() will accept it
            # additionally, we are capturing output from the guppy_aligner. I do not plan on using the output as of now, but it is there in case it is needed
            message = message.split(" ")
            command = subprocess.run(message, stdout=PIPE, stderr=PIPE)

            # we need to move the alignment_summary.txt file into the appropriate place immediately after running guppy_aligner
            self.__move_summary_files(file)
            self.iteration += 1

    def __move_summary_files(self, file_name):
        """
        guppy_aligner creates a result file, log file, and a .sam file for every .fastq file used. I don't like these files
        in the same directory, as the result file is more useful.

        Because of this, all files are initially saved to the
        SAM_Files directory, then the result and log files are moved one level up.

        :return: None
        """

        # make the AlignmentSummary folder
        alignment_summary_path = self.save_directory + "/AlignmentSummary"
        log_path = self.save_directory + "/logs"

        # make the AlignmentSummary and logs folders
        pathlib.Path.mkdir(self=pathlib.Path(alignment_summary_path),   # convert a string to a path
                           exist_ok=True)                               # it is okay if the path already exists

        pathlib.Path.mkdir(self=pathlib.Path(log_path),     # convert a string to a path
                           exist_ok=True)                   # it is okay if the path already exists

        # get the barcode number from the file name. It will be the second to last item after splitting by `_` and `.`
        barcode_name = re.split('[_.]', file_name)[-2]

        # move the alignment_summary.txt and read_processor to the parent directory
        sam_files = self.save_directory + "/SAM_Files"
        for root, directory, files in os.walk(sam_files):
            for file in files:
                # move alignment summary into the AlignmentSummary folder (located one folder up)
                if "alignment_summary" in file:
                    shutil.move(src=sam_files + "/" + file,
                                dst=alignment_summary_path + "/alignment_summary_" + barcode_name + ".txt")
                elif "read_processor" in file:
                    # this will rename files to the current date/time and barcode number
                    file_name = self.__get_date_time(barcode_number=barcode_name)

                    shutil.move(src=sam_files + "/" + file,
                                dst=log_path + "/" + file_name)

    def __get_date_time(self, barcode_number):
        return time.strftime("%Y_%m_%d-%H_%M-{0}.txt".format(barcode_number))  # YEAR_MONTH_DAY-HOUR_MINUTE-BARCODE##.txt

    def __read_percentage(self):
        """
        This function will look at the alignment_summary.txt in the folder specified by self.save_directory.
        It will calculate the percentage of reads that have been classified, and save its own text file in the same location

        :return: None
        """

        # read file into a data frame
        data_frame = pd.read_csv(filepath_or_buffer=self.save_directory + "/alignment_summary.txt",
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

        total_id = 0
        classified_id = 0
        unclassified_id = 0
        for row in range(len(data_frame)):
            if data_frame['alignment_genome'][row] != "*":
                classified_id += 1
            else:
                unclassified_id += 1
            total_id += 1

        rows = [
            "Total reads: %s" % total_id,
            "Classified reads: %s" % classified_id,
            "Unclassified reads: %s" % unclassified_id,
            "Percent classified: %.3f%%" % ((classified_id / total_id) * 100) ,
            "Percent unclassified: %.3f%%" % ((unclassified_id / total_id) * 100)
        ]

        with open(self.save_directory + "/simple_statistics.txt", 'w') as file:
            for row in rows:
                file.write(row)
                file.write("\n")

class MiniMap2:
    def __init__(self, input_directory, save_directory, align_reference):
        import mappy as mp
        # mp.Aligner(fn_idx_in=r"/home/joshl/PycharmProjects/ARS/ScriptResults/Files/zymogen_community_database.fasta", preset="map-ont", fn_idx_out="/home/joshl/Desktop/temp")
        # mp.Alignment(r"/home/joshl/PycharmProjects/ARS/ScriptResults/Trimmed_Barcodes/fastq_runid_67a0761ea992f55d7000e748e88761780ca1bb60_barcode01.fastq")

        self.input_directory = input_directory
        self.save_directory = save_directory
        self.alignment_reference = align_reference
        self.file_paths = []
        self.iteration = 1
        self.num_files = 0

        self.__collect_files()
        self.__perform_alignment()

        # reset iteration to 1, go to next line for new output
        self.iteration = 1
        print("")

        self.__convert_tabs_to_spaces()

        # go to next line for new output
        print("")

    def __collect_files(self):
        """
        This function will collect .fastq/.fasta files from the self.input_directory and save their file path to the self.file_paths list.

        :return: None
        """

        for root, directory, files in os.walk(self.input_directory):
            for file in files:
                if ".fasta" in file or ".fastq" in file:
                    self.file_paths.append( os.path.join( root, file ) )
                    self.num_files += 1

    def __perform_alignment(self):
        """
        This function will perform MiniMap2 alignment on the file paths located in self.file_paths using the self.alignment_reference as the reference file

        :return: None
        """
        for file in self.file_paths:
            self.__update_task(True)
            save_path = self.__return_save_path(file)

            message = "minimap2 {reference} {input} -o {output}".format(reference=self.alignment_reference,
                                                                        input=file,
                                                                        output=save_path).split(" ")

            # I am collecting all output from the MiniMap2 commands because it is not needed. If it is needed in the future, remove the PIPE commands from here
            # alternatively, print the results with print(command.stdout) and print(command.stderr)
            command = subprocess.run( message, stdout=PIPE, stderr=PIPE, universal_newlines=True )

            self.iteration += 1

    def __convert_tabs_to_spaces(self):
        """
        This function will convert the tab-delimited files output by MiniMap2 to comma-delimited files.

        :return: None
        """
        for root, directory, files in os.walk( self.save_directory ):
            for file in files:

                self.__update_task(False)

                # read data from file into input_lines
                with open( os.path.join(root, file) , 'r' ) as file_input: input_lines = file_input.read()

                # replace tabs with commas
                input_lines = input_lines.replace("\t", ",")

                # write new lines back into file
                with open( os.path.join(root, file), 'w' ) as file_output: file_output.writelines(input_lines)

                self.iteration += 1

    def __return_save_path(self, input_file):
        """
        This function will extract the barcode number of the file MiniMap2 is going to analyze. It will return the full file path of where this output should be stored
        MiniMap2 will create the files as needed

        :return: save_path: The full file path of the new file
        """
        barcode_number = re.split('[_.]', input_file)[-2]  # we want the second to last item in the list, the barcode number
        save_path = self.save_directory + "/minimap_{0}.csv".format(barcode_number)
        return save_path

    def __update_task(self, minimap_analyze:bool):
        if minimap_analyze:
            print("\rMiniMap2 acting on file {0} of {1}".format(self.iteration, self.num_files), end="")
        else:
            print("\rtabs -> spaces on file {0} of {1}".format(self.iteration, self.num_files), end="")