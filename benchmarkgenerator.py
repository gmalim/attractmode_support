#!/usr/bin/python -tt
"""
Program to generate MAME emulation benchmarks of a single game or a list of games.

Usage:

1) Change the following three directories according to your setup:
"""

MAMEexecdir   = "/Users/uci/Games/SDLMAME v0.193 64-bit/" # Directory containing your MAME executable
MAMEconfigdir = "/Users/uci/Games/SDLMAME Config/"        # Directory containing your MAME config files
AMconfigdir   = "/Users/uci/Games/Attract-Mode Config/"   # Directory containing your Attract-Mode config files

"""
2) Create a directory called "benchmarks" in your $MAMEconfigdir
3) To process a single game, type: 
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

def generatebenchmark(game, benchmarktimeperiod):

    print("--- Generate new MAME benchmark file for {}...".format(game))

    # Generate new MAME speed benchmark:

    command = ["./mame64", "-str", benchmarktimeperiod, game]

    benchmarkfile = open(MAMEbenchmarkdir + game + "_lastgame.log", "w")
    subprocess.call(command, cwd = MAMEexecdir, stdout = benchmarkfile)
    benchmarkfile.close()
    
    print("------ New MAME benchmark file for {} generated!".format(game))
        
    return 0

def main():

    # Check directories:

    if not os.path.isdir(MAMEconfigdir):
        print("MAME config directory does not exist  - EXIT")
        return 1
    
    if not os.path.isdir(AMconfigdir):
        print("AM config directory does not exist  - EXIT")
        return 1
    
    if not os.path.isdir(MAMEexecdir):
        print("MAME exec directory does not exist  - EXIT")
        return 1

    if not os.path.isdir(MAMEromdir):
        print("MAME rom directory does not exist  - EXIT")
        return 1
    
    if not os.path.isdir(MAMEbenchmarkdir):
        print("MAME benchmark directory does not exist  - EXIT")
        return 1
    
    # Input:
    
    inputargument = sys.argv[1]

    benchmarktimeperiod = raw_input('Enter benchmark running time in seconds (default: 60 secs) and press return/enter: ') or '60'
    
    if (inputargument == 'all'):
        
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
            generatebenchmark(game, benchmarktimeperiod)
                        
    else:
        generatebenchmark(inputargument, benchmarktimeperiod)

    return 0

if __name__ == '__main__':
    main()
