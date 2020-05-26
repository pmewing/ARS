import plotly.express as px
import pandas as pd
import numpy as np
import subprocess


class Visualize:
    def __init__(self, data_file: str, save_directory: str, fastq_file=None):
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
        self.fastq_file = fastq_file

        self.__create_nanoplot()
        self.__create_plotly_histogram()

    def __create_nanoplot(self):
        """
        fastq_files are an optional parameter. If the user did not pass them in (i.e. does not want to perform NanoPlot,
           tell them that NanoPlot will not be run. If they did pass something in, tell them their file was not found
           (if the file could not be used)

        :return: None
       """
        message = "NanoPlot --fastq %s --outdir %s" % (
            self.fastq_file, self.save_directory)
        try:
            subprocess.run( message )
        except FileNotFoundError:
            if not self.fastq_file:
                print("A file was not passed in for the fastq_file argument. NanoPlot visualizations not performed.")
            else:
                self.file = self.fastq_file.split("/")[-1]  # split the file path by `/` and get the last item (the file name)
                print( "Your file `%s` was not found, please try again." % self.file )
                print( "Path of file: %s" % self.fastq_file )

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

        file_name = self.save_directory + "/density_plot.html"
        figure = px.histogram(data_frame=data,
                              x=read_count,
                              y=barcode_number,
                              hover_name=data[barcode_number],
                              hover_data=[data[read_count]],
                              labels={'reads_in_barcode': 'Reads in barcode',
                                      'barcode_number': 'barcodes'},
                              marginal="box"  # rug: data points above graph; box: boxplot above graph
                              )

        figure.update_layout(
            # format data when hovering over points
            hoverlabel=dict(
                bgcolor="white",
                font_size=16,
                font_family="Rockwell"
            ),
            # format the title
            title={
                'text'   : 'Comparison between read length and barcode number',
                'x'      : 0.5,
                'xanchor': 'center',
                'font'     : dict(size=25)
            },
            # format extra info (will appear right below title)
            annotations=[dict(xref='paper',
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
                         ],
            # set axis titles and size
            xaxis_title="Reads in Barcode",
            yaxis_title="Frequency",
            font=dict(
                size=17
            )
        )
        figure.write_html(file_name)
