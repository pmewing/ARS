import csv
import pandas as pd
import numpy as np


class Frame:
    def __init__(self, output_directory, read_ids,
                 zymogen_alignment, zymogen_percent,
                 reduced_zymogen_alignment, reduced_zymogen_percent,
                 silva_alignment, silva_percent):
        """
        This class is responsible for creating a csv file/data frame that contains infomration about mapping from sequences to the zymogen database, reduced zymogen database,
            and the silva database
        TODO: Currently, zymogen, rzymogen, and silva alignments/percentages are not required. These need to be required at some point
        """
        self.output_directory = output_directory
        self.read_ids = read_ids
        self.zymo_alignment = zymogen_alignment
        self.zymo_percent = zymogen_percent
        self.reduced_zymo_alignment = reduced_zymogen_alignment
        self.reduced_zymo_percent = reduced_zymogen_percent
        self.silva_alignment = silva_alignment
        self.silva_percent = silva_percent

        self.correct_data = self.__check_data()
        if not self.correct_data:
            print("The input parameters (below) are not of equal length. Please check your inputs and try again.")
            print("self.read_ids")
            print("self.zymo_alignment\t\t\t\tself.zymo_percent")
            print("self.reduced_zymo_alignment\t\tself.reduced_zymo_percent")
            print("self.silva_alignment\t\t\tself.silva_percent")
        else:
            self.__make_dataframe()

    def __check_data(self):
        """
        This class will make sure that the zymogen, rzymogen, and silva results are the same length. If they are not, it will return false

        :return: Boolean
        """

        average_length = ( len(self.read_ids) +
                           len(self.zymo_alignment) + len(self.zymo_percent) +
                           len(self.reduced_zymo_alignment) + len(self.reduced_zymo_percent) +
                           len(self.silva_alignment) + len(self.silva_percent) ) / 7.0

        if average_length == len(self.zymo_alignment): correct_results = True
        else: correct_results = False

        return correct_results

    def __make_dataframe(self):
        """
        This function will be responsible for writing rows to the csv file

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

            # iterate through each item in the parameters
            for i in range(len(self.zymo_alignment)):

                # test if the zymo_alignment equals the reduced_zymogen_alignment. If they are equal write 1 to the csv, otherwise 0
                if self.zymo_alignment[i] == self.reduced_zymo_alignment[i]: rzymo_zymo_equal = True
                else: rzymo_zymo_equal = False

                # test if the silva_alignment equals the zymogen_alignment. If they are equal, write 1 to the csv, otherwise 0
                if self.silva_alignment[i] == self.zymo_alignment[i]: silva_zymo_equal = True
                else: silva_zymo_equal = False

                # assemble the row to be written
                row = [self.read_ids[i],
                       self.zymo_alignment[i], self.zymo_percent[i],
                       self.reduced_zymo_alignment[i], self.reduced_zymo_percent[i],
                       self.silva_alignment[i], self.silva_percent[i],
                       rzymo_zymo_equal, silva_zymo_equal]

                # write the row
                file_writer.writerow(row)