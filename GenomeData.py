from Global import Files


class Genome:
    def __init__(self, input_directory: str, save_directory: str):
        """
        This function will collect the genome, species, and subspecies from .csv files after they have been
            processed by guppy_aligner or MiniMap2
        Args:
            input_directory: This is the input csv files from guppy_aligner or MiniMap2
            save_directory: This is the directory where output files should be saved.
        """
        self.input_directory = input_directory
        self.save_directory = save_directory
        self.file_paths = []
        self.number_of_files = 0

        self.__collect_file_paths()

    def __collect_file_paths(self):
        self.file_paths = Files(input_directory=self.input_directory,
                                file_extensions=[".csv"]).return_file_paths
