from CountReads import CountReads  # This will count the number of raw reads in a file
from MergeFiles import MergeFiles  # This will merge multiple files of the same barcode into one file
from FastQC import FastQC

from BarcodeAlignment import alignment
if __name__ == '__main__':

    """
    str(CountReads.Count()) is needed becuase the __repr__ function within Count() returns the a class object.
    MergeFiles.Merge() expects a string, not a class object (of type Count). To resolve this, simply convert the Count
        object to a str() object
    """

    print("")
    barcode_file_location = str(CountReads.Count())
    MergeFiles.Merge(barcode_file_location)
    FastQC.FastQCAnalysis(barcode_file_location)

