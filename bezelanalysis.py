#!/usr/bin/python -tt
"""
MAME support program to analyze MAME bezel artwork:
- Analysis is based on the standard .lay file structure as defined here: http://wiki.mamedev.org/index.php/LAY_File_Basics_-_Part_I
- User chooses whether to create a low resolution version of each bezel (since bezel files usually are high resolution and therefore can 
  be slow to render in Attract-Mode), or create symbolic links to the original bezel files.
- Low-resolution bezels / symlinks are saved in a dedicated Attract-Mode bezels directory.
- Bezel data are reformatted and saved in a formatted ASCII file (AMbezels.ini). This file can be used to display bezels in Attract-Mode.

Usage:

1) Change configsetup.py according to your system setup.
2) Change myAMbezeldir according to your setup:
"""

myAMbezeldir = "${HOME}/Games/Arcade Art/bezel/AMbezels/" # Directory where AM bezels will be saved

"""
3) Provide data/bezeldirectories.txt file with a list of directories which contain bezel artwork.
4) Make sure {game}.zip files are unzipped. This can be accomplished by using unziplist.sh: For each directory in your list, 
   copy unziplist.sh to the directory, cd to the directory and type: ./bash unziplist.sh 
   (Note: unzipping bezel artwork costs hardly any extra diskspace)
5) Provide optional data/bezelexceptions.txt file for games which should be excluded from this analysis.
6) In a terminal, type: ./bezelanalysis.py

Author: Gordon Lim
Last Edit: 7 Feb 2018 
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

    bezeldirectoriesfilename = configsetup.AMsupportdir + 'data/bezeldirectories.txt'

    MAMEbezeldirs = []

    if (os.path.isfile(bezeldirectoriesfilename)):
        bezeldirectoriesfile = open(bezeldirectoriesfilename, 'r')
        header = bezeldirectoriesfile.readline() # skip header
        for mydir in bezeldirectoriesfile.readlines():
            dir = os.path.expandvars(mydir.strip('\n'))
            if not os.path.isdir(dir):
                print("Bezel art directory {} does not exist...".format(dir))
                return 1
            else:
                MAMEbezeldirs.append(dir)        
        bezeldirectoriesfile.close()
    else:
        print("ERROR: {} does not exist - EXIT".format(bezeldirectoriesfilename))
        return 1

    if (len(MAMEbezeldirs) == 0):
        print("No bezel art directories defined - EXIT".format(bezeldirectoriesfilename))
        return 1
    
    AMbezeldir = os.path.expandvars(myAMbezeldir)
        
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

    if (clearAMbezels == 'y'):
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
    artdirdict = {}
    
    for game in games:
        for MAMEbezeldir in MAMEbezeldirs:
            if os.path.isdir(MAMEbezeldir + game[0]):
                gameswithartwork.append(game[0])
                artdirdict[game[0]] = MAMEbezeldir # Does this overwrite?

    if (len(gameswithartwork) == 0):
        print("There are no unzipped bezel artwork directories for games in {} - EXIT".format(MAMEbezeldirs))
        return 1
    
    # Construct list of excluded games:
    
    bezelexceptionsfilename = configsetup.AMsupportdir + 'data/bezelexceptions.txt'

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

    counts = [0, 0, 0, 0, 0, 0, 0, 0]

    for game in games:

        romname = game[0]
        
        print("--- Analyzing bezels for {}...".format(romname))
        
        # Skip excluded games:
        
        if romname in excludedgames:
            print("------ included in list of excluded games - EXIT0")
            gameswithoutbezel.append(game)
            counts[0] += 1
            continue
        else:
            print("------ {} is not included in list of excluded games...".format(romname))            
    
        # Skip games without artwork:
        
        if romname not in gameswithartwork:
            print("------ no artwork - EXIT1")
            gameswithoutbezel.append(game)
            counts[1] += 1
            continue
        else:
            print("------ {} exists...".format(artdirdict[romname] + romname))

        # Find and read .lay file (there should be only one):

        listOfFiles = os.listdir(artdirdict[romname] + romname)
        
        layfilename = ''
        for entry in listOfFiles:  
            if fnmatch.fnmatch(entry, "*.lay"):
                layfilename = entry
        
        layfile = open(artdirdict[romname] + romname + "/" + layfilename, 'r')
        laytextstring = layfile.read()
        layfile.close()

        # Use regular expression searches to find bezel data in .lay file: 

        # 1) Search for bezel tag in "Artwork type:" line:
        
        matchobject = re.search('Artwork type:[\w\s,;]*[Bb]ezel', laytextstring)

        if matchobject:
            print("------ regex search found a bezel tag in .lay file...")
        else:
            print("------ regex search did not find a bezel tag in .lay file - EXIT2")
            gameswithoutbezel.append(game)
            counts[2] += 1
            continue

        # 2) Search for view name and bezel element name:

        bezelelement_patterns1 = ['[Bb]ez[\w-]+','[Oo]uter[\w-]*','[Ii]nner[\w-]*', 'sac[\w-]*', \
                                  '[\w-]+[Bb]ez[\w-]+','[\w-]+[Oo]uter[\w-]*','[\w-]+[Ii]nner[\w-]*']
        
        bezelelement_patterns2 = ['[Cc]oc[\w-]+', '[\w-]+[Cc]oc[\w-]+', '[Bb]ez[\w-]+', '[\w-]+[Bb]ez[\w-]+']

        bezelelementfound = False
        
        for bezelelement_pattern in bezelelement_patterns1:
            regexquery = '<view name=\"([\w-]*[Uu]p[\w-]+)\">\s*\n(?:.+\n)*?\s+<bezel element=\"(' + bezelelement_pattern + ')\"'
            matchobject = re.search(regexquery, laytextstring)
            if matchobject:
                print("------ .lay file contains view name '{}' and bezel element '{}' ...".format(matchobject.group(1), matchobject.group(2)))
                bezelelementfound = True
                break

        if (bezelelementfound and (excludegenericbezels == 'y') and (matchobject.group(2)[0:3] == 'sac')):
            print("------ png file is a generic bezel - EXIT5")
            gameswithoutbezel.append(game)
            counts[5] += 1
            continue

        if not bezelelementfound:
            for bezelelement_pattern in bezelelement_patterns2:                
                regexquery = '<view name=\"([\w-]*[Co]oc[\w-]+)\">\s*\n(?:.+\n)*?\s+<bezel element=\"(' + bezelelement_pattern + ')\"'
                matchobject = re.search(regexquery, laytextstring)
                if matchobject:
                    print("------ .lay file contains view name '{}' and bezel element '{}' ...".format(matchobject.group(1), matchobject.group(2)))
                    bezelelementfound = True
                    break
        
        if not bezelelementfound:
            print("------ regex search did not find a view name and bezel element in .lay file - EXIT3")
            gameswithoutbezel.append(game)
            counts[3] += 1
            continue
        
        viewname     = matchobject.group(1)
        bezelelement = matchobject.group(2)
        
        # 3) Search for .png filename:

        regexquery = '<element name=\"' + bezelelement + '\"\s*>\s*\n\s+<image file=\"([\w-]+.png)\"'
        
        matchobject = re.search(regexquery, laytextstring)

        if matchobject:
            print("------ bezel .png file found ({})...".format(matchobject.group(1)))
        else:
            print("------ bezel regex search did not find a .png filename in .lay file - EXIT4")
            gameswithoutbezel.append(game)
            counts[4] += 1
            continue

        bezelfilename = matchobject.group(1)

        # Exclude generic bezels:

        if (excludegenericbezels == 'y'):
            if (bezelfilename == "taito_f3_bezel.png" or
                bezelfilename == "bally_sente_bezel_sac1.png" or
                bezelfilename == "bally_sente_bezel_sac1_deluxe.png" or
                bezelfilename == "sac1_deluxe_bezel.png" or
                bezelfilename == "bm_1_vert.png" or
                bezelfilename == "bm_2_vert.png" or
                bezelfilename == "bm_1_horiz.png" or
                bezelfilename == "bm_2_horiz.png" or
                bezelfilename[:14] == "rockola_bezel_" or
                bezelfilename[:10] == "deco_bezel" or 
                bezelfilename[:13] == "generic_bezel"):
                
                print("------ png file is a generic bezel - EXIT5")
                gameswithoutbezel.append(game)
                counts[5] += 1
                continue

        # 4) Search for screen dimensions:
            
        regexquery = '<view name=\"' + viewname + '\">\s*\n(?:.+\n)*?\s+<screen index=\"\d+\">\s*\n\s+<bounds x=\"([-.\d]+)\" y=\"([-.\d]+)\" width=\"([.\d]+)\" height=\"([.\d]+)\"'
        
        matchobject = re.search(regexquery, laytextstring)

        if matchobject:
            print("------ artwork contains screen dimensions...")
        else:
            print("------ bezel dimension regex search found nothing in .lay file - EXIT6")
            gameswithoutbezel.append(game)
            counts[6] += 1
            continue

        x_screen = float(matchobject.group(1))
        y_screen = float(matchobject.group(2))
        w_screen = float(matchobject.group(3))
        h_screen = float(matchobject.group(4))

        # 5) Search for bezel dimensions:
            
        regexquery = '<view name=\"' + viewname + '\">\s*\n(?:.+\n)*?\s+<bezel element=\"' + bezelelement + '\">\s*\n\s+<bounds x=\"([-.\d]+)\" y=\"([-.\d]+)\" width=\"([.\d]+)\" height=\"([.\d]+)\"'
        
        matchobject = re.search(regexquery, laytextstring)

        if matchobject:
            print("------ artwork contains bezel dimensions...")
        else:
            print("------ bezel dimension regex search found nothing in .lay file - EXIT7")
            gameswithoutbezel.append(game)
            counts[7] += 1
            continue

        x_bezel = float(matchobject.group(1))
        y_bezel = float(matchobject.group(2))
        w_bezel = float(matchobject.group(3))
        h_bezel = float(matchobject.group(4))

        # 6) Search for total bezel dimensions (if available):
        
        x_bezeltotal = x_bezel
        y_bezeltotal = y_bezel
        w_bezeltotal = w_bezel
        h_bezeltotal = h_bezel

        regexquery = '<view name=\"' + viewname + '\">\s*\n\s+<bounds x=\"([-.\d]+)\" y=\"([-.\d]+)\" width=\"([.\d]+)\" height=\"([.\d]+)\"'

        matchobject = re.search(regexquery, laytextstring)

        if matchobject:
            print("------ artwork contains total bezel dimensions...")
            x_bezeltotal = float(matchobject.group(1))
            y_bezeltotal = float(matchobject.group(2))
            w_bezeltotal = float(matchobject.group(3))
            h_bezeltotal = float(matchobject.group(4))
            #counts[8] += 1

        print("------ bezel filename = {}".format(bezelfilename))
        print("------ x_screen = {}".format(x_screen))
        print("------ y_screen = {}".format(y_screen))
        print("------ w_screen = {}".format(w_screen))
        print("------ h_screen = {}".format(h_screen))
        print("------ x_bezel = {}".format(x_bezel))
        print("------ y_bezel = {}".format(y_bezel))
        print("------ w_bezel = {}".format(w_bezel))
        print("------ h_bezel = {}".format(h_bezel))
        print("------ x_bezeltotal = {}".format(x_bezeltotal))
        print("------ y_bezeltotal = {}".format(y_bezeltotal))
        print("------ w_bezeltotal = {}".format(w_bezeltotal))
        print("------ h_bezeltotal = {}".format(h_bezeltotal))
            
        # Create low-resolution version of bezel or symbolic link to bezel:
        
        if (rescale == "y"):
        
            # Copy .png file to ${AMbezeldir}, rename the file and change the resolution:
        
            oldpngfile = artdirdict[romname] + romname + "/" + bezelfilename
            newpngfile = AMbezeldir + romname + ".png"
            
            subprocess.call(["cp", oldpngfile, newpngfile])
        
            # Get original image pixel height:
            
            tmpfilename = configsetup.AMsupportdir + 'tmp.txt'
            
            tmpfile = open(tmpfilename, 'w')
            subprocess.call(["sips", "-g", "pixelWidth", "-g", "pixelHeight", newpngfile], stdout = tmpfile)    # Use SIPS
            #subprocess.call("identify " + romname + ".png", cwd = AMbezeldir, stdout = tmpfile, shell = True)  # Use ImageMagick (Does not work when called from within python on OSX, DYLD libraries are not loaded when called from within python, something to do with Mac's System Integrity Protection...)
            tmpfile = open(tmpfilename, 'r')
            tmpstring = tmpfile.read()
            matchobject = re.search("pixelWidth:\s*([.\d]+)\s*\n\s*pixelHeight:\s*([.\d]+)", tmpstring) # Use SIPS
            #matchobject = re.search("PNG ([.\d]+)x([.\d]+) ", tmpstring)   # Use ImageMagick
            oldpixelwidth  = float(matchobject.group(1))
            oldpixelheight = float(matchobject.group(2))
            
            # Change image resolution:
            
            FNULL = open(os.devnull, 'w')
            subprocess.call(["sips", "-Z", AMbezelresolution, newpngfile], stdout = FNULL)                                 # Use SIPS
            #subprocess.call(["convert", "-resize", AMbezelresolution + "x" + AMbezelresolution, newpngfile, newpngfile])  # Use ImageMagick (Does not work when called from within python on OSX, DYLD libraries are not loaded when called from within python, something to do with Mac's System Integrity Protection...)
            
            # Get low-res image pixel height:
            
            tmpfile = open(tmpfilename, 'w')
            subprocess.call(["sips", "-g", "pixelWidth", "-g", "pixelHeight", newpngfile], stdout = tmpfile) # Use SIPS
            #subprocess.call(["identify", newpngfile], stdout = tmpfile)                                     # Use ImageMagick (Does not work when called from within python on OSX, DYLD libraries are not loaded when called from within python, something to do with Mac's System Integrity Protection...)
            tmpfile = open(tmpfilename, 'r')
            tmpstring = tmpfile.read()
            tmpfile.close()
            matchobject = re.search("pixelWidth:\s*([.\d]+)\s*\n\s*pixelHeight:\s*([.\d]+)", tmpstring) # Use SIPS
            #matchobject = re.search("PNG ([.\d]+)x([.\d]+) ", tmpstring)   # Use ImageMagick
            newpixelwidth  = float(matchobject.group(1))
            newpixelheight = float(matchobject.group(2))
            subprocess.call(["rm", tmpfilename])

            # Rescale saved bezel data:

            pixelscalefactor = 1
            if (oldpixelwidth > oldpixelheight):
                pixelscalefactor = newpixelwidth/oldpixelwidth
            else:
                pixelscalefactor = newpixelheight/oldpixelheight
            
            x_screen     *= pixelscalefactor
            y_screen     *= pixelscalefactor
            w_screen     *= pixelscalefactor
            h_screen     *= pixelscalefactor

            x_bezel      *= pixelscalefactor
            y_bezel      *= pixelscalefactor
            w_bezel      *= pixelscalefactor
            h_bezel      *= pixelscalefactor

            x_bezeltotal *= pixelscalefactor
            y_bezeltotal *= pixelscalefactor
            w_bezeltotal *= pixelscalefactor
            h_bezeltotal *= pixelscalefactor

            print("------ old .png pixel width  = {}".format(oldpixelwidth))
            print("------ old .png pixel height = {}".format(oldpixelheight))
            print("------ new .png pixel width  = {}".format(newpixelwidth))
            print("------ new .png pixel height = {}".format(newpixelheight))
            print("------ .png pixelscalefactor = {}".format(pixelscalefactor))
            
            print("------ low-resolution version of {}.png created...".format(romname))
            
        else: # Create symlink to bezel file:

            source      = artdirdict[romname] + romname + "/" + bezelfilename
            destination = AMbezeldir + romname + '.png' 
            
            try:
                os.symlink(source, destination)
            except OSError:
                print("------ symlink to {}.png exists already".format(romname))
            else:
                print("------ symlink to {}.png created...".format(romname))

        # Save bezel data to bezels list:

        bezel = [romname, bezelfilename,                                 \
                 int(round(x_screen)),     int(round(y_screen)),     int(round(w_screen)),     int(round(h_screen)),     \
                 int(round(x_bezel)),      int(round(y_bezel)),      int(round(w_bezel)),      int(round(h_bezel)),      \
                 int(round(x_bezeltotal)), int(round(y_bezeltotal)), int(round(w_bezeltotal)), int(round(h_bezeltotal))]
        bezels.append(bezel)
        
        print("------ bezel data saved - SUCCESS".format(romname))
        count += 1

        #dummy = raw_input("press return/enter")

    print("==> 'EXIT0' indicates excluded game")
    print("--> 'EXIT1' indicates game without artwork")
    print("--> 'EXIT2' indicates game without bezel artwork")
    print("--> 'EXIT3' indicates game with bezel artwork but no valid view name and bezel element")
    print("--> 'EXIT4' indicates game with bezel artwork but no .png file")
    print("--> 'EXIT5' indicates game with bezel artwork but with generic .png file")
    print("--> 'EXIT6' indicates game with bezel artwork but no screen dimensions")
    print("--> 'EXIT7' indicates game with bezel artwork but no bezel dimensions")
    #print("--> '8' indicates game with bezel artwork and bezeltotal dimensions")
    
    print("==> Total # of exit code games = {}".format(sum(counts)))
    for i in range(0, len(counts)):
        print("--> # of exit code '{}' games = {}".format(i, counts[i]))
        
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

    AMbezelfilename = configsetup.AMsupportdir + "data/AMbezels.ini"
        
    AMbezelfile = open(AMbezelfilename, 'w')
    for bezel in bezels:
        AMbezelfile.write("[{}]\n".format(bezel[0]))
        AMbezelfile.write("filename={}\n".format(bezel[1]))
        AMbezelfile.write("screen_xtopleft={}\n".format(bezel[2]))
        AMbezelfile.write("screen_ytopleft={}\n".format(bezel[3]))
        AMbezelfile.write("screen_width={}\n".format(bezel[4]))
        AMbezelfile.write("screen_height={}\n".format(bezel[5]))
        AMbezelfile.write("bezel_xtopleft={}\n".format(bezel[6]))
        AMbezelfile.write("bezel_ytopleft={}\n".format(bezel[7]))
        AMbezelfile.write("bezel_width={}\n".format(bezel[8]))
        AMbezelfile.write("bezel_height={}\n".format(bezel[9]))
        AMbezelfile.write("bezeltotal_xtopleft={}\n".format(bezel[10]))
        AMbezelfile.write("bezeltotal_ytopleft={}\n".format(bezel[11]))
        AMbezelfile.write("bezeltotal_width={}\n".format(bezel[12]))
        AMbezelfile.write("bezeltotal_height={}\n".format(bezel[13]))
    AMbezelfile.close()
    
    print("=> {} out of {} games have artwork".format(len(gameswithartwork), len(games)))
    print("=> {} out of {} games have bezel artwork".format(count, len(gameswithartwork)))
        
    return 0

if __name__ == '__main__':
    main()
