#!/usr/bin/python -tt
'''
MAME support program to reformat and save game controls data in a formatted ASCII file (AMcontrols.ini). This file can be used to display game controls data in Attract-Mode.

Requirements:

- Latest controls.ini file. This file is no longer developed (?), currently v0.141.1, e.g. see here: http://ledblinky.net/downloads/controls.ini.0.141.1.zip

Usage:

1) Change configsetup.py according to your system setup.
2) Download latest controls.ini file and replace the controls.ini file in the data folder, or use the provided version of this file (v0.141.1)
3) In a terminal, type: ./reformatcontrols.py

Author: Gordon Lim
Last Edit: 1 Feb 2018 
'''

import configsetup
import os
import re

def main():

    # Setup configuration:
    
    configsetup.init()

    filename = configsetup.AMsupportdir + 'data/controls.ini'

    if not os.path.isfile(filename):
        print("controls.ini does not exist - EXIT")
        return 1

    # Reformat:
    
    file = open(filename, 'r')

    header = file.readline() # skip header
    
    goodlines = []

    for line in file.readlines():
        matchobject = re.search('\[.+\]\r', line)
        if matchobject:
            goodlines.append(line)
        matchobject = re.search('.+=.+\r', line)
        if matchobject:
            goodlines.append(line)

    file.close()

    # Save:
    
    filename = configsetup.AMsupportdir + 'data/AMcontrols.ini'
    
    file = open(filename, 'w')

    for goodline in goodlines:
        file.write(goodline)
        
    file.close()
    
    return 0

if __name__ == '__main__':
    main()
