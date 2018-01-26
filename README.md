# MAME support tools for Attract-Mode

This repository contains a collection of programs that provides [MAME](http://www.mamedev.org/) support for the [Attract-Mode](http://www.attractmode.org/) frontend:

- [MAME hiscore support for Attract-Mode](#hiscore) ([*hiscoreanalysis.py*](hiscoreanalysis.py))
- [MAME benchmark support for Attract-Mode](#bench) ([*benchmarkgenerator.py*](benchmarkgenerator.py) and [*benchmarkanalysis.py*](benchmarkanalysis.py))
- [MAME bezel artwork support for Attract-Mode](#bezel) ([*bezelanalysis.py*](bezelanalysis.py))
- [MAME controls support for Attract-Mode](#control) ([*controlanalysis.py*](controlanalysis.py))
- [MAME title display and sorting support for Attract-Mode](#title) ([*updateromlist.py*](updateromlist.py))
- [MAME startup scripts](#start) ([*mame.bash*](mame.bash) and [*mame.csh*](mame.csh))
- [New Attract-Mode layout with above functionality](#layout) ([*mylayout*](mylayout))

---
<a name="hiscore" />

### MAME hiscore support for Attract-Mode: [*hiscoreanalysis.py*](hiscoreanalysis.py)

Python program to get hiscores of a single game or a list of games using the [*hi2txt*](http://greatstone.free.fr/hi2txt/) Java archive, 
and save them in formatted ASCII files in a dedicated Attract-Mode *hiscores* directory. This allows hiscores to be displayed 
in any Attract-Mode layout using the *file-format* module.

Requirements:

- [*hi2txt.jar* and *hi2txt.zip*](http://greatstone.free.fr/hi2txt/)
- [*Java*](https://www.java.com)
- [*hiscore.dat*](http://highscore.mameworld.info/)
<a name="bench" />

### MAME benchmark support for Attract-Mode: [*benchmarkgenerator.py*](benchmarkgenerator.py) and [*benchmarkanalysis.py*](benchmarkanalysis.py)

Python program to generate and analyze MAME benchmark files of a single game or a list of games. For each game:
- Calculate average emulation speed and total emulation time by taking into account previous benchmark data. 
- Convert average emulation speed in to a 1-5 star rating.
- Convert MAME benchmark files into formatted ASCII files in a dedicated Attract-Mode *benchmarks* directory. 
- This allows benchmark data to be displayed in any Attract-Mode layout using the *file-format* module. 

<a name="bezel" />

### MAME bezel artwork support for Attract-Mode: [*bezelanalysis.py*](bezelanalysis.py)

Python program to analyze MAME bezel artwork:
- Creates a bezeldimensions.txt file with bezel data 
- Creates a list of symbolic links to bezel art
- Analysis is based on the [*.lay* file structure](http://wiki.mamedev.org/index.php/LAY_File_Basics_-_Part_I)
- This allows bezel artwork to be displayed in any Attract-Mode layout using the *file-format* module.

Requirements:
- Bezel artwork, e.g. [*http://www.progettosnaps.net/artworks/*](http://www.progettosnaps.net/artworks/)

<a name="control" />

### MAME controls support for Attract-Mode: [*controlanalysis.py*](controlanalysis.py)

Python program to... 

<a name="title" />

### MAME title display and sorting support for Attract-Mode: [*updateromlist.py*](updateromlist.py)

Python program to update Attract-Mode MAME romlist with additional game data:
- Replace *AltTitle* with updated title without parentheses, leading *The*, *Vs.*, etc. - for title display purposes.
- Replace *Extra* with formatted bezel dimensions string as provided by [*bezelanalysis.py*](bezelanalysis.py)
- Replace *Buttons* with sortable title and update *AltTitle* if game is part of a series, as provided by 
  [*sortanddisplaytitles.txt*](sortanddisplaytitles.txt) 

<a name="start" />

### MAME startup scripts: [*mame.bash*](mame.bash) and [*mame.csh*](mame.csh)

Startup scripts to automate the execution of [*hiscoreanalysis.py*](hiscoreanalysis.py) and [*benchmarkanalysis.py*](benchmarkanalysis.py) immediately after running a game.

<a name="layout" />

### New Attract-Mode layout with above functionality: [*mylayout*](mylayout)

New Attract-Mode layout which uses the above functionality:
- Current hiscore displayed for each game (if available)
- Current benchmark displayed for each game
- Bezel artwork displayed for each game (if available)
- Controls displayed for each game (if available)
- Custom titles
