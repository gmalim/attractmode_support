#!/usr/bin/python -tt
"""
Program to generate MAME emulation benchmarks of a single game or a list of games. For each game:
- User is asked to enter a benchmark timeperiod (default is 60 secs)
- Benchmarks are generated and saved in a dedicated MAME benchmarks directory (${MAMEconfigdir}/benchmarks).

Usage:

1) Change configsetup.py according to your system setup.
2) To process a single game, type: 
   ./benchmarkgenerator.py {game}
   where {game} is the romname of the game (e.g. pacman) 
OR to process all games in your Attract-Mode MAME romlist, type:
   ./benchmarkgenerator.py all

Author: Gordon Lim
Last Edit: 30 Jan 2018 
"""

import configsetup
import os
import subprocess
import sys

def generatebenchmark(game, benchmarktimeperiod):

    print("--- Generate new MAME benchmark file for {}...".format(game))

    # Generate new MAME speed benchmark:

    command = ["./mame64", "-str", benchmarktimeperiod, game]

    benchmarkfile = open(MAMEbenchmarkdir + game + "_lastgame.log", "w")
    subprocess.call(command, cwd = configsetup.MAMEexecdir, stdout = benchmarkfile)
    benchmarkfile.close()
    
    print("------ New MAME benchmark file for {} generated!".format(game))
        
    return 0

def main():

    # Setup configuration:
    
    configsetup.init()

    global MAMEbenchmarkdir
    
    MAMEbenchmarkdir = configsetup.MAMEconfigdir + "benchmarks/"

    if not os.path.isdir(MAMEbenchmarkdir):
        subprocess.call(["mkdir", "benchmarks"], cwd = configsetup.MAMEconfigdir)
        if not os.path.isdir(MAMEbenchmarkdir):
            print("ERROR: MAME benchmark directory does not exist  - EXIT")
            return 1
    
    # Check input and process game(s):
    
    inputargument = sys.argv[1]

    benchmarktimeperiod = raw_input('Enter benchmark running time in seconds (default: 60 secs) and press return/enter: ') or '60'
    
    if (inputargument == 'all'):

        # Transform AM romlist into list of games:

        games, header = configsetup.create_list_of_games_from_romlist()
    
        if (len(games) == 0):
            print("AM romlist is empty - EXIT")
            return 1

        # Create MAME benchmark file for each game:
        
        for game in games:
            generatebenchmark(game[0], benchmarktimeperiod)
                        
    else:
        generatebenchmark(inputargument, benchmarktimeperiod)

    return 0

if __name__ == '__main__':
    main()
