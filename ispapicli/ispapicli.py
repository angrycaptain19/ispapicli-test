#!/usr/bin/python

import os
import sys
import argparse
from hexonet.apiconnector.response import Response
from pathlib import Path
from modules.core import Core
from modules.scrap import Scrap
from gui.mainframe import MainFrame
import textwrap
from PyQt5.QtWidgets import QApplication


def main(args):

    # create core logic object
    core_obj = Core()
    # get the python standard parser initialised
    parser = core_obj.initParser()
    # overwrite defualt error function of the parser with our local function
    parser.error = errorFunction
    # clean extra spaces, leave only single spaces among commands
    original_args = ' '.join(args)
    # remove extra spaces around the = cases are ' =', '= ', ' = '
    original_args = original_args.replace(" = ", "=")
    original_args = original_args.replace(" =", "=")
    original_args = original_args.replace("= ", "=")
    print("Command entered: " + original_args)
    print("----------------")
    # split args in an array
    splitted_args = original_args.split()
    try:
        # get main commands such as "-c checkdomain"
        args = vars(parser.parse_args(splitted_args))
        # get other parameters such as "limit=5"
        reminderargs = args['args']
        # execute the command and show the results
        result, data = core_obj.parseArgs(args)

        # case gui requested
        if result == 'gui':
            startGUI()

        # case show help requested
        elif result == 'help':
            print('\n')
            print(
                textwrap.dedent('''\
                ISPAPI - Commandline Tool
                ------------------------------------------------------------
                The tool can be used in two modes:
                 - By using '=' sign e.g. --command=QueryDomainList limit=5
                 - By using spaces e.g. --command QueryDomainList limit 5
                ------------------------------------------------------------

                '''))
            parser.print_help()

        # case command requested
        elif result == 'cmd':
            # append reminder args with the command
            params_list = core_obj.parseParameters(reminderargs)
            cmd = data
            # add them to data which is the command list
            cmd.update(params_list)
            response = core_obj.request(cmd)
            result = response.getPlain()
            print(result)
        # update current commands
        elif result == 'update':
            scraper = Scrap()
            scraper.scrapCommands()
        # cases for msg
        else:
            print(data)

        sys.exit(0)

    except Exception as e:
        print("Command failed due to: " + str(e))


def startGUI():
    app = QApplication(sys.argv)
    appGui = MainFrame()
    appGui.startGui()
    sys.exit(app.exec_())


def errorFunction(message):
    print('\nAn error occured: ' + message + '\n')
    sys.exit(0)


if __name__ == "__main__":

    argsLen = len(sys.argv)
    # if gui triggred
    # if argsLen == 0: # after finishing debugging mode
    if argsLen == 1:  # only in debugging mode
        startGUI()
    else:
        main(sys.argv[1:])
