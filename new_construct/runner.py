#!/usr/bin/env python3

import os
import os.path
import sys
import glob
from bs4 import BeautifulSoup

class SecFileReader(object):
    text_version = "text_version"
    def __init__(self):
        self.file_name = None
        self.soup = None
    
    def parseTextVersion(self):
        print("HERE 4")
        if not self.soup: yield None
        text_version = self.soup.get_text("\n")
        print("HERE 5")
        yield ('text_version', text_version)
    
    def parse(self, file_name = None):
        self.file_name = file_name
        if not self.file_name:
            yield None
        print("HERE 1")
        with open(self.file_name) as _fd:
            print("HERE 2")
            self.soup = BeautifulSoup(_fd,"html.parser")
            print("HERE 3")
            for each_object in self.parseTextVersion():
                yield each_object
            print("HERE 3a")
        yield 

class SecFileParserCommand(object):
    def __init__(self, input_dir = None, output_dir = None):
        "constructure"
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.parser = SecFileReader()
        self.current_input_file = None
    
    def writeTextFile(self,file_content):
        if not self.current_input_file: return
        old_filename = os.path.split(self.current_input_file)[1]
        old_filename = old_filename[:old_filename.find(".htm")]
        new_file_name = "{}{}.txt".format(self.output_dir,old_filename)
        with open(new_file_name,"w") as _fd:
            _fd.write(file_content)
    
    def execute(self):
        """The main execution function.
        """
        print('input_dir: {}'.format(self.input_dir))
        print('output_dir: {}'.format(self.output_dir))
        
        targeted_files = '{}*'.format(self.input_dir)
        found_files = glob.glob('{}*'.format(targeted_files))
        
        print ("targeted_files: {}".format(targeted_files))
        print ("found_files: {}".format(found_files))
        
        for each_file in found_files:
            self.current_input_file = each_file
            print ("each_file: {}".format(self.current_input_file))
            
            for each_object in self.parser.parse(self.current_input_file):
                #import pdb; pdb.set_trace()
                if each_object is None: return
                
                if each_object[0] is SecFileReader.text_version:
                    self.writeTextFile(each_object[1])
                    
        



def run(args):
    """command line tool"""
    try:
        runner = SecFileParserCommand(args[0],args[1])
        runner.execute()
    except Exception as e:
        print("exception: {}".format(e))
        raise
        sys.exit(2)

if __name__ == '__main__':
    run(sys.argv[1:])