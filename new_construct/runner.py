#!/usr/bin/env python3
##runner.py
##An instance of the __main__ function
##for parsing a raw SEC Filling in HTML format
##into two distinct outputs.
##One output file is the raw text from the SEC filling
##without the HTML tags.  The second output is all the
##text/paragraphs from the Sec filling that contained dollar
##signs ($)

import os
import os.path
import sys
import glob
from bs4 import BeautifulSoup 

##SecFileReader: A wrapper on the Beautiful Soup Python library,
##for pulling data out of Sec filling documents in HTML format.
##Specifically, it uses the Python html5lib parser.
##It takes a full path to the intended SEC Filling as input.
##The class operates as a Python generator. Upon reading the
##input file, it 'yield' two distinct types of tuples. One
##of the tuples contain all the text within the SEC HTML documents
##with the HTML stripped off, and delimited by new lines (\n)
##The second type of tuple contain the parapgraphs (div) items
##of the parse tree that contain the dollar sign ($), excluding
##paragraphs that are contained within HTML tables.  The client
##could then consume the yielded tuples as needed.
class SecFileReader(object):
    text_version = "text_version"
    paragraph_version = 'paragraph_version'
    paragraph_text = 'text'
    start_location = 'start_location'
    end_location = 'end_location'
    target_text = None
    
    def __init__(self):
        """
            Constructor to instantiate objects,
            and initialze pertinent atributes.
        """
        self.file_name = None
        self.soup = None
        self.original_text_version = None
    
    def parseTextVersion(self):
        """
            parseTextVersion: generator function
            Assuming that the self.soup attribute has been
            initialized with a BeautifulSoup  object, this
            generator function yield a tuple object containing
            the raw text within the SEC filling.  The HTML is
            stripped off using the Beautiful Soup get_text function;
            The resulting text is delimitted by new lines (\n).
            The tuple is in the form (OUTPUT_TYPE,OUTPUT)
            In this case, the OUTPUT_TYPE is 'text_version'.
            And OUTPUT is the html-stripped text document.
        """
        #yield None is the self.soup object hasn't been initialize
        if not self.soup:
            yield None
        else:
            #yield a tuple containing only the non-html
            #text within the SEC filling document
            yield (self.text_version, self.soup.get_text("\n"))
        yield
    
    def parseParagraphs(self):
        """
            parseParagraphs: generator function.
            Assuming that the self.soup attribute has been
            initialized with a BeautifulSoup  object, this
            generator function 'yield' tuple objects containing
            raw text paragraphs/divs within the SEC filling.
            It only yileds paragraphs that contain the dollar
            sign ($).  It excludes all paragraphs that are
            within table elements within the html document.
            The tuple is in the form (OUTPUT_TYPE,
            {OUTPUT_TEXT: 'The actual raw text document,
             START_INDEX: 'Index location of the paragrah sub-string
                           within the whole raw text document,
             END_INDEX: 'end location of the paragrah sub-string
                        within the whole raw text document,
            }
            )
            In this case, the OUTPUTTYPE is 'paragraph_version'.
            And OUTPUT is a paragraph containing a $ symbol.
        """
        
        if not self.soup:
            yield None
        
        def paragraph_is_qualified(tag):
            """
                An auxillary fucntion to check if a given
                tag (paragraph node on the parse tree) containes
                a dollar sign ($).  If the paragraph does contain
                a dollar sign, an extra check is made to ensure that
                it is not within a table element (<table>) within the
                parsed tree.
            """
            retval = False
            parents = []
            
            #Check if this particular tag contains a
            #dollar sign ($)
            if tag.get_text().find("$") != -1:
                
                parents = tag.find_parents(name="table")
                if len(parents) == 0:
                        retval = True
            return retval
        
        #No paragraph tags (<p>) in the sample document
        #So we are going off the <div> tags
        for each_tag in self.soup.find_all("div"):

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
        """
            parse: generator function.
            Given the full path to a certain SEC filling
            document, this function opens the file and
            instantiates BeautifulSoup object.  The BeautifulSoup
            object is instructed to use the Python html5lib parser.
            This function calls the parseTextVersion and
            parseParagraphs and yields thier outputs to the client/caller
            routine.
             
        """
        #Get the full path name of the targeted file to parse
        self.file_name = file_name
        
        #yield None is file name is not provided
        if not self.file_name:
            yield None
        #Open the input file
        with open(self.file_name) as _fd:
            #Instantiate the BeautifulSoup object
            #and get a copy of the text version
            #of the HTML document.
            self.soup = BeautifulSoup(_fd,"html5lib")
            self.original_text_version = self.soup.get_text()
            
            #yield the whole document as a text string.
            #This text string has all the html tags removed
            for each_object in self.parseTextVersion():
                yield each_object
            
            #yield paragraph the paragraph texts that
            #contains the dollar sign, but are
            #not descendants of <table> tags
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
        self.added_indecies = []
    
    def writeTextFile(self,file_content):
        if not self.current_input_file: return
        old_filename = os.path.split(self.current_input_file)[1]
        old_filename = old_filename[:old_filename.find(".htm")]
        new_file_name = "{}{}.txt".format(self.output_dir,old_filename)
        with open(new_file_name,"w") as _fd:
            _fd.write(file_content)
    
    def writePargrapsFile(self,file_content):
        #work-around to prevent multiple inserts for now
        if file_content[SecFileReader.start_location] in self.added_indecies:
            return
        else:
            with open(self.paragraphs_file,"a") as _fd:
                _fd.write("{}text:{}\nstart:{}\nend:{}\n{}".format(
                    "\n\t{\n\t",
                    file_content[SecFileReader.paragraph_text],
                    file_content[SecFileReader.start_location],
                    file_content[SecFileReader.end_location],
                    "\n\t}\n\t"
                    )
                )
                #Keep track of paragraphs that has been inserted into the ouput file
                self.added_indecies.append(file_content[SecFileReader.start_location])
    
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
            self.added_indecies = []
        
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