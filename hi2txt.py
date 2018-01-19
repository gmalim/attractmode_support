#!/usr/bin/python -tt
"""
Program to get hiscores from a MAME game using the 'hi2txt' Java archive (see http://greatstone.free.fr/hi2txt/), and save them in a formatted ini file in a dedicated Attract-Mode hiscore directory. This allows hiscores to be displayed in any Attract-Mode layout using the 'file-format' module (e.g. see my Silky layout).

Requirements:

- hi2txt.jar and hi2txt.zip (http://greatstone.free.fr/hi2txt/)
- Java (to run hi2txt.jar)
- hiscore.dat (http://highscore.mameworld.info/)

Usage:

Step 1) Change $MAMEdir and $AMdir according to your setup:
"""

MAMEdir = "/Users/uci/Games/SDLMAME Config/"
AMdir   = "/Users/uci/Games/Attract-Mode Config/"

"""
Step 2)  Create a $MAMEdir/hi2txt/ directory and put hi2txt.jar and hi2txt.zip in this directory
Step 3)  Unzip hi2txt.zip and rename the unzipped directory "hi2txt_zip_contents"
Step 4)  Make sure hiscore.dat is located in your $MAMEdir/dats/ directory
Step 5a) To process a single game, type: 
         ./hi2txt.py {game}
         where {game} is the romname of the game (e.g. pacman) 
Step 5b) Or, to process all games in your Attract-Mode MAME romlist, type:
         ./hi2txt.py all

Author: Gordon Lim
Last Edit: 18 Jan 2018 
"""

# Setup environment variables:

hiscoredat_dir = MAMEdir   + "dats/"
hi2txtdir      = MAMEdir   + "hi2txt/"
hi2txt_zipdir  = hi2txtdir + "hi2txt_zip_contents/"
outputdir      = AMdir     + "hiscores/"

import sys
import os
import subprocess

def createhiscorefile(game):

    print("--- Creating AM hiscore file for {}:".format(game))
    
    # Check if unzipped hi2txt.zip contains game.xml file:
    
    if not os.path.isfile(hi2txt_zipdir + game + ".xml"):
        print("------ hi2txt.zip does not contain {}.xml => the hiscores of this game have not been identified or decoded yet => EXIT1".format(game))
        return 1
    else:
        print("------ hi2txt.zip contains {}.xml...".format(game))

    # Check if nvram/game/ or hi/game.hi exists in MAME directory:

    hiscorefile = ''
    
    if os.path.isdir(MAMEdir + 'nvram/' + game):
        hiscorefile = MAMEdir + 'nvram/' + game
        print("------ nvram/{}/ exists...".format(game))
    elif os.path.isfile(MAMEdir + 'hi/' + game + '.hi'):
        hiscorefile = MAMEdir + 'hi/' + game + '.hi'
        print("------ hi/{}.hi exists...".format(game))
    else:
        print("------ nvram/{0} nor hi/{0}.hi exists => this game has not been played yet => EXIT2".format(game))
        return 2

    # Run hi2txt.jar and pipe output to temporary txt file:

    hiscoredat = hiscoredat_dir + 'hiscore.dat'
    
    command = ["java", "-jar", "hi2txt.jar", "-r", hiscorefile,
               "-hiscoredat", hiscoredat]
#               "-keep-field", '"RANK"',  # Does not work with subprocess.call()?
#               "-keep-field", '"SCORE"', # Does not work with subprocess.call()?
#               "-keep-field", '"NAME"']  # Does not work with subprocess.call()?

    subprocess.call(["cd", hi2txtdir])
    tmpfile = open("tmp.txt", "w")
    subprocess.call(command, stdout=tmpfile)
    tmpfile.close()
    
    # Open temporary txtfile containing hi2txt output and create list of scores:

    hi2txtfile = open(hi2txtdir + "tmp.txt", 'r')

    firstline = hi2txtfile.readline()
    if (len(firstline) == 0):
        print("------ hi2txt.jar output w.r.t. {} is empty => this game has been played but no hiscore has been saved in nvram or hi yet => EXIT3".format(game))
        return 3
    
    #print("first line = {}".format(firstline))
    scores = []
    for line in hi2txtfile.readlines():
        score = [field for field in line.rstrip('\n').split('|')]
        #print(score)
        if (len(score) == 1) and (score[0] == ''):
            continue
        if (len(score) == 2):
            score.append("   ")
        scores.append(score[0:3])

    #print scores
    
    hi2txtfile.close()
    subprocess.call(["rm","tmp.txt"])
    
    # Create formatted .ini file to be used by the Attract-Mode 'file-format' module:
    
    outputfilename = outputdir + game + ".ini"

    outputfile = open(outputfilename, 'w')

    for score in scores:
        outputfile.write("[Score_{}]\n".format(score[0]))
        outputfile.write("score={}\n".format(score[1]))
        outputfile.write("name={}\n".format(score[2]))

    outputfile.close()

    print("------ AM hiscore file for {} created => SUCCESS".format(game))
        
    return 0

def main():

    # Input:
    
    name = sys.argv[1]

    if (name == 'all'):

        # Open inputfile:
    
        filename = AMdir + 'romlists/mame.txt'
        file = open(filename, 'r')
        firstline = file.readline()
                
        # Create list of games:
        
        games = []
        for line in file.readlines():
            game = [field for field in line.rstrip('\n').split(";")]
            games.append(game[0])
            
        file.close()
    
        # Create hiscore file for each game:
        
        for game in games:
            createhiscorefile(game)
                        
    else:
        createhiscorefile(name)

    return 0

if __name__ == '__main__':
    main()
