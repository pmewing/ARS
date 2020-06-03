import csv
from Global import Log


class Frame:
    def __init__(self, output_directory, zymogen_results_directory, reduced_zymogen_results_directory, silva_results_directory):
        """
        This class is responsible for creating a csv file/data frame that contains infomration about mapping from sequences to the zymogen database, reduced zymogen database,
            and the silva database
        TODO: What should the resulting file be called?
        """
        self.output_directory = output_directory
        self.zymogen_results = zymogen_results_directory
        self.reduced_zymogen_results = reduced_zymogen_results_directory
        self.silva_results = silva_results_directory

        self.__collect_data()
        self.__make_dataframe()

    def __collect_data(self):
        # TODO: Pull in data from zymogen_results, reduced_zymogen_results, ande silva_results for making a data frame
        pass

    def __make_dataframe(self):
        """
        This function will be responsible for writing rows to the csv file

        # TODO: write results from collect_data into a csv file

        :return: None
        """

        # file name and path to be used
        file_name = "database_results.csv"
        file_path = self.output_directory + "/{0}".format(file_name)

        # open the csv file
        with open(file_path, 'w') as file:
            file_writer = csv.writer(file)

            # write a header row
            file_writer.writerow(["read_ids", "zymogen alignment", "zymogen %", "rzymo alignment", "rzymo %", "silva alignment", "silva %", "rzymo == zymo", "silva == zymo"])
        self.__write_logs_to_file(file_path)

    def __write_logs_to_file(self, file_name):
        """
        This function will write logs to the log file specified when a successful dataframe has been completed

        :param str file_name: This is the name of the csv file the dataframe is located in
        """

        log_path = "ScriptResults/Script_Logs/data_frame_log.txt"

        Log("DataFrame saved to file: {0}".format(file_name),
            log_path=log_path,
            erase_file=False)
