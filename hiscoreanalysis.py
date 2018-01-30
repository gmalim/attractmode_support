#!/usr/bin/python -tt
"""
Program to get hiscores from a single game or a list of games. For each game:
- Hiscores are readout using the 'hi2txt' Java archive (see http://greatstone.free.fr/hi2txt/).
- The hi2txt output is saved in a dedicated MAME hiscores directory (${MAMEconfigdir}/hiscores).
- The top hiscore is reformatted and saved in a formatted ASCII file: AMhiscores.ini
- This allows hiscores to be displayed in Attract-Mode layouts by using the 'file-format' module.

Requirements:

- hi2txt.jar and hi2txt.zip (see http://greatstone.free.fr/hi2txt/)
- Java (see https://www.java.com)
- hiscore.dat (see http://highscore.mameworld.info/)

Usage:

1) Change configsetup.py according to your system setup.
2) Create a ${MAMEconfigdir}/hi2txt/ directory and put hi2txt.jar and hi2txt.zip in this directory.
3) Unzip hi2txt.zip here and rename the unzipped directory "hi2txt_zip_contents".
4) Make sure hiscore.dat is located in your ${MAMEconfigdir}/dats/ directory.
5) To process a single game, type: 
   ./hiscoreanalysis.py {game}
   where {game} is the romname of the game (e.g. pacman) 
OR to process all games in your Attract-Mode MAME romlist, type:
   ./hiscoreanalysis.py all

Author: Gordon Lim
Last Edit: 30 Jan 2018 
"""

import configsetup
import os
import sys
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

    MAMEbinaryhiscorefile = configsetup.MAMEconfigdir
    
    if os.path.isdir(MAMEbinaryhiscorefile + 'nvram/' + game):
        MAMEbinaryhiscorefile += 'nvram/' + game
        print("------ nvram/{}/ exists...".format(game))
    elif os.path.isfile(MAMEbinaryhiscorefile + 'hi/' + game + '.hi'):
        MAMEbinaryhiscorefile += 'hi/' + game + '.hi'
        print("------ hi/{}.hi exists...".format(game))
    else:
        print("------ nvram/{0} nor hi/{0}.hi exists => this game has not been played yet => EXIT2".format(game))
        return 2

    # Run Java on hi2txt.jar and save output in MAME hiscores directory:

    MAMEhiscorefilename = MAMEhiscoredir + game + ".ini"
    MAMEhiscorefile = open(MAMEhiscorefilename, 'w')
    
    command = ["java", "-jar", hi2txtdir + "hi2txt.jar", "-r", MAMEbinaryhiscorefile, "-hiscoredat", hiscoredat,
               "-keep-field", 'RANK', 
               "-keep-field", 'SCORE',
               "-keep-field", 'NAME'] 

    subprocess.call(command, stdout=MAMEhiscorefile)
    MAMEhiscorefile.close()

    # Read temporary txt file containing hi2txt output and check hiscore table structure:

    MAMEhiscorefile = open(MAMEhiscorefilename, "r")    
    firstline = MAMEhiscorefile.readline()
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
    for line in MAMEhiscorefile.readlines():
        score = [field for field in line.rstrip('\n').split('|')]
        if (len(score) < 2): # remove anomalous entries
            continue
        if (len(score) == 2): # add empty name for games like pacman, invaders, etc.
            score.append("   ")
        scores.append(score[0:3])
    
    MAMEhiscorefile.close()

    # Save top hiscore in AMhiscores.ini:

    AMhiscorefilename = configsetup.AMsupportdir + "AMhiscores.ini"

    AMhiscorefilename_exists = False
    if os.path.isfile(AMhiscorefilename):
        AMhiscorefilename_exists = True
        AMhiscorefile = open(AMhiscorefilename, 'r')
        lines = []
        while True:
            line = AMhiscorefile.readline()
            if not line:
                break
            if (line == "[{}]\n".format(game)):
                dummy = AMhiscorefile.readline() # skip score
                dummy = AMhiscorefile.readline() # skip name
            else:
                lines.append(line)
        AMhiscorefile.close()
        
    AMhiscorefile = open(AMhiscorefilename, 'w')
    if AMhiscorefilename_exists:
        for line in lines:
            AMhiscorefile.write(line)
    AMhiscorefile.write("[{}]\n".format(game))
    AMhiscorefile.write("score={}\n".format(scores[0][1]))
    AMhiscorefile.write("name={}\n".format(scores[0][2]))
    AMhiscorefile.close()
   
    print("------ AM hiscore file for {} created => SUCCESS".format(game))
        
    return 0

def main():

    # Setup configuration:
    
    configsetup.init()

    global hi2txtdir
    global hi2txtzipdir
    global hiscoredat
    global MAMEhiscoredir
    
    hi2txtdir      = configsetup.MAMEconfigdir + "hi2txt/"
    hi2txtzipdir   = hi2txtdir                 + "hi2txt_zip_contents/"
    hiscoredat     = configsetup.MAMEconfigdir + "dats/hiscore.dat"
    MAMEhiscoredir = configsetup.MAMEconfigdir + "hiscores/"

    if not os.path.isdir(hi2txtdir):
        print("MAME hi2txt directory does not exist - EXIT")
        return 1

    if not os.path.isdir(hi2txtzipdir):
        print("MAME hi2txt_zip_contents directory does not exist - EXIT")
        return 1

    if not os.path.isfile(hiscoredat):
        print("MAME hiscore.dat does not exist - EXIT")
        return 1

    if not os.path.isdir(MAMEhiscoredir):
        subprocess.call(["mkdir", "hiscores"], cwd = configsetup.MAMEconfigdir)
        if not os.path.isdir(MAMEhiscoredir):
            print("ERROR: AM hiscores directory does not exist - EXIT")
            return 1
    
    # Check input and process game(s):
    
    inputargument = sys.argv[1]

    if (inputargument == 'all'):

        # Transform AM romlist into list of games:

        games, header = configsetup.create_list_of_games_from_romlist()
        
        if (len(games) == 0):
            print("AM romlist is empty - EXIT")
            return 1

        # Create hiscore file for each game:

        counts = [0, 0, 0, 0, 0, 0]

        for game in games:
            returncode = createhiscorefile(game[0])
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
