from CountReads import Count
from MergeFiles import Merge  # This will merge multiple files of the same barcode into one file
from TrimReads import Trim
from Aligner import GuppyAlignment, MiniMap2, VSearch
from PlotVisualizations import Plotly, NanoPlot
from BasecallBarcode import Basecall, Barcode
from NanoQC import NanoQCAnalysis
from DataFrames import Frame


if __name__ == '__main__':

    # zymogen
    MiniMap2(input_directory=r"/home/joshl/Desktop/temp/input",
             save_directory=r"/home/joshl/Desktop/temp/output/zymogen",
             align_reference=r"/home/joshl/PycharmProjects/ARS/ScriptResults/Files/zymogen_alignment_reference.fasta")

    # modified zymogen
    MiniMap2(input_directory=r"/home/joshl/Desktop/temp/input",
             save_directory=r"/home/joshl/Desktop/temp/output/modified_zymogen",
             align_reference=r"/home/joshl/PycharmProjects/ARS/ScriptResults/Files/zymogen_modified_alignment_reference.fasta")

    # silva reference file
    MiniMap2(input_directory=r"/home/joshl/Desktop/temp/input",
             save_directory=r"/home/joshl/Desktop/temp/output/silva",
             align_reference=r"/home/joshl/PycharmProjects/ARS/ScriptResults/Files/silva_alignment_reference.fasta")