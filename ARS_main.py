import os
from CountReads.CountReads import Count # This will count the number of raw reads in a file
from MergeFiles.MergeFiles import Merge  # This will merge multiple files of the same barcode into one file
from Trimming.TrimReads import Trim
from BarcodeAlignment.Aligner import Alignment
from PlotVisualizations import Visualize


def basecall(input_directory, output_directory):
    """
    This is a direct copy-paste from the bash script provided by patrick
    Basecall using the fast neural network.
    """
    message = "guppy_basecaller " \
              "--recursive " \
              "--input_path {0} " \
              "--save_path {1} " \
              "--config dna_r9.4.1_450bps_fast.cfg " \
              "--num_callers 1 " \
              "--cpu_threads_per_caller 12".format( input_directory, output_directory )
    os.system( message )


def barcode(input_directory, output_directory):
    message = "guppy_barcoder" \
              "--input_path {0}" \
              "--save_path {1} " \
              "--recursive " \
              "--config configuration.cfg " \
              "--worker_threads 12 " \
              "--barcode_kits EXP-PBC096 " \
              "--require_barcodes_both_ends".format( input_directory, output_directory )
    os.system( message )


if __name__ == '__main__':
    basecall("/home/joshl/minknow_data/SBGX_CLC", "/home/joshl/minknow_data/basecalled")
    barcode("/home/joshl/minknow_data/basecalled", "/home/joshl/minknow_data/demultiplex_dual")
    Count(input_directory=r"/home/joshl/minknow_data/demultiplex_dual", save_directory=r"/home/joshl/PycharmProjects/ARS/ScriptResults/Count_Reads")
    Merge(input_directory=r"/home/joshl/minknow_data/demultiplex_dual/", save_directory=r"/home/joshl/PycharmProjects/ARS/ScriptResults/Merge_Files")
    Trim(input_directory=r"/home/joshl/PycharmProjects/ARS/ScriptResults/Merge_Files", save_directory=r"/home/joshl/PycharmProjects/ARS/ScriptResults/Trimmed_Barcodes")
    Alignment(input_directory=r"/home/joshl/PycharmProjects/ARS/ScriptResults/Trimmed_Barcodes", save_directory=r"/home/joshl/PycharmProjects/ARS/ScriptResults/Alignment", align_reference=r"/home/joshl/PycharmProjects/ARS/ScriptResults/GUPPY_ALIGNMENT_REFERENCE.txt")
    Visualize(data_file=r"/home/joshl/PycharmProjects/ARS/ScriptResults/Count_Reads/barcode_counts.csv", save_directory=r"/home/joshl/PycharmProjects/ARS/ScriptResults/Visualizations", fastq_file=None)
