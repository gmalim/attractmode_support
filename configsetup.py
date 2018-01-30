#!/usr/bin/python -tt
"""
Program to setup attractmode_support configuration.

Change the following directories according to your system setup:
"""

myAMsupportdir  = "${HOME}/Programming/attractmode_support/" # Your attractmode_support directory
myMAMEconfigdir = "${HOME}/.mame/"                           # Directory containing your MAME configuration files
myAMconfigdir   = "${HOME}/.attract/"                        # Directory containing your Attract-Mode configuration files
myMAMEexecdir   = "${HOME}/Games/SDLMAME v0.193 64-bit/"     # Directory containing your MAME executable
myAMexecdir     = "${HOME}/Games/attract/"                   # Directory containing your Attract-Mode executable

import os

def init():

    global AMsupportdir    
    global MAMEconfigdir 
    global AMconfigdir  
    global MAMEexecdir    
    global AMexecdir

    AMsupportdir  = os.path.expandvars(myAMsupportdir)
    MAMEconfigdir = os.path.expandvars(myMAMEconfigdir) 
    AMconfigdir   = os.path.expandvars(myAMconfigdir)
    MAMEexecdir   = os.path.expandvars(myMAMEexecdir)
    AMexecdir     = os.path.expandvars(myAMexecdir)
    
    if not os.path.isdir(AMsupportdir):
        print("attractmode_support directory does not exist  - EXIT")
        exit
        
    if not os.path.isdir(MAMEconfigdir):
        print("MAME config directory does not exist  - EXIT")
        exit
        
    if not os.path.isdir(AMconfigdir):
        print("AM config directory does not exist  - EXIT")
        exit
            
    if not os.path.isdir(MAMEexecdir):
        print("MAME executable directory does not exist  - EXIT")
        exit

    if not os.path.isdir(AMexecdir):
        print("AM executable directory does not exist  - EXIT")
        exit

    return 0

def create_list_of_games_from_romlist():
    
    filename = AMconfigdir + 'romlists/mame.txt'
    file = open(filename, 'r')
    header = file.readline() # first line
    
    games = []
    for line in file.readlines():
        game = [field for field in line.rstrip('\n').split(";")]
        games.append(game)
        
    file.close()

    return games, header
