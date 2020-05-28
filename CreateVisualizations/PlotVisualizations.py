import plotly.express as px
import pathlib
import os
import re
import pandas as pd
import numpy as np
import subprocess
from subprocess import PIPE

class Plotly:
    def __init__(self, data_file: str, save_directory: str):
        """
        This will optionally create two plots: The first is a NanoPlot graph, which requires a fastq file.
        The second is a plotly graph, which requires the csv file generated from CountReads
        :param str data_file: This is the csv file generated from CountReads
        :param str save_directory: This is where the output should be saved
        :param fastq_file: This is the fastq file that NanoPlot should use to generate its own visuals
        :return: None
        """
        self.data_file = data_file
        self.save_directory = save_directory

        self.__create_plotly_histogram()

    def __create_plotly_histogram(self):
        """
        This function will create a plotly density graph using the self.data_file paramater from __init__
        It will attempt to exclude outliers from showing on the graph, and instead show them as an overlay on the side

        :params: None
        :return: None
        """

        barcode_number = 'barcode_number'
        read_count = 'reads_in_barcode'

        # load csv file
        csv_path = self.data_file
        data = pd.read_csv(filepath_or_buffer=csv_path,
                           delimiter=",",
                           header=0,  # first row
                           dtype={ barcode_number: str,
                                   read_count    : int })
        unclassified_count = 'Unknown'
        for row in range(len(data[barcode_number])):
            if data[barcode_number][row] == "unclassified":
                unclassified_count = data[read_count][row]
        data = data[:-1]

        grouped_data_file_name = self.save_directory + "/grouped_plot.html"
        individual_data_file_name = self.save_directory + "/individual_plot.html"


        grouped_histogram = px.histogram(data_frame=data,
                                         x=read_count,
                                         y=barcode_number,
                                         hover_name=data[barcode_number],
                                         hover_data=[data[read_count]],
                                         labels={'reads_in_barcode': 'Reads in barcode',
                                                 'barcode_number': 'barcodes'},
                                         marginal="box"  # rug: data points above graph; box: boxplot above graph
                                         )

        # TODO: The same color will appear right next to itself on some occations; see if this can be changed
        #   so every color is surrounded by a different color. Colors may still be repeated.
        individual_histogram = px.histogram(data_frame=data,
                                            x=read_count,
                                            y=barcode_number,
                                            hover_name=data[barcode_number],
                                            hover_data=[data[read_count]],
                                            color=barcode_number,
                                            labels={'reads_in_barcode':'Reads in barcode',
                                                    'barcode_number': 'barcodes'},
                                            marginal='violin'  # rug: data points above graph; box: boxplot above graph
                                            )

        hover_label_data = dict(
                bgcolor="white",
                font_size=16,
                font_family="Rockwell"
            )

        title_data = {
                'text'   : 'Comparison between read length and barcode number',
                'x'      : 0.5,
                'xanchor': 'center',
                'font'     : dict(size=25)
            }

        annotation_data = [dict(xref='paper',
                                yref='paper',
                                x=0.5,
                                y=1.035,
                                showarrow=False,
                                text='Performed after trimming barcodes',
                                font=dict(
                                    size=18
                                )),
                           # add unclassified annotation
                           dict(xref='paper',
                                yref='paper',
                                x=0.99,
                                y=0.83,
                                showarrow=False,
                                text="Unclassified Reads: %s" % unclassified_count,
                                font=dict(
                                    size=18
                                )),
                           # average reads (excludes unclassified
                           dict(xref='paper',
                                yref='paper',
                                x=0.99,
                                y=0.79,
                                showarrow=False,
                                text="Average reads (excluding unclassified): %.0f" % np.average(data[read_count][:-1]),
                                font=dict(
                                    size=18
                                ))
                           ]

        xaxis_title_data = "Reads in Barcode"
        yaxis_title_data = "Frequency"
        font_data = dict( size=17 )

        grouped_histogram.update_layout(
            # format data when hovering over points
            hoverlabel=hover_label_data,
            # format the title
            title=title_data,
            # format extra info (will appear right below title)
            annotations=annotation_data,
            # set axis titles and size
            xaxis_title=xaxis_title_data,
            yaxis_title=yaxis_title_data,
            font=font_data
        )

        individual_histogram.update_layout(
            # format data when hovering over points
            hoverlabel=hover_label_data,
            # format the title
            title=title_data,
            # format extra info (will appear right below title)
            annotations=annotation_data,
            # set axis titles and size
            xaxis_title=xaxis_title_data,
            yaxis_title=yaxis_title_data,
            font=font_data
        )

        grouped_histogram.write_html(grouped_data_file_name)
        individual_histogram.write_html(individual_data_file_name)

        self.__change_html_title_page(grouped_data_file_name, individual_data_file_name)

    def __change_html_title_page(self, grouped_html, individual_html):

        # read data from grouped_html, then from individual_html
        with open(grouped_html, 'r') as grouped_original: grouped_data = grouped_original.read()
        with open(individual_html, 'r') as individual_original: individual_data = individual_original.read()

        # write new data to grouped_html, then to individual_html
        # this will add a title to the html file (on the first line)
        with open(grouped_html, 'w') as grouped_modified: grouped_modified.write("<title>Grouped Histogram Plot</title>\n" + grouped_data)
        with open(individual_html, 'w') as individual_modified: individual_modified.write("<title>Individual Histogram Plot</title\n" + individual_data)


class NanoPlot:
    def __init__(self, input_directory, save_directory):
        self.input_directory = input_directory
        self.save_directory = save_directory
        self.file_paths = []
        self.invalid_files = []
        self.iteration = 1

        self.__collect_fastq_files()
        self.__create_nanoplot()
        self.__print_invalid_files()

    def __collect_fastq_files(self):
        """
        This function will collect .fastq/.fasta files and append them to the self.file_paths variable.

        :returns: None
        """
        for root, directory, files in os.walk(self.input_directory):
            for file in files:
                if ".fastq" in file or ".fasta" in file:
                    self.file_paths.append( os.path.join(root, file) )

    def __create_nanoplot(self):
        """
        This function will take the file paths from self.file_paths and use them to make a shell call with NanoPlot.
        It will store output into the `command` variable. In this way, I can implement my own 'loading' screen.

        :return: None
       """
        for file in self.file_paths:
            self.__update_task()
            save_folder = self.__get_new_folder_name(file)
            message = "NanoPlot --fastq {0} --outdir {1}".format( file, save_folder )
            message = message.split(" ")
            try:
                command = subprocess.run(message, stdout=PIPE, stderr=PIPE, universal_newlines=True)

            except FileNotFoundError:
                self.invalid_files.append(file)
            self.iteration += 1

    def __get_new_folder_name(self, file):
        barcode_number = re.split('[_.]', file)[-2]  # get the second to last item after splitting by underscores and periods
        new_save_path = self.save_directory + "/{0}".format(barcode_number)
        pathlib.Path.mkdir(pathlib.Path(new_save_path), exist_ok=True)
        return new_save_path

    def __print_invalid_files(self):
        if len(self.invalid_files) > 1:
            print("\rThe following files could not be found. If a large number of files appear below, please make sure your input and output directories exist.")
            for file in self.invalid_files:
                print(file)
        elif len(self.invalid_files) == 1:
            print("\rThe following file could not be found.")
            print(self.invalid_files[0])
        else:
            print("\r{0} of {0} files processed successfully".format(self.iteration, len(self.file_paths)))

    def __update_task(self):    
        print( "\rNanoPlot running on file {0} of {1}.".format(self.iteration, len(self.file_paths)), end="" )