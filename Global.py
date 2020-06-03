"""
This file is responsible for holding methods that many other files currently execute.
Examples:
    Collecting files
    Writing to logs
    Updating Tasks
"""
import time


class Log:
    def __init__(self, log_line: str, log_path: str, erase_file: bool):
        """
        This class will be used to write a specified log line to a certain file. The date and time will be calculated.
        The only input needed is the exact line to write, and the path of the log file.

        Data written to the log file will be appended to the end of the path.
        If you would like to erase the log path and start fresh, pass `True` for erase_file


        The following options are used to format the date/time of logs
        %Y  Year with century as a decimal number.
        %m  Month as a decimal number [01,12].
        %d  Day of the month as a decimal number [01,31].
        %H  Hour (24-hour clock) as a decimal number [00,23].
        %M  Minute as a decimal number [00,59].


        Args:
            log_line: This is the exact line that should be written to the file
            log_path: This is the exact path to the log file that should be written to.
            erase_file: If you would like to erase the log file and start new, pass True here
        """

        date = time.strftime("%Y-%m-%d %H:%M")
        if erase_file:
            output_file = open(log_path, 'w')
        else:
            output_file = open(log_path, 'a')

        output_file.write("{0} | {1}\n".format(date, log_line))
        output_file.close()


class Update:
    def __init__(self, program, current, total):
        """
        This method is responsible for writing a line to stdout stating the progress of programs (guppy_aligner, minimap, etc).
        It will overwrite the current line
        Args:
            program: The program that is running
            current: The index of the current file (i.e. file 4 / 10)
            total: The total number of files to process
        """
        print("\r{program} has started file {current} / {total}".format(
            program=program,
            current=current,
            total=total), end="")


class Files:
    def __init__(self, input_directory: str, file_extensions: list = None):
        """
        This class will collect all files in input_directory containing the file_extensions.
        If no file_extensions argument is provided, the following list will be used: [".fastq", ".fasta"]


        Warnings:
            This class will iterate through all folders in the input_directory, not just the top-level folder, and return ANY matching file extension.
        Args:
            input_directory: The directory that should be examined for files
            file_extensions: The extension(s) that should be matched
        Returns:
            file_paths: A list of file paths that match any extension in the argument file_extensions list
        """

        self.input_directory = input_directory
        self.file_extensions = file_extensions
        self.file_paths = []

        if self.file_extensions is None:
            self.file_extensions = [".fastq", ".fasta"]

    def __collect_files(self):
        """
        This method is responsible for collecting files from self.input_directory.
        I am creating a second method here instead of inside __init__ simply to separate the tasks each method is doing
        Returns: None
        """
        import os

        # Unfortunately, this is O(n^2) complexity. This is the most simple, yet most intensive, method of finding files.
        # I am unsure if there is a better method of matching file extensions
        for root, directory, files in os.walk(self.input_directory):

            for file in files:                              # iterate through all files
                for extension in self.file_extensions:      # iterate through all extensions
                    if extension.lower() in file.lower():   # match extension with file
                        self.file_paths.append( os.path.join(root, file) )

    @property
    def return_file_paths(self):
        """
        Use the dot operator after creating a Files instance to return file paths inside self.input_directory
        Returns list: file_paths
        """
        self.__collect_files()
        return self.file_paths
