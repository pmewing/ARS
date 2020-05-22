from CountReads.CountReads import Count # This will count the number of raw reads in a file
from MergeFiles.MergeFiles import Merge  # This will merge multiple files of the same barcode into one file
from Trimming.TrimReads import Trim
from BarcodeAlignment.Aligner import Alignment
from PlotVisualizations import Visualize


if __name__ == '__main__':

    """
    str(CountReads.Count()) is needed becuase the __repr__ function within Count() returns the a class object.
    MergeFiles.Merge() expects a string, not a class object (of type Count). To resolve this, simply convert the Count
        object to a str() object
    """

    Count(input_directory=r"/home/joshl/minknow_data/script_results/Trimmed_Barcodes",
          save_directory=r"/home/joshl/minknow_data/script_results/Visualizations")
    #
    # Merge(input_directory=r"/home/joshl/minknow_data/demultiplex_dual/",
    #       save_directory=r"/home/joshl/minknow_data/script_results/Merge_Files")
    #
    # Trim(input_directory=r"/home/joshl/minknow_data/script_results/Merge_Files",
    #      save_directory=r"/home/joshl/minknow_data/script_results/Trimmed_Barcodes")
    #
    # Alignment(input_directory=r"/home/joshl/minknow_data/script_results/Merge_Files",
    #           save_directory=r"/home/joshl/minknow_data/script_results/Alignment/",
    #           align_reference=r"/home/joshl/minknow_data/script_results/GUPPY_ALIGNMENT_REFERENCE.txt")

    Visualize(data_file=r"/home/joshl/minknow_data/script_results/Visualizations/barcode_counts.csv",
              save_directory=r"/home/joshl/minknow_data/script_results/Visualizations",
              fastq_file=None)