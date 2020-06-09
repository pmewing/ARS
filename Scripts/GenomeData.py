import csv
from Scripts.Global import Files


class MiniMapGenome:
    def __init__(self, input_directory: str, save_directory: str):
        """

        This function will collect the genome, species, and subspecies from .csv files after they have been processed by guppy_aligner or MiniMap2
        The minimap2 results may not look like they are in a specified format; however, everything is delimited by a tab ('\t')
        Because of this, determining if specific tags are present can be (relatively) easily done.
        See the manual pages to determine which column tags fall into: https://lh3.github.io/minimap2/minimap2.html#10
            The tags are under the section "Output Format".

        TODO: Write .csv data from the method self.__write_primary_alignment_to_csv into a csv file
        TODO: Read unclassified data from minimap csv (col 2 == 512) into a separate csv file

        Args:
            input_directory (str): This is the input csv files from guppy_aligner or MiniMap2
            save_directory (str): This is the directory where output files should be saved.
        """
        self.input_directory = input_directory
        self.save_directory = save_directory
        self.file_paths = []
        self.primary_alignment_instances = []
        self.number_of_files = 0

        self.__collect_file_paths()
        self.__find_primary_alignments()
        self.__write_primary_alignment_to_csv()

    def __collect_file_paths(self):
        self.file_paths = Files(input_directory=self.input_directory,
                                file_extensions=[".csv"]).return_file_paths

    def __find_primary_alignments(self):
        """
        This function will take the .csv files from self.file_paths and collect the primary alignments from them
        This uses the idea that the second column from minimap output will be a `0` if the sequence is primary.
            If this column contains a `0`, it will also check that the tag `tp:A:P` is listed in the row; this is to double check that the correct data is being pulled
        If any item does not appear to have content, the item is not present in this row
        Returns: None
        """

        index = 0
        for file in self.file_paths:
            with open(file, 'r') as input_file:
                csv_reader = csv.reader(input_file, delimiter='\t')
                for line in csv_reader:

                    # collect all rows that match primary alignment parameters
                    if line[1] == "0" and line[15] == "tp:A:P":
                        sequence_name = line[0]
                        alignment_name = line[2]
                        mapping_quality = int(line[4])
                        alignment_score = line[13]
                        per_base_divergence = line[19]

                        self.primary_alignment_instances.append(
                            MiniMapPrimaryAlignmentData(
                                file_path=file,
                                row_index=index,
                                sequence_name=sequence_name,
                                alignment_name=alignment_name,
                                mapping_quality=mapping_quality,
                                alignment_score=alignment_score,
                                per_base_divergence=per_base_divergence
                            )
                        )
                        index += 1

    def __write_primary_alignment_to_csv(self):
        """
        This function will take the data from self.primary_alignment_instances and write it to a CSV file with the same barcode name as the input data.
        It will be saved to to self.save_directory
        Returns: None
        """
        for item in self.primary_alignment_instances:
            print(item.file_path)


class MiniMapPrimaryAlignmentData:
    def __init__(self, file_path: str, row_index: int, sequence_name: str, alignment_name: str, mapping_quality: int, alignment_score: str, per_base_divergence: str):
        """
        This class will simply be used to hold data about each row that is a primary alignment.

        This data will be added to a list of instances within the MiniMapGenome class; this will be written to a csv file

        Args:
            file_path (str): This is the path of the input file
            row_index (int): This is the row index that is being appended
            sequence_name (str):  The name of the sequence (read_id)
            alignment_name (str): The name of the alignment/species that was aligned
            mapping_quality (int): A value indicating the quality of mapping
            alignment_score (str):  A value indicating the quality of alignment (matches needleman-wunsch alignment score)
            per_base_divergence (str):  A value depicting how far the sequence has diverged
        """
        self.file_path = file_path
        self.row_index = row_index
        self.sequence_name = sequence_name
        self.alignment_name = alignment_name
        self.mapping_quality = mapping_quality
        self.alignment_score = alignment_score
        self.per_base_divergence = per_base_divergence


# TODO: Read data from guppy_aligner .csv files and collect appropriate data to write to a .csv file
