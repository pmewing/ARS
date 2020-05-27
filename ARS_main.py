from CountReads.CountReads import Count # This will count the number of raw reads in a file
from MergeFiles.MergeFiles import Merge  # This will merge multiple files of the same barcode into one file
from Trimming.TrimReads import Trim
from Alignment.Aligner import Alignment
from PlotVisualizations import Plotly, NanoPlot
from BasecallBarcode import Basecall, Barcode
from NanoQC import NanoQCAnalysis

if __name__ == '__main__':

    # Basecall(input_directory=r"/home/joshl/minknow_data/SBGX_CLC", save_directory=r"/home/joshl/minknow_data/basecalled")
    # Barcode(input_directory=r"/home/joshl/minknow_data/basecalled", save_directory=r"/home/joshl/minknow_data/demultiplex_dual")
    # Count(input_directory=r"/home/joshl/minknow_data/demultiplex_dual", save_directory=r"/home/joshl/PycharmProjects/ARS/ScriptResults/Count_Reads")
    # Visualize(data_file=r"/home/joshl/PycharmProjects/ARS/ScriptResults/Count_Reads/barcode_counts.csv", save_directory=r"/home/joshl/PycharmProjects/ARS/ScriptResults/Count_Reads/")

    # Merge(input_directory=r"/home/joshl/minknow_data/demultiplex_dual/", save_directory=r"/home/joshl/PycharmProjects/ARS/ScriptResults/Merge_Files")
    # Count(input_directory=r"/home/joshl/PycharmProjects/ARS/ScriptResults/Merge_Files", save_directory=r"/home/joshl/PycharmProjects/ARS/ScriptResults/CreateVisualizations/MergeVisual")
    # Visualize(data_file=r"/home/joshl/PycharmProjects/ARS/ScriptResults/CreateVisualizations/MergeVisual/barcode_counts.csv", save_directory=r"/home/joshl/PycharmProjects/ARS/ScriptResults/CreateVisualizations/MergeVisual/")

    # Trim(input_directory=r"/home/joshl/PycharmProjects/ARS/ScriptResults/Merge_Files", save_directory=r"/home/joshl/PycharmProjects/ARS/ScriptResults/Trimmed_Barcodes")
    # Count(input_directory=r"/home/joshl/PycharmProjects/ARS/ScriptResults/Trimmed_Barcodes", save_directory=r"/home/joshl/PycharmProjects/ARS/ScriptResults/CreateVisualizations/TrimmedVisual")
    # Visualize(data_file=r"/home/joshl/PycharmProjects/ARS/ScriptResults/CreateVisualizations/TrimmedVisual/barcode_counts.csv", save_directory=r"/home/joshl/PycharmProjects/ARS/ScriptResults/CreateVisualizations/TrimmedVisual")

    # NanoQCAnalysis(input_directory=r"/home/joshl/PycharmProjects/ARS/ScriptResults/Trimmed_Barcodes", save_directory=r"/home/joshl/PycharmProjects/ARS/ScriptResults/Quality_Control/")
    # Alignment(input_directory=r"/home/joshl/PycharmProjects/ARS/ScriptResults/Trimmed_Barcodes", save_directory=r"/home/joshl/PycharmProjects/ARS/ScriptResults/Alignment", align_reference=r"/home/joshl/PycharmProjects/ARS/ScriptResults/GUPPY_ALIGNMENT_REFERENCE.txt")
    NanoPlot(input_directory=r"/home/joshl/PycharmProjects/ARS/ScriptResults/Trimmed_Barcodes", save_directory=r"/home/joshl/PycharmProjects/ARS/ScriptResults/VisualizationResults/NanoPlot")
