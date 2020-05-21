from CountReads.CountReads import Count # This will count the number of raw reads in a file
from MergeFiles.MergeFiles import Merge  # This will merge multiple files of the same barcode into one file
import FastQC
from BarcodeAlignment.alignment import Alignment
import alignment
import TrimReads

if __name__ == '__main__':

    """
    str(CountReads.Count()) is needed becuase the __repr__ function within Count() returns the a class object.
    MergeFiles.Merge() expects a string, not a class object (of type Count). To resolve this, simply convert the Count
        object to a str() object
    """

    print("")
    Count(open_directory=r"/home/joshl/minknow_data/demultiplex_dual",
                                  save_directory=r"/home/joshl/minknow_data/script_results/Count Reads")

    Merge(open_directory=r"/home/joshl/minknow_data/demultiplex_dual/",
          save_directory=r"/home/joshl/minknow_data/script_results/Merge Files")

    TrimReads.Trim(open_directory=r"/home/joshl/minknow_data/script_results/Merge Files",
                   save_directory=r"/home/joshl/minknow_data/script_results/Trimmed Barcodes")
