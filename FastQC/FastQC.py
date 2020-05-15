import subprocess
import os
import progressbar

class FastQCAnalysis:
    def __init__(self, barcode_file_location):
        self.barcode_location = barcode_file_location + "/_merged_files/"

        bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
        for root, directory, files in os.walk(self.barcode_location):
            for name in files:
                self.perform_fastqc_analysis( os.path.join(root, name) )
                bar.update()

    def perform_fastqc_analysis(self, file):
        """
        This function will perform FastQC analysis on all files in the _merged_files folder. It does not work at the
            moment, but it will eventually
        TODO: This does not work in its current state. the `analysis` list breaks the call to the command line.
         not sure how to fix it at this point in time

         :param str file: this is the location of the file to be analyzed
         :return: None
        """
        output_file_name = file.split("/")[-1]
        output_directory = r"/home/joshl/Desktop/output/"
        analysis = [
            "fastqc ",
            "-q "
            "-o ",
            output_directory + output_file_name,
            " ",
            file
        ]
        subprocess.call(analysis)
