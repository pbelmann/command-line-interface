"""
biobox verify - Verify that a Docker image matches the given specification type

Usage:
    biobox verify <biobox_type> <image> [--task=TASK] [--verbose]

Options:
  -h, --help             Show this screen.
  -t TASK, --task=TASK   Specify which biobox task to test. [default: default]
  -V, --verbose          Show the status of each biobox verification test.

Available Biobox types:

  short_read_assembler  Assemble short reads into contigs
"""

import biobox_cli.util.misc        as util
import biobox_cli.util.error       as error
import biobox_cli.util.functional  as fn
import biobox_cli.behave_interface as behave
import biobox_cli.container        as ctn

import string

from fn    import F
from fn.op import flip

def run(argv):
    opts    = util.parse_docopt(__doc__, argv, False)
    biobox  = opts['<biobox_type>']
    image   = opts['<image>']
    task    = opts['--task']
    verbose = opts['--verbose']

    ctn.exit_if_no_image_available(image)

    results = behave.run(biobox, image, task)

    if verbose:
        None
    elif behave.is_failed(results):
        error = fn.thread([
            behave.get_failing_scenarios(results),
            F(map, behave.scenario_name),
            F(flip, string.join, "\n")])

        error.err_exit('failed_verification', {'image': image, 'error': error, 'biobox' : biobox})
