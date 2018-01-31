#!/usr/bin/python -tt
"""
======
TO DO: 

Search for bezel png file: 
Check if more than one hit. 
If more than one found, analyze which one should be used - right now the first found is used. 
If no hits, just search for '(\w+.png)'. 
If only one is found, that one has to be the bezel
If more than one found, analyze which one should be used. If you do nothing the first one found is used?
======

Program to analyze unzipped MAME bezels:
- Analysis is based on the .lay file structure as defined here: http://wiki.mamedev.org/index.php/LAY_File_Basics_-_Part_I
- A lower resolution version of each bezel or a symbolic link to each bezel is saved in a dedicated AM bezels directory.
- Bezel data is reformatted and saved in a formatted ASCII file: AMbezels.ini
- This allows bezels to be displayed in Attract-Mode layouts by using the 'file-format' module.

Usage:

1) Change configsetup.py according to your system setup.
2) Change environment variables according to your setup:
"""

myMAMEbezeldir = "${HOME}/Games/Arcade Art/bezel/artwork_pS_official/" # Directory containing unzipped MAME artwork
myAMbezeldir   = "${HOME}/Games/Arcade Art/bezel/AMbezels/"            # Directory where AM bezels will be saved

"""
3) Make sure artwork in $myMAMEbezeldir is unzipped, otherwise copy unziplist.sh to $myMAMEbezeldir, cd to this directory
   and type: ./bash unziplist.sh (Note: unzipping bezel artwork costs hardly any extra diskspace)
4) Provide optional bezelexceptions.txt file for excluded games
5) In a terminal, type: ./bezelanalysis.py

Author: Gordon Lim
Last Edit: 31 Jan 2018 
"""

import configsetup
import fnmatch
import os
import re
import subprocess
import sys

