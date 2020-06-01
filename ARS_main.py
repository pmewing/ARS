from CountReads.CountReads import Count # This will count the number of raw reads in a file
from MergeFiles.MergeFiles import Merge  # This will merge multiple files of the same barcode into one file
from Trimming.TrimReads import Trim
from Alignment.Aligner import GuppyAlignment, MiniMap2
from PlotVisualizations import Plotly, NanoPlot
from BasecallBarcode import Basecall, Barcode
from NanoQC import NanoQCAnalysis
from DataFrame import Frame


if __name__ == '__main__':
    Basecall(input_directory=r"/home/joshl/minknow_data/SBGX_CLC",
             save_directory=r"/home/joshl/minknow_data/basecalled")

    Barcode(input_directory=r"/home/joshl/minknow_data/basecalled",
            save_directory=r"/home/joshl/minknow_data/demultiplex_dual")

    # Merge(input_directory=r"/home/joshl/minknow_data/demultiplex_dual",
    #       save_directory=r"/home/joshl/PycharmProjects/ARS/ScriptResults/Merge_Files")

    # Count(input_directory=r"/home/joshl/minknow_data/demultiplex_dual",
    #       save_directory=r"/home/joshl/PycharmProjects/ARS/ScriptResults/Count_Reads")
