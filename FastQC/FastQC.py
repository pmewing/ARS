import subprocess
import os

class FastQCAnalysis:
    def __init__(self, barcode_file_location):
        self.barcode_location = barcode_file_location + "/_merged_reads/"
        print(self.barcode_location)
        for root, directory, files in os.walk(self.barcode_location):
            for name in files:
                self.perform_fastqc_analysis( os.path.join(root, name) )

    def perform_fastqc_analysis(self, file):
        output = r"/home/joshl/Desktop/output/"
        analysis = [
            "fastqc",
            "-o",
            output,
            file
        ]
        subprocess.call(analysis)
