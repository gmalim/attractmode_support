#!/usr/bin/python -tt
"""
Program to update Attract-Mode MAME romlist with additional game data:
- Replace 'AltTitle' with updated title (parentheses removed, leading "The" removed, etc)
- Replace 'Extra' with formatted tag to indicate whether hiscore, benchmark, bezel and/or controls data are available. 
  This can be used to contruct Attract-Mode filters.
- Replace 'Buttons' with sortable title and update 'AltTitle' if game is part of a series, as provided by 
  AMtitles.txt (create by hand)

Usage:

1) Change configsetup.py according to your system setup.
2) Create/update AMtitles.txt in a text editor to change the order of specific games in Attract-Mode.
   You can also indicate if specific games are part of a series.
3) See README.md on how to create .ini files with hiscore, benchmark, bezel and/or controls data
4) In a terminal, cd to your Attract-Mode romlist directory and type: 
   ./updateromlist.py
5) Type y/n if you want Attract-Mode to create a new romlist first (y), or process your old romlist (n).

Author: Gordon Lim
Last Edit: 31 Jan 2018 
"""

import configsetup
import re
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

# Update 'Extra' field in romlist with formatted string indicating
# if hiscore, benchmark, bezel and controls data is available:

def gameinfile(romname, filename):

    file = open(filename, 'r')
    text = file.read()
    file.close()

    matchobject = re.search('\[{}\]'.format(romname), text)

    if matchobject:
        return 1
    else:
        return 0

def update_Extra_field(game, files_available):
    
    romname = game[0]

    tags = [0, 0, 0, 0]
    
    if (files_available[0]):
        tags[0] = gameinfile(romname, filename_hiscores)

    if (files_available[1]):
        tags[1] = gameinfile(romname, filename_benchmarks)

    if (files_available[2]):
        tags[2] = gameinfile(romname, filename_bezels)

    if (files_available[3]):
        tags[3] = gameinfile(romname, filename_controls)

    encodedtag = ["Hi" + str(tags[0]), \
                  "Bm" + str(tags[1]), \
                  "Be" + str(tags[2]), \
                  "Co" + str(tags[3])]
    
    game[15] = "-".join(encodedtag)
    
    return

# Update 'Buttons' field in romlist with new sorting title,
# and update 'AltTitle' field with "series" display title (if available):

def update_Buttons_and_AltTitle_fields(game):
    
    sortingtitle = game[1]
    displaytitle = game[14]

    # Read titles data from file:

    file_titles = open(filename_titles, 'r')
    file_titles.readline() # skip first line

    titles = []

    for line in file_titles.readlines():
        sortanddisplaytitle = [field for field in line.rstrip('\n').split(";")]
        titles.append(sortanddisplaytitle)

    file_titles.close()

    # Update sorting and display titles for special games:
    
    for title in titles:    

        if (title[0] == game[0]):
            sortingtitle = title[1]
            if (title[2] == ''):
                displaytitle = game[14] 
            else:
                displaytitle = title[2] + ' ' + game[14]
                
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

    global filename_hiscores  
    global filename_benchmarks
    global filename_bezels    
    global filename_controls  
    global filename_titles    

    filename_hiscores   = configsetup.AMsupportdir + "AMhiscores.ini"
    filename_benchmarks = configsetup.AMsupportdir + "AMbenchmarks.ini"
    filename_bezels     = configsetup.AMsupportdir + "AMbezels.ini"
    filename_controls   = configsetup.AMsupportdir + "AMcontrols.ini"
    filename_titles     = configsetup.AMsupportdir + "AMtitles.txt"

    # Check if romlist exists:

    AMromlist = configsetup.AMconfigdir + "romlists/mame.txt"

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

    if (len(games) == 0):
        print("AM romlist is empty - EXIT")
        return 3

    # Check if files exist:

    files_available = [0, 0, 0, 0, 0]
        
    if os.path.isfile(filename_hiscores):
        files_available[0] = 1
    else:
        print("--- {} does not exist".format(filename_hiscores))
        
    if os.path.isfile(filename_benchmarks):
        files_available[1] = 1
    else:
        print("--- {} does not exist".format(filename_benchmarks))

    if os.path.isfile(filename_bezels):
        files_available[2] = 1
    else:
        print("--- {} does not exist".format(filename_bezels))

    if os.path.isfile(filename_controls):
        files_available[3] = 1
    else:
        print("--- {} does not exist".format(filename_controls))
    
    if os.path.isfile(filename_titles):
        files_available[4] = 1
    else:
        print("--- {} does not exist".format(filename_titles))
    
    # Update fields in list of games:
    
    for game in games:

        # Update 'AltTitle' field in romlist:
        update_AltTitle_field(game)

        # Update 'Extra' field in romlist:
        update_Extra_field(game, files_available[0:4])
                    
        # Update 'Buttons' and 'AltTitle' fields in romlist:
        if (files_available[4]):
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
