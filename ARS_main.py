from CountReads import Count
from MergeFiles import Merge  # This will merge multiple files of the same barcode into one file
from TrimReads import Trim, Pychopper
from Aligner import GuppyAlignment, MiniMap2, VSearch
from PlotVisualizations import Plotly, NanoPlot
from BasecallBarcode import Basecall, Barcode
from NanoQC import NanoQCAnalysis
from DataFrames import Frame
from GenomeData import MiniMapGenome


if __name__ == '__main__':

    MiniMapGenome(input_directory=r"/home/joshl/Desktop/MiniMap_Results/modified_zymogen",
                  save_directory=r"/home/joshl/Desktop/MiniMap_Results/output")
