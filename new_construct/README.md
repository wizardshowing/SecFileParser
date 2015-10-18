# SecFileParser
A python parser for SEC filings

                    USAGE

Recommended Software:
1) Git 1.7.9.5: https://git-scm.com/
        For downloading the this git repository.

Required Software:
1) virtualenv 13.1.2: https://virtualenv.pypa.io/en/latest/
              For running the exercise sandbox (virtual environment)
                    
               FOR A QUICK RUN

Assuming you are running linux/MAC OS based operating system with
the standard Python virtualenv installed. You can get virtualenv here:
https://virtualenv.pypa.io/en/latest/

This exercise ships a virtulenv sandbox.  Pull up a terminal on
your Lunix/MAC OS based Operating System.
For a quick run, execute the following on your terminal:


1) cd ~

2) git clone https://github.com/alchemiccoruja/SecFileParser.git

   NOTE: If you dont have git installed, you can
   download a zip file of the repository
   here https://github.com/alchemiccoruja/SecFileParser
   Just look for  the 'DownloadZip' button
   unzip and the file and proceed to step (3) below.
   

3) cd SecFileParser

4) source bin/activate

5) bin/python3 new_construct/runner.py  new_construct/input/ new_construct/output/

6) ls -lrt new_construct/output/


                MORE EXPLANATION
The commands will download the SecFilParser git repository
and run it with the sample SEC filling document.

You will find the sample document in SecFileParser/new_construct/input/

Output documents will be in SecFileParser/new_construct/output/

You can add arbitrary SEC fillings into SecFileParser/new_construct/input/
as needed.


                LIBRARIES USED
BeautifulSoup 4

pip3 (pip 7.1.2)

python3 (3.3.5)

virtualenv 13.1.2

git 1.7.9.5

libxml

html5lib

                MODULE DOCUMENTATION
On a web browser, open SecFileParser/new_construct/docs/new_construct.runner.html

