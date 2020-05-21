import subprocess
import os
import time

class Trim:
    def __init__(self, input_directory, save_directory):
        # cutadapt --revcomp -a <3' PRIMER SEQUENCE> -g <5' PRIMER SEQUENCE> -e <ERROR RATE (0.2)> -o <OUTPUT DIRECTORY> <INPUT FILE>

        self.input_directory = input_directory
        self.save_directory = save_directory

        self.primer_5 = "TTTCTGTTGGTGCTGATATTGCAGRGTTYGATYMTGGCTCAG"
        self.primer_3 = "ACTTGCCTGTCGCTCTATCTTCTACCTTGTTACGACTT"
        self.primer_5_no_adapter = "AGRGTTYGATYMTGGCTCAG"
        self.primer_3_no_adapter = "TACCTTGTTACGACTT"
        self.error_rate = 0.15

        self.num_files = len(os.listdir(self.input_directory))
        self.iteration = 1

        for root, directory, files in os.walk(self.input_directory):
            for file in files:
                self.update_task()
                # cutadapt needs the output file to be created before it is able to write to it
                # we will create it here
                write_file = open(os.path.join(self.save_directory, file), 'w')
                write_file.close()

                message = ["cutadapt",
                           "--revcomp",                              # orient strands
                           "--quiet",                                # do not show output on command line (unless there is an error)
                           "-j 0",                                   # threads (0 = auto)
                           "-a %s" % self.primer_3,                  # 3' end
                           "-g %s" % self.primer_5,                  # 5' end
                           "-e %s" % self.error_rate,                # error rate
                           "-o%s/%s" % (self.save_directory, file),  # there must not be a space between the `o` and `%` otherwise cutadapt throws an error. Unsure why
                           "%s" % os.path.join(root, file)
                           ]
                subprocess.run(message)

    def update_task(self):
        """
        This function will simply over-write the current line and print and update statement
        """
        print("'\rTrimming {0} of {1}".format(self.iteration, self.num_files), end='')
        # print('\r', 'Trimming %s of %s' % (self.iteration, self.num_files), end='')
        self.iteration += 1