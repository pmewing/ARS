import os
import shutil
from CountReads.CountReads import Count # This will count the number of raw reads in a file
from MergeFiles.MergeFiles import Merge  # This will merge multiple files of the same barcode into one file
from Trimming.TrimReads import Trim
from BarcodeAlignment.Aligner import Alignment
from PlotVisualizations import Visualize
from BasecallBarcode import Basecall, Barcode


if __name__ == '__main__':
    Basecall(input_directory="/home/joshl/minknow_data/SBGX_CLC", output_directory="/home/joshl/minknow_data/basecalled")
    Barcode(input_directory="/home/joshl/minknow_data/basecalled", output_directory="/home/joshl/minknow_data/demultiplex_dual")
    # Count(input_directory=r"/home/joshl/minknow_data/demultiplex_dual", save_directory=r"/home/joshl/PycharmProjects/ARS/ScriptResults/Count_Reads")
    # Merge(input_directory=r"/home/joshl/minknow_data/demultiplex_dual/", save_directory=r"/home/joshl/PycharmProjects/ARS/ScriptResults/Merge_Files")
    # Trim(input_directory=r"/home/joshl/PycharmProjects/ARS/ScriptResults/Merge_Files", save_directory=r"/home/joshl/PycharmProjects/ARS/ScriptResults/Trimmed_Barcodes")
    # Alignment(input_directory=r"/home/joshl/PycharmProjects/ARS/ScriptResults/Trimmed_Barcodes", save_directory=r"/home/joshl/PycharmProjects/ARS/ScriptResults/Alignment", align_reference=r"/home/joshl/PycharmProjects/ARS/ScriptResults/GUPPY_ALIGNMENT_REFERENCE.txt")
    # Visualize(data_file=r"/home/joshl/PycharmProjects/ARS/ScriptResults/Count_Reads/barcode_counts.csv", save_directory=r"/home/joshl/PycharmProjects/ARS/ScriptResults/Visualizations", fastq_file=None)
