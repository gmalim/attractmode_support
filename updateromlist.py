#!/usr/bin/python -tt
"""
Program to update Attract-Mode MAME romlist with additional game data:
- Change 'AltTitle' field to display title
- Change 'Extra' field to formatted bezel dimensions string, 
  as provided by bezeldimensions.dat
- Change 'Buttons' field to sortable title and update 'AltTitle' field if game is part of a series,
  as provided by specialgames.dat

Usage:

1) Copy this program, specialgames.dat (if available) and bezeldimensions.dat (if available) to
   your Attract-Mode romlist directory (i.e. the directory that contains the 'mame.txt' romlist)
2) Change 'attractmodeexecutable' variable according to your setup:
"""

attractmodeexecutable = "/Users/uci/Games/Attract-Mode v2.3.0/attract" 

"""
3) In a terminal, cd to your Attract-Mode romlist directory and type: 
   ./updateromlist.py
4) Type y/n if you want Attract-Mode to create a new romlist first (y), or process your old romlist (n).

Author: Gordon Lim
Last Edit: 19 Jan 2018 
"""

# Setup environment variables:

bezeldimensionsfilename = "bezeldimensions.dat"
specialgamesfilename    = "specialgames.dat"

import subprocess
import os
from shutil import copy2

# Update AltTitle field with new display title:

def update_AltTitle_field(game):

    alttitle = game[1]
    
    newalttitle = ''

    # Strip regular and square parentheses from title:
    
    skip1c = 0
    skip2c = 0

    for i in alttitle:
        if i == '[':
            skip1c += 1
        elif i == '(':
            skip2c += 1
        elif i == ']' and skip1c > 0:
            skip1c -= 1
        elif i == ')'and skip2c > 0:
            skip2c -= 1
        elif skip1c == 0 and skip2c == 0:
            newalttitle += i

    game[14] = newalttitle.rstrip() # game[14] = AltTitle
            
    return

# Update Extra field with formatted bezel dimensions string

def update_Extra_field(game): 

    # Read bezel dimensions from file:
        
    file = open(bezeldimensionsfilename, 'r')
    firstline = file.readline() # skip first line

    bezels = []
    for line in file.readlines():
        bezel = [field for field in line.rstrip('\n').split(";")]
        bezels.append(bezel)

    file.close()

    # Create formatted bezel dimenions string and update Extra field:

    game[15] = '' # game[15] = Extra
    
    for bezel in bezels:
        if bezel[0] == game[0]:
            encoded_str = str(bezel[2]) + "-" + \
                          str(bezel[3]) + "-" + \
                          str(bezel[4]) + "-" + \
                          str(bezel[5])
            game[15] = encoded_str
        else:
            continue
    
    return

# Update Buttons field with new sorting title and update AltTitle with "series" display title (if available):

def update_Buttons_and_AltTitle_fields(game):
    
    sortingtitle = game[1]
    displaytitle = game[14]

    # Read special games data from file:

    file = open(specialgamesfilename, 'r')
    firstline = file.readline() # skip first line

    specialgames = []

    for line in file.readlines():
        specialgame = [field for field in line.rstrip('\n').split(";")]
        specialgames.append(specialgame)

    file.close()

    # Update sorting and display titles for special games:
    
    for specialgame in specialgames:    

        if (specialgame[0] == game[0]):
            sortingtitle = specialgame[1]
            if (specialgame[2] == ''):
                displaytitle = game[14] 
            else:
                displaytitle = specialgame[2] + ' ' + game[14]
                
    # Remove "The" and "Vs." from sorting title:
           
    if (sortingtitle[0:4] == 'The '):
        sortingtitle = sortingtitle[4:]
    if (sortingtitle[0:4] == 'Vs. '):
        sortingtitle = sortingtitle[4:]

    # Update romlist fields:
        
    game[14] = displaytitle # AltTitle
    game[16] = sortingtitle # Buttons
 
    return

def main():

    # Check if romlist exists:

    romlistexists = False
    if os.path.isfile('mame.txt'):
        romlistexists = True
        
    # Create new Attract-Mode MAME romlist or not:

    createnewromlist = raw_input('Create new romlist? [y/n]: ')

    if (createnewromlist == 'y'):
        if romlistexists: # Remove old romlist:
            subprocess.call(["rm", "mame.txt"]) 
        subprocess.call([attractmodeexecutable, "--build-romlist", "mame"])
        copy2('mame.txt', 'mame_ORIG.txt') # Create backup romlist
    elif (createnewromlist == 'n'):
        if not romlistexists:
            print("Romlist does not exist in this directory - EXIT")
            return 1
        if os.path.isfile('mame_ORIG.txt'): # Use backup romlist:
            copy2('mame_ORIG.txt', 'mame.txt')
    else:
        print("Next time please type 'y' or 'n'")
        return 2
    
    # Parse romlist into list of games:
    
    filename = 'mame.txt'
    file = open(filename, 'r')
    firstline = file.readline()

    games = []
    for line in file.readlines():
        game = [field for field in line.rstrip('\n').split(";")]
        games.append(game)

    file.close()
    
    # Update fields in list of games:

    bezeldimensionsfile_exists = False
    if os.path.isfile(bezeldimensionsfilename):
        bezeldimensionsfile_exists = True
    else:
        print("--- bezeldimensions.dat does not exist in this directory, skipping update of Extra field")

    specialgamesfile_exists = False
    if os.path.isfile(specialgamesfilename):
        specialgamesfile_exists = True
    else:
        print("--- specialgames.dat does not exist in this directory, skipping update of Buttons and AltTitle fields")

    for game in games:
        
        # Update 'AltTitle' field with display title:
        update_AltTitle_field(game)

        # Update 'Extra' field with formatted bezel dimensions string:
        if (bezeldimensionsfile_exists):
            update_Extra_field(game)
                    
        # Update 'Buttons' field with sorting title, and 'AltTitle' field with "series" display title:
        if (specialgamesfile_exists):
            update_Buttons_and_AltTitle_fields(game)

        # Exceptions:

        if (game[0] == 'bm1stmix'):
            game[1]  = 'Beatmania (ver JA-B)'
            game[14] = 'Beatmania'
            game[16] = 'Beatmania (ver JA-B)'
            
        if (game[0] == 'garou'):
            game[1]  = 'Fatal Fury 9 / Garou - Mark of the Wolves (NGM-2530)'
            game[14] = 'Fatal Fury 9 / Garou - Mark of the Wolves'
            game[16] = 'Fatal Fury 9 / Garou - Mark of the Wolves (NGM-2530)'    
        
    # Create updated romlist:

    file = open(filename, 'w')
    file.write(firstline)

    for game in games:

        # Remove anomalous 'series' entry
        if (game[0] == 'series'):
            continue
        
        line = ";".join(game)
        file.write(line + '\n')

    file.close()
        
    return 0

if __name__ == '__main__':
    main()
