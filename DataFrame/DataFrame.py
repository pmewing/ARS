import csv
import pandas as pd
import numpy as np


class Frame:
    def __init__(self, output_directory, zymogen_results=None, reduced_zymogen_results=None, silva_results=None):
        self.output_directory = output_directory
        self.zymogen = zymogen_results
        self.reduced_zymogen = reduced_zymogen_results
        self.silva = silva_results

        print("writing")
        self.__make_dataframe()

    def __make_dataframe(self):
        file_name = "database_results.csv"
        file_path = self.output_directory + "/{0}".format(file_name)

        with open(file_path, 'w') as file:
            file_writer = csv.writer(file)

            # write a header row
            file_writer.writerow(["read_ids", "zymogen alignment", "zymogen %", "rzymo alignment", "rzymo %", "silva alignment", "silva %", "rzymo == zymo", "silva == zymo"])

