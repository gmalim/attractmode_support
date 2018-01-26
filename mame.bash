#!/bin/bash
#
# MAME startup script for the sh shell family which invokes MAME, followed by some quick analysis programs:
# - hiscoreanalysis.py   : Reformats hiscores (if available) into ascii code
# - benchmarkanalysis.py : Saves and analyzes benchmark data
#
# To run a game with MAME:
#
# 1) Follow instructions in the code of the programs above.
# 2) Change the following two directories according to your setup:

MAMEDIR="${HOME}/Games/SDLMAME v0.193 64-bit/"          # Directory containing your mame executable 
AMSUPPORTDIR="${HOME}/Programming/attractmode_support/" # Your 'attractmode_support' directory 

# 3) Create an alias for this script in your main bash startup script, i.e. add the line:
#    alias mame='source ${AMSUPPORTDIR}/mame.bash'
#    to your ${HOME}/.bash_profile, where ${AMSUPPORTDIR} points to your 'attractmode_support' directory
# 4) Open a terminal and type: mame {game}

cd "${MAMEDIR}"
if [ "$#" == "0" ]; then         # To start MAME without any game 
    ./mame64
elif [ "$1" = "-listxml" ]; then # To accommodate Attract-Mode's --build-romlist option
    ./mame64 $1
else                             # To start a game
    ./mame64 $1 > /Users/uci/Games/SDLMAME\ Config/benchmarks/$1_lastgame.log
    ${AMSUPPORTDIR}/hiscoreanalysis.py   $1
    ${AMSUPPORTDIR}/benchmarkanalysis.py $1
fi
cd -

unset MAMEDIR
unset AMSUPPORTDIR

