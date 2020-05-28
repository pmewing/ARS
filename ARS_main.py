from CountReads.CountReads import Count # This will count the number of raw reads in a file
from MergeFiles.MergeFiles import Merge  # This will merge multiple files of the same barcode into one file
from Trimming.TrimReads import Trim
from Alignment.Aligner import GuppyAlignment, MiniMap2
from PlotVisualizations import Plotly, NanoPlot
from BasecallBarcode import Basecall, Barcode
from NanoQC import NanoQCAnalysis
from DataFrame import Frame

if __name__ == '__main__':
    # zymogen community
    #GuppyAlignment(input_directory=r"/home/joshl/Desktop/input",
    #               save_directory=r"/home/joshl/Desktop/output",
    #               align_reference=r"/home/joshl/PycharmProjects/ARS/ScriptResults/Files/zymogen_community_database.fasta")
    # modified zymogen
    GuppyAlignment(input_directory=r"/home/joshl/Desktop/input",
             save_directory=r"/home/joshl/Desktop/output",
                   align_reference=r"/home/joshl/PycharmProjects/ARS/ScriptResults/Files/modified_zymogen_community_database.fasta")

    # zymogen community
    #MiniMap2(input_directory=r"/home/joshl/Desktop/input",
    #         save_directory=r"/home/joshl/Desktop/output",
    #         align_reference=r"/home/joshl/PycharmProjects/ARS/ScriptResults/Files/zymogen_community_database.fasta")

    # modified zymogen
    MiniMap2(input_directory=r"/home/joshl/Desktop/input",
             save_directory=r"/home/joshl/Desktop/output",
             align_reference=r"/home/joshl/PycharmProjects/ARS/ScriptResults/Files/zymogen_modified_community_database.fasta")