#!/bin/bash

# test script 1 for basecalling the SBGx CLC study
# run `guppy_basecaller --print_workflows` for a list of kits, flow cells, and config files
# run `guppy_basecaller --help` for help


# Basecall using the fast neural network.
# uncomment --barcode-kits to demultiplex in one command using default settings
guppy_basecaller --resume \
				 --input_path ~/minknow_data/SBGX_CLC \
				 --save_path ~/minknow_data/basecalled \
				 --recursive \
				 --config dna_r9.4.1_450bps_fast.cfg \
				 --num_callers 1 \
				 --cpu_threads_per_caller 12 \
				# --barcode_kits EXP-PBC096


# This is the de-multiplexing call
# Parameters not thoroughly investigated yet
# Below requires the barcode at both ends of the read. Changes from default are minor (not properly analyzed yet)
# Can also look for barcodes midstrand to detect chimeras. Does something, but not sure how effective. And MUCH slower.
guppy_barcoder --input_path ~/minknow_data/basecalled \
			   --save_path ~/minknow_data/demultiplex_dual \
			   --recursive \
			   --config configuration.cfg \
			   --worker_threads 12 \
			   --barcode_kits EXP-PBC096 \
			   --require_barcodes_both_ends
