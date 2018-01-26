#!/bin/bash
#
# MAME startup script which invokes MAME, followed by some quick analysis programs:
# - hiscoreanalysis.py   : Reformats hiscores (if available) into ascii code
# - benchmarkanalysis.py : Saves and analyzes benchmark data
#
# Usage:
# 1) Follow instructions in the code of the program above.
# 2) Change the following two directories according to your setup:

MAMEDIR="/Users/uci/Games/SDLMAME v0.193 64-bit/"                 # Directory containing your mame executable 
AMSUPPORTDIR="/Users/uci/Programming/Python/attractmode_support/" # Your 'attractmode_support' directory 

# 2) Open a terminal and cd to the directory that contains this startup script.
# 3) Type: source mame.csh {game}
#
# OR, instead of steps 2 and 3, create an alias for this startup script in your main .bash startup script, i.e. add the line:
# alias mame = 'bash ${AMSUPPORTDIR}/mame.bash'
# to your ~/.bashrc, where ${AMSUPPORTDIR} points to your 'attractmode_support' directory

cd "${MAMEDIR}"
if [ "$1" = "-listxml" ] ; then
    ./mame64 $1
else
    ./mame64 $1 > /Users/uci/Games/SDLMAME\ Config/benchmarks/$1_lastgame.log
    ${AMSUPPORTDIR}/hiscoreanalysis.py   $1
    ${AMSUPPORTDIR}/benchmarkanalysis.py $1
fi
cd -

exit

