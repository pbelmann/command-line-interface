from abc import ABCMeta, abstractmethod
import biobox_cli.container   as ctn
import biobox_cli.util.misc   as util
import biobox_cli.util.error  as error
import inspect
import os

class Biobox:
    __metaclass__ = ABCMeta

    @abstractmethod
    def prepare_volumes(opts):
        pass

    def run(self, argv):
        doc = inspect.getdoc(inspect.getmodule(self))
        opts = util.parse_docopt(doc, argv, False)
        task        = opts['--task']
        image       = opts['<image>']
        output      = opts['--output']
        if os.listdir(output):
            error.err_exit("non_empty_output_dir", { "dir": output})
        volumes = self.prepare_volumes(opts, output)
        ctn.exit_if_no_image_available(image)
        ctnr = ctn.create(image, task, volumes)
        ctn.run(ctnr)
        return ctnr

    def remove(self, container):
            """
            Removes a container
            Note this method is not tested due to limitations of circle ci
            """
            ctn.remove(container)