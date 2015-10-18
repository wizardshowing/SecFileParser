#!/usr/bin/env python3

import os
import os.path
import sys
import glob
from bs4 import BeautifulSoup

class SecFileReader(object):
    text_version = "text_version"
    paragraph_version = 'paragraph_version'
    paragraph_text = 'text'
    start_location = 'start_location'
    end_location = 'end_location'
    target_text = None
    def __init__(self):
        self.file_name = None
        self.soup = None
        self.original_text_version = None
    
    def parseTextVersion(self):
        if not self.soup: yield None
        self.target_text = self.soup.get_text("\n")
        yield (self.text_version, self.target_text)
    
    def parseParagraphs(self):
        if not self.soup: yield None
        text_version = self.soup.get_text()
        
        def paragraph_is_qualified(tag, tag_content = None):
            retval = False
            parents = []
            #Check if this particular tag contains a 
            if tag.get_text().find("$") != -1:
                
                parents = tag.find_parents(name="table")
                #import pdb;pdb.set_trace()
                if len(parents) == 0:
                        retval = True
            #if retval is True:
            #    print("good tag: {}".format(tag.get_text()))
            #    print("good tag.parents: {}\n---------------------".format(parents))
            return retval
        
        #No paragraph tags (<p>) in the sample document
        #So we are going off the <div> tags
        #
        only_paragraph_tags = self.soup.find_all("div")
        
        for each_tag in only_paragraph_tags:

            if paragraph_is_qualified(each_tag) is True:
                _text = each_tag.get_text()
                _start_location = self.original_text_version.find(_text)
                _end_location = _start_location + len(_text)
                #import pdb; pdb.set_trace()
                
                retval = {
                    self.paragraph_text: _text,
                    self.start_location: _start_location,
                    self.end_location: _end_location
                }
                yield (self.paragraph_version,retval)
    
    def parse(self, file_name = None):
        self.file_name = file_name
        if not self.file_name:
            yield None
        with open(self.file_name) as _fd:
            self.soup = BeautifulSoup(_fd,"html.parser")
            self.original_text_version = self.soup.get_text()
            #yieeld text file items
            for each_object in self.parseTextVersion():
                yield each_object
            #yield paragraph file items
            for each_object in self.parseParagraphs():
                yield each_object
        yield 

class SecFileParserCommand(object):
    def __init__(self, input_dir = None, output_dir = None):
        "constructure"
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.parser = SecFileReader()
        self.current_input_file = None
        self.paragraphs_file = "{}pargraphs.txt".format(self.output_dir)
    
    def writeTextFile(self,file_content):
        if not self.current_input_file: return
        old_filename = os.path.split(self.current_input_file)[1]
        old_filename = old_filename[:old_filename.find(".htm")]
        new_file_name = "{}{}.txt".format(self.output_dir,old_filename)
        with open(new_file_name,"w") as _fd:
            _fd.write(file_content)
    
    def writePargrapsFile(self,file_content):
        #import pdb; pdb.set_trace()
        with open(self.paragraphs_file,"a") as _fd:
            _fd.write("{}text:{}\nstart:{}\nend:{}\n{}".format(
                "\n\t{\n\t",
                file_content[SecFileReader.paragraph_text],
                file_content[SecFileReader.start_location],
                file_content[SecFileReader.end_location],
                "\n\t}\n\t"
                )
            )
    
    def execute(self):
        """The main execution function.
        """
        targeted_files = '{}*'.format(self.input_dir)
        found_files = glob.glob('{}*'.format(targeted_files))
        
        try:
            #Remove old output if any
            os.remove(self.paragraphs_file)
        except:
            pass
        
        with open(self.paragraphs_file,"a") as _fd:
            _fd.write("[")

        for each_file in found_files:
            self.current_input_file = each_file
        
            for each_object in self.parser.parse(self.current_input_file):
                if each_object is None:
                    continue
                elif each_object[0] is SecFileReader.text_version:
                    self.writeTextFile(each_object[1])
                elif each_object[0] is SecFileReader.paragraph_version:
                    self.writePargrapsFile(each_object[1])

        with open(self.paragraphs_file,"a") as _fd:
            _fd.write("]")
        



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