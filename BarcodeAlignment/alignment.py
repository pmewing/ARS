# use guppy_aligner to align the reads (from _merged_files) into something coherent
# see what this does/how it works/etc
import os
import subprocess


class Alignment:
    def __init__(self):

        # guppy_aligner --input_path ~/minknow_data/CLC_2020-02-11/demultiplex_dual/_merged_files/ --output_path ~/Desktop/alignment_output --align_ref ~/Downloads/zymogen_alignment.fq

        # silva_alignment = silva_alignment.arb
        # zymogen_alignment = zymogen_alignment.fq

        message = "guppy_aligner " \
                  "--input_path /home/joshl/minknow_data/CLC_2020-02-11/demultiplex_dual/_merged_files/ " \
                  "--save_path /home/joshl/Desktop/zymogen_alignment " \
                  "--align_ref /home/joshl/Downloads/zymogen_alignment.fq".split(" ")

        subprocess.run( message )
