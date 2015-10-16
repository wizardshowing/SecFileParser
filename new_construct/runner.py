#!/usr/bin/env python3

import os
import sys

class SecFileParserCommand(object):
    def __init__(self, input_dir = None, output_dir = None):
        "constructure"
        self.input_dir = input_dir
        self.output_dir = output_dir
    
    def execute(self):
        """The main execution function.
        """
        print('input_dir: :{}'.format(self.input_dir))
        print('output_dir: :{}'.format(self.output_dir))



def run(args):
    """command line tool"""
    try:
        runner = SecFileParserCommand(args[0],args[1])
        runner.execute()
    except Exception as e:
        print("exception: {}".format(e))
        sys.exit(2)

if __name__ == '__main__':
    run(sys.argv[1:])