def main():

    # Setup configuration:
    
    configsetup.init()
    
    # Check directories:
    
    MAMEbezeldir = os.path.expandvars(myMAMEbezeldir)
    AMbezeldir   = os.path.expandvars(myAMbezeldir)
        
    if not os.path.isdir(MAMEbezeldir):
        print("MAME bezels directory does not exist - EXIT")
        return 1

    if not os.path.isdir(AMbezeldir):
        subprocess.call(["mkdir", AMbezeldir])
        if not os.path.isdir(AMbezeldir):
            print("ERROR: AM bezels directory does not exist - EXIT")
            return 1
        else:
            print("AM bezels will be saved in {}...".format(AMbezeldir))

    # Get user input:

    clearAMbezels = raw_input('Remove all .png files in the AM bezel directory? Press "y" or "n" followed by return/enter: ')

    if not ((clearAMbezels == 'y') or (clearAMbezels == 'n')):
        print("Next time please type 'y' or 'n'")
        return 1

    if clearAMbezels:
        subprocess.call('rm *.png', cwd = AMbezeldir, shell = True)
        
    rescale = raw_input('Create low-resolution bezels? Press "y" or "n" followed by return/enter: ')

    if not ((rescale == 'y') or (rescale == 'n')):
        print("Next time please type 'y' or 'n'")
        return 1

    if not os.path.isfile('/usr/bin/sips'): # If Sips does not exist:
        print("Sips is not installed on this system => Symbolic links to the original bezel images will be created instead...")
        rescale = 'n'
        
    AMbezelresolution = 0
    
    if (rescale == 'y'):
        
        AMbezelresolution = raw_input('Enter maximum AM bezel resolution for width or height - whichever is largest - in number of pixels (default: 800 pixels) and press return/enter: ') or '800'

        if ((int(AMbezelresolution) < 0) or (int(AMbezelresolution) > 2000)):
            check = raw_input('AM bezel resolution is set to {}. Are you sure? Press "n" followed by return/enter if you want to quit: '.format(AMbezelresolution))
            if (check == 'n'):
                return 1

    excludegenericbezels = raw_input('Exclude generic bezels? Press "y" or "n" followed by return/enter: ')

    if not ((excludegenericbezels == 'y') or (excludegenericbezels == 'n')):
        print("Next time please type 'y' or 'n'")
        return 1
            
    # Transform AM romlist into list of games:

    games, header = configsetup.create_list_of_games_from_romlist()

    if (len(games) == 0):
        print("AM romlist is empty - EXIT")
        return 1

    # Construct list of games with artwork:
    
    gameswithartwork = []
    
    for game in games:
        if os.path.isdir(MAMEbezeldir + game[0]):
            gameswithartwork.append(game[0])                

    if (len(gameswithartwork) == 0):
        print("There are no unzipped bezel artwork directories for games in {} - EXIT".format(MAMEbezeldir))
        return 1
    
    # Construct list of excluded games:
    
    bezelexceptionsfilename = configsetup.AMsupportdir + 'bezelexceptions.txt'

    excludedgames = []

    if (os.path.isfile(bezelexceptionsfilename)):
        bezelexceptionsfile = open(bezelexceptionsfilename, 'r')
        for line in bezelexceptionsfile.readlines():
            excludedgame = line.rstrip('\n')
            excludedgames.append(excludedgame)
        bezelexceptionsfile.close()
    else:
        print("{} does not exist".format(bezelexceptionsfilename))

    # Analyze games:

    count = 0

    gameswithoutbezel = []
    bezels = []
    
    for game in games:

        romname = game[0]
        
        print("--- Analyzing bezels for {}...".format(romname))
        
        # Skip excluded games:
        
        if romname in excludedgames:
            print("------ included in list of excluded games - EXIT1")
            gameswithoutbezel.append(game)
            continue
        else:
            print("------ {} is not included in list of excluded games...".format(romname))            
    
        # Skip games without artwork:
        
        if romname not in gameswithartwork:
            print("------ no artwork - EXIT2")
            gameswithoutbezel.append(game)
            continue
        else:
            print("------ {} exists...".format(MAMEbezeldir + romname))

        # Find and read .lay file (there should be only one):

        listOfFiles = os.listdir(MAMEbezeldir + romname)
        
        layfilename = ''
        for entry in listOfFiles:  
            if fnmatch.fnmatch(entry, "*.lay"):
                layfilename = entry
        
        layfile = open(MAMEbezeldir + romname + "/" + layfilename, 'r')
        laytextstring = layfile.read()

        #print laytextstring

        layfile.close()

        # Check if artwork contains bezel: 
        
        matchobject = re.search('-\s*Artwork\s*type:\s*Bezel', laytextstring)

        if matchobject:
            print("------ artwork contains bezel...")
        else:
            print("------ bezel regex search found nothing in .lay file - EXIT3")
            gameswithoutbezel.append(game)
            continue
                
        # Search for bezel png file:

        bezelpattern = '<\s*element\s*name\s*=\s*"bezel\w*"\s*>\s*\n\s+<\s*image\s*file\s*=\s*"(\w+.png)"\s*/>'
        
        matchobject = re.search(bezelpattern, laytextstring)

        if matchobject:
            print("------ {} found...".format(matchobject.group(1)))
        else:
            print("------ .png regex search found nothing in .lay file - EXIT4")
            gameswithoutbezel.append(game)
            continue

        bezelfilename = matchobject.group(1)

        # Exclude generic bezels:

        if (excludegenericbezels == 'y'):
            if (bezelfilename == "taito_f3_bezel.png" or
                bezelfilename == "bally_sente_bezel_sac1.png" or
                bezelfilename == "bally_sente_bezel_sac1_deluxe.png" or
                bezelfilename == "bm_1_vert.png" or
                bezelfilename == "bm_2_vert.png" or
                bezelfilename == "bm_1_horiz.png" or
                bezelfilename == "bm_2_horiz.png" or
                bezelfilename[:14] == "rockola_bezel_" or
                bezelfilename[:10] == "deco_bezel" or 
                bezelfilename[:13] == "generic_bezel"):
                print("------ png file is a generic bezel - EXIT5")
                gameswithoutbezel.append(game)
                continue

        # Search for bezel dimensions:

        dimpattern = '<\s*screen\s*index\s*=\s*"\d+"\s*>\s*\n\s+<\s*bounds\s*x\s*=\s*"(\d+)"\s*y\s*=\s*"(\d+)"\s*width\s*=\s*"(\d+)"\s*height\s*=\s*"(\d+)"\s*/>'
        
        matchobject = re.search(dimpattern, laytextstring)

        if matchobject:
            print("------ artwork contains bezel dimensions...")
        else:
            print("------ bezel dimension regex search found nothing in .lay file - EXIT6")
            gameswithoutbezel.append(game)
            continue

        x = float(matchobject.group(1))
        y = float(matchobject.group(2))
        w = float(matchobject.group(3))
        h = float(matchobject.group(4))

        # Create low-resolution version of bezel or symbolic link to bezel:
        
        if (rescale):
        
            # Copy .png file to ${AMbezeldir}, rename the file and change the resolution:
        
            oldpngfile = MAMEbezeldir + romname + "/" + bezelfilename
            newpngfile = AMbezeldir + romname + ".png"
            
            subprocess.call(["cp", oldpngfile, newpngfile])
        
            # Get original image pixel height:
            
            tmpfilename = configsetup.AMsupportdir + 'tmp.txt'
            
            tmpfile = open(tmpfilename, 'w')
            subprocess.call(["sips", "-g", "pixelHeight", newpngfile], stdout = tmpfile)
            tmpfile = open(tmpfilename, 'r')
            sipsstring = tmpfile.read()
            matchobject = re.search("pixelHeight:\s*(\d+)", sipsstring)
            oldpixelheight = float(matchobject.group(1))
            
            # Change image resolution:
            
            FNULL = open(os.devnull, 'w')
            subprocess.call(["sips", "-Z", AMbezelresolution, newpngfile], stdout = FNULL)
            
            # Get low-res image pixel height:
            
            tmpfile = open(tmpfilename, 'w')
            subprocess.call(["sips", "-g", "pixelHeight", newpngfile], stdout = tmpfile)
            tmpfile = open(tmpfilename, 'r')
            sipsstring = tmpfile.read()
            tmpfile.close()
            matchobject = re.search("pixelHeight:\s*(\d+)", sipsstring)
            newpixelheight = float(matchobject.group(1))
            
            subprocess.call(["rm", tmpfilename])

            # Rescale saved bezel data:
            
            x *= newpixelheight/oldpixelheight
            y *= newpixelheight/oldpixelheight
            w *= newpixelheight/oldpixelheight
            h *= newpixelheight/oldpixelheight

            print("------ low-resolution version of {}.png created...".format(romname))
            
        else: # Create symlink to bezel file:

            source      = MAMEbezelsdir + romname + "/" + bezelfilename
            destination = AMbezelsdir + romname + '.png' 
            
            try:
                os.symlink(source, destination)
            except OSError:
                print("------ symlink to {}.png exists already".format(romname))
            else:
                print("------ symlink to {}.png created...".format(romname))

        # Save bezel data to bezels list:

        bezel = [romname, bezelfilename, x, y, w, h]
        bezels.append(bezel)
        
        print("------ bezel data saved - SUCCESS".format(romname))
        count += 1

        #dummy = raw_input("press return/enter")
        
    # Clone handling - Loop over games without artwork:
    
    for gamewithoutbezel in gameswithoutbezel:

        # Check if game is a clone:

        original = gamewithoutbezel[3]

        if (original == ''): # game is not a clone
            continue

        # Loop over bezels to check if the original game has a bezel:

        for bezel in bezels:
            
            if (original == bezel[0]): # gamewithoutbezel has no bezel but is a clone of a game that does have a bezel 
                outputclone = bezel[:] # copy
                outputclone[0] = gamewithoutbezel[0]
                bezels.append(outputclone)
                count += 1

    # Save bezel data in AMbezels.ini:

    AMbezelfilename = configsetup.AMsupportdir + "AMbezels.ini"
        
    AMbezelfile = open(AMbezelfilename, 'w')
    for bezel in bezels:
        AMbezelfile.write("[{}]\n".format(bezel[0]))
        AMbezelfile.write("filename={}\n".format(bezel[1]))
        AMbezelfile.write("xtopleft={}\n".format(bezel[2]))
        AMbezelfile.write("ytopleft={}\n".format(bezel[3]))
        AMbezelfile.write("screenwidth={}\n".format(bezel[4]))
        AMbezelfile.write("screenheight={}\n".format(bezel[5]))
    AMbezelfile.close()
    
    print("=> {} out of {} games have artwork".format(len(gameswithartwork), len(games)))
    print("=> {} out of {} games have bezel artwork".format(count, len(gameswithartwork)))
        
    return 0

if __name__ == '__main__':
    main()
