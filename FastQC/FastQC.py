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

    def perform_fastqc_analysis(self, input_file):
        """
        This function will perform FastQC analysis on all files in the _merged_files folder. It does not work at the
            moment, but it will eventually
        TODO: This does not work in its current state. the `analysis` list breaks the call to the command line.
         not sure how to fix it at this point in time

         :param str input_file: this is the location of the file to be analyzed
         :return: None
        """

        output_directory = r"/home/joshl/Desktop/output/"
        output_result = subprocess.run(['fastqc',                # call fastqc
                                        '-q',                    # do not show output on console. This will show a loading bar instead
                                        '-o', output_directory,  # where to save output
                                        input_file])             # file we are analyzing
