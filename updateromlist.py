#!/usr/bin/python -tt
"""
Program to update Attract-Mode MAME romlist with additional game data:

- Replace 'AltTitle' with updated title (parentheses removed, leading "The" removed, etc)
- Replace 'Extra' with formatted bezel dimensions string, as provided by bezeldimensions.txt (see analyzebezels.py)
- Replace 'Buttons' with sortable title and update 'AltTitle' if game is part of a series, as provided by 
  sortanddisplaytitles.txt (create by hand)

Usage:

1) Change configsetup.py according to your system setup.
2) If you want to use bezels in your Attract-Mode layout, use bezelanalysis.py to create bezeldimensions.txt.
3) If you want to change the order of specific games in Attract-Mode, create/update sortanddisplaytitles.txt file 
   by hand. You can also indicate specific games are part of a series.
4) In a terminal, cd to your Attract-Mode romlist directory and type: 
   ./updateromlist.py
5) Type y/n if you want Attract-Mode to create a new romlist first (y), or process your old romlist (n).

Author: Gordon Lim
Last Edit: 26 Jan 2018 
"""

# Setup environment variables:

#filename_bezeldimensions      = "bezeldimensions.txt"
filename_bezeldimensions      = "bezeldimensions_GOOD.txt"
filename_sortanddisplaytitles = "sortanddisplaytitles.txt"

import configsetup
import subprocess
import os

# Update 'AltTitle' field in romlist with new display title:

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

# Update 'Extra' field in romlist with formatted bezel dimensions string

def update_Extra_field(game): 

    # Read bezel dimensions from file:
        
    file_bezeldimensions = open(filename_bezeldimensions, 'r')
    file_bezeldimensions.readline() # skip first line

    bezels = []
    for line in file_bezeldimensions.readlines():
        bezel = [field for field in line.rstrip('\n').split(";")]
        bezels.append(bezel)

    file_bezeldimensions.close()

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

# Update 'Buttons' field in romlist with new sorting title, and update
# 'AltTitle' field with "series" display title (if available):

def update_Buttons_and_AltTitle_fields(game):
    
    sortingtitle = game[1]
    displaytitle = game[14]

    # Read special games data from file:

    file_sortanddisplaytitles = open(filename_sortanddisplaytitles, 'r')
    file_sortanddisplaytitles.readline() # skip first line

    sortanddisplaytitles = []

    for line in file_sortanddisplaytitles.readlines():
        sortanddisplaytitle = [field for field in line.rstrip('\n').split(";")]
        sortanddisplaytitles.append(sortanddisplaytitle)

    file_sortanddisplaytitles.close()

    # Update sorting and display titles for special games:
    
    for sortanddisplaytitle in sortanddisplaytitles:    

        if (sortanddisplaytitle[0] == game[0]):
            sortingtitle = sortanddisplaytitle[1]
            if (sortanddisplaytitle[2] == ''):
                displaytitle = game[14] 
            else:
                displaytitle = sortanddisplaytitle[2] + ' ' + game[14]
                
    # Remove "The" and "Vs." from sorting title:
           
    if (sortingtitle[0:4] == 'The '):
        sortingtitle = sortingtitle[4:]
    if (sortingtitle[0:4] == 'Vs. '):
        sortingtitle = sortingtitle[4:]

    # Update romlist fields:
        
    game[14] = displaytitle # AltTitle
    game[16] = sortingtitle # Buttons
 
    return

# Update 'Title', 'Alttitle' and 'Buttons' fields in romlist for specific games:

def update_exceptional_games(game):

    if (game[0] == 'bm1stmix'):
        game[1]  = 'Beatmania (ver JA-B)'
        game[14] = 'Beatmania'
        game[16] = 'Beatmania (ver JA-B)'
        
    if (game[0] == 'garou'):
        game[1]  = 'Fatal Fury 9 / Garou - Mark of the Wolves (NGM-2530)'
        game[14] = 'Fatal Fury 9 / Garou - Mark of the Wolves'
        game[16] = 'Fatal Fury 9 / Garou - Mark of the Wolves (NGM-2530)'    

    return

def main():

    # Setup configuration:
    
    configsetup.init()

    AMromlist = configsetup.AMconfigdir + "romlists/mame.txt"

    print(AMromlist)
    
    # Check if romlist exists:

    romlistexists = False
    if os.path.isfile(AMromlist):
        romlistexists = True
        
    # Create new Attract-Mode MAME romlist or not:

    createnewromlist = raw_input('Create new romlist? Press "y" or "n" and press enter/return: ')

    if (createnewromlist == 'y'):
        if romlistexists: # Remove old romlist:
            subprocess.call(["rm", AMromlist]) 
        subprocess.call("./attract --build-romlist mame", cwd = configsetup.AMexecdir, shell = True) # Create new romlist
        subprocess.call(["cp", AMromlist, AMromlist[:-4] + "_original.txt"])                         # Backup new romlist
    elif (createnewromlist == 'n'):
        if not romlistexists:
            print("Romlist does not exist in this directory - EXIT")
            return 1
        if os.path.isfile(AMromlist + ".original"): # Use backup romlist: 
            subprocess.call(["cp", AMromlist[:-4] + "_original.txt", AMromlist]) 
    else:
        print("Next time please type 'y' or 'n'")
        return 2

    # Transform AM romlist into list of games:

    games, header = configsetup.create_list_of_games_from_romlist()

    # Update fields in list of games:

    bezeldimensionsfile_exists = False
    if os.path.isfile(filename_bezeldimensions):
        bezeldimensionsfile_exists = True
    else:
        print("--- bezeldimensions.txt does not exist in this directory, skipping update of Extra field")

    sortanddisplaytitlesfile_exists = False
    if os.path.isfile(filename_sortanddisplaytitles):
        sortanddisplaytitlesfile_exists = True
    else:
        print("--- sortanddisplaytitles.txt does not exist in this directory, skipping update of Buttons and AltTitle fields")

    for game in games:

        # Update 'AltTitle' field in romlist:
        update_AltTitle_field(game)

        # Update 'Extra' field in romlist:
        if (bezeldimensionsfile_exists):
            update_Extra_field(game)
                    
        # Update 'Buttons' and 'AltTitle' fields in romlist:
        if (sortanddisplaytitlesfile_exists):
            update_Buttons_and_AltTitle_fields(game)

        # Update romlist for specific games:
        update_exceptional_games(game)
        
    # Create updated romlist:

    outputfile = open(AMromlist, 'w')
    outputfile.write(header)

    for game in games:

        # Remove anomalous 'series' entry
        if (game[0] == 'series'):
            continue
        
        line = ";".join(game)
        outputfile.write(line + '\n')

    outputfile.close()
        
    return 0

if __name__ == '__main__':
    main()
