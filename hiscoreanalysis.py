#!/usr/bin/python -tt
"""
Program to get hiscores from MAME games using the 'hi2txt' Java archive (see http://greatstone.free.fr/hi2txt/), 
and save them in formatted .ini files in a dedicated Attract-Mode hiscores directory. This allows hiscores to be 
displayed in any Attract-Mode layout using the 'file-format' module.

Requirements:

- hi2txt.jar and hi2txt.zip (see http://greatstone.free.fr/hi2txt/)
- Java (see https://www.java.com)
- hiscore.dat (see http://highscore.mameworld.info/)

Usage:

1) Change the following two directories according to your setup:
"""

MAMEconfigdir = "/Users/uci/Games/SDLMAME Config/"      # Directory containing your MAME configuration files
AMconfigdir   = "/Users/uci/Games/Attract-Mode Config/" # Directory containing your Attract-Mode configuration files

"""
2) Create a $MAMEconfigdir/hi2txt/ directory and put hi2txt.jar and hi2txt.zip in this directory.
3) Unzip hi2txt.zip here and rename the unzipped directory "hi2txt_zip_contents".
4) Make sure hiscore.dat is located in your $MAMEconfigdir/dats/ directory.
5) Create a $AMconfigdir/hiscores/ directory where hiscore .ini files will be saved.
6) To process a single game, type: 
   ./hiscoreanalysis.py {game}
   where {game} is the romname of the game (e.g. pacman) 
OR to process all games in your Attract-Mode MAME romlist, type:
   ./hiscoreanalysis.py all

Author: Gordon Lim
Last Edit: 24 Jan 2018 
"""

hiscoredat    = MAMEconfigdir + "dats/hiscore.dat"
hi2txtdir     = MAMEconfigdir + "hi2txt/"
hi2txtzipdir  = hi2txtdir     + "hi2txt_zip_contents/"
AMhiscoredir  = AMconfigdir   + "hiscores/"

import sys
import os
import subprocess

def createhiscorefile(game):

    print("--- Creating AM hiscore file for {}:".format(game))
    
    # Check if unzipped hi2txt.zip contains game.xml file:
    
    if not os.path.isfile(hi2txtzipdir + game + ".xml"):
        print("------ hi2txt.zip does not contain {}.xml => the hiscores of this game have not been identified or decoded yet => EXIT1".format(game))
        return 1
    else:
        print("------ hi2txt.zip contains {}.xml...".format(game))

    # Check if nvram/game/ or hi/game.hi exists in MAME directory:

    hiscorefile = ''
    
    if os.path.isdir(MAMEconfigdir + 'nvram/' + game):
        hiscorefile = MAMEconfigdir + 'nvram/' + game
        print("------ nvram/{}/ exists...".format(game))
    elif os.path.isfile(MAMEconfigdir + 'hi/' + game + '.hi'):
        hiscorefile = MAMEconfigdir + 'hi/' + game + '.hi'
        print("------ hi/{}.hi exists...".format(game))
    else:
        print("------ nvram/{0} nor hi/{0}.hi exists => this game has not been played yet => EXIT2".format(game))
        return 2

    # Run hi2txt.jar and pipe output to temporary txt file:
    
    command = ["java", "-jar", hi2txtdir + "hi2txt.jar", "-r", hiscorefile, "-hiscoredat", hiscoredat,
               "-keep-field", 'RANK', 
               "-keep-field", 'SCORE',
               "-keep-field", 'NAME'] 

    tmpfile = open("tmp.txt", "w")
    subprocess.call(command, stdout=tmpfile)
    tmpfile.close()
    
    # Read temporary txt file containing hi2txt output and check hiscore table structure:

    tmpfile = open("tmp.txt", "r")    
    firstline = tmpfile.readline()
    hiscoretablefields = firstline.rstrip('\n').split('|')

    if (len(firstline) == 0):
        print("------ hi2txt.jar output w.r.t. {} is empty => this game has been played but no hiscore has been saved in nvram or hi yet => EXIT3".format(game))
        return 3
    elif (len(hiscoretablefields) < 2):
        print("------ Incompatible hiscore table format => EXIT4".format(game))
        return 4
    elif ((hiscoretablefields[0] != "RANK") and (hiscoretablefields[1] != "SCORE")):
        print("------ Incompatible hiscore table format => EXIT5".format(game))
        return 5

    # Create hiscore list:
    
    scores = []
    for line in tmpfile.readlines():
        score = [field for field in line.rstrip('\n').split('|')]
        #if (len(score) == 1) and (score[0] == ''): # remove empty lines
        #    continue
        if (len(score) < 2): # remove anomalous entries
            continue
        if (len(score) == 2): # add empty name for games like pacman, invaders, etc.
            score.append("   ")
        scores.append(score[0:3])
    
    tmpfile.close()
    subprocess.call(["rm","tmp.txt"])
    
    # Create formatted .ini file to be used by the Attract-Mode 'file-format' module:
    
    AMhiscorefilename = AMhiscoredir + game + ".ini"
    AMhiscorefile = open(AMhiscorefilename, 'w')

    for score in scores:
        AMhiscorefile.write("[Score_{}]\n".format(score[0]))
        AMhiscorefile.write("score={}\n".format(score[1]))
        AMhiscorefile.write("name={}\n".format(score[2]))

    AMhiscorefile.close()

    print("------ AM hiscore file for {} created => SUCCESS".format(game))
        
    return 0

def main():

    # Check directories:

    if not os.path.isdir(MAMEconfigdir):
        print("MAME config directory does not exist  - EXIT")
        return 1

    if not os.path.isdir(hi2txtdir):
        print("MAME hi2txt directory does not exist  - EXIT")
        return 1

    if not os.path.isdir(hi2txtzipdir):
        print("MAME hi2txt_zip_contents directory does not exist  - EXIT")
        return 1

    if not os.path.isdir(AMconfigdir):
        print("AM config directory does not exist  - EXIT")
        return 1

    if not os.path.isdir(AMhiscoredir):
        print("AM hiscores directory does not exist  - EXIT")
        return 1
    
    if not os.path.isfile(hiscoredat):
        print("MAME hiscore.dat does not exist  - EXIT")
        return 1
    
    # Input:
    
    inputargument = sys.argv[1]

    if (inputargument == 'all'):

        # Open inputfile:
    
        filename = AMconfigdir + 'romlists/mame.txt'
        file = open(filename, 'r')
        firstline = file.readline()
                
        # Create list of games:
        
        games = []
        for line in file.readlines():
            game = [field for field in line.rstrip('\n').split(";")]
            games.append(game[0])
            
        file.close()
    
        # Create hiscore file for each game:

        counts = [0, 0, 0, 0, 0, 0]

        for game in games:
            returncode = createhiscorefile(game)
            counts[returncode] += 1
            
        print("==> Return code '0' indicates a succesfully processed game")
        print("--> Return code '1' indicates a hi2txt-incompatible game")
        print("--> Return code '2' indicates a hi2txt-compatible game, but it has not been played yet")
        print("--> Return code '3' indicates a hi2txt-compatible game that has been played, but no hiscore has been saved yet")
        print("--> Return code '4' indicates a hi2txt-compatible game, but the hiscore table format is anomalous")
        print("--> Return code '5' indicates a hi2txt-compatible game, but the hiscore table format is anomalous")

        print("==> Total # of games = {}".format(sum(counts)))
        for i in range(0, len(counts)):
            print("--> # of return code '{}' games = {}".format(i, counts[i]))
            
    else:
        createhiscorefile(inputargument)

    return 0

if __name__ == '__main__':
    main()
