#!/usr/bin/python -tt
"""
Program to generate new MAME emulation benchmarks of a single game or a list of games.

Usage:

1) Change $MAMEdir and $AMdir according to your setup:
   $MAMEdir = directory where {game}.log files created by mame.csh/mame.sh are stored.

"""

MAMEexecdir   = "/Users/uci/Games/SDLMAME v0.193 64-bit/" # Directory containing your MAME executable
MAMEconfigdir = "/Users/uci/Games/SDLMAME Config/"        # Directory containing your MAME config files
AMconfigdir   = "/Users/uci/Games/Attract-Mode Config/"  # Directory containing your Attract-Mode config files

"""

2) To process a single game, type: 
   ./benchmarkgenerator.py {game}
   where {game} is the romname of the game (e.g. pacman) 
OR to process all games in your Attract-Mode MAME romlist, type:
   ./benchmarkgenerator.py all

Author: Gordon Lim
Last Edit: 24 Jan 2018 
"""

import subprocess
import sys

MAMEromdir       = MAMEexecdir   + "roms/"
MAMEbenchmarkdir = MAMEconfigdir + "benchmarks/"

benchmarktimeperiod = 60 # secs

def generatebenchmark(game):

    print("--- Generate new MAME benchmark file for {}...".format(game))

    # Generate new MAME speed benchmark:

    command = ["./mame64", "-str", str(benchmarktimeperiod), game]

    benchmarkfile = open(MAMEbenchmarkdir + game + "_lastgame.log", "w")
    subprocess.call(command, cwd = MAMEexecdir, stdout = benchmarkfile)
    benchmarkfile.close()
    
    print("------ New MAME benchmark file for {} generated!".format(game))
        
    return 0

def main():

    # Input:
    
    name = sys.argv[1]
    
    if (name == 'all'):

        # Transform AM romlist into list of games:
    
        filename = AMconfigdir + 'romlists/mame.txt'
        file = open(filename, 'r')
        firstline = file.readline()
                
        games = []
        for line in file.readlines():
            game = [field for field in line.rstrip('\n').split(";")]
            games.append(game[0])
            
        file.close()
    
        # Create MAME speed file for each game:
        
        for game in games:
            generatebenchmark(game)
                        
    else:
        generatebenchmark(name)

    return 0

if __name__ == '__main__':
    main()
