import subprocess


def run():
    fastq_file = r"/home/joshl/minknow_data/CLC_2020-02-11/demultiplex_dual/_merged_files/fastq_runid_67a0761ea992f55d7000e748e88761780ca1bb60_barcode08.fastq"
    output = r"/home/joshl/Desktop/output/"

    message = [
        "fastqc",
        "-o",
        output,
        fastq_file
    ]

    subprocess.call(message)
