#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
htcondor_gce_provisioner: Provisioner of Google Compute Engine for HTCondor
"""

from __future__ import print_function
import os
import sys
from gce_manager import Output, GceManager

__prog__ = os.path.basename(__file__)
__description__ = __doc__
__author__ = "Michiru Kaneda"
__copyright__ = "Copyright (c) 2018 Michiru Kaneda"
__credits__ = ["Michiru Kaneda"]
__license__ = "MIT"
__version__ = "v0.0.1"
__date__ = "05/Jun/2018"
__maintainer__ = "Michiru Kaneda"
__email__ = "Michiru.Kaneda@cern.ch"
__status__ = "Prototype"


class HTCondorGCEProvisioner(object):
    """Provisioner of Google Compute Engine for HTCondor"""

    def __init__(self):
        """__init__"""
        self.params = {
            "config_file":
            os.environ["HOME"] + "/.config/htcondor-gce-provisioner/config",
            "verbose": 2,
        }
        self.output = Output(self.params["verbose"])

    def debug(self, text, verbose=3):
        """Debug level output wrapper"""
        self.output.debug(text, verbose)

    def info(self, text, verbose=2):
        """Information level output wrapper"""
        self.output.info(text, verbose)

    def warn(self, text, verbose=1):
        """Warning level output wrapper"""
        self.output.warn(text, verbose)

    def err(self, text, verbose=0):
        """Error level output wrapper"""
        self.output.err(text, verbose)

    def set_params(self, params):
        """Set parameters"""
        for (k, v) in params.items():
            self.params[k] = v
        self.output.set_verbose(self.params["verbose"])

    def read_config(self):
        """Read configuration file"""
        if os.path.isfile(self.params["config_file"]):
            params = {}
            with open(self.params["config_file"]) as conf_file:
                for line in conf_file:
                    line_orig = line
                    if line.find("#") != -1:
                        line = line.split("#")[0].strip()
                    if line == "":
                        continue
                    if line.find("=") == -1 or len(line.split("=")) > 2:
                        self.warn("Wrong configuration line: " + line_orig)
                        continue
                    (k, v) = line.split("=")
                    params[k.strip()] = v.strip()
            self.set_params(params)

    def get_activity(self):
        """Get condor activity"""
        from subprocess import Popen, PIPE
        p = Popen("condor_status", stdout=PIPE, stderr=PIPE, shell=True)
        stdout_data, stderr_data = p.communicate()
        print(stdout_data)


    def execute(self, argv=None):
        """Main function"""

        self.read_config()

        #import argparse
        #parser = argparse.ArgumentParser(
        #    add_help=False,
        #    formatter_class=argparse.RawTextHelpFormatter,
        #    description=__description__,
        #)

        #subparsers = parser.add_subparsers(
        #    title="subcommands", metavar="[command]", help="", dest="command")

        #help_doc = "or -h/--help\nPrint Help (this message)\n\n"
        #subparsers.add_parser("help", description=help_doc, help=help_doc,
        #                      formatter_class=argparse.RawTextHelpFormatter)

        #parser.add_argument("-h", "--help",
        #                    action="store_true",
        #                    help="Print Help (this message)")

        #if argv is None:
        #    argv = sys.argv[1:]
        #command = None
        #for a in argv:
        #    if a in subparsers.choices:
        #        if command is not None:
        #            self.err("More than two commands are given: " +
        #                     command + ", " + a)
        #            return 20
        #        command = a
        #if command is not None:
        #    argv.remove(command)
        #    argv.append(command)

        #args = parser.parse_args(argv)

        #if args.help or args.command == "help" or args.command is None:
        #    parser.print_help()
        #    return 0
        #self.set_params(vars(args))

        #gm = GceManager()
        #ret = gm.execute()

        self.get_activity()
        return ret

if __name__ == "__main__":
    p = HTCondorGCEProvisioner()
    ret = p.execute()
    sys.exit(ret)
