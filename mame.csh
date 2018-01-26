#!/bin/csh
#
# MAME startup script for the csh shell family which invokes MAME, followed by some quick analysis programs:
# - hiscoreanalysis.py   : Reformats hiscores (if available) into ascii code
# - benchmarkanalysis.py : Saves and analyzes benchmark data
#
# Usage:
# 1) Follow instructions in the code of the program above.
# 2) Change the following two directories according to your setup:

set MAMEDIR      = "${HOME}/Games/SDLMAME v0.193 64-bit/"     # Directory containing your mame executable 
set AMSUPPORTDIR = "${HOME}/Programming/attractmode_support/" # Your 'attractmode_support' directory 

# 3) To run a game, open a terminal and cd to the directory that contains this startup script.
# 4) Type: ./mame.csh {game}
#
# OR:
#
# 3) Create an alias for this script in your main csh startup script, i.e. add the line:
#    alias mame 'source ${AMSUPPORTDIR}/mame.csh'
#    to your ${HOME}/.cshrc, where ${AMSUPPORTDIR} points to your 'attractmode_support' directory
# 4) To run a game, open a terminal and type: mame {game}

cd "${MAMEDIR}"
if ("$#" == "0") then
    ./mame64
else if ("$1" == "-listxml") then
    ./mame64 $1
else
    ./mame64 $1 > /Users/uci/Games/SDLMAME\ Config/benchmarks/$1_lastgame.log
    ${AMSUPPORTDIR}/hiscoreanalysis.py   $1
    ${AMSUPPORTDIR}/benchmarkanalysis.py $1
endif
cd -

unset MAMEDIR
unset AMSUPPORTDIR

