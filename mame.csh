#! /bin/csh
#
# MAME startup script which invokes MAME, followed by some quick analysis programs:
# - hiscoreanalysis.py   : Reformats hiscores (if available) into ascii code
# - benchmarkanalysis.py : Saves and analyzes benchmark data
#
# Usage:
# 1) Follow instructions in the code of the program above.
# 2) Change the following two directories according to your setup:

set MAMEDIR      = "/Users/uci/Games/SDLMAME v0.193 64-bit/"
set AMSUPPORTDIR = "/Users/uci/Programming/Python/attractmode_support/"

# 2) Open a terminal and cd to the directory that contains this startup script.
# 3) Type: source mame.csh {game}
#
# OR create an alias for this startup script in your main .cshrc startup script:
# (i.e. alias mame 'source ${AMSUPPORTDIR}/mame.csh')

cd "${MAMEDIR}"
./mame64 $1 > /Users/uci/Games/SDLMAME\ Config/benchmarks/$1_lastgame.log
${AMSUPPORTDIR}/hiscoreanalysis.py   $1
${AMSUPPORTDIR}/benchmarkanalysis.py $1
cd -

unset MAMEDIR
unset AMSUPPORTDIR

exit
