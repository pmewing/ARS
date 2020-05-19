import plotly
import plotly.express as px
import pandas as pd


class Visualize:
    def __init__(self):

        barcode_number = 'barcode_number'
        read_count = 'read_count'

        # load csv file
        self.csv_path = r"/home/joshl/minknow_data/CLC_2020-02-11/demultiplex_dual/barcode_counts.csv"
        self.data_frame = pd.read_csv(filepath_or_buffer=self.csv_path,
                                      delimiter=",",
                                      header=0,  # first row
                                      dtype={barcode_number: str,
                                             read_count: int})

        self.file_name = r"/home/joshl/PycharmProjects/ARS Projects/Visualizations/density_plot.html"
        self.figure = px.histogram(data_frame=self.data_frame,
                                   title="Comparison between read length and barcode number",
                                   x=read_count,
                                   y=barcode_number,
                                   hover_name=self.data_frame[barcode_number],
                                   hover_data=[self.data_frame[read_count]],
                                   marginal="box"    # rug: data points above graph; box: boxplot above graph
                                   )
        self.figure.update_layout(
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
        self.figure.write_html(self.file_name)
