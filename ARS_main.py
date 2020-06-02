from CountReads import Count
from MergeFiles import Merge  # This will merge multiple files of the same barcode into one file
from TrimReads import Trim
from Aligner import GuppyAlignment, MiniMap2
from PlotVisualizations import Plotly, NanoPlot
from BasecallBarcode import Basecall, Barcode
from NanoQC import NanoQCAnalysis
from DataFrames import Frame


if __name__ == '__main__':
    import sys
    print("\nINPUT")
    for i in sys.argv:
        print(i)
    print("\n")
