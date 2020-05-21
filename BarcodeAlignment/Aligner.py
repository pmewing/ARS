import os
import shutil
import subprocess
import pandas as pd
import numpy as np

class Alignment:
    def __init__(self, open_directory, save_directory, align_reference):
        """
        This class will be responsible for results pertaining to read alignments. This class uses the guppy_alignment tool.
        guppy_aligner MUST be added to your $PATH, otherwise it will not work
        :param str open_directory: The location of input files (usually a directory)
        :param str save_directory: The location of output files (usually a directory)
        :param str align_reference: The location of the reference file to use (a file)
        :return: None
        """

        self.open_directory = open_directory
        self.save_directory = save_directory
        self.alignment_reference = align_reference

        self.perform_alignment()
        self.move_summary_files()
        self.read_percentage()

    def perform_alignment(self):
        """
        This function will call a shell command to run the guppy_aligner with the input/ouput/reference arguments provided

        :return: None
        """
        message = "guppy_aligner --input_path %s --save_path %s --align_ref %s" % (
            self.open_directory, self.save_directory + "/SAM_Files", self.alignment_reference)
        message = message.split(" ")  # we must split the messgae into a list before subprocess.run() will accept it
        subprocess.run(message)

    def move_summary_files(self):
        """
        guppy_aligner creates a result file, log file, and a .sam file for every .fastq file used. I don't like these files
        in the same directory, as the result file is more useful.

        Because of this, all files are initially saved to the
        SAM_Files directory, then the result and log files are moved one level up.

        :return: None
        """
        # move the alignment_summary.txt and read_processor to the parent directory
        for root, directory, files in os.walk(self.save_directory):
            for file in files:
                if "alignment_summary" in file or "read_processor" in file:
                    try:
                        shutil.move( os.path.join(root, file), os.path.join(self.save_directory, file) )
                    except PermissionError:
                        pass

    def read_percentage(self):
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
