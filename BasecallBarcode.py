import os
import shutil


class Basecall:
    def __init__(self, input_directory, output_directory):
        self.__basecall(input_directory=input_directory, output_directory=output_directory)

    def __basecall(self, input_directory, output_directory):
        """
        This is a direct copy-paste from the bash script provided by patrick
        Basecall using the fast neural network.
        Two underscores on this function classifies this as a private function

        :param str input_directory: This is where basecalling should get files from
        :param str output_directory: This is where the output of basecalling should be saved
        :return: None
        """
        message = "guppy_basecaller " \
                  "--recursive " \
                  "--input_path {0} " \
                  "--save_path {1} " \
                  "--config dna_r9.4.1_450bps_fast.cfg " \
                  "--num_callers 1 " \
                  "--cpu_threads_per_caller 12".format(input_directory, output_directory)
        os.system(message)
        move_log_files(output_directory=output_directory)


class Barcode:
    def __init__(self, input_directory, output_directory):
        self.__barcode(input_directory=input_directory, output_directory=output_directory)

    def __barcode(self, input_directory, output_directory):
        """
        This function will call guppy_barcoder on the input_directory, and save files into the output_directory
        :param str input_directory: This is where barcoding should get files from
        :param str output_directory: This is where the output of barcoding should be saved
        :return: None
        """
        message = "guppy_barcoder" \
                  "--input_path {0}" \
                  "--save_path {1} " \
                  "--recursive " \
                  "--config configuration.cfg " \
                  "--worker_threads 12 " \
                  "--barcode_kits EXP-PBC096 " \
                  "--require_barcodes_both_ends".format(input_directory, output_directory)
        os.system(message)
        move_log_files(output_directory=output_directory)


def move_log_files(output_directory):
    """
    This function will move log files to their own folder within the output_directory parameter
    :param str output_directory: This is the location where the output is stored. A new folder`logs` will be created here
    """

    # these lines will move log files into their own folder within the output_directory
    new_path = output_directory + "/logs"
    for root, directory, files in os.walk(output_directory):
        for file in files:
            if ".log" in file:
                # the output files may not be created. Try to move files. If they cannot be moved, create them
                try:
                    shutil.move(os.path.join(root, file), os.path.join(new_path, file))
                except FileNotFoundError:
                    os.mkdir(new_path)
                    shutil.move(os.path.join(root, file), os.path.join(new_path, file))
