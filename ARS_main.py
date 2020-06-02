from CountReads.CountReads import Count # This will count the number of raw reads in a file
from MergeFiles.MergeFiles import Merge  # This will merge multiple files of the same barcode into one file
from Trimming.TrimReads import Trim
from Alignment.Aligner import GuppyAlignment, MiniMap2
from PlotVisualizations import Plotly, NanoPlot
from BasecallBarcode import Basecall, Barcode
from NanoQC import NanoQCAnalysis
from DataFrame import Frame


if __name__ == '__main__':
    MiniMap2(input_directory=r"/home/joshl/Desktop/temp/input",
             save_directory=r"/home/joshl/Desktop/temp/output/MiniMap2",
             align_reference=r"/home/joshl/PycharmProjects/ARS/ScriptResults/Files/zymogen_alignment_reference.fasta")
