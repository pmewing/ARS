import plotly.express as px
import pandas as pd
import subprocess
import sys
from PyQt5.QtWidgets import QFileDialog, QApplication, QWidget


class Visualize:
    def __init__(self):
        self.starting_directory = r"/home/joshl/"
        app = QApplication(sys.argv)
        widget = QWidget()
        input_file = QFileDialog.getOpenFileName(parent=widget,
                                                 caption="Select the input file",
                                                 directory=self.starting_directory)

        output_directory = QFileDialog.getExistingDirectory(parent=widget,
                                                            caption="Select the output directory",
                                                            directory=self.starting_directory)

        message = "NanoPlot --fastq %s --outdir %s" % (input_file, output_directory)
        subprocess.run(message.split(" "))
        self.create_plotly_histogram()

    def create_plotly_histogram(self):
        barcode_number = 'barcode_number'
        read_count = 'reads_in_barcode'

        # load csv file
        csv_path = r"/home/joshl/minknow_data/CLC_2020-02-11/demultiplex_dual/barcode_counts.csv"
        data_frame = pd.read_csv(filepath_or_buffer=csv_path,
                                 delimiter=",",
                                 header=0,  # first row
                                 dtype={ barcode_number: str,
                                         read_count    : int })

        file_name = r"/home/joshl/PycharmProjects/ARS Projects/Visualizations/density_plot.html"
        figure = px.histogram(data_frame=data_frame,
                                   title="Comparison between read length and barcode number",
                                   x=read_count,
                                   y=barcode_number,
                                   hover_name=data_frame[barcode_number],
                                   hover_data=[data_frame[read_count]],
                                   marginal="box"  # rug: data points above graph; box: boxplot above graph
                                   )
        figure.update_layout(
            hoverlabel=dict(
                bgcolor="white",
                font_size=16,
                font_family="Rockwell"
            ),
            xaxis_title="Reads in Barcode",
            yaxis_title="Frequency",
            font=dict(
                size=16
            )
        )
        figure.write_html(file_name)
