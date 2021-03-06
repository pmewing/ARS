import plotly.express as px
import pathlib
import re
import pandas as pd
import numpy as np
import subprocess
from subprocess import PIPE
from Scripts.Global import Update, Log, Files


class Plotly:
    def __init__(self, data_file: str, save_directory: str, grouped_file_name=None, individual_file_name=None):
        """
        This will optionally create two plots: The first is a NanoPlot graph, which requires a fastq file.
        The second is a plotly graph, which requires the csv file generated from CountReads

        :param str data_file: This is the csv file generated from CountReads
        :param str save_directory: This is where the output should be saved
        :param str grouped_file_name: If you would like to set a name for the plotly graph that contains all data points of the same color, set a file name here. This is not required
        :param str individual_file_name: If you would like to set a name for the plotly graph separating the data points by color, specify a file name here. This is not required
        :return: None
        """
        self.data_file = data_file
        self.save_directory = save_directory
        self.grouped_file_name = grouped_file_name
        self.individual_file_name = individual_file_name

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

        # set grouped-graph file name (if one is present)
        if self.grouped_file_name is None:
            grouped_data_file_name = self.save_directory + "/grouped_plot.html"
        else:
            grouped_data_file_name = self.save_directory + "/{0}.html".format(self.grouped_file_name)

        # set individual-graph file name (if one is present)
        if self.individual_file_name is None:
            individual_data_file_name = self.save_directory + "/individual_plot.html"
        else:
            individual_data_file_name = self.save_directory + "/{0}.html".format(self.individual_file_name)

        grouped_histogram.write_html(grouped_data_file_name)
        individual_histogram.write_html(individual_data_file_name)

        self.__change_html_title_page(grouped_data_file_name, individual_data_file_name)
        self.__write_logs_to_file( file_path=grouped_data_file_name )
        self.__write_logs_to_file( file_path=individual_data_file_name )

    def __change_html_title_page(self, grouped_html, individual_html):

        # read data from grouped_html into grouped_data
        with open(grouped_html, 'r') as grouped_original:
            grouped_data = grouped_original.read()

        # read data from individual_html into individual_data
        with open(individual_html, 'r') as individual_original:
            individual_data = individual_original.read()

        # write new data to grouped_html, then to individual_html
        # this will add a title to the html file (on the first line)
        with open(grouped_html, 'w') as grouped_modified:
            if self.grouped_file_name is None:
                grouped_modified.write("<title>Grouped Plot</title>\n")
                grouped_modified.write(grouped_data)

            else:
                grouped_modified.write( "<title>{0}</title>\n".format(self.grouped_file_name) )
                grouped_modified.write(grouped_data)

        with open(individual_html, 'w') as individual_modified:
            if self.individual_file_name is None:
                individual_modified.write("<title>Individual Plot</title>\n")
                individual_modified.write(individual_data)
            else:
                individual_modified.write( "<title>{0}</title>\n".format(self.individual_file_name) )
                individual_modified.write(individual_data)

    def __write_logs_to_file(self, file_path):
        """
        This function will write the time that a plotly graph was created. It will be ran for each graph that is created
        :param str file_path: This is where the file will be saved
        """

        log_path = "Results/Script_Logs/plotly_logs.txt"
        Log("data_file: {0}\tsave_path: {1}".format(self.data_file, file_path),
            log_path=log_path,
            erase_file=False)


class NanoPlot:
    def __init__(self, input_directory, save_directory):
        """
        This function will run NanoPlot on an input folder. Enter the directory of multiple .fastq/.fasta files as input, and the results will be saved into the save_directory
        :param str input_directory: This is the parent folder of the .fastq/.fasta files
        :param str save_directory: This is where you would like to save the output files of NanoPlot; NanoPlot creates many files per .fastq/.fastsa, so they will be placed in their own barcode folder
        """
        self.input_directory = input_directory
        self.save_directory = save_directory
        self.file_paths = []
        self.invalid_files = []
        self.iteration = 0

        self.__collect_files()
        self.__create_nanoplot()
        self.__print_invalid_files()

    def __collect_files(self):
        """
        This function will collect .fastq/.fasta files and append them to the self.file_paths variable.

        :returns: None
        """
        self.file_paths = Files(input_directory=self.input_directory,
                                file_extensions=[".fastq", ".fasta"]).return_file_paths


    def __create_nanoplot(self):
        """
        This function will take the file paths from self.file_paths and use them to make a shell call with NanoPlot.
        It will store output into the `command` variable. In this way, I can implement my own 'loading' screen.

        :return: None
       """
        for file in self.file_paths:
            self.__update_task()
            save_folder = self.__get_new_folder_name(file)

            # try to make the output directory
            try:
                pathlib.Path.mkdir( self=pathlib.Path(self.save_directory), exist_ok=True )
            except FileExistsError:
                pass

            message = "NanoPlot --fastq {0} --outdir {1}".format( file, save_folder )
            try:
                self.__write_logs_to_file(message)
                message = message.split(" ")
                command = subprocess.run(message, stdout=PIPE, stderr=PIPE, universal_newlines=True)

            except FileNotFoundError:
                self.invalid_files.append(file)

    def __get_new_folder_name(self, file):
        barcode_number = re.split('[_.]', file)[-2]  # get the second to last item after splitting by underscores and periods
        new_save_path = self.save_directory + "/{0}".format(barcode_number)
        pathlib.Path.mkdir(pathlib.Path(new_save_path), exist_ok=True)
        return new_save_path

    def __print_invalid_files(self):
        if len(self.invalid_files) > 1:
            print("\rThe following files could not be found. If you are trying to procedss a large number of files and they do not appear,")
            print("\tensure your input and output directories are correct.")
            for file in self.invalid_files:
                print(file)
        elif len(self.invalid_files) == 1:
            print("\rThe following file could not be found.")
            print(self.invalid_files[0])
        else:
            print("\rNanoPlot has successfully processed {0} of {0} files.".format(self.iteration, len(self.file_paths)))

    def __write_logs_to_file(self, command):
        """
        This will call the Log function to write a line to the specified log path.

        :param str command: This is the line that will be written to the log. Its parameters can be found in self.__create_nanoplot
        """

        log_path = "Results/Script_Logs/nanoplot_logs.txt"
        Log(log_line=command,
            log_path=log_path,
            erase_file=False)

    def __update_task(self):
        Update("NanoPlot", self.iteration, len(self.file_paths))
        self.iteration += 1
