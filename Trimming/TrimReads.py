import subprocess
import os


class Trim:
    def __init__(self, open_directory, save_directory):
        # cutadapt --revcomp -a <3' PRIMER SEQUENCE> -g <5' PRIMER SEQUENCE> -e <ERROR RATE (0.2)> -o <OUTPUT DIRECTORY> <INPUT FILE>

        self.open_directory = open_directory
        self.save_directory = save_directory

        self.primer_3 = "TTTCTGTTGGTGCTGATATTGCAGRGTTYGATYMTGGCTCAG"
        self.primer_5 = "ACTTGCCTGTCGCTCTATCTTCTACCTTGTTACGACTT"
        error_rate = 0.2

        self.num_files = len(os.listdir(self.open_directory))
        self.iteration = 1
        for root, directory, files in os.walk(self.open_directory):
            for file in files:
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
                           "-e 0.2",                                 # error rate
                           "-o%s/%s" % (self.save_directory, file),  # there must not be a space between the `o` and `%` otherwise cutadapt throws an error. Unsure why
                           "%s" % os.path.join(root, file)
                           ]
                subprocess.run(message)
                self.update_time(self.num_files)

    def update_time(self, total):
        print("%s of %s complete" % (self.iteration, total), end="")
        print("\r", end="")
        self.iteration += 1
