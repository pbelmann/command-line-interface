"""
Usage:
    biobox run short_read_assembler <image> [--no-rm] --input=FILE --output=FILE [--task=TASK]

Options:
-h, --help              Show this screen.
-v, --version           Show version.
-i FILE, --input=FILE   Source FASTQ file containing paired short reads
-o DIR, --output=DIR    Destination FASTA file for assembled contigs
-t TASK, --task=TASK    Optionally specify a biobox task to run [default: default]
-r, --no-rm             Don't remove the container after the process finishes
"""

import biobox_cli.container   as ctn
import biobox_cli.biobox_file as fle
from biobox_cli.biobox import Biobox

import os

class Assembler(Biobox):

    def get_yaml(self):
        return self.yaml_data

    def prepare_volumes(self, opts, host_dst_dir):
        fastq_file  = opts['--input']

        cntr_fastq_file = "/fastq/input.fq.gz"
        fastq_values = [(cntr_fastq_file, "paired")]
        yaml_data = [fle.fastq_arguments(fastq_values)]
        biobox_yaml = fle.generate(yaml_data)

        host_src_dir = os.path.abspath(fastq_file)

        volumes = [
            ctn.volume_string(host_src_dir, cntr_fastq_file),
            ctn.biobox_file_volume_string(fle.create_biobox_directory(biobox_yaml)),
            ctn.output_directory_volume_string(host_dst_dir)]
        return volumes

    def after_run(self, output):
        pass