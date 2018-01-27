#!/usr/bin/python -tt
"""
Program to analyze MAME benchmark files of a single game or a list of games. For each game:
- Average emulation speed and total emulation time is calculated by taking into account the benchmark from the last game and
  the previous benchmark, which is udated and saved in a dedicated MAME benchmarks directory (${MAMEconfigdir}/benchmarks).
- Average emulation speed is converted into a 1-5 star rating.
- The benchmark data are reformatted and saved in a dedicated Attract-Mode benchmarks directory (${AMconfigdir}/benchmarks).
- This allows benchmark data to be displayed in any Attract-Mode layout using the 'file-format' module.

Usage:

1) Change configsetup.py according to your system setup.
2) Optionally adjust star rating levels to your liking:
"""

starlevels = [80, 90, 95, 99]

"""
3) To process a single game, type: 
   ./benchmarkanalysis.py {game}
   where {game} is the romname of the game (e.g. pacman) 
OR to process all games in your MAME benchmarks directory, type:
   ./benchmarkanalysis.py all

Author: Gordon Lim
Last Edit: 26 Jan 2018 
"""

import configsetup
import os
import re
import subprocess
import sys

regexsearchpattern = 'Average speed: (\d+)\.\d*% \((\d+) seconds\)'

def getbenchmarkdata(MAMEbenchmarkfilename):

    # Use regex search to extract benchmark data from file:
        
    MAMEbenchmarkfile = open(MAMEbenchmarkfilename, "r")    
    line = MAMEbenchmarkfile.readline()
    MAMEbenchmarkfile.close()
    
    matchobject = re.search(regexsearchpattern, line)
    
    if not matchobject:
        print("------ regex search of MAME benchmark file failed - EXIT")
        return 0, 0
    
    speed = float(matchobject.group(1))
    time  = float(matchobject.group(2))

    return speed, time   

def calculatestarrating(speed):

    speed = int(speed)
    stars = 0
    
    if (0 < speed < starlevels[0]):
        stars = 1
    elif (starlevels[0] < speed < starlevels[1]):
        stars = 2
    elif (starlevels[1] < speed < starlevels[2]):
        stars = 3
    elif (starlevels[2] < speed < starlevels[3]):
        stars = 4
    else:
        stars = 5
        
    return stars

def createbenchmarkfile(game):

    print("--- Creating AM benchmark file for {}:".format(game))

    # Get benchmark data from last MAME benchmark file:

    speed_new = 0
    time_new  = 0
    
    MAMEbenchmarkfilename_lastgame = MAMEbenchmarkdir + game + '_lastgame.log'
    if os.path.isfile(MAMEbenchmarkfilename_lastgame):
        speed_new, time_new = getbenchmarkdata(MAMEbenchmarkfilename_lastgame)
        subprocess.call(["rm", MAMEbenchmarkfilename_lastgame])

    # Get benchmark data from previous MAME benchmark file:
        
    speed_old = 0
    time_old  = 0
        
    MAMEbenchmarkfilename_allgames = MAMEbenchmarkdir + game + '_allgames.log'
    if os.path.isfile(MAMEbenchmarkfilename_allgames):
        speed_old, time_old = getbenchmarkdata(MAMEbenchmarkfilename_allgames)

    if ((time_old == 0) and (time_new == 0)):
        print("------ MAME benchmark files do not exist - EXIT")
        return
        
    # Calculate total time and average speed weigthed by time:

    time_total = time_old + time_new
    speed_ave  = speed_old*(time_old/time_total) + speed_new*(time_new/time_total)

    # Update previous MAME benchmark file:

    MAMEbenchmarkfile = open(MAMEbenchmarkfilename_allgames, "w")    
    benchmarkline = "Average speed: {:.2f}% ({} seconds)".format(float(speed_ave), int(time_total))
    MAMEbenchmarkfile.write(benchmarkline)
    MAMEbenchmarkfile.close()
    
    # Calculate "star" rating:

    stars = calculatestarrating(speed_ave)

    # Create and save formatted .ini file to be used by the Attract-Mode 'file-format' module:

    AMbenchmarkfilename = AMbenchmarkdir + game + '.ini'
    AMbenchmarkfile = open(AMbenchmarkfilename, "w")    

    AMbenchmarkfile.write("[MyMAMEBenchmark]\n")
    AMbenchmarkfile.write("speed={:.2f}\n".format(round(speed_ave)))
    AMbenchmarkfile.write("stars={}\n".format(stars))
    AMbenchmarkfile.write("time={}\n".format(int(time_total)))
    
    AMbenchmarkfile.close()

    print("------ AM benchmark file for {} created => SUCCESS".format(game))
        
    return 0

def main():

    # Setup configuration:
    
    configsetup.init()

    global MAMEbenchmarkdir
    global AMbenchmarkdir
    
    MAMEbenchmarkdir = configsetup.MAMEconfigdir + "benchmarks/"
    AMbenchmarkdir   = configsetup.AMconfigdir   + "benchmarks/"

    if not os.path.isdir(MAMEbenchmarkdir):
        subprocess.call(["mkdir", "benchmarks"], cwd = configsetup.MAMEconfigdir)
        if not os.path.isdir(MAMEbenchmarkdir):
            print("ERROR: MAME benchmark directory does not exist  - EXIT")
            return 1

    if not os.path.isdir(AMbenchmarkdir):
        subprocess.call(["mkdir", "benchmarks"], cwd = configsetup.AMconfigdir)
        if not os.path.isdir(AMbenchmarkdir):
            print("ERROR: AM benchmark directory does not exist  - EXIT")
            return 1

    # Check input and process game(s):
    
    inputargument = sys.argv[1]

    if (inputargument == 'all'):
        for filename in os.listdir(MAMEbenchmarkdir): # For all files in MAME benchmark directory:
            #print(filename)
            if (filename[-13:] == "_lastgame.log"):
                romname = filename[:-13]
                createbenchmarkfile(romname)
    else:
        createbenchmarkfile(inputargument)

    return 0

if __name__ == '__main__':
    main()